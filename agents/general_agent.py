from agents.base_agent import BaseAgent

class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__("General")
        self.system_prompt = """You are a friendly AI assistant for a tutoring center in Pakistan.
        Be warm, encouraging, and motivating to students.
        Keep responses short and friendly."""

    def run(self, state: dict) -> dict:
        query = state["user_query"]
        state["agent_response"] = self.call_llm(query)
        state["retrieved_context"] = ""
        print("💬 General Agent responded!")
        return state