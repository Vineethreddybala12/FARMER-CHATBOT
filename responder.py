from typing import Optional


_CROP_SPECIFIC_INFO = {
    "ask_fertilizer": {
        "maize": "Apply N-P-K 15:15:15 at planting, then side-dress urea (46-0-0) at 6-8 weeks and tasseling stage. Total: ~200 kg/ha.",
        "wheat": "Use 40-50 kg N, 20 kg P, 15 kg K per hectare. Split nitrogen: 50% at planting, 50% at shooting stage.",
        "rice": "Apply 60-80 kg N, 40 kg P, 40 kg K per hectare. Use split applications: 25% at tillering, 50% at panicle initiation, 25% at boot stage.",
        "tomato": "Use 150-200 kg NPK/ha with high K (more than N). Drip application: 2 kg/week after flowering. Include micronutrients (Zn, B).",
        "potato": "Apply 40 kg N, 80 kg P, 150 kg K per hectare (potatoes need high K). Use FYM 20 tons/ha + chemical fertilizers.",
        "soybean": "Soybean fixes nitrogen; apply 60 kg P and 40 kg K per hectare. Avoid excess nitrogen.",
        "cotton": "Apply 80-100 kg N, 40 kg P, 40 kg K per hectare. Avoid excess nitrogen (causes vegetative growth).",
        "sugarcane": "Apply 120 kg N, 60 kg P, 60 kg K per hectare. Add 30 tons FYM/ha.",
        "onion": "Apply 100 kg N, 50 kg P, 40 kg K per hectare. Avoid chloride-based potassium.",
        "cabbage": "Apply 80-100 kg N, 60 kg P, 40 kg K per hectare with 15 tons FYM/ha.",
    },
    "ask_pest": {
        "maize": "Armyworm: Spray Bt formulation (1 spray at 3-4 leaf stage). Stem borer: Carbofuran 3% CG at 1.5 kg/ha.",
        "wheat": "Early sown crops more prone to pests. Aphids: Spray imidacloprid 17.8% (50 ml/acre). Thrips: Triazophos 40% EC.",
        "rice": "Stem borer: Spray endosulfan 35% EC (2.5L/ha) at boot stage. Leaf folder: Hand collection or Spinosad.",
        "tomato": "Whiteflies: Yellow sticky traps + insecticidal soap. Fruit worm: Quinalphos 25% EC (2 ml/L water).",
        "potato": "Late blight: Mancozeb 75% WP (2.5 kg/ha) every 7-10 days. Aphids: Imidacloprid spray.",
        "cotton": "Pink bollworm: Install pheromone traps. Spray Bt @ 500-600 ml/ha at flower bud stage.",
        "cabbage": "Diamondback moth: Spinosad or Bt spray. Cabbage butterfly: Hand-pick eggs/young caterpillars.",
    },
    "ask_disease": {
        "maize": "Maize rust: Spray sulfur or triadimefon @ 2g/L. Blight: Use disease-resistant varieties.",
        "wheat": "Leaf rust: Propiconazole 25% EC (0.5 ml/L). Stripe rust: Hexaconazole. Powdery mildew: Sulfur spray.",
        "rice": "Blast: Tricyclazole @ 1g/L. Sheath blight: Validamycin A @ 1 ml/L or Hexaconazole.",
        "tomato": "Early blight: Mancozeb @ 2.5 g/L every 7-10 days. Late blight: Metalaxyl+Mancozeb.",
        "potato": "Late blight: Mancozeb 75% (2.5 kg/ha) every 7 days. Early blight: Carbendazim @ 0.5g/L.",
        "cabbage": "Black rot: Use disease-free seeds. White rot: Soil treatment with Trichoderma.",
    },
    "ask_irrigation": {
        "maize": "Total water needed: 450-600 mm. Critical stages: V6 (6 leaves), VT (tasseling), R3 (milk). Irrigate at 75% readily available water.",
        "wheat": "Total water: 300-450 mm across 3-4 irrigations. First irrigation at CRI (Crown Root Initiation, 20-25 days), then at boot and milking stage.",
        "rice": "Standing water 5-7 cm. Maintain this throughout season except at harvest. Drain 7-10 days before harvest.",
        "tomato": "Drip irrigation best (saves 35% water). 400-600 mm total. Frequent but light irrigation. Avoid wetting foliage.",
        "potato": "600-750 mm total water. Critical: 50-80 days after planting. Irrigate when soil moisture drops to 50%.",
        "cotton": "600-1000 mm depending on rainfall. Irrigate at flower bud + flowering. Avoid irrigation 30 days before harvest.",
    },
    "ask_planting": {
        "maize": "Sow June-July for kharif (monsoon). Seed rate: 20 kg/ha. Spacing: 60 x 25 cm (2 seeds/hill). Soil pH: 6-7.5.",
        "wheat": "Sow Nov-Dec for rabi. Seed rate: 100-125 kg/ha. In-row spacing: 20-25 cm for line sowing.",
        "rice": "Sow June-July after soil moisture. Nursery: 4-5 kg/100 sqm. Transplant after 25-35 days. Spacing: 20x15 cm.",
        "tomato": "Sep-Jan for best quality. Nursery in Aug-Oct. Transplant 35-40 days old seedlings. Spacing: 60x45 cm.",
        "potato": "Oct-Nov planting. Seed rate: 1.5-2 tons/ha (25g seed tubers). Depth: 5-7 cm. Spacing: 20 x 50 cm.",
        "cotton": "May-June sowing. Seed rate: 20 kg/ha (short duration) to 25 kg/ha (medium). Spacing: 90 x 60 cm.",
    },
    "ask_harvesting": {
        "maize": "Cobs turn dark, kernels become dull. Moisture 18-20%. Cut stalks when grain moisture reaches 15-18%. Dry to 12% for storage.",
        "wheat": "Plant turns golden, grain hard (cannot be dented). Harvest when moisture 10-12%. Use combine harvester for efficiency.",
        "rice": "Panicles droop, 80% grains hard. Harvest when moisture 15-20% (easier threshing). Thresh within 2 days.",
        "tomato": "Pick at breaker stage (first color change). Fully red: highly perishable. Store at 10-13°C, 85% RH.",
        "potato": "75-90 days after planting. Vine dies, tubers mature. Harvest when soil dry. Handle carefully to avoid bruising.",
        "cotton": "Bolls split, white lint visible, leaves start defoliation. Pick when 75% bolls open. Store in dry place.",
    },
    "ask_crop_info": {
        "maize": "Maize (corn): Kharif crop, 120-150 days. Needs 500-750 mm water. Uses soils pH 6-7.5. Hybrid varieties give 40-50 qt/ha.",
        "wheat": "Rabi cereal crop, 120-140 days. Temp: 15-25°C. Better in well-drained soils. Varieties: HD2967, DBW17. Yield: 40-60 qt/ha.",
        "rice": "Monsoon/kharif crop, 120-150 days. Waterlogged conditions needed. Yield: 50-70 qt/ha.",
        "tomato": "Solanaceae, 60-80 days to first picking, 120-150 days total cycle. Needs support, high K, warm days.",
        "potato": "75-90 day cycle. Cool season crop. Uses 20-25 tons compost/ha. High yielder: 250-400 qt/ha.",
        "cotton": "180-210 day crop. High-value commodity. Needs 40 cm rainfall minimum. Yield: 15-20 qt/ha (seed cotton).",
    },
    "ask_soil": {
        "default": "Ideal soil: pH 6.0-7.5, 2-3% organic matter. Add 15-20 tons compost/ha yearly. Get soil test every 2 years. Add lime if pH <6, sulfur if pH >7.5."
    },
    "ask_weather": {
        "default": "Monitor 7-day forecast. Heavy rain: risk of fungal diseases, reduce irrigation. Heatwave: increase irrigation, apply mulch. Frost: cover young plants."
    },
    "ask_seed": {
        "default": "Buy certified seeds from govt agencies (PKVY, FSI). Check: germination % (minimum 85%), purity (95%), moisture (8%). Store in cool, dry place (<20°C, <50% RH)."
    },
    "ask_market": {
        "default": "Check mandi prices (AGMARKNET.gov.in). Post-harvest loss: reduce through drying, storage in cool place. Do value addition: bottled juice, dried chips, etc."
    },
    "ask_subsidy": {
        "default": "Contact block/district agriculture office. Many schemes: PM-KISAN (income support), crop insurance, equipment subsidy. Verify eligibility & documentation needed."
    },
    "ask_equipment": {
        "default": "Small farms: Manual tools. Medium: Walking tractor (20-25 hp). Large: Tractor + implements. Rent equipment via cooperatives to reduce costs."
    }
}


def build_response(intent: str, crop: Optional[str], query: str) -> str:
    """Build specific crop-based responses."""
    intent = intent or "unknown"
    
    # Handle greeting/thanks
    if intent == "greeting":
        return "Namaste! I'm here to help with farming advice. Ask me about fertilizers, pests, diseases, irrigation, planting, harvesting, or crops."
    
    if intent == "thanks":
        return "You're welcome! Hope the advice is helpful. Ask more questions anytime!"
    
    # For non-crop-specific intents, return default
    if intent in ["ask_weather", "ask_seed", "ask_market", "ask_subsidy", "ask_equipment"]:
        return _CROP_SPECIFIC_INFO.get(intent, {}).get("default", "Please rephrase your question.")
    
    if intent == "ask_soil":
        return _CROP_SPECIFIC_INFO.get("ask_soil", {}).get("default", "Soil health is critical.")
    
    # For crop-specific intents, get advice for the crop
    if intent in _CROP_SPECIFIC_INFO:
        crop_advice_dict = _CROP_SPECIFIC_INFO[intent]
        
        if crop and crop in crop_advice_dict:
            return f"{crop.capitalize()} – {crop_advice_dict[crop]}"
        elif crop:
            # Fallback for crops not in database
            return f"For {crop}: {_CROP_SPECIFIC_INFO[intent].get(list(crop_advice_dict.keys())[0], 'Please consult local extension services for specific advice.')}"
        else:
            # No crop specified
            if intent == "ask_fertilizer":
                return "Which crop are you asking about? This helps me give specific fertilizer advice."
            elif intent == "ask_pest":
                return "Which crop has pests? Tell me the crop and I can recommend specific pest control."
            elif intent == "ask_disease":
                return "Which crop is affected? Pest management depends on the crop."
            elif intent == "ask_irrigation":
                return "Which crop needs irrigation? Water requirements vary by crop."
            elif intent == "ask_planting":
                return "Which crop are you planning to plant? Each has different planting dates & methods."
            elif intent == "ask_harvesting":
                return "Which crop are you harvesting? Harvest time varies significantly by crop."
            elif intent == "ask_crop_info":
                return "Which crop would you like to know about? Please mention the crop name."
    
    return "I couldn't understand that. Ask me about: fertilizer, pests, diseases, irrigation, planting, harvesting, or specific crops."


if __name__ == "__main__":
    print(build_response("ask_fertilizer", "maize", "Which fertilizer for maize?"))
