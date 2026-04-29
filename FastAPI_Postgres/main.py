from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)



class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class ChoiceResponse(BaseModel):
    id: int
    choice_text: str
    is_correct: bool

    class Config:
        orm_mode = True


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    choices: List[ChoiceResponse]

    class Config:
        orm_mode = True


@app.post("/questions/")
def create_question(question: QuestionBase, db: Session = Depends(get_db)):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)

    db.commit()

    return {"message": "Question créée", "id": db_question.id}


@app.get("/questions/", response_model=List[QuestionResponse])
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(models.Questions).all()


@app.get("/questions/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@app.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(question)
    db.commit()

    return {"message": "Deleted"}