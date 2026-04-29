

import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate


llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=500,
)


prompt_template = PromptTemplate.from_template(
    "List {n} cooking/meal titles for {cuisine} cuisine (name only)."
)


print("=" * 60)
print("EXEMPLE 1 — Utilisation directe avec format()")
print("=" * 60)

prompt = prompt_template.format(n=3, cuisine="Italian")
response = llm.invoke(prompt)
print(f"Prompt : {prompt}")
print(f"\nRéponse :\n{response.content}\n")


print("=" * 60)
print("EXEMPLE 2 — Chaîne LCEL (LangChain Expression Language)")
print("=" * 60)

chain = prompt_template | llm

test_cases = [
    {"n": 5, "cuisine": "Italian"},
    {"n": 3, "cuisine": "Japanese"},
    {"n": 4, "cuisine": "Tunisian"},
]

for params in test_cases:
    response = chain.invoke(params)
    print(f"\n── {params['n']} plats {params['cuisine']} ──")
    print(response.content)
