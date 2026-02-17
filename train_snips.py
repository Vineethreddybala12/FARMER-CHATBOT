import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, Dataset, DatasetDict
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import json
import os


class FarmingIntentClassifier:
    """Fine-tuned intent classifier using farming dataset."""

    def __init__(self, model_name="distilbert-base-uncased", num_labels=7):
        self.model_name = model_name
        self.num_labels = num_labels
        self.tokenizer = None
        self.model = None
        self.label_to_intent = {}
        self.intent_to_label = {}

    def load_farming_data(self):
        """Load custom farming dataset."""
        print("Loading farming dataset...")

        # Load JSON files
        with open("farming_dataset/train.json", "r") as f:
            train_data = json.load(f)

        with open("farming_dataset/validation.json", "r") as f:
            val_data = json.load(f)

        with open("farming_dataset/test.json", "r") as f:
            test_data = json.load(f)

        # Get unique intents
        intents = set()
        for example in train_data + val_data + test_data:
            intents.add(example["intent"])

        # Create label mappings
        self.label_to_intent = {i: intent for i, intent in enumerate(sorted(intents))}
        self.intent_to_label = {intent: i for i, intent in self.label_to_intent.items()}
        self.num_labels = len(intents)

        print(f"Found {self.num_labels} intents: {list(self.label_to_intent.values())}")

        # ✅ CONVERT TO DatasetDict (THIS IS THE FIX)
        dataset = DatasetDict({
            "train": Dataset.from_list(train_data),
            "validation": Dataset.from_list(val_data),
            "test": Dataset.from_list(test_data)
        })

        return dataset

    def preprocess_function(self, examples):
        """Tokenize and encode the text."""
        return self.tokenizer(
            examples["text"],
            truncation=True,
            padding="max_length",
            max_length=128
        )

    def encode_labels(self, examples):
        """Convert intent strings to integers."""
        examples["label"] = [self.intent_to_label[intent] for intent in examples["intent"]]
        return examples

    def compute_metrics(self, eval_pred):
        """Compute accuracy, precision, recall, F1."""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)

        accuracy = accuracy_score(labels, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, predictions, average="weighted"
        )

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }

    def train(self, output_dir="./farming_model", epochs=10, batch_size=8):
        """Fine-tune the model on farming dataset."""
        print("Setting up tokenizer and model...")

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=self.num_labels
        )

        # Load and preprocess data
        dataset = self.load_farming_data()

        print("Preprocessing data...")
        encoded_dataset = dataset.map(self.preprocess_function, batched=True)
        encoded_dataset = encoded_dataset.map(self.encode_labels, batched=True)

        # Set format for PyTorch
        encoded_dataset.set_format(
            type="torch",
            columns=["input_ids", "attention_mask", "label"]
        )

        # Training arguments - improved for better convergence
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=50,
            weight_decay=0.01,
            learning_rate=2e-5,
            logging_dir="./logs",
            logging_steps=5,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            greater_is_better=True,
            gradient_accumulation_steps=2,
        )

        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=encoded_dataset["train"],
            eval_dataset=encoded_dataset["validation"],
            compute_metrics=self.compute_metrics,
        )

        print("Starting training...")
        trainer.train()

        # Save model
        print(f"Saving model to {output_dir}")
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)

        # Save label mappings
        with open(os.path.join(output_dir, "label_mappings.json"), "w") as f:
            json.dump(
                {
                    "label_to_intent": self.label_to_intent,
                    "intent_to_label": self.intent_to_label
                },
                f,
                indent=2
            )

        return trainer

    def load_model(self, model_dir="./farming_model"):
        """Load a trained model."""
        print(f"Loading model from {model_dir}")

        with open(os.path.join(model_dir, "label_mappings.json"), "r") as f:
         mappings = json.load(f)

    # Convert keys back to int (JSON makes them strings)
        self.label_to_intent = {
        int(k): v for k, v in mappings["label_to_intent"].items()
    }
        self.intent_to_label = {
        k: int(v) for k, v in mappings["intent_to_label"].items()
    }
        self.num_labels = len(self.label_to_intent)
       
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)

    def predict(self, text):
        """Predict intent for a given text."""
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=128
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()

        intent = self.label_to_intent[predicted_class]

        all_probs = probabilities[0].tolist()
        all_intents_scores = list(zip(
            [self.label_to_intent[i] for i in range(len(all_probs))],
            all_probs
        ))

        return {
            "intent": intent,
            "score": confidence,
            "all": all_intents_scores
        }


if __name__ == "__main__":
    classifier = FarmingIntentClassifier()
    classifier.train(epochs=5, batch_size=16)

    test_texts = [
        "What's the best fertilizer for maize?",
        "How to control pests in tomatoes",
        "When should I harvest wheat",
        "Watering schedule for rice",
        "Planting guide for potatoes",
        "Disease control in cotton"
    ]

    print("\nTesting predictions:")
    for text in test_texts:
        result = classifier.predict(text)
        print(f"Text: '{text}' -> Intent: {result['intent']} (confidence: {result['score']:.3f})")
