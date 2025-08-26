import React, { useState, useEffect } from 'react';

const AnimationViewer = ({ imageUrls, onDayChange, currentDay }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const API_BASE_URL = "http://127.0.0.1:8000";

  useEffect(() => {
    let interval;
    if (isPlaying && imageUrls.length > 0) {
      interval = setInterval(() => {
        onDayChange(prevDay => {
            const nextDay = (prevDay % imageUrls.length) + 1;
            return nextDay;
        });
      }, 100);
    }
    return () => clearInterval(interval);
  }, [isPlaying, imageUrls.length, onDayChange]);

  if (!imageUrls || imageUrls.length === 0) {
    return <div className="text-center text-gray-500">Run simulation to generate 3D visualization.</div>;
  }

  const handleSliderChange = (event) => {
    setIsPlaying(false);
    onDayChange(Number(event.target.value));
  };

  const togglePlay = () => setIsPlaying(!isPlaying);

  const currentImageUrl = `${API_BASE_URL}${imageUrls[currentDay - 1]}`;

  return (
    <div className="w-full mt-8 p-4 bg-gray-700/50 rounded-lg shadow-lg">
      <h3 className="text-xl font-semibold text-center text-gray-300 mb-4">
        3D Daily Visualization
      </h3>
      <div className="bg-gray-900 rounded-md p-2 flex justify-center items-center h-96 mb-4">
        <img src={currentImageUrl} alt={`Farm visualization for day ${currentDay}`} className="max-w-full max-h-full object-contain" />
      </div>
      <div className="flex items-center justify-center gap-4">
        <button onClick={togglePlay} className="px-4 py-2 w-24 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors">
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        <span className="text-lg font-mono text-white w-32 text-center">
          Day: {currentDay} / {imageUrls.length}
        </span>
        <input type="range" min="1" max={imageUrls.length} value={currentDay} onChange={handleSliderChange}
          className="w-full h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer" />
      </div>
    </div>
  );
};

export default AnimationViewer;