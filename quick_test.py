
from intent_classifier import IntentClassifier

c = IntentClassifier()

test_queries = [
    "What fertilizer for maize?",
    "How to harvest wheat?",
    "Pest control for rice",
    "When to plant tomatoes",
    "Disease prevention in cotton"
]

print("Testing Farming Intent Classifier")
print("=" * 50)

for query in test_queries:
    result = c.predict(query)
    intent = result['intent']
    score = result['score']
    print(f"Query: {query}")
    print(f"Intent: {intent} (confidence: {score:.3f})")
    print()
