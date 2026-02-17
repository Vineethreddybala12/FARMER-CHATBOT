from rapidfuzz import process, fuzz


# Simple crop list (extendable)
_CROPS = [
    "maize",
    "wheat",
    "rice",
    "soybean",
    "potato",
    "tomato",
    "onion",
    "banana",
    "mango",
    "sugarcane",
    "cotton",
    "barley",
    "sorghum",
    "peas",
    "beans",
    "lentils",
    "chickpeas",
    "groundnut",
    "sunflower",
    "mustard",
    "cabbage",
    "cauliflower",
    "broccoli",
    "carrot",
    "spinach",
    "lettuce",
    "cucumber",
    "eggplant",
    "pepper",
    "okra",
    "bitter gourd",
    "pumpkin",
    "watermelon",
    "melon",
    "grapes",
    "apple",
    "orange",
    "lemon",
    "lime",
    "papaya",
    "pineapple",
    "guava",
    "pomegranate",
    "cashew",
    "almond",
    "walnut",
    "coffee",
    "tea",
    "cocoa",
    "rubber",
    "jute",
    "hemp",
    "flax",
    "sisal",
]


def extract_crop(text, threshold=70):
    """Return best crop match from text or None.

    Uses fuzzy matching to find crop names mentioned in farmer text.
    """
    if not text or not text.strip():
        return None
    text_lower = text.lower()
    # try direct containment first
    for c in _CROPS:
        if c in text_lower:
            return c

    # fallback: fuzzy match using rapidfuzz
    best = process.extractOne(text_lower, _CROPS, scorer=fuzz.partial_ratio)
    if best and best[1] >= threshold:
        return best[0]
    return None


if __name__ == "__main__":
    print(extract_crop("Should I apply urea to my maize?"))
