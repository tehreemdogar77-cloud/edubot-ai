from agents.base_agent import BaseAgent

class RouterAgent(BaseAgent):
    def __init__(self):
        super().__init__("Router")
        self.system_prompt = """You are a query classifier for a tutoring center AI.

        Look at the student's question and reply with ONLY one word:
        - Reply 'rag' if the student is asking about study topics, concepts, fees, or schedules
        - Reply 'quiz' if the student wants a quiz, test, or practice questions
        - Reply 'general' if the student is just greeting or having casual conversation

        Reply with ONLY one word. Nothing else."""

    def run(self, state: dict) -> dict:
        query = state["user_query"]
        result = self.call_llm(query).strip().lower()

        if result not in ["rag", "quiz", "general"]:
            result = "rag"

        state["query_type"] = result
        print(f"🔀 Router decided: {result}")
        return state