// // frontend/src/App.jsx

// import React, { useState, useEffect, useRef } from 'react';
// import axios from 'axios';
// // We don't need Plot here anymore, as it should be in its own component.
// // To keep things clean, we will assume you have a PlotlyChart component.
// // If not, you can keep the Plot import here.
// // import Plot from 'react-plotly.js'; 

// // Components
// import ControlPanel from './components/ControlPanel';
// import DailyPlan from './components/DailyPlan';
// import FiveDayOutlook from './components/FiveDayOutlook';
// // --- CHANGE HERE: Replace AnimationViewer with ThreeDeeViewer ---
// // import AnimationViewer from './components/AnimationViewer'; 
// import ThreeDeeViewer from './components/ThreeDeeViewer';
// import ResultsSummary from './components/ResultsSummary';
// import PlotlyChart from './components/PlotlyChart'; // Assuming you have this

// // Utils
// import { createChartFigure } from './utils/chartUtils';
// import { locations } from './utils/locations';


// function App() {
//   const [simulationData, setSimulationData] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [loadingMessage, setLoadingMessage] = useState('');
//   const [error, setError] = useState('');
//   const [chartFigure, setChartFigure] = useState({ data: [], layout: {} });
//   const [currentDay, setCurrentDay] = useState(1);
//   const [planStartDate, setPlanStartDate] = useState(new Date());
//   const pollingIntervalRef = useRef(null);

//   const checkStatus = (simId) => {
//     if (pollingIntervalRef.current) clearInterval(pollingIntervalRef.current);
//     pollingIntervalRef.current = setInterval(async () => {
//       try {
//         const response = await axios.get(`http://127.0.0.1:8000/simulate/status/${simId}`);
//         const status = response.data.status;
//         setLoadingMessage(`Status: ${status}`);
//         if (status === "complete") {
//           clearInterval(pollingIntervalRef.current);
//           setLoadingMessage("Fetching final results...");
//           const resultsResponse = await axios.get(`http://127.0.0.1:8000/simulate/results/${simId}`);
//           const data = resultsResponse.data;
//           setSimulationData(data);
//           if (data && data.daily_log) {
//             setChartFigure(createChartFigure(data.daily_log));
//             setCurrentDay(1);
//           }
//           setLoading(false);
//         } else if (status.startsWith("error")) {
//           clearInterval(pollingIntervalRef.current);
//           setError(`Simulation failed: ${status}`);
//           setLoading(false);
//         }
//       } catch (err) {
//         clearInterval(pollingIntervalRef.current);
//         setError("Failed to poll for simulation status. Check backend connection.");
//         setLoading(false);
//       }
//     }, 3000);
//   };

//   const handleRunSimulation = async (payload) => {
//     setLoading(true);
//     setLoadingMessage("Sending simulation request...");
//     setError('');
//     setSimulationData(null);
//     setChartFigure({ data: [], layout: {} });
//     setPlanStartDate(new Date());
//     try {
//       const response = await axios.post("http://127.0.0.1:8000/simulate/start", payload);
//       const simId = response.data.simulation_id;
//       setLoadingMessage("Simulation is running in the background...");
//       checkStatus(simId);
//     } catch (err) {
//       setError("Failed to start the simulation. Is the backend server running?");
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     return () => { if (pollingIntervalRef.current) clearInterval(pollingIntervalRef.current); };
//   }, []);

//   return (
//     <div className="min-h-screen bg-gray-900 text-white font-sans flex flex-col">
//       <header className="bg-gray-800 p-6 shadow-lg text-center border-b-4 border-green-500">
//         <h1 className="text-4xl md:text-5xl font-bold text-green-400 tracking-wider">
//           AI-Powered Digital Twin Farm
//         </h1>
//         <p className="text-lg text-gray-300 mt-2">
//           Your Personal AI Farming Assistant
//         </p>
//       </header>

//       <main className="p-4 md:p-8 flex-grow">
//         <div className="max-w-4xl mx-auto mb-8">
//             <ControlPanel 
//               onRunSimulation={handleRunSimulation} 
//               loading={loading} 
//               locations={locations}
//             />
//             {loading && <p className="text-center text-yellow-400 mt-4 text-lg animate-pulse">{loadingMessage}</p>}
//         </div>

//         {error && <p className="text-red-400 bg-red-900/50 p-4 rounded-lg text-center text-xl">{error}</p>}
        
//         {simulationData && (
//           <div className="max-w-7xl mx-auto space-y-12">
//             <div>
//               <DailyPlan 
//                   dailyLog={simulationData.daily_log} 
//                   currentDay={currentDay}
//                   startDate={planStartDate}
//               />
//               <FiveDayOutlook 
//                   dailyLog={simulationData.daily_log}
//                   currentDay={currentDay}
//                   startDate={planStartDate}
//               />
//             </div>
            
//             <div className="bg-gray-800/50 rounded-lg shadow-2xl p-6 backdrop-blur-sm border border-gray-700">
//               <h2 className="text-3xl font-bold text-center mb-6 text-green-300 border-b-2 border-gray-700 pb-2">
//                 Full Season Analysis
//               </h2>
              
//               <ResultsSummary simulationData={simulationData} />

//               {/* --- CHANGE HERE: Replace AnimationViewer with ThreeDeeViewer --- */}
//               <ThreeDeeViewer 
//                 dailyLog={simulationData.daily_log} 
//                 onDayChange={setCurrentDay} 
//                 currentDay={currentDay} 
//               />

//               {/* Assuming you have PlotlyChart as a separate component */}
//               <PlotlyChart chartFigure={chartFigure} />
//             </div>
//           </div>
//         )}
//       </main>

//       <footer className="text-center p-4 text-gray-500 text-sm mt-auto">
//         Built by two brothers.
//       </footer>
//     </div>
//   );
// }

// export default App;














// frontend/src/App.jsx

import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';

// Components
import ControlPanel from './components/ControlPanel';
import DailyPlan from './components/DailyPlan';
import FiveDayOutlook from './components/FiveDayOutlook';
import ResultsSummary from './components/ResultsSummary';
import PlotlyChart from './components/PlotlyChart';
import ThreeDeeViewer from './components/ThreeDeeViewer';

// Utils
import { locations } from './utils/locations';
import { createChartFigure } from './utils/chartUtils';

// Constants
const API_BASE_URL = 'http://127.0.0.1:8000';
const POLL_INTERVAL = 3000;

// Custom hook for simulation polling
const useSimulationPolling = () => {
  const intervalRef = useRef(null);

  const startPolling = useCallback((callback, interval = POLL_INTERVAL) => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    intervalRef.current = setInterval(callback, interval);
  }, []);

  const stopPolling = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }, []);

  useEffect(() => {
    return () => stopPolling();
  }, [stopPolling]);

  return { startPolling, stopPolling };
};

// Loading states enum
const LOADING_STATES = {
  IDLE: '',
  SENDING: 'Sending simulation request...',
  RUNNING: 'Simulation is running in the background...',
  FETCHING: 'Fetching final results...',
};

function App() {
  // Core state
  const [simulationData, setSimulationData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState(LOADING_STATES.IDLE);
  const [error, setError] = useState('');
  
  // UI state
  const [chartFigure, setChartFigure] = useState({ data: [], layout: {} });
  const [currentDay, setCurrentDay] = useState(1);
  const [planStartDate, setPlanStartDate] = useState(new Date());
  
  // Custom hook
  const { startPolling, stopPolling } = useSimulationPolling();

  // Reset application state
  const resetState = useCallback(() => {
    setError('');
    setSimulationData(null);
    setChartFigure({ data: [], layout: {} });
    setPlanStartDate(new Date());
  }, []);

  // Handle successful simulation completion
  const handleSimulationSuccess = useCallback(async (simId) => {
    try {
      setLoadingMessage(LOADING_STATES.FETCHING);
      
      const { data } = await axios.get(`${API_BASE_URL}/simulate/results/${simId}`);
      
      setSimulationData(data);
      
      if (data?.daily_log) {
        setChartFigure(createChartFigure(data.daily_log));
        setCurrentDay(1);
      }
      
      setLoading(false);
      setLoadingMessage(LOADING_STATES.IDLE);
    } catch (err) {
      throw new Error('Failed to fetch simulation results');
    }
  }, []);

  // Handle simulation status polling
  const checkSimulationStatus = useCallback(async (simId) => {
    try {
      const { data } = await axios.get(`${API_BASE_URL}/simulate/status/${simId}`);
      const { status } = data;
      
      setLoadingMessage(`Status: ${status}`);
      
      switch (true) {
        case status === 'complete':
          stopPolling();
          await handleSimulationSuccess(simId);
          break;
          
        case status.startsWith('error'):
          stopPolling();
          throw new Error(`Simulation failed: ${status}`);
          
        default:
          // Continue polling
          break;
      }
    } catch (err) {
      stopPolling();
      setError(err.message || 'Failed to poll simulation status');
      setLoading(false);
      setLoadingMessage(LOADING_STATES.IDLE);
    }
  }, [stopPolling, handleSimulationSuccess]);

  // Start simulation
  const handleRunSimulation = useCallback(async (payload) => {
    setLoading(true);
    setLoadingMessage(LOADING_STATES.SENDING);
    resetState();
    
    try {
      const { data } = await axios.post(`${API_BASE_URL}/simulate/start`, payload);
      const { simulation_id: simId } = data;
      
      setLoadingMessage(LOADING_STATES.RUNNING);
      startPolling(() => checkSimulationStatus(simId));
    } catch (err) {
      setError('Failed to start simulation. Is the backend server running?');
      setLoading(false);
      setLoadingMessage(LOADING_STATES.IDLE);
    }
  }, [resetState, startPolling, checkSimulationStatus]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white font-sans flex flex-col">
      {/* Header */}
      <header className="bg-gray-800/80 backdrop-blur-sm p-6 shadow-2xl text-center border-b border-green-500/30">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-green-400 to-emerald-300 bg-clip-text text-transparent tracking-tight">
            Fasalytics
          </h1>
          <p className="text-lg text-gray-300 mt-3 font-light">
            Your AI Farming Analysis
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow p-4 md:p-8">
        {/* Control Panel Section */}
        <section className="max-w-4xl mx-auto mb-12">
          <ControlPanel 
            onRunSimulation={handleRunSimulation} 
            loading={loading} 
            locations={locations}
          />
          
          {/* Loading Indicator */}
          {loading && (
            <div className="text-center mt-6">
              <div className="inline-flex items-center space-x-3">
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-yellow-400 border-t-transparent"></div>
                <p className="text-yellow-400 text-lg font-medium animate-pulse">
                  {loadingMessage}
                </p>
              </div>
            </div>
          )}
        </section>

        {/* Error Display */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8">
            <div className="bg-red-900/20 border border-red-500/50 rounded-xl p-6 text-center">
              <div className="text-red-400 text-xl font-medium">
                ⚠️ {error}
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {simulationData && (
          <div className="max-w-7xl mx-auto space-y-16">
            {/* Daily Planning Section */}
            <section className="space-y-8">
              <div className="text-center">
                <h2 className="text-3xl font-bold text-green-300 mb-2">
                  Daily Farm Management
                </h2>
                <div className="w-24 h-1 bg-gradient-to-r from-green-400 to-emerald-300 mx-auto rounded-full"></div>
              </div>
              
              <DailyPlan 
                dailyLog={simulationData.daily_log} 
                currentDay={currentDay}
                startDate={planStartDate}
                cropType={simulationData.simulation_parameters.crop_type}
              />
              
              <FiveDayOutlook 
                dailyLog={simulationData.daily_log}
                currentDay={currentDay}
                startDate={planStartDate}
              />
            </section>

            {/* Analytics Section */}
            <section className="bg-gray-800/30 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-8 shadow-2xl">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-green-300 mb-2">
                  Full Season Analysis
                </h2>
                <div className="w-24 h-1 bg-gradient-to-r from-green-400 to-emerald-300 mx-auto rounded-full"></div>
              </div>
              
              <div className="space-y-12">
                <ResultsSummary simulationData={simulationData} />

                <ThreeDeeViewer 
                  dailyLog={simulationData.daily_log} 
                  onDayChange={setCurrentDay} 
                  currentDay={currentDay} 
                />

                <PlotlyChart dailyLog={simulationData.daily_log} />
              </div>
            </section>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="text-center p-6 text-gray-500 text-sm border-t border-gray-800">
        <div className="max-w-4xl mx-auto">
          Built with 💚 for Farmers
        </div>
      </footer>
    </div>
  );
}

export default App;