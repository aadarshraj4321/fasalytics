// frontend/src/components/SummaryMetrics.jsx

import React from 'react';

function SummaryMetrics({ summary }) {
  if (!summary) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 text-center mb-8">
      <div className="bg-gray-700/50 p-4 rounded-lg shadow-lg">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Final Yield</h3>
        <p className="text-3xl font-bold text-green-400 mt-2">
          {summary.final_yield_kg_per_ha.toFixed(0)} 
          <span className="text-xl text-gray-300 ml-1">kg/ha</span>
        </p>
      </div>
      <div className="bg-gray-700/50 p-4 rounded-lg shadow-lg">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Total Irrigation</h3>
        <p className="text-3xl font-bold text-blue-400 mt-2">
          {summary.total_irrigation_applied_mm.toFixed(0)} 
          <span className="text-xl text-gray-300 ml-1">mm</span>
        </p>
      </div>
      <div className="bg-gray-700/50 p-4 rounded-lg shadow-lg">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Total Fertilizer</h3>
        <p className="text-3xl font-bold text-amber-400 mt-2">
          {summary.total_fertilizer_applied_kg_per_ha.toFixed(0)} 
          <span className="text-xl text-gray-300 ml-1">kg/ha</span>
        </p>
      </div>
      <div className="bg-gray-700/50 p-4 rounded-lg shadow-lg">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Pesticide Apps</h3>
        <p className="text-3xl font-bold text-purple-400 mt-2">
          {summary.total_pesticide_applications}
          <span className="text-xl text-gray-300 ml-1"> times</span>
        </p>
      </div>
      <div className="bg-gray-700/50 p-4 rounded-lg shadow-lg">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Final Profit</h3>
        <p className={`text-3xl font-bold mt-2 ${summary.final_profit >= 0 ? 'text-green-500' : 'text-red-500'}`}>
          {summary.final_profit.toFixed(0)} 
          <span className="text-xl text-gray-300 ml-1">units</span>
        </p>
      </div>
      <div className="bg-gray-700/50 p-4 rounded-lg shadow-lg">
        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Avg. Rust Risk</h3>
        <p className="text-3xl font-bold text-red-500 mt-2">
          {(summary.avg_rust_risk * 100).toFixed(1)}
          <span className="text-xl text-gray-300 ml-1">%</span>
        </p>
      </div>
    </div>
  );
}

export default SummaryMetrics;