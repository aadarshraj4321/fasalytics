import React from 'react';

function ResultsSummary({ simulationData }) {
    if (!simulationData || !simulationData.results_summary) {
        return null;
    }

    const { results_summary, daily_log } = simulationData;

    // Calculate the average of the highest risk for each day
    const avgHighestRisk = daily_log.reduce((acc, log) => {
        const highestRisk = log.disease_risks ? Math.max(0, ...Object.values(log.disease_risks)) : 0;
        return acc + highestRisk;
    }, 0) / daily_log.length;

    const metrics = [
        {
            title: 'Final Yield',
            value: results_summary.final_yield_kg_per_ha.toFixed(0),
            unit: 'kg/ha',
            color: 'text-green-400',
            bgColor: 'from-green-400/10 to-green-600/10',
            borderColor: 'border-green-400/20',
            icon: '🌾'
        },
        {
            title: 'Total Irrigation',
            value: results_summary.total_irrigation_applied_mm.toFixed(0),
            unit: 'mm',
            color: 'text-blue-400',
            bgColor: 'from-blue-400/10 to-blue-600/10',
            borderColor: 'border-blue-400/20',
            icon: '💧'
        },
        {
            title: 'Total Fertilizer',
            value: results_summary.total_fertilizer_applied_kg_per_ha.toFixed(0),
            unit: 'kg/ha',
            color: 'text-amber-400',
            bgColor: 'from-amber-400/10 to-amber-600/10',
            borderColor: 'border-amber-400/20',
            icon: '🧪'
        },
        {
            title: 'Pesticide Apps',
            value: results_summary.total_pesticide_applications,
            unit: 'times',
            color: 'text-purple-400',
            bgColor: 'from-purple-400/10 to-purple-600/10',
            borderColor: 'border-purple-400/20',
            icon: '🛡️'
        },
        {
            title: 'Final Profit',
            value: results_summary.final_profit.toFixed(0),
            unit: 'units',
            color: results_summary.final_profit >= 0 ? 'text-emerald-400' : 'text-red-400',
            bgColor: results_summary.final_profit >= 0 ? 'from-emerald-400/10 to-emerald-600/10' : 'from-red-400/10 to-red-600/10',
            borderColor: results_summary.final_profit >= 0 ? 'border-emerald-400/20' : 'border-red-400/20',
            icon: results_summary.final_profit >= 0 ? '💰' : '📉'
        },
        {
            title: 'Avg Disease Risk',
            value: (avgHighestRisk * 100).toFixed(1),
            unit: '%',
            color: 'text-red-400',
            bgColor: 'from-red-400/10 to-red-600/10',
            borderColor: 'border-red-400/20',
            icon: '🦠'
        },
        {
            title: 'Heat Wave Days',
            value: results_summary.heat_wave_alert_days,
            unit: 'days',
            color: 'text-orange-400',
            bgColor: 'from-orange-400/10 to-orange-600/10',
            borderColor: 'border-orange-400/20',
            icon: '🌡️'
        },
        {
            title: 'Heavy Rain Days',
            value: results_summary.heavy_rain_alert_days,
            unit: 'days',
            color: 'text-cyan-400',
            bgColor: 'from-cyan-400/10 to-cyan-600/10',
            borderColor: 'border-cyan-400/20',
            icon: '🌧️'
        }
    ];

    return (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
            {metrics.map((metric, index) => (
                <div 
                    key={index}
                    className={`relative bg-gradient-to-br ${metric.bgColor} backdrop-blur-sm rounded-2xl p-6 border ${metric.borderColor} group hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl`}
                >
                    {/* Glow effect */}
                    <div className={`absolute inset-0 bg-gradient-to-br ${metric.bgColor} rounded-2xl blur-xl opacity-0 group-hover:opacity-50 transition-opacity duration-300`}></div>
                    
                    <div className="relative text-center space-y-3">
                        <div className="text-2xl">{metric.icon}</div>
                        <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider leading-tight">
                            {metric.title}
                        </h3>
                        <div className={`${metric.color} space-y-1`}>
                            <p className="text-2xl md:text-3xl font-bold leading-none">
                                {metric.value}
                            </p>
                            <p className="text-sm text-gray-300 font-medium">
                                {metric.unit}
                            </p>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}


export default ResultsSummary;