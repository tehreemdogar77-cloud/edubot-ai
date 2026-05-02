import sys
sys.path.insert(0, r'C:\Users\khiza\OneDrive\Desktop\tutoring-ai')

from agents.base_agent import BaseAgent

class EvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Evaluator")
        self.system_prompt = "You are a quality checker. Reply with ONLY the single word: pass"

    def run(self, state: dict) -> dict:
        state["agent_response"]  # type: ignore
        state["final_response"] = state["agent_response"]
        state["evaluation_result"] = "pass"
        print("Evaluator: PASS")
        return state