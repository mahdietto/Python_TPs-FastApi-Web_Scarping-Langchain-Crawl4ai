
import os
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage



llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7,
    max_tokens=500,
)


print("=" * 60)
print("EXEMPLE 1 — Appel simple")
print("=" * 60)

response = llm.invoke("What are the 7 wonders of the world?")
print(f"Réponse :\n{response.content}\n")


print("=" * 60)
print("EXEMPLE 2 — Personnalité Pirate avec SystemMessage")
print("=" * 60)

system_message = SystemMessage(
    content=(
        "You are a friendly pirate who loves to share knowledge. "
        "Always respond in pirate speech, use pirate slang, and include "
        "plenty of nautical references. Add relevant emojis throughout "
        "your responses to make them more engaging. Arr! "
    )
)

question = "What are the 7 wonders of the world?"
messages = [
    system_message,
    HumanMessage(content=question),
]

response = llm.invoke(messages)
print(f"\nQuestion : {question}")
print(f"\nRéponse Pirate :\n{response.content}")
