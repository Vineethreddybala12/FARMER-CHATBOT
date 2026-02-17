from transformers import pipeline


class IntentClassifier:
    """Intent classifier using zero-shot BART (pre-trained, no fine-tuning)."""

    def __init__(self):
        """Initialize zero-shot classifier."""
        print("Loading intent classifier (zero-shot BART)...")
        
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        # Main farming intents
        self.intents = [
            "ask_crop_info",
            "ask_fertilizer",
            "ask_pest",
            "ask_irrigation",
            "ask_planting",
            "ask_harvesting",
            "ask_disease",
        ]
        
        print("Classifier loaded successfully!")

    def predict(self, text):
        """Predict intent using zero-shot classification."""
        try:
            result = self.classifier(text, self.intents, multi_class=False)
            
            top_intent = result["labels"][0]
            confidence = float(result["scores"][0])
            
            return {
                "intent": top_intent,
                "score": confidence,
                "all": [
                    {"intent": label, "score": float(score)}
                    for label, score in zip(result["labels"], result["scores"])
                ]
            }
        except Exception as e:
            print(f"Error in predict: {e}")
            return {
                "intent": "unknown",
                "score": 0.0,
                "error": str(e),
                "all": []
            }


if __name__ == "__main__":
    c = IntentClassifier()
    print(c.predict("Which fertilizer should I use for maize?"))
