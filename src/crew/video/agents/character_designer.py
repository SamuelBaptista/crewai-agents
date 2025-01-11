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

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

anthropic_llm = LLM(
    model="claude-3-5-sonnet-20241022",
    temperature=0.0,
    api_key=anthropic_api_key
)

agent = Agent(
    role=ROLE,
    goal=GOAL,
    backstory=BACKSTORY,
    llm=anthropic_llm,
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