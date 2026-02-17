

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from train_snips import FarmingIntentClassifier
import json

def test_model():
    """Test the trained farming model."""
    print("Testing Farming Intent Classifier")
    print("=" * 40)

    # Load the trained model
    classifier = FarmingIntentClassifier()
    classifier.load_model("./farming_model")

    # Test cases
    test_cases = [
        "What fertilizer should I use for maize?",
        "How to control pests in tomatoes?",
        "When should I harvest wheat?",
        "Watering schedule for rice fields",
        "Planting guide for potatoes",
        "Disease control in cotton crops",
        "Information about growing soybeans",
        "Irrigation tips for sugarcane"
    ]

    print(f"Testing {len(test_cases)} examples:\n")

    correct_predictions = 0
    total_predictions = len(test_cases)

    for i, text in enumerate(test_cases, 1):
        result = classifier.predict(text)
        intent = result['intent']
        confidence = result['score']

        # Expected intents based on the text
        expected_mapping = {
            "What fertilizer should I use for maize?": "ask_fertilizer",
            "How to control pests in tomatoes?": "ask_pest",
            "When should I harvest wheat?": "ask_harvesting",
            "Watering schedule for rice fields": "ask_irrigation",
            "Planting guide for potatoes": "ask_planting",
            "Disease control in cotton crops": "ask_disease",
            "Information about growing soybeans": "ask_crop_info",
            "Irrigation tips for sugarcane": "ask_irrigation"
        }

        expected = expected_mapping.get(text, "unknown")
        is_correct = intent == expected

        if is_correct:
            correct_predictions += 1

        status = "✓" if is_correct else "✗"
        print(f"{i}. {status} '{text}'")
        print(f"   Predicted: {intent} ({confidence:.3f}) | Expected: {expected}")
        print()

    accuracy = correct_predictions / total_predictions * 100
    print(f"Accuracy: {correct_predictions}/{total_predictions} ({accuracy:.1f}%)")

    return accuracy

def compare_models():
    """Compare fine-tuned model vs zero-shot classifier."""
    print("\nComparing Models")
    print("=" * 40)

    # Load fine-tuned model
    fine_tuned = FarmingIntentClassifier()
    fine_tuned.load_model("./farming_model")

    # Test text
    test_text = "Which fertilizer for maize?"

    print(f"Test query: '{test_text}'")
    print()

    # Fine-tuned prediction
    ft_result = fine_tuned.predict(test_text)
    print("Fine-tuned model:")
    print(f"  Intent: {ft_result['intent']}")
    print(f"  Confidence: {ft_result['score']:.3f}")
    print()

    # # Zero-shot prediction (fallback)
    # fine_tuned.model = None  # Force zero-shot
    # zs_result = fine_tuned.predict(test_text)
    # print("Zero-shot classifier:")
    # print(f"  Intent: {zs_result['intent']}")
    # print(f"  Confidence: {zs_result['score']:.3f}")

if __name__ == "__main__":
    if not os.path.exists("./farming_model"):
        print("❌ farming_model directory not found!")
        print("Please run training first: python train_snips.py")
        sys.exit(1)

    try:
        test_model()
        compare_models()
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        sys.exit(1)