// frontend/src/components/PestDiagnosis.jsx

import React from 'react';

function PestDiagnosis({ diseaseRisks, highestRiskSolution }) {
    // If there's no disease risk data, don't render anything
    if (!diseaseRisks || Object.keys(diseaseRisks).length === 0) {
        return null;
    }

    // Find the disease with the highest risk score for the day
    let topThreat = { name: "None", risk: 0 };
    for (const [disease, risk] of Object.entries(diseaseRisks)) {
        if (risk > topThreat.risk) {
            topThreat = { name: disease, risk: risk };
        }
    }

    // If the highest risk is very low, show a "clear" message
    if (topThreat.risk < 0.2) {
        return (
            <div className="mt-4 bg-green-800/30 p-3 rounded-lg text-center">
                <p className="text-green-300 font-semibold"> No significant disease risk today.</p>
            </div>
        );
    }

    // Determine the color based on risk level
    const riskColor = topThreat.risk > 0.6 ? 'text-red-400' : 'text-yellow-400';

    return (
        <div className="mt-4 p-4 rounded-lg bg-gray-800/50 border border-gray-700">
            <h4 className="text-lg font-bold text-gray-300 text-center">AI Pest & Disease Diagnosis</h4>
            <div className="text-center mt-2">
                <p className="text-gray-400">Highest Threat Today:</p>
                <p className={`text-2xl font-bold ${riskColor}`}>{topThreat.name}</p>
                <p className={`text-xl font-semibold ${riskColor}`}>Risk Level: {(topThreat.risk * 100).toFixed(0)}%</p>
            </div>
            
            {/* If there is a solution from the backend, display it */}
            {highestRiskSolution && (
                <div className="mt-3 bg-blue-900/30 p-3 rounded">
                    <p className="text-sm font-bold text-blue-300 uppercase">Recommended Solution:</p>
                    <p className="text-blue-200 mt-1">{highestRiskSolution}</p>
                </div>
            )}
        </div>
    );
}

export default PestDiagnosis;