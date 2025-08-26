import React, { useState, useEffect } from 'react';

const ControlPanel = ({ onRunSimulation, loading, locations }) => {
    const cropDefaults = { "Wheat": 90, "Rice": 110, "Sugarcane": 300 };
    const [locationName, setLocationName] = useState("Aurangabad, Bihar");
    const [cropType, setCropType] = useState('Rice');
    const [soilType, setSoilType] = useState('Alluvial');
    const [simulationDays, setSimulationDays] = useState(cropDefaults[cropType]);

    useEffect(() => {
        setSimulationDays(cropDefaults[cropType] || 90);
    }, [cropType]);

    const handleRunClick = () => {
        const payload = {
            crop_type: cropType,
            soil_type: soilType,
            simulation_days: simulationDays,
            latitude: locations[locationName].lat,
            longitude: locations[locationName].lon,
        };
        onRunSimulation(payload);
    };

    const cropIcons = {
        'Rice': '',
        'Wheat': '', 
        'Sugarcane': ''
    };

    const soilIcons = {
        'Alluvial': '🟤',
        'Black': '⚫',
        'Red': '🔴'
    };

    return (
        <div className="relative bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm p-8 rounded-2xl shadow-2xl border border-gray-700/50">
            {/* Decorative elements */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-400 via-emerald-400 to-teal-400 rounded-t-2xl"></div>
            <div className="absolute -top-1 -left-1 w-3 h-3 bg-green-400 rounded-full blur-sm animate-pulse"></div>
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full blur-sm animate-pulse"></div>
            
            <div className="text-center mb-8">
                <h3 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-emerald-300 bg-clip-text text-transparent mb-2">
                    Simulation Control
                </h3>
                <p className="text-gray-400 text-sm">Configure your digital farm parameters</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Location */}
                <div className="space-y-3">
                    <label className="flex items-center space-x-2 text-sm font-medium text-gray-300">
                        <span>Location</span>
                    </label>
                    <div className="relative">
                        <select 
                            value={locationName} 
                            onChange={(e) => setLocationName(e.target.value)}
                            className="w-full bg-gray-700/50 backdrop-blur-sm border border-gray-600/50 text-white rounded-xl p-3 focus:ring-2 focus:ring-green-400/50 focus:border-green-400 transition-all duration-300 appearance-none cursor-pointer hover:bg-gray-700/70"
                        >
                            {Object.keys(locations).map(loc => 
                                <option key={loc} value={loc}>{loc}</option>
                            )}
                        </select>
                        <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
                            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                        </div>
                    </div>
                </div>

                {/* Crop Type */}
                <div className="space-y-3">
                    <label className="flex items-center space-x-2 text-sm font-medium text-gray-300">
                        <span>Crop Type</span>
                    </label>
                    <div className="relative">
                        <select 
                            value={cropType} 
                            onChange={(e) => setCropType(e.target.value)}
                            className="w-full bg-gray-700/50 backdrop-blur-sm border border-gray-600/50 text-white rounded-xl p-3 focus:ring-2 focus:ring-green-400/50 focus:border-green-400 transition-all duration-300 appearance-none cursor-pointer hover:bg-gray-700/70"
                        >
                            {Object.keys(cropDefaults).map(crop => 
                                <option key={crop} value={crop}>
                                    {cropIcons[crop]} {crop}
                                </option>
                            )}
                        </select>
                        <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
                            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                        </div>
                    </div>
                </div>

                {/* Soil Type */}
                <div className="space-y-3">
                    <label className="flex items-center space-x-2 text-sm font-medium text-gray-300">
                        <span>Soil Type</span>
                    </label>
                    <div className="relative">
                        <select 
                            value={soilType} 
                            onChange={(e) => setSoilType(e.target.value)}
                            className="w-full bg-gray-700/50 backdrop-blur-sm border border-gray-600/50 text-white rounded-xl p-3 focus:ring-2 focus:ring-green-400/50 focus:border-green-400 transition-all duration-300 appearance-none cursor-pointer hover:bg-gray-700/70"
                        >
                            {Object.keys(soilIcons).map(soil => 
                                <option key={soil} value={soil}>
                                    {soilIcons[soil]} {soil}
                                </option>
                            )}
                        </select>
                        <div className="absolute right-3 top-1/2 transform -translate-y-1/2 pointer-events-none">
                            <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                        </div>
                    </div>
                </div>

                {/* Simulation Days */}
                <div className="space-y-3">
                    <label className="flex items-center justify-between text-sm font-medium text-gray-300">
                        <div className="flex items-center space-x-2">
                            <span>Simulation Period</span>
                        </div>
                        <span className="px-3 py-1 bg-green-400/20 text-green-400 rounded-full text-xs font-bold">
                            {simulationDays} days
                        </span>
                    </label>
                    <div className="relative">
                        <input 
                            type="range" 
                            min="30" 
                            max="365" 
                            value={simulationDays}
                            onChange={(e) => setSimulationDays(Number(e.target.value))}
                            className="w-full h-3 bg-gray-700/50 rounded-full appearance-none cursor-pointer slider-thumb"
                            style={{
                                background: `linear-gradient(to right, #10b981 0%, #10b981 ${((simulationDays - 30) / (365 - 30)) * 100}%, #374151 ${((simulationDays - 30) / (365 - 30)) * 100}%, #374151 100%)`
                            }}
                        />
                        <div className="flex justify-between text-xs text-gray-500 mt-1">
                            <span>30 days</span>
                            <span>365 days</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Run Button */}
            <div className="mt-10 text-center">
                <button 
                    onClick={handleRunClick} 
                    disabled={loading}
                    className="relative px-10 py-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold text-lg rounded-2xl shadow-xl hover:from-green-600 hover:to-emerald-700 focus:outline-none focus:ring-4 focus:ring-green-400/50 transform hover:scale-105 transition-all duration-300 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed disabled:scale-100 group overflow-hidden"
                >
                    {/* Button glow effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-green-400/20 to-emerald-400/20 blur-xl group-hover:blur-2xl transition-all duration-300"></div>
                    
                    <div className="relative flex items-center justify-center space-x-3">
                        {loading ? (
                            <>
                                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <span>Simulating Farm...</span>
                            </>
                        ) : (
                            <>
                               
                                <span>Generate Farming Plan</span>
                            </>
                        )}
                    </div>
                </button>
            </div>

            <style jsx>{`
                .slider-thumb::-webkit-slider-thumb {
                    appearance: none;
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    background: linear-gradient(45deg, #10b981, #34d399);
                    cursor: pointer;
                    border: 2px solid white;
                    box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
                }
                .slider-thumb::-moz-range-thumb {
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    background: linear-gradient(45deg, #10b981, #34d399);
                    cursor: pointer;
                    border: 2px solid white;
                    box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
                }
            `}</style>
        </div>
    );
};



export default ControlPanel;