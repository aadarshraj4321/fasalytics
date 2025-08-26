// frontend/src/utils/chartUtils.js

// This helper function creates the data and layout for the main Plotly chart.
export const createChartFigure = (dailyLog) => {
    // Return empty figure if there is no data to prevent errors.
    if (!dailyLog || dailyLog.length === 0) {
        return { data: [], layout: {} };
    }
    
    const days = dailyLog.map(log => log.day);
    const plotData = [];

    // --- Basic Traces (Lines) ---
    plotData.push({ x: days, y: dailyLog.map(l => l.soil_moisture), name: 'Soil Moisture', type: 'scatter', mode: 'lines', yaxis: 'y1', line: { color: '#3b82f6' } });
    plotData.push({ x: days, y: dailyLog.map(l => l.soil_nitrogen), name: 'Soil Nitrogen', type: 'scatter', mode: 'lines', yaxis: 'y1', line: { color: '#ca8a04' } });
    plotData.push({ x: days, y: dailyLog.map(l => l.yield_kg_per_ha), name: 'Yield (kg/ha)', type: 'scatter', mode: 'lines', yaxis: 'y2', line: { color: '#22c55e' } });
    
    // --- Application Traces (Bars) ---
    plotData.push({ x: days, y: dailyLog.map(l => l.irrigation_mm), name: 'Irrigation', type: 'bar', yaxis: 'y3', marker: { color: '#60a5fa', opacity: 0.7 } });
    plotData.push({ x: days, y: dailyLog.map(l => l.fertilizer_kg_per_ha), name: 'Fertilizer', type: 'bar', yaxis: 'y3', marker: { color: '#f59e0b', opacity: 0.7 } });
    plotData.push({ x: days, y: dailyLog.map(l => l.pesticide_applied), name: 'Pesticide', type: 'bar', yaxis: 'y3', marker: { color: '#8b5cf6', opacity: 0.8 } });

    // --- Dynamic Disease Risk Traces (Lines) ---
    // This code finds all unique disease names from the log and creates a line for each.
    const diseaseNames = dailyLog.length > 0 ? Object.keys(dailyLog[0].disease_risks || {}) : [];
    const diseaseColors = ['#ef4444', '#f97316', '#eab308']; // Red, Orange, Yellow for different risks

    diseaseNames.forEach((diseaseName, index) => {
        plotData.push({
            x: days,
            y: dailyLog.map(log => log.disease_risks[diseaseName] || 0),
            name: `${diseaseName} Risk`,
            type: 'scatter',
            mode: 'lines',
            yaxis: 'y1', // Shares the same axis as moisture/nitrogen
            line: { color: diseaseColors[index % diseaseColors.length], dash: 'dash' }
        });
    });
    
    // --- Chart Layout ---
    const plotLayout = {
      title: 'Full Season Analysis', 
      autosize: true, 
      height: 600,
      plot_bgcolor: '#1f2d37', 
      paper_bgcolor: 'rgba(0,0,0,0)',
      font: { color: '#e5e7eb' },
      legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1 },
      yaxis: { title: 'Soil Level / Risk (Normalized)', domain: [0, 1], titlefont: { color: '#9ca3af' }, side: 'left', gridcolor: '#374151' },
      yaxis2: { title: 'Yield (kg/ha)', domain: [0, 1], titlefont: { color: '#22c55e' }, tickfont: { color: '#22c55e' }, overlaying: 'y', side: 'right' },
      yaxis3: { title: 'Applications', showgrid: false, overlaying: 'y', side: 'right', position: 1.0, showticklabels: false},
      xaxis: { title: 'Simulation Day', gridcolor: '#374151' },
      barmode: 'stack'
    };
    
    return { data: plotData, layout: plotLayout };
};