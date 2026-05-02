from agents.base_agent import BaseAgent
from tools.rag_tool import search_documents

class QuizAgent(BaseAgent):
    def __init__(self, vectorstore):
        super().__init__("Quiz")
        self.vectorstore = vectorstore
        self.system_prompt = """You are a quiz generator for a tutoring center.
        Create clear multiple-choice questions in this format:

        Q1: [Question]
        A) [Option]
        B) [Option]
        C) [Option]
        D) [Option]
        Answer: [Correct letter]

        Always create exactly 3 questions."""

    def run(self, state: dict) -> dict:
        query = state["user_query"]
        context = search_documents(self.vectorstore, query)
        state["retrieved_context"] = context

        quiz_prompt = f"""Based on this study material:
{context}

Student request: {query}

Generate a 3-question multiple choice quiz:"""

        state["agent_response"] = self.call_llm(quiz_prompt)
        print("🧪 Quiz Agent generated questions!")
        return state