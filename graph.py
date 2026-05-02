from typing import TypedDict
from langgraph.graph import StateGraph, END
from tools.rag_tool import load_knowledge_base, create_vectorstore
from agents.router_agent import RouterAgent
from agents.rag_agent import RAGAgent
from agents.quiz_agent import QuizAgent
from agents.general_agent import GeneralAgent
from agents.evaluator_agent import EvaluatorAgent

class AgentState(TypedDict):
    user_query: str
    query_type: str
    retrieved_context: str
    agent_response: str
    evaluation_result: str
    final_response: str
    retry_count: int

print('Loading knowledge base...')
documents = load_knowledge_base('knowledge_base/')
vectorstore = create_vectorstore(documents)

router = RouterAgent()
rag = RAGAgent(vectorstore)
quiz = QuizAgent(vectorstore)
general = GeneralAgent()
evaluator = EvaluatorAgent()

def route_query(state):
    return state['query_type']

def check_evaluation(state):
    if state['evaluation_result'] == 'pass':
        return 'pass'
    elif state.get('retry_count', 0) >= 1:
        return 'pass'
    else:
        state['retry_count'] = state.get('retry_count', 0) + 1
        return 'fail'

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node('router', router.run)
    workflow.add_node('rag_agent', rag.run)
    workflow.add_node('quiz_agent', quiz.run)
    workflow.add_node('general_agent', general.run)
    workflow.add_node('evaluator', evaluator.run)
    workflow.set_entry_point('router')
    workflow.add_conditional_edges('router', route_query, {
        'rag': 'rag_agent',
        'quiz': 'quiz_agent',
        'general': 'general_agent'
    })
    workflow.add_edge('rag_agent', 'evaluator')
    workflow.add_edge('quiz_agent', 'evaluator')
    workflow.add_edge('general_agent', 'evaluator')
    workflow.add_conditional_edges('evaluator', check_evaluation, {
        'pass': END,
        'fail': 'rag_agent'
    })
    return workflow.compile()

app = build_graph()
