

import os
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, Tool
from langchain.agents.structured_chat.base import StructuredChatAgent


llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.3,
    max_tokens=1024,
)


math_prompt = PromptTemplate.from_template(
    "Calculate the following expression and return the result "
    "in the format 'Answer: <number>': {question}"
)

llm_math_chain = LLMMathChain.from_llm(llm=llm, prompt=math_prompt, verbose=True)


search = DuckDuckGoSearchRun()


calculator = Tool(
    name="calculator",
    description=(
        "Use this tool for arithmetic calculations. "
        "Input should be a mathematical expression."
    ),
    func=lambda x: llm_math_chain.run({"question": x}),
)

tools = [
    Tool(
        name="search",
        description=(
            "Search the internet for information about current events, data, or facts. "
            "Use this for looking up population numbers, statistics, or other factual information."
        ),
        func=search.run,
    ),
    calculator,
]


agent = StructuredChatAgent.from_llm_and_tools(
    llm=llm,
    tools=tools,
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,
    verbose=True,  
)


print("=" * 60)
print("AGENT IA — Recherche + Calcul")
print("=" * 60)

questions = [
    "What is the population difference between Tunisia and Algeria?",
    "What is the square root of the population of France?",
]

for question in questions:
    print(f"\nQuestion : {question}")
    print("-" * 60)
    result = agent_executor.invoke({"input": question})
    print(f"\nRéponse finale : {result['output']}")
    print("=" * 60)
