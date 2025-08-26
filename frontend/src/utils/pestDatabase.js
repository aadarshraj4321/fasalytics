// frontend/src/utils/pestDatabase.js

// This is a frontend version of our backend pest database.
// It helps in displaying the correct solution for a given disease name.
export const PEST_DATABASE = {
    "Wheat": [
        { "name": "Rust (Gerua Rog)", "solution": "Apply fungicides like Propiconazole or Tebuconazole. Contact local agriculture expert for dosage." },
        { "name": "Powdery Mildew (Chhachhiya Rog)", "solution": "Spray wettable sulphur or consult expert for specific fungicides like Dinocap." }
    ],
    "Rice": [
        { "name": "Blast (Jhonka Rog)", "solution": "Use resistant varieties. Spray fungicides like Tricyclazole at first sign of disease." },
        { "name": "Bacterial Blight (Jhulsa Rog)", "solution": "Ensure proper drainage. Use copper-based bactericides as a preventive measure." }
    ],
    "Sugarcane": [
        { "name": "Red Rot", "solution": "Use disease-free seeds. Uproot and destroy affected plants. Practice crop rotation." },
        { "name": "Smut", "solution": "Use resistant varieties. Remove and carefully bag/destroy smutted whips." }
    ]
};

export const getSolutionForDisease = (cropType, diseaseName) => {
    const cropDiseases = PEST_DATABASE[cropType] || [];
    const diseaseInfo = cropDiseases.find(d => d.name === diseaseName);
    return diseaseInfo ? diseaseInfo.solution : "Consult a local agricultural expert for advice.";
};