from crewai import Crew, Process

from src.crew.video.agents.character_designer import agent as character_agent
from src.crew.video.agents.character_designer import task as character_task

from src.crew.video.agents.scene_director import agent as scene_agent
from src.crew.video.agents.scene_director import task as scene_task

from src.crew.video.agents.story_creator import agent as story_agent
from src.crew.video.agents.story_creator import task as story_task

from src.crew.video.agents.voice_script import agent as voice_agent
from src.crew.video.agents.voice_script import task as voice_task


video_crew = Crew(
    agents=[
        story_agent,
        voice_agent,
        scene_agent,
        character_agent,
    ],
    tasks=[
        story_task,
        character_task,
        voice_task,
        scene_task,
    ],
    process=Process.sequential
)