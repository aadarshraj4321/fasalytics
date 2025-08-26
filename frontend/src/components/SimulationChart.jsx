import React from 'react';
import Plot from 'react-plotly.js';

function SimulationChart({ dailyLog }) {
    const days = dailyLog.map(log => log.day);
    const soilMoisture = dailyLog.map(log => log.soil_moisture);
    const cropYield = dailyLog.map(log => log.yield_kg_per_ha);
    const irrigation = dailyLog.map(log => log.irrigation_mm);
    const cropHealth = dailyLog.map(log => log.crop_health);

    const plotData = [
        {
            x: days,
            y: soilMoisture,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Soil Moisture',
            line: { color: '#3b82f6', width: 3 },
            marker: { size: 6, color: '#3b82f6' },
            hovertemplate: '<b>Soil Moisture</b><br>Day %{x}<br>%{y:.1f}%<extra></extra>'
        },
        {
            x: days,
            y: cropYield,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Yield (kg/ha)',
            line: { color: '#10b981', width: 3 },
            marker: { size: 6, color: '#10b981' },
            hovertemplate: '<b>Crop Yield</b><br>Day %{x}<br>%{y:.0f} kg/ha<extra></extra>'
        },
        {
            x: days,
            y: cropHealth,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Crop Health (%)',
            yaxis: 'y2',
            line: { color: '#f59e0b', width: 3, dash: 'dot' },
            marker: { size: 6, color: '#f59e0b' },
            hovertemplate: '<b>Crop Health</b><br>Day %{x}<br>%{y:.1f}%<extra></extra>'
        },
        {
            x: days,
            y: irrigation,
            type: 'bar',
            name: 'Irrigation (mm)',
            yaxis: 'y3',
            marker: { 
                color: '#06b6d4', 
                opacity: 0.7,
                line: { color: '#0891b2', width: 1 }
            },
            hovertemplate: '<b>Irrigation</b><br>Day %{x}<br>%{y} mm<extra></extra>'
        }
    ];

    const plotLayout = {
        title: {
            text: '📊 Farm Performance Analytics',
            font: { 
                color: '#10b981', 
                size: 24,
                family: 'Arial, sans-serif'
            },
            x: 0.5
        },
        autosize: true,
        height: 650,
        plot_bgcolor: '#1f2937',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { 
            color: '#e5e7eb', 
            family: 'Arial, sans-serif' 
        },
        legend: {
            orientation: 'h',
            yanchor: 'bottom',
            y: 1.02,
            xanchor: 'center',
            x: 0.5,
            bgcolor: 'rgba(55, 65, 81, 0.8)',
            bordercolor: '#374151',
            borderwidth: 1,
            font: { size: 12 }
        },
        yaxis: {
            title: {
                text: '💧 Moisture & 🌾 Yield',
                font: { color: '#9ca3af', size: 14 }
            },
            titlefont: { color: '#9ca3af' },
            tickfont: { color: '#d1d5db' },
            gridcolor: '#374151',
            zerolinecolor: '#4b5563'
        },
        yaxis2: {
            title: {
                text: '❤️ Health (%)',
                font: { color: '#f59e0b', size: 14 }
            },
            titlefont: { color: '#f59e0b' },
            tickfont: { color: '#f59e0b' },
            overlaying: 'y',
            side: 'right',
            showgrid: false
        },
        yaxis3: {
            title: {
                text: '🚿 Irrigation (mm)',
                font: { color: '#06b6d4', size: 14 }
            },
            titlefont: { color: '#06b6d4' },
            tickfont: { color: '#06b6d4' },
            overlaying: 'y',
            side: 'right',
            position: 0.95,
            showgrid: false,
            range: [0, Math.max(...irrigation) * 2.5]
        },
        xaxis: {
            title: {
                text: '📅 Simulation Day',
                font: { color: '#9ca3af', size: 14 }
            },
            titlefont: { color: '#9ca3af' },
            tickfont: { color: '#d1d5db' },
            gridcolor: '#374151',
            zerolinecolor: '#4b5563'
        },
        hovermode: 'x unified',
        margin: { t: 80, r: 80, b: 60, l: 60 }
    };

    return (
        <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 backdrop-blur-sm rounded-2xl p-8 border border-gray-700/50">
            <Plot
                data={plotData}
                layout={plotLayout}
                useResizeHandler={true}
                style={{ width: '100%', height: '100%' }}
                config={{ 
                    responsive: true,
                    displayModeBar: true,
                    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
                    displaylogo: false,
                    toImageButtonOptions: {
                        format: 'png',
                        filename: 'farm_analytics',
                        height: 650,
                        width: 1200,
                        scale: 2
                    }
                }}
            />
        </div>
    );
}


export default SimulationChart;