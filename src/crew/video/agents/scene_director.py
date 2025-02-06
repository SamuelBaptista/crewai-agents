import os

from crewai import Agent, LLM, Task
from src.utils.schemas import CenasModel

from src.crew.video.agents.character_designer import task as character_task
from src.crew.video.agents.voice_script import task as voice_task


# Config

ROLE = """
Diretor de Cenas
"""

GOAL = """
Criar roteiro visual detalhado para vídeos do YouTube
"""

BACKSTORY = """
Especialista em narrativa visual que cria roteiros otimizados para vídeos infantis do YouTube.
Tem foco em cenas com imagens estáticas.
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
Criar roteiro visual detalhado para cada cena do vídeo. 
A cena será uma imagem estática. 
A história precisa ter a quantidade de cenas correta (todas as cenas). 
Seja o mais descritivo possível e mantenha o mesmo estilo e cores em todas as cenas. 
Evite colocar mais de uma pessoa na mesma cena. 
Cada cena tem um prompt indivudal para ser gerada, portando, considere que o prompt esteja completo com todas as informações necessárias e sem referências à cenas anteriores. 
Sempre mantenha o padrão da imagem como 2D digital art, vibrant colors, children's book style. 
Sempre coloque todas as caracteristicas da personagem de maneira descritiva para que seja gerado imagens semelhantes. SEMPRE GERE TODAS AS CENAS!
As cenas são geradas a partir de prompts idependentes. 
Cada cena não tem conciência das outras cenas, porém, através de uma descrição detalhada, precisamos manter a coerência entre elas, considerando a personagem da história. 
Todas as cenas devem fazer uma descrição completa da personagem, com cor da pele, olhos, cabelas, roupas e acessórios. 
Não existe limite de cenas ou caractheres! Sempre faça tudo completo.
"""

OUTPUT = """
Cenas formatadas em dicionário. 
Prompt em inglês para cada cena individualmente. 
Prompt com coerência entre o personagem e as cenas.
"""

task = Task(
    description=DESCRIPTION,
    expected_output=OUTPUT,
    context=[character_task, voice_task],
    agent=agent,
    output_json=CenasModel
)