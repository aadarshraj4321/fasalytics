// frontend/src/components/PlotlyChart.jsx

import React from 'react';
import Plot from 'react-plotly.js';

// The chart creation logic is now inside this component.
const createChartFigure = (dailyLog) => {
    const days = dailyLog.map(log => log.day);
    const soilMoisture = dailyLog.map(log => log.soil_moisture);
    const soilNitrogen = dailyLog.map(log => log.soil_nitrogen);
    const rustRisk = dailyLog.map(log => log.rust_risk);
    const cropYield = dailyLog.map(log => log.yield_kg_per_ha);
    const irrigation = dailyLog.map(log => log.irrigation_mm);
    const fertilizer = dailyLog.map(log => log.fertilizer_kg_per_ha);
    const pesticide = dailyLog.map(log => log.pesticide_applied);

    const plotData = [
      { x: days, y: soilMoisture, type: 'scatter', mode: 'lines', name: 'Soil Moisture', yaxis: 'y1', line: { color: '#3b82f6' } },
      { x: days, y: soilNitrogen, type: 'scatter', mode: 'lines', name: 'Soil Nitrogen', yaxis: 'y1', line: { color: '#ca8a04' } },
      { x: days, y: rustRisk, type: 'scatter', mode: 'lines', name: 'Rust Risk', yaxis: 'y1', line: { color: '#ef4444', dash: 'dash' } },
      { x: days, y: cropYield, type: 'scatter', mode: 'lines', name: 'Yield (kg/ha)', yaxis: 'y2', line: { color: '#22c55e' } },
      { x: days, y: irrigation, type: 'bar', name: 'Irrigation', yaxis: 'y3', marker: { color: '#60a5fa', opacity: 0.7 } },
      { x: days, y: fertilizer, type: 'bar', name: 'Fertilizer', yaxis: 'y3', marker: { color: '#f59e0b', opacity: 0.7 } },
      { x: days, y: pesticide, type: 'bar', name: 'Pesticide', yaxis: 'y3', marker: { color: '#8b5cf6', opacity: 0.8 } }
    ];
    const plotLayout = {
      title: 'Full Season Analysis', autosize: true, height: 600,
      plot_bgcolor: '#1f2d37', paper_bgcolor: 'rgba(0,0,0,0)',
      font: { color: '#e5e7eb' },
      legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
      yaxis: { title: 'Soil Level / Risk', domain: [0, 1], titlefont: { color: '#9ca3af' }, side: 'left' },
      yaxis2: { title: 'Yield (kg/ha)', domain: [0, 1], titlefont: { color: '#22c55e' }, tickfont: { color: '#22c55e' }, overlaying: 'y', side: 'right' },
      yaxis3: { title: 'Applications', showgrid: false, overlaying: 'y', side: 'right', position: 1.0, showticklabels: false},
      xaxis: { title: 'Simulation Day' },
      barmode: 'stack'
    };
    return { data: plotData, layout: plotLayout };
};

function PlotlyChart({ dailyLog }) {
    if (!dailyLog) return null;

    const figure = createChartFigure(dailyLog);

    return (
        <div className="mt-8">
            <Plot
                data={figure.data}
                layout={figure.layout}
                useResizeHandler={true}
                style={{ width: '100%', height: '100%' }}
                config={{ responsive: true }}
            />
        </div>
    );
}

export default PlotlyChart;