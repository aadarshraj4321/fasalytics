// import React from 'react';

// const FiveDayOutlook = ({ dailyLog, currentDay, startDate }) => {
//     if (!dailyLog || dailyLog.length === 0) return null;
//     const outlookLog = dailyLog.slice(currentDay, currentDay + 5);
//     if (outlookLog.length === 0) {
//         return (
//             <div className="text-center py-8">
//                 <div className="text-6xl mb-4">🏁</div>
//                 <p className="text-xl text-gray-400">End of simulation period</p>
//             </div>
//         );
//     }

//     const getRiskColor = (risk) => {
//         if (risk > 0.7) return 'text-red-400 bg-red-400/10 border-red-400/20';
//         if (risk > 0.4) return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20';
//         return 'text-green-400 bg-green-400/10 border-green-400/20';
//     };

//     const getRiskIcon = (risk) => {
//         if (risk > 0.7) return '🚨';
//         if (risk > 0.4) return '⚠️';
//         return '✅';
//     };

//     return (
//         <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 backdrop-blur-sm rounded-2xl p-8 border border-gray-700/50">
//             <div className="text-center mb-8">
//                 <h4 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent mb-2">
//                     5-Day Farm Outlook
//                 </h4>
//                 <p className="text-gray-400 text-sm">Upcoming actions and conditions</p>
//             </div>

//             <div className="overflow-hidden rounded-xl border border-gray-700/50">
//                 <div className="overflow-x-auto">
//                     <table className="w-full">
//                         <thead>
//                             <tr className="bg-gradient-to-r from-gray-700/50 to-gray-800/50">
//                                 <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">Day</th>
//                                 <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">Date</th>
//                                 <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">💧 Irrigation</th>
//                                 <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">🧪 Fertilizer</th>
//                                 <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">🦠 Pest Risk</th>
//                             </tr>
//                         </thead>
//                         <tbody className="divide-y divide-gray-700/50">
//                             {outlookLog.map((log, index) => {
//                                 const date = new Date(startDate);
//                                 date.setDate(date.getDate() + log.day - 1);
//                                 const riskLevel = log.rust_risk;
                                
//                                 return (
//                                     <tr 
//                                         key={log.day} 
//                                         className={`bg-gray-800/20 hover:bg-gray-700/30 transition-colors duration-200 ${index === 0 ? 'bg-gradient-to-r from-blue-500/10 to-transparent' : ''}`}
//                                     >
//                                         <td className="px-6 py-4">
//                                             <div className="flex items-center space-x-3">
//                                                 {index === 0 && <span className="text-blue-400">👉</span>}
//                                                 <span className={`font-bold ${index === 0 ? 'text-blue-400' : 'text-white'}`}>
//                                                     {log.day}
//                                                 </span>
//                                             </div>
//                                         </td>
//                                         <td className="px-6 py-4 text-gray-300 font-medium">
//                                             {date.toLocaleDateString('en-US', { 
//                                                 month: 'short', 
//                                                 day: 'numeric' 
//                                             })}
//                                         </td>
//                                         <td className="px-6 py-4">
//                                             <span className="px-3 py-1 bg-blue-400/10 text-blue-400 rounded-full text-sm font-semibold border border-blue-400/20">
//                                                 {log.irrigation_mm} mm
//                                             </span>
//                                         </td>
//                                         <td className="px-6 py-4">
//                                             <span className="px-3 py-1 bg-amber-400/10 text-amber-400 rounded-full text-sm font-semibold border border-amber-400/20">
//                                                 {log.fertilizer_kg_per_ha} kg/ha
//                                             </span>
//                                         </td>
//                                         <td className="px-6 py-4">
//                                             <div className="flex items-center space-x-2">
//                                                 <span className="text-lg">{getRiskIcon(riskLevel)}</span>
//                                                 <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${getRiskColor(riskLevel)}`}>
//                                                     {(riskLevel * 100).toFixed(0)}%
//                                                 </span>
//                                             </div>
//                                         </td>
//                                     </tr>
//                                 );
//                             })}
//                         </tbody>
//                     </table>
//                 </div>
//             </div>
//         </div>
//     );
// };



// export default FiveDayOutlook;
















import React, { useState } from 'react';

const CompleteSeasonOutlook = ({ dailyLog, currentDay, startDate, totalDays = 90 }) => {
    const [viewMode, setViewMode] = useState('remaining'); // 'remaining' or 'all'
    const [showCount, setShowCount] = useState(10); // For pagination
    
    if (!dailyLog || dailyLog.length === 0) return null;
    
    // Get the appropriate data based on view mode
    const getOutlookData = () => {
        if (viewMode === 'remaining') {
            return dailyLog.slice(currentDay); // All remaining days
        } else {
            return dailyLog; // All days from start
        }
    };
    
    const outlookLog = getOutlookData();
    const displayedLog = outlookLog.slice(0, showCount);
    
    if (outlookLog.length === 0) {
        return (
            <div className="text-center py-8">
                <div className="text-6xl mb-4">🏁</div>
                <p className="text-xl text-gray-400">End of simulation period</p>
            </div>
        );
    }

    const getRiskColor = (risk) => {
        if (risk > 0.7) return 'text-red-400 bg-red-400/10 border-red-400/20';
        if (risk > 0.4) return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20';
        return 'text-green-400 bg-green-400/10 border-green-400/20';
    };

    const getRiskIcon = (risk) => {
        if (risk > 0.7) return '🚨';
        if (risk > 0.4) return '⚠️';
        return '✅';
    };

    const getProgressPercentage = () => {
        return ((currentDay / totalDays) * 100).toFixed(1);
    };

    return (
        <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/40 backdrop-blur-sm rounded-2xl p-8 border border-gray-700/50">
            {/* Header with controls */}
            <div className="text-center mb-8">
                <h4 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent mb-2">
                    Complete Season Outlook
                </h4>
                <p className="text-gray-400 text-sm mb-4">
                    {viewMode === 'remaining' 
                        ? `${outlookLog.length} days remaining (${getProgressPercentage()}% complete)`
                        : `Full season: ${outlookLog.length} days total`
                    }
                </p>
                
                {/* View Mode Toggle */}
                <div className="flex justify-center space-x-4 mb-4">
                    <button
                        onClick={() => setViewMode('remaining')}
                        className={`px-4 py-2 rounded-lg transition-all duration-200 ${
                            viewMode === 'remaining'
                                ? 'bg-blue-500/20 text-blue-400 border border-blue-400/30'
                                : 'bg-gray-700/20 text-gray-400 hover:bg-gray-600/20'
                        }`}
                    >
                        📅 Remaining Days
                    </button>
                    <button
                        onClick={() => setViewMode('all')}
                        className={`px-4 py-2 rounded-lg transition-all duration-200 ${
                            viewMode === 'all'
                                ? 'bg-blue-500/20 text-blue-400 border border-blue-400/30'
                                : 'bg-gray-700/20 text-gray-400 hover:bg-gray-600/20'
                        }`}
                    >
                        📊 Full Season
                    </button>
                </div>

                {/* Show count selector */}
                <div className="flex justify-center items-center space-x-4">
                    <span className="text-gray-400 text-sm">Show:</span>
                    <select
                        value={showCount}
                        onChange={(e) => setShowCount(Number(e.target.value))}
                        className="bg-gray-700/50 text-gray-300 rounded-lg px-3 py-1 text-sm border border-gray-600/50"
                    >
                        <option value={10}>10 days</option>
                        <option value={20}>20 days</option>
                        <option value={30}>30 days</option>
                        <option value={50}>50 days</option>
                        <option value={outlookLog.length}>All ({outlookLog.length})</option>
                    </select>
                </div>
            </div>

            {/* Progress bar for season completion */}
            <div className="mb-6">
                <div className="flex justify-between text-sm text-gray-400 mb-2">
                    <span>Season Progress</span>
                    <span>{getProgressPercentage()}% Complete</span>
                </div>
                <div className="w-full bg-gray-700/50 rounded-full h-2">
                    <div 
                        className="bg-gradient-to-r from-green-400 to-blue-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${getProgressPercentage()}%` }}
                    ></div>
                </div>
            </div>

            {/* Data Table */}
            <div className="overflow-hidden rounded-xl border border-gray-700/50">
                <div className="overflow-x-auto max-h-96 overflow-y-auto">
                    <table className="w-full">
                        <thead className="sticky top-0 z-10">
                            <tr className="bg-gradient-to-r from-gray-700/80 to-gray-800/80 backdrop-blur-sm">
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">Day</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">💧 Irrigation</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">🧪 Fertilizer</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">🦠 Pest Risk</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-gray-300 uppercase tracking-wider">🌡️ Weather</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-700/50">
                            {displayedLog.map((log, index) => {
                                const date = new Date(startDate);
                                date.setDate(date.getDate() + log.day - 1);
                                const riskLevel = log.rust_risk || 0;
                                const isCurrentDay = log.day === currentDay;
                                const isPastDay = log.day < currentDay;
                                
                                return (
                                    <tr 
                                        key={log.day} 
                                        className={`transition-colors duration-200 ${
                                            isCurrentDay 
                                                ? 'bg-gradient-to-r from-blue-500/20 to-transparent border-l-4 border-blue-400' 
                                                : isPastDay
                                                ? 'bg-gray-800/10 opacity-60'
                                                : 'bg-gray-800/20 hover:bg-gray-700/30'
                                        }`}
                                    >
                                        <td className="px-6 py-4">
                                            <div className="flex items-center space-x-3">
                                                {isCurrentDay && <span className="text-blue-400 animate-pulse">👉</span>}
                                                <span className={`font-bold ${
                                                    isCurrentDay ? 'text-blue-400' : 
                                                    isPastDay ? 'text-gray-500' : 'text-white'
                                                }`}>
                                                    {log.day}
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`font-medium ${
                                                isPastDay ? 'text-gray-500' : 'text-gray-300'
                                            }`}>
                                                {date.toLocaleDateString('en-US', { 
                                                    month: 'short', 
                                                    day: 'numeric' 
                                                })}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                                                isCurrentDay 
                                                    ? 'bg-blue-400/20 text-blue-400 border border-blue-400/30' 
                                                    : isPastDay
                                                    ? 'bg-gray-600/20 text-gray-500 border border-gray-600/30'
                                                    : 'bg-green-400/20 text-green-400 border border-green-400/30'
                                            }`}>
                                                {isCurrentDay ? 'Current' : isPastDay ? 'Complete' : 'Upcoming'}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${
                                                isPastDay 
                                                    ? 'bg-gray-600/10 text-gray-500 border-gray-600/20'
                                                    : 'bg-blue-400/10 text-blue-400 border-blue-400/20'
                                            }`}>
                                                {log.irrigation_mm || 0} mm
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${
                                                isPastDay 
                                                    ? 'bg-gray-600/10 text-gray-500 border-gray-600/20'
                                                    : 'bg-amber-400/10 text-amber-400 border-amber-400/20'
                                            }`}>
                                                {log.fertilizer_kg_per_ha || 0} kg/ha
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center space-x-2">
                                                <span className="text-lg">{getRiskIcon(riskLevel)}</span>
                                                <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${
                                                    isPastDay 
                                                        ? 'bg-gray-600/10 text-gray-500 border-gray-600/20'
                                                        : getRiskColor(riskLevel)
                                                }`}>
                                                    {(riskLevel * 100).toFixed(0)}%
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center space-x-2 text-sm">
                                                <span>🌡️ {log.temperature || '--'}°C</span>
                                                <span>🌧️ {log.rainfall || 0}mm</span>
                                            </div>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Show more button if there are more days */}
            {showCount < outlookLog.length && (
                <div className="text-center mt-4">
                    <button
                        onClick={() => setShowCount(outlookLog.length)}
                        className="px-6 py-2 bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-blue-400 rounded-lg hover:from-blue-500/30 hover:to-cyan-500/30 transition-all duration-200 border border-blue-400/30"
                    >
                        Show All {outlookLog.length} Days
                    </button>
                </div>
            )}

            {/* Summary Stats */}
            <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gray-700/30 rounded-lg p-3 text-center">
                    <div className="text-blue-400 text-lg font-bold">
                        {displayedLog.reduce((sum, log) => sum + (log.irrigation_mm || 0), 0)}mm
                    </div>
                    <div className="text-gray-400 text-xs">Total Irrigation</div>
                </div>
                <div className="bg-gray-700/30 rounded-lg p-3 text-center">
                    <div className="text-amber-400 text-lg font-bold">
                        {displayedLog.reduce((sum, log) => sum + (log.fertilizer_kg_per_ha || 0), 0)}kg
                    </div>
                    <div className="text-gray-400 text-xs">Total Fertilizer</div>
                </div>
                <div className="bg-gray-700/30 rounded-lg p-3 text-center">
                    <div className="text-red-400 text-lg font-bold">
                        {displayedLog.filter(log => (log.rust_risk || 0) > 0.5).length}
                    </div>
                    <div className="text-gray-400 text-xs">High Risk Days</div>
                </div>
                <div className="bg-gray-700/30 rounded-lg p-3 text-center">
                    <div className="text-green-400 text-lg font-bold">
                        {displayedLog.length}
                    </div>
                    <div className="text-gray-400 text-xs">Days Shown</div>
                </div>
            </div>
        </div>
    );
};

export default CompleteSeasonOutlook;