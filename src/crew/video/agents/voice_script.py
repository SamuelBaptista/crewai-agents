import os

from crewai import Agent, LLM, Task
from src.utils.schemas import NarracaoModel

from src.crew.video.agents.story_creator import task as story_task


# Config

ROLE = """
Contador de histórias
"""

GOAL = """
Quebrar a história em cenas alinhadas com o texto otimizado para text-to-speech. 
Criar textos longos e descritivos, incrementando a história para ficar mais interessante.
"""

BACKSTORY = """
Especialista em criar textos para sistemas text-to-speech."
"""

# Agent

openai_api_key = os.getenv("OPENAI_API_KEY")

openai_llm = LLM(
    model="o1-preview",
    temperature=0.5,
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
Criar script de texto otimizado para text-to-speech contendo a história. 
A narração deve conter a história completa, com todos os detalhes e quebrá-la de acordo com as cenas. 
A história precisa a quantidade de cenas correta. 
Pense passo a passo antes de dar a resposta para que o texto a quantidade correta de caracteres e palavras. 
Não omita nenhum detalhe e crie mais detalhes caso seja necessário.
O texto precisa ser claro em português para evitar que o modelo identifique o texto como sendo outra língua.
"""

OUTPUT = """
Script de texto em dicionário contendo a história completa e quebrada em cenas.
O texto_tts deve conter ao menos 600 caracteres ou 100 palavras.
"""

task = Task(
    description=DESCRIPTION,
    expected_output=OUTPUT,
    context=[story_task],
    agent=agent,
    output_json=NarracaoModel
)