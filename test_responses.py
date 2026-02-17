import requests

queries = [
    'How to plant tomatoes?',
    'What disease affects wheat?',
    'When should I harvest maize?',
    'What irrigation for rice?',
    'Tell me about potato',
    'What soil do I need?'
]

for q in queries:
    r = requests.post('http://127.0.0.1:5000/query', json={'query': q})
    data = r.json()
    intent = data.get('intent', 'unknown')
    advice = data.get('advice', 'N/A')
    print(f'Q: {q}')
    print(f'Intent: {intent}')
    print(f'Answer: {advice}')
    print('-' * 70)
