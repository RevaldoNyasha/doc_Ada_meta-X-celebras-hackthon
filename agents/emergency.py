  # Emergency handling agent
from livekit.agents import Agent
from livekit.agents import deepgram, silero
from livekit.agents import openai
from utils.context_loader import load_context

class EmergencyAgent(Agent):
    def __init__(self):
        context = load_context()
        llm = openai.LLM.with_cerebras(model="llama-4-scout-17b-16e-instruct")
        stt = deepgram.STT()
        tts = deepgram.TTS()
        vad = silero.VAD.load()

        instructions = f"""
        You are an emergency medical agent. Your goal is to identify urgent cases and instruct the user
        to seek immediate medical attention when necessary.
        """
        super().__init__(instructions=instructions, stt=stt, llm=llm, tts=tts, vad=vad)

    async def on_enter(self):
        print("🚨 Emergency Agent Active")
        await self.session.generate_reply(user_input="Please call emergency services or go to the nearest hospital.")
