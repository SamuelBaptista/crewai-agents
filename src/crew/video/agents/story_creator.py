import os

from crewai import Agent, LLM, Task
from src.utils.schemas import StoryModel


# Config

ROLE = """
Criador de Histórias Infantis para YouTube
"""

GOAL = """
Criar histórias educativas e envolventes para vídeos do YouTube.
Se baseia em imagens estáticas para representar cada cena.
A história deve conter apenas um personagem.
"""

BACKSTORY = """
Especialista em conteúdo infantil para YouTube.
Foco em histórias longas e dinâmicas que mantêm a atenção das crianças em formato de vídeo.
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
Criar uma história longa, interessante e educativa para YouTube
Público de 3-10 anos
Tema: {tema}
"""

OUTPUT = """
A história completa precisa ser longa e conter ao menos 6000 caracteres ou 1000 palavras.
"""

task = Task(
    description=DESCRIPTION,
    expected_output=OUTPUT,
    agent=agent,
    output_json=StoryModel
)