 # Specialist agent (cardiology, pediatrics, etc.)

from livekit.agents import Agent, function_tool
from livekit.agents import openai, silero, deepgram
from utils.context_loader import load_context

class SpecialistAgent(Agent):
    def __init__(self):
        context = load_context()
        llm = openai.LLM.with_cerebras(model="llama-4-scout-17b-16e-instruct")
        stt = deepgram.STT()
        tts = deepgram.TTS()
        vad = silero.VAD.load()

        instructions = f"""
        You are a medical specialist agent. Focus on in-depth explanations and technical details.
        Use ONLY the following context:

        {context}

        CRITICAL RULES:
        - Answer questions with accurate medical information
        - If unsure, advise consulting a qualified doctor
        """
        super().__init__(instructions=instructions, stt=stt, llm=llm, tts=tts, vad=vad)

    async def on_enter(self):
        print("🔬 Specialist Agent Active")
        await self.session.generate_reply(user_input="Hello! I can provide detailed medical guidance.")
