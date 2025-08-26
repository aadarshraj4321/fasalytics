// frontend/src/components/DailyPlan.jsx

import React from 'react';
import { getSolutionForDisease } from '../utils/pestDatabase';

// --- Sub-component for Weather Alerts ---
const getAlertStyle = (alertText) => {
    if (alertText.includes("HEAT WAVE")) return { color: "bg-red-500/20 text-red-300 border-red-500", icon: "🔥" };
    if (alertText.includes("HEAVY RAIN")) return { color: "bg-blue-500/20 text-blue-300 border-blue-500", icon: "💧" };
    if (alertText.includes("COLD WAVE")) return { color: "bg-sky-500/20 text-sky-300 border-sky-500", icon: "❄️" };
    if (alertText.includes("DROUGHT")) return { color: "bg-yellow-500/20 text-yellow-300 border-yellow-500", icon: "☀️" };
    return { color: "bg-gray-700 text-gray-300 border-gray-600", icon: "ℹ️" };
};

function WeatherAlerts({ alerts }) {
    if (!alerts || alerts.length === 0) {
        return (
             <div className="mt-4 bg-green-800/30 p-3 rounded-lg text-center">
                <p className="text-green-300 font-semibold">✅ No extreme weather alerts for the next 7 days.</p>
            </div>
        );
    }
    return (
        <div className="mt-4 space-y-2">
            <h4 className="text-base font-bold text-gray-300 text-center uppercase tracking-wider">Upcoming Weather Alerts</h4>
            {alerts.map((alert, index) => {
                const { color, icon } = getAlertStyle(alert);
                return (
                    <div key={index} className={`p-3 rounded-lg border ${color} flex items-center gap-3`}>
                        <span className="text-xl">{icon}</span>
                        <p className="font-semibold">{alert}</p>
                    </div>
                );
            })}
        </div>
    );
}

// --- Sub-component for Pest Diagnosis ---
function PestDiagnosis({ diseaseRisks, cropType }) {
    if (!diseaseRisks || Object.keys(diseaseRisks).length === 0) {
        return null;
    }

    let topThreat = { name: "None", risk: 0 };
    for (const [disease, risk] of Object.entries(diseaseRisks)) {
        if (risk > topThreat.risk) {
            topThreat = { name: disease, risk: risk };
        }
    }

    if (topThreat.risk < 0.2) {
        return (
            <div className="mt-4 bg-green-800/30 p-3 rounded-lg text-center">
                <p className="text-green-300 font-semibold">✅ No significant disease risk today.</p>
            </div>
        );
    }

    const riskColor = topThreat.risk > 0.6 ? 'text-red-400' : 'text-yellow-400';
    const solution = getSolutionForDisease(cropType, topThreat.name);

    return (
        <div className="mt-4 p-4 rounded-lg bg-gray-800/50 border border-gray-700">
            <h4 className="text-base font-bold text-gray-300 text-center uppercase tracking-wider">AI Pest & Disease Diagnosis</h4>
            <div className="text-center mt-2">
                <p className="text-gray-400">Highest Threat Today:</p>
                <p className={`text-2xl font-bold ${riskColor}`}>{topThreat.name}</p>
                <p className={`text-xl font-semibold ${riskColor}`}>Risk Level: {(topThreat.risk * 100).toFixed(0)}%</p>
            </div>
            
            {solution && (
                <div className="mt-3 bg-blue-900/30 p-3 rounded">
                    <p className="text-sm font-bold text-blue-300 uppercase">Recommended Solution:</p>
                    <p className="text-blue-200 mt-1">{solution}</p>
                </div>
            )}
        </div>
    );
}

// --- Main DailyPlan Component ---
function DailyPlan({ dailyLog, currentDay, startDate, cropType }) {
    if (!dailyLog || dailyLog.length === 0) return null;
    const logEntry = dailyLog[currentDay - 1];
    if (!logEntry) return null;

    const currentDate = new Date(startDate);
    currentDate.setDate(currentDate.getDate() + currentDay - 1);

    return (
        <div className="bg-gray-900/50 p-4 rounded-lg shadow-lg border border-gray-700">
            <h3 className="text-2xl font-semibold mb-4 text-center text-gray-300">
                Plan for Day {logEntry.day} <span className="text-lg text-gray-400">({currentDate.toLocaleDateString()})</span>
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div className="bg-gray-800 p-3 rounded">
                    <p className="text-sm text-gray-400">Soil Moisture</p>
                    <p className="text-2xl font-bold text-blue-400">{(logEntry.soil_moisture * 100).toFixed(0)}%</p>
                </div>
                <div className="bg-gray-800 p-3 rounded">
                    <p className="text-sm text-gray-400">Soil Nitrogen</p>
                    <p className="text-2xl font-bold text-amber-400">{(logEntry.soil_nitrogen * 100).toFixed(0)}%</p>
                </div>
                <div className="bg-gray-800 p-3 rounded">
                    <p className="text-sm text-gray-400">Crop Health</p>
                    <p className="text-2xl font-bold text-green-400">{logEntry.crop_health.toFixed(0)}%</p>
                </div>
                <div className="bg-gray-800 p-3 rounded">
                    <p className="text-sm text-gray-400">Highest Disease Risk</p>
                    <p className="text-2xl font-bold text-red-500">
                      {(Math.max(0, ...Object.values(logEntry.disease_risks || {})) * 100).toFixed(0)}%
                    </p>
                </div>
            </div>
            
            <WeatherAlerts alerts={logEntry.extreme_weather_alerts} />
            <PestDiagnosis diseaseRisks={logEntry.disease_risks} cropType={cropType} />

            <div className="mt-6 bg-green-800/30 p-4 rounded-lg text-center">
                <h4 className="text-lg font-bold text-green-300 uppercase">AI Recommendations for Today</h4>
                <div className="flex flex-col md:flex-row justify-around mt-2 text-lg">
                    <p>Irrigation: <span className="font-bold text-xl">{logEntry.irrigation_mm} mm</span></p>
                    <p>Fertilizer: <span className="font-bold text-xl">{logEntry.fertilizer_kg_per_ha} kg/ha</span></p>
                    <p>Pesticide: <span className="font-bold text-xl">{logEntry.pesticide_applied ? "Apply Today" : "Not Needed"}</span></p>
                </div>
            </div>
        </div>
    );
}

export default DailyPlan;