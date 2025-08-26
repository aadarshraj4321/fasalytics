# simulation/pest_database.py

# This file acts as a knowledge base for crop-specific diseases,
# their environmental triggers, and recommended solutions.

PEST_DATABASE = {
    "Wheat": [
        {
            "name": "Rust (Gerua Rog)",
            "type": "Fungus",
            # Rust thrives in cool (but not cold) and very humid conditions.
            "trigger_conditions": {
                "min_temp": 15, 
                "max_temp": 22, 
                "min_humidity_pct": 85
            },
            "symptoms": "Yellow, brown, or black powdery pustules on leaves and stems.",
            "solution": "Use resistant varieties. Apply fungicides like Propiconazole or Tebuconazole at the first sign of infection. Avoid excessive nitrogen fertilizer."
        },
        {
            "name": "Powdery Mildew (Chhachhiya Rog)",
            "type": "Fungus",
            # This disease prefers slightly warmer and drier (but still humid) conditions than rust.
            "trigger_conditions": {
                "min_temp": 20, 
                "max_temp": 25, 
                "min_humidity_pct": 80
            },
            "symptoms": "White, powdery patches on the surface of leaves, stems, and heads.",
            "solution": "Ensure good air circulation. Spray wettable sulphur or specific fungicides like Dinocap. Remove and destroy infected plant parts."
        }
    ],
    "Rice": [
        {
            "name": "Blast (Jhonka Rog)",
            "type": "Fungus",
            # Rice Blast is famous for loving high humidity and warm nights.
            "trigger_conditions": {
                "min_temp": 25, 
                "max_temp": 28, 
                "min_humidity_pct": 90
            },
            "symptoms": "Spindle-shaped or diamond-shaped spots on leaves. Can cause 'neck rot'.",
            "solution": "Use resistant seed varieties. Avoid over-fertilization with nitrogen. Apply fungicides like Tricyclazole or Isoprothiolane."
        },
        {
            "name": "Bacterial Blight (Jhulsa Rog)",
            "type": "Bacteria",
            # Spreads rapidly in rainy, windy weather and high temperatures.
            "trigger_conditions": {
                "min_temp": 25, 
                "max_temp": 30, 
                "min_humidity_pct": 70
            },
            "symptoms": "Water-soaked streaks starting from the leaf tips that turn yellow and die.",
            "solution": "Use disease-free seeds. Ensure proper field drainage to avoid standing water. Apply copper-based bactericides as a preventive measure."
        }
    ],
    "Sugarcane": [
        {
            "name": "Red Rot",
            "type": "Fungus",
            # Spreads through infected seed canes and soil in warm, wet conditions.
            "trigger_conditions": {
                "min_temp": 20, 
                "max_temp": 30, 
                "min_humidity_pct": 75
            },
            "symptoms": "Reddening of the internal tissues of the cane, often with white spots. Gives off a sour, alcoholic smell.",
            "solution": "Crucially, use certified disease-free seed canes. Practice crop rotation. Uproot and destroy affected clumps to prevent spread."
        },
        {
            "name": "Smut",
            "type": "Fungus",
            # Thrives in dry, hot weather.
            "trigger_conditions": {
                "min_temp": 26, 
                "max_temp": 32, 
                "min_humidity_pct": 50 # Note: this disease prefers lower humidity
            },
            "symptoms": "A long, black, whip-like structure emerges from the central shoot of the cane.",
            "solution": "Use resistant varieties. Remove and carefully place smutted whips in a bag to avoid spreading spores, then destroy them. Treat seed canes with hot water."
        }
    ]
}

# Example of how to access the data
if __name__ == '__main__':
    print("--- Accessing Pest Database ---")
    
    # Get all diseases for Wheat
    wheat_diseases = PEST_DATABASE.get("Wheat", [])
    print(f"\nDiseases for Wheat: {[d['name'] for d in wheat_diseases]}")
    
    # Get the trigger conditions for Rice Blast
    for disease in PEST_DATABASE.get("Rice", []):
        if disease["name"] == "Blast (Jhonka Rog)":
            print(f"\nTrigger conditions for Rice Blast: {disease['trigger_conditions']}")
            print(f"Recommended solution: {disease['solution']}")
            break