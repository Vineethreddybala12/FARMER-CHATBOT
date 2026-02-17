import json
import os
from sklearn.model_selection import train_test_split


def create_farming_dataset():
    """Create a farming-specific dataset in SNIPS format."""

    # Expanded farming intent examples with 20+ per intent for better training
    farming_data = {
        "ask_crop_info": [
            "Tell me about maize cultivation",
            "What do I need to know about growing wheat",
            "Information on rice farming",
            "How to grow tomatoes",
            "Details about potato farming",
            "Banana cultivation guide",
            "Mango farming tips",
            "Sugarcane growing information",
            "Cotton farming basics",
            "How do you grow soybean",
            "General information about lentil crop",
            "Crop details for chickpeas",
            "What are barley cultivation methods",
            "Groundnut growing information",
            "Coffee plant characteristics",
            "Tea plant cultivation",
            "Sunflower growing guide",
            "Rapeseed farming information",
            "Mustard seed cultivation",
            "Provide crop information"
        ],
        "ask_fertilizer": [
            "What fertilizer should I use for maize",
            "Fertilizer recommendations for wheat",
            "Which fertilizer for rice fields",
            "Fertilizer for tomato plants",
            "What to use for potato fertilizer",
            "Fertilizer advice for soybeans",
            "Best fertilizer for cotton",
            "Fertilizer for sugarcane",
            "Best NPK ratio for maize",
            "Urea application for wheat",
            "Phosphorus fertilizer for rice",
            "Potassium for vegetables",
            "Organic fertilizer options for tomatoes",
            "Compost application rates",
            "Micronutrient fertilizers",
            "Calcium deficiency treatment",
            "Magnesium fertilizer needs",
            "Boron application timing",
            "How to apply foliar fertilizers",
            "Describe fertilizer requirements"
        ],
        "ask_pest": [
            "How to control pests in maize",
            "Pest management for wheat",
            "Rice pest control methods",
            "Pests affecting tomatoes",
            "Potato pest problems",
            "Soybean pest control",
            "Cotton pest management",
            "Sugarcane pest control",
            "Controlling aphids on crops",
            "Dealing with armyworms",
            "Prevention of fall armyworm",
            "Managing spider mites",
            "Whitefly control strategies",
            "Thrips management methods",
            "Scale insect control",
            "Nematode pest management",
            "Caterpillar identification",
            "Biological pest control options",
            "Pesticide safety measures",
            "Explain pest management"
        ],
        "ask_irrigation": [
            "Watering schedule for maize",
            "Irrigation for wheat crops",
            "Rice field irrigation",
            "Tomato plant watering",
            "Potato irrigation needs",
            "Soybean watering requirements",
            "Cotton irrigation methods",
            "Sugarcane irrigation",
            "How often to water vegetables",
            "Drip irrigation for tomatoes",
            "Flood irrigation for rice",
            "Micro-irrigation systems",
            "Water requirements for wheat",
            "Sprinkler system setup",
            "Soil moisture monitoring",
            "Irrigation scheduling tips",
            "Water conservation methods",
            "Canal irrigation management",
            "Efficient water use techniques",
            "Tell me about irrigation"
        ],
        "ask_planting": [
            "When to plant maize",
            "Planting time for wheat",
            "Rice planting season",
            "Tomato planting guide",
            "Potato planting tips",
            "Soybean planting dates",
            "Cotton planting information",
            "Sugarcane planting methods",
            "Best planting season for vegetables",
            "Seed spacing for maize",
            "How deep to plant seeds",
            "Planting density for rice",
            "Recommended row spacing for wheat",
            "Seed germination requirements",
            "Soil preparation before planting",
            "Nursery establishment guide",
            "Transplanting seedlings correctly",
            "Intercropping planting patterns",
            "Direct seeding vs transplanting",
            "Explain planting procedures"
        ],
        "ask_harvesting": [
            "When to harvest maize",
            "Wheat harvesting time",
            "Rice harvesting guide",
            "Tomato harvesting tips",
            "Potato harvesting season",
            "Soybean harvesting",
            "Cotton harvesting methods",
            "Sugarcane harvesting",
            "Signs of crop maturity",
            "How to identify ripe tomatoes",
            "Wheat maturity indicators",
            "Rice grain ripeness",
            "When to harvest potatoes",
            "Post-harvest handling of crops",
            "Grain storage after harvest",
            "Fruit preservation techniques",
            "Harvest timing for best quality",
            "Equipment for harvesting grains",
            "Mechanical harvester operation"
        ],
        "ask_disease": [
            "Maize disease control",
            "Wheat disease management",
            "Rice disease prevention",
            "Tomato diseases and treatment",
            "Potato disease control",
            "Soybean disease management",
            "Cotton disease control",
            "Sugarcane disease prevention",
            "Fungal disease treatment",
            "Bacterial wilt management",
            "Leaf blight control",
            "Root rot prevention",
            "Powdery mildew treatment",
            "Early blight management",
            "Downy mildew control",
            "Leaf spot disease prevention",
            "Damping off disease prevention",
            "Fungicide application timing",
            "Disease-resistant variety selection"
        ]
    }

    # Convert to balanced training format
    train_data = []
    validation_data = []
    test_data = []

    for intent, examples in farming_data.items():
        # Split examples: 70% train, 15% validation, 15% test
        train_examples, temp_examples = train_test_split(examples, test_size=0.3, random_state=42)
        val_examples, test_examples = train_test_split(temp_examples, test_size=0.5, random_state=42)

        # Add to train
        for example in train_examples:
            train_data.append({"text": example, "intent": intent})

        # Add to validation
        for example in val_examples:
            validation_data.append({"text": example, "intent": intent})

        # Add to test
        for example in test_examples:
            test_data.append({"text": example, "intent": intent})

    # Create dataset directory
    os.makedirs("farming_dataset", exist_ok=True)

    # Save as JSON
    with open("farming_dataset/train.json", "w") as f:
        json.dump(train_data, f, indent=2)

    with open("farming_dataset/validation.json", "w") as f:
        json.dump(validation_data, f, indent=2)

    with open("farming_dataset/test.json", "w") as f:
        json.dump(test_data, f, indent=2)

    print(f"✓ Farming dataset created:")
    print(f"  Train: {len(train_data)} examples")
    print(f"  Validation: {len(validation_data)} examples")
    print(f"  Test: {len(test_data)} examples")
    print(f"  Total: {len(train_data) + len(validation_data) + len(test_data)} examples")
    print(f"  Intents: {len(farming_data)}")


if __name__ == "__main__":
    create_farming_dataset()