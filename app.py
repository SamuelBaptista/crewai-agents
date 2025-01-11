import io
import base64
import os

import streamlit as st

from PIL import Image
from openai import OpenAI

from src.crew.video.video_crew import video_crew

from repenseai.genai.api.selector import APISelector
from repenseai.genai.tasks.api_task import Task


if "response" not in st.session_state:
    st.session_state.response = None

if "personagem" not in st.session_state:
    st.session_state.personagem = None

if "cena" not in st.session_state:
    st.session_state.cena = None

if "cenas" not in st.session_state:
    st.session_state.cenas = []

if "audio" not in st.session_state:
    st.session_state.audio = None

if "audios" not in st.session_state:
    st.session_state.audios = []   

if "step" not in st.session_state:
    st.session_state.step = 0

if "click" not in st.session_state:
    st.session_state.click = False


st.title("Video Crew")
st.write("A Video Crew é um grupo de especialistas em criação de conteúdo de vídeo, incluindo histórias, cenas, personagens e roteiros de voz.")

tema = st.text_input("Nome do Projeto", "História Infantil para YouTube")

print(st.session_state.step)

if st.button("Gerar História") or st.session_state.click:

    st.session_state.click = True

    if st.session_state.response is not None:
        crew_response = st.session_state.response
    else:
        crew_response = video_crew.kickoff({'tema': tema})
        st.session_state.response = crew_response

    historia = crew_response.tasks_output[0].to_dict()

    st.subheader("História")
    st.text(f"Título: {historia['titulo']}\n\nTema Educacional: {historia['tema_educacional']}\n\nObjetivo de Aprendizagem: {historia['objetivo_aprendizagem']}\n\nHistória Completa:\n\n{historia['historia']}")

    cenas = crew_response.tasks_output[3].to_dict()['cenas']

    st.divider()
    st.subheader("Cenas")

    for cena in cenas:
        st.write(f"Cena {cena['numero']}: {cena['racional']}")

    st.divider()
    st.subheader("Personagem")

    descrição_personagem = crew_response.tasks_output[1].to_dict()
    st.text(f"Características: {descrição_personagem['caracteristicas']}\n\nEstilo Visual: {descrição_personagem['estilo_visual']}\n\nPrompt IA: {descrição_personagem['prompt_ia']}")

    selector = APISelector(
        model="stability/generate/default/core", 
        model_type="image", 
        aspect_ratio="16:9", 
        style_preset="tile-texture",
        seed=27,
    )

    prompt_personagem = crew_response.tasks_output[1].to_dict()['prompt_ia']

    if st.session_state.personagem is not None:
        image = st.session_state.personagem
    else:
        task = Task(
            instruction=prompt_personagem,
            selector=selector,
            simple_response=True,
        )

        personagem = task.predict({})

        image_data = base64.b64decode(personagem)
        image = io.BytesIO(image_data)

        st.session_state.personagem = image

    st.image(image, use_container_width=True)

    st.divider()
    st.subheader(f"Cena {st.session_state.step + 1}")

    audios = crew_response.tasks_output[2].to_dict()['cenas']

    selector2 = APISelector(
        model="black-forest-labs/FLUX.1.1-pro",
        model_type="image", 
        aspect_ratio='16:9',
        style_preset="tile-texture",
        seed=1,
    )

    seed_image = Image.open(image)

    if st.session_state.step >= len(cenas) - 1:
        st.session_state.step = len(cenas) - 1

    cena = cenas[st.session_state.step]
    audio = audios[st.session_state.step]

    texto_cena = st.text_area("Narração", f"{audio['texto_tts']}", height=200)

    if st.button("Gerar Narração"):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        tts_response = client.audio.speech.create(
            model="tts-1-hd",
            voice="shimmer",
            input=texto_cena,
            response_format="wav",
            speed=1.0,
        )

        st.session_state.audio = tts_response.content

    if st.session_state.audio is not None:
        st.audio(st.session_state.audio, format='audio/wav')

        try:
            if st.session_state.audios[st.session_state.step] is not None:
                st.session_state.audios[st.session_state.step] = st.session_state.audio
        except:
            pass        

    st.divider()

    descricao_cena = st.text_area("Imagem",  f"{cena['prompt_ia']}", height=150)

    if st.button("Gerar Cena"):

        task = Task(
            instruction=descricao_cena,
            selector=selector2,
            simple_response=True,
        )

        cena_image_str = task.predict({"base_image": image})

        cena_image_data = base64.b64decode(cena_image_str)
        cena_image = io.BytesIO(cena_image_data)

        st.session_state.cena = cena_image

    if st.session_state.cena is not None:
        st.image(st.session_state.cena, use_container_width=True)

        try:
            if st.session_state.cenas[st.session_state.step] is not None:
                st.session_state.cenas[st.session_state.step] = st.session_state.cena
        except:
            pass

    st.divider()

    cols = st.columns(3)

    if cols[0].button("Começar Novamente", type="primary", use_container_width=True):
        st.session_state.step = 0
        st.session_state.click = False
        st.session_state.response = None
        st.session_state.personagem = None
        st.session_state.cena = None
        st.session_state.audio = None
        st.session_state.cenas = []
        st.session_state.audios = []

        st.rerun()

    if cols[1].button("Anterior", use_container_width=True):
        st.session_state.step -= 1
        st.session_state.step = max(0, st.session_state.step)

        try:
            st.session_state.cena = st.session_state.cenas[st.session_state.step]
            st.session_state.audio = st.session_state.audios[st.session_state.step]
        except:
            pass

        st.rerun()

    if cols[2].button("Próxima", use_container_width=True):
        if st.session_state.cena is None:
            st.error("Por favor, gere a cena antes de avançar.")
            st.stop()
        if st.session_state.audio is None:
            st.error("Por favor, gere a narração antes de avançar.")
            st.stop()

        st.session_state.step += 1  

        if st.session_state.step < len(st.session_state.cenas):
            st.session_state.cena = st.session_state.cenas[st.session_state.step]
            st.session_state.audio = st.session_state.audios[st.session_state.step]
        else:   
            st.session_state.cenas.append(st.session_state.cena)
            st.session_state.audios.append(st.session_state.audio)

            st.session_state.cena = None
            st.session_state.audio = None

        st.rerun()
    