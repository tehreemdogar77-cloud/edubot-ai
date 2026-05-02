import sys
sys.path.insert(0, r'C:\Users\khiza\OneDrive\Desktop\tutoring-ai')

from graph import app

def run_chatbot():
    print('EduBot - Tutoring Center AI!')
    print('Ask: Math, Science, English, Fees, or Quiz')
    print('Type quit to exit')
    print('-'*40)
    while True:
        user_input = input('You: ').strip()
        if not user_input:
            continue
        if user_input.lower() in ['quit', 'exit']:
            print('Goodbye!')
            break
        initial_state = {
            'user_query': user_input,
            'query_type': '',
            'retrieved_context': '',
            'agent_response': '',
            'evaluation_result': '',
            'final_response': '',
            'retry_count': 0
        }
        print('Thinking...')
        result = app.invoke(initial_state)
        print('EduBot: ' + str(result['final_response']))
        print('-'*40)

if __name__ == '__main__':
    run_chatbot()
