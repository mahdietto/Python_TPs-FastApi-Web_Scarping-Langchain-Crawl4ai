
import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=500,
)

class Movie(BaseModel):
    title: str = Field(description="The title of the movie.")
    genre: list[str] = Field(description="The genre of the movie.")
    year: int = Field(description="The year the movie was released.")


parser = PydanticOutputParser(pydantic_object=Movie)


prompt_template_text = """
Response with a movie recommendation based on the query:

{format_instructions}

{query}
"""

format_instructions = parser.get_format_instructions()
prompt_template = PromptTemplate(
    template=prompt_template_text,
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)


print("=" * 60)
print("MÉTHODE A — Appel manuel (format → invoke → parse)")
print("=" * 60)

prompt = prompt_template.format(query="A 90s movie with Nicolas Cage.")
text_output = llm.invoke(prompt)
print(f"Sortie brute (JSON) :\n{text_output.content}\n")

parsed_output = parser.parse(text_output.content)
print(f"Sortie parsée (objet Python) :\n{parsed_output}")
print(f"  → Titre : {parsed_output.title}")
print(f"  → Genre : {parsed_output.genre}")
print(f"  → Année : {parsed_output.year}")


print("\n" + "=" * 60)
print("MÉTHODE B — Chaîne LCEL (prompt | llm | parser)")
print("=" * 60)

chain = prompt_template | llm | parser

queries = [
    "A 90s movie with Nicolas Cage.",
    "A recent sci-fi movie with time travel.",
    "A classic French comedy.",
]

for query in queries:
    response = chain.invoke({"query": query})
    print(f"\nQuery : {query}")
    print(f"  → {response.title} ({response.year}) — {', '.join(response.genre)}")
