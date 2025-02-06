import os

from crewai import Agent, LLM, Task
from src.utils.schemas import PersonagemModel


# Config

ROLE = """
Designer de Personagens
"""

GOAL = """
Criar perfis detalhados de personagens para geração por IA.
"""

BACKSTORY = """
Especialista em design de personagens infantis, criando descrições detalhadas para geração consistente por IA.
"""

# Agent

openai_api_key = os.getenv("OPENAI_API_KEY")

openai_llm = LLM(
    model="o1-mini",
    temperature=0.0,
    api_key=openai_api_key
)

agent = Agent(
    role=ROLE,
    goal=GOAL,
    backstory=BACKSTORY,
    llm=openai_llm,
    verbose=False
)


# Task

DESCRIPTION = """
Criar um perfil detalhado de uma personagem para geração por IA.
Considerar o tema da história e a história a ser contada. 
Manter o formato da arte como 2D digital art, vibrant colors, children's book style.
"""

OUTPUT = """
Prompt do personagem
"""

task = Task(
    description="",
    expected_output="",
    agent=agent,
    output_json=PersonagemModel
)