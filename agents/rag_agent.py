from agents.base_agent import BaseAgent
from tools.rag_tool import search_documents

class RAGAgent(BaseAgent):
    def __init__(self, vectorstore):
        super().__init__("RAG")
        self.vectorstore = vectorstore
        self.system_prompt = """You are a helpful tutoring center AI assistant.
        Answer the student's question using ONLY the context provided.
        Be clear, friendly, and educational.
        If the answer is not in the context, say: 'I dont have information about that. Please ask your teacher.'"""

    def run(self, state: dict) -> dict:
        query = state["user_query"]

        rewrite_prompt = f"Rewrite this question to be better for document search (just rewrite, no explanation): {query}"
        better_query = self.call_llm(rewrite_prompt)

        context = search_documents(self.vectorstore, better_query)
        state["retrieved_context"] = context

        answer_prompt = f"""Context from tutoring center documents:
{context}

Student Question: {query}

Answer the student based on the context above:"""

        state["agent_response"] = self.call_llm(answer_prompt)
        print("📚 RAG Agent answered!")
        return state