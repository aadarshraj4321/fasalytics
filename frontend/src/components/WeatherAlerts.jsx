// frontend/src/components/WeatherAlerts.jsx

import React from 'react';

// A helper function to determine the color and icon for each alert
const getAlertStyle = (alertText) => {
    if (alertText.includes("HEAT WAVE")) return { color: "bg-red-500/20 text-red-300 border-red-500", icon: "🔥" };
    if (alertText.includes("HEAVY RAIN")) return { color: "bg-blue-500/20 text-blue-300 border-blue-500", icon: "💧" };
    if (alertText.includes("COLD WAVE")) return { color: "bg-sky-500/20 text-sky-300 border-sky-500", icon: "❄️" };
    if (alertText.includes("DROUGHT")) return { color: "bg-yellow-500/20 text-yellow-300 border-yellow-500", icon: "☀️" };
    return { color: "bg-gray-700 text-gray-300 border-gray-600", icon: "ℹ️" };
};

function WeatherAlerts({ alerts }) {
    // If there are no alerts for the day, don't render anything
    if (!alerts || alerts.length === 0) {
        return (
             <div className="mt-4 bg-green-800/30 p-3 rounded-lg text-center">
                <p className="text-green-300 font-semibold">No extreme weather alerts for the next 7 days.</p>
            </div>
        );
    }

    return (
        <div className="mt-4 space-y-2">
            <h4 className="text-lg font-bold text-gray-300 text-center">Upcoming Weather Alerts</h4>
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

export default WeatherAlerts;