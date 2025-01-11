from pydantic import BaseModel
from typing import List

# Pydantic Models
class StoryModel(BaseModel):
    titulo: str
    tema_educacional: str
    objetivo_aprendizagem: str
    historia: str
    quantidade_de_cenas: int

class PersonagemModel(BaseModel):
    caracteristicas: str
    estilo_visual: str
    prompt_ia: str

class Cena(BaseModel):
    numero: str
    elementos_visuais: str
    racional: str
    prompt_ia: str

class CenasModel(BaseModel):
    cenas: List[Cena]

class Narracao(BaseModel):
    numero: str
    racional: str
    texto_tts: str

class NarracaoModel(BaseModel):
    cenas: List[Narracao]