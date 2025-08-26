// //take help from this code please


// import React, { useMemo, useRef, useEffect, Suspense, useState } from 'react';
// import { Canvas, useFrame } from '@react-three/fiber';
// import { OrbitControls, Environment, Stars, Cloud, Text } from '@react-three/drei';
// import * as THREE from 'three';

// // Import our realistic farm components from the index file (auto-resolves .jsx)
// import { 
//   WeatherSystem, 
//   SoilSystem, 
//   PlantSystem, 
//   EnvironmentDetails, 
//   FarmAnimations,
//   PestIndicators,
//   DiseaseIndicators 
// } from './farm3d';

// // Enhanced Camera Controller
// function CameraController({ autoRotate = false, followPlants = false }) {
//   const controlsRef = useRef();
  
//   useFrame((state, delta) => {
//     if (!controlsRef.current) return;
    
//     if (autoRotate) {
//       controlsRef.current.azimuthAngle += delta * 0.1;
//     }
    
//     if (followPlants) {
//       const time = state.clock.elapsedTime;
//       controlsRef.current.target.set(
//         Math.sin(time * 0.2) * 10,
//         0,
//         Math.cos(time * 0.2) * 10
//       );
//     }
//   });
  
//   return (
//     <OrbitControls 
//       ref={controlsRef}
//       minDistance={15} 
//       maxDistance={100} 
//       enablePan={true}
//       maxPolarAngle={Math.PI / 2.2}
//       minPolarAngle={Math.PI / 6}
//     />
//   );
// }

// // Loading placeholder component
// function LoadingFarm() {
//   const meshRef = useRef();
  
//   useFrame((state) => {
//     if (meshRef.current) {
//       meshRef.current.rotation.y = state.clock.elapsedTime;
//     }
//   });
  
//   return (
//     <group>
//       <mesh ref={meshRef} position={[0, 2, 0]}>
//         <torusGeometry args={[2, 0.5, 8, 16]} />
//         <meshBasicMaterial color="#4ade80" wireframe />
//       </mesh>
//       <Text
//         position={[0, -2, 0]}
//         fontSize={1}
//         color="#ffffff"
//         anchorX="center"
//         anchorY="middle"
//       >
//         Loading Farm...
//       </Text>
//     </group>
//   );
// }

// // Main Farm Scene Component
// function FarmScene({ dailyLog, currentDay, weatherCondition, timeOfDay, cameraSettings }) {
//   const sceneRef = useRef();
  
//   // Calculate derived values from dailyLog
//   const farmData = useMemo(() => {
//     if (!dailyLog || !dailyLog[currentDay - 1]) {
//       return {
//         moistureLevel: 50,
//         fertility: 75,
//         plantCount: 500,
//         pestActivity: 0,
//         diseaseLevel: 0
//       };
//     }
    
//     const entry = dailyLog[currentDay - 1];
//     return {
//       moistureLevel: entry.soil_moisture || 50,
//       fertility: 75 + (entry.crop_health - 50) * 0.5,
//       plantCount: Math.max(100, 500 - (entry.pest_activity || 0) * 10),
//       pestActivity: entry.pest_activity || 0,
//       diseaseLevel: 100 - (entry.crop_health || 100)
//     };
//   }, [dailyLog, currentDay]);
  
//   return (
//     <FarmAnimations enabled={true}>
//       <group ref={sceneRef}>
//         {/* Weather and Lighting */}
//         <WeatherSystem 
//           weatherCondition={weatherCondition}
//           intensity={timeOfDay === 'night' ? 0.3 : 1.0}
//         />
        
//         {/* Environment */}
//         <EnvironmentDetails timeOfDay={timeOfDay} />
        
//         {/* Stars for night time */}
//         {timeOfDay === 'night' && (
//           <Stars 
//             radius={100} 
//             depth={50} 
//             count={5000} 
//             factor={4} 
//             saturation={0} 
//             fade 
//           />
//         )}
        
//         {/* Soil System */}
//         <SoilSystem 
//           moistureLevel={farmData.moistureLevel}
//           fertility={farmData.fertility}
//           size={[100, 100]}
//         />
        
//         {/* Plant System */}
//         <PlantSystem 
//           dailyLog={dailyLog}
//           currentDay={currentDay}
//           plantCount={farmData.plantCount}
//         />
        
//         {/* Pest indicators (flying particles) */}
//         {farmData.pestActivity > 0 && (
//           <PestIndicators count={farmData.pestActivity * 5} />
//         )}
        
//         {/* Disease indicators (brown patches) */}
//         {farmData.diseaseLevel > 20 && (
//           <DiseaseIndicators severity={farmData.diseaseLevel} />
//         )}
//       </group>
//     </FarmAnimations>
//   );
// }

// // Components are now imported from farm3d/index.js - no need to redefine them here

// // Control Panel Component
// function ControlPanel({ 
//   weatherCondition, setWeatherCondition,
//   timeOfDay, setTimeOfDay,
//   autoRotate, setAutoRotate,
//   followPlants, setFollowPlants 
// }) {
//   return (
//     <div className="flex flex-wrap gap-4 mb-4 p-4 bg-gray-800 rounded-lg">
//       <div className="flex flex-col">
//         <label className="text-sm text-gray-300 mb-1">Weather</label>
//         <select 
//           value={weatherCondition} 
//           onChange={(e) => setWeatherCondition(e.target.value)}
//           className="bg-gray-700 text-white px-3 py-1 rounded"
//         >
//           <option value="sunny">Sunny</option>
//           <option value="cloudy">Cloudy</option>
//           <option value="rainy">Rainy</option>
//         </select>
//       </div>
      
//       <div className="flex flex-col">
//         <label className="text-sm text-gray-300 mb-1">Time</label>
//         <select 
//           value={timeOfDay} 
//           onChange={(e) => setTimeOfDay(e.target.value)}
//           className="bg-gray-700 text-white px-3 py-1 rounded"
//         >
//           <option value="day">Day</option>
//           <option value="night">Night</option>
//         </select>
//       </div>
      
//       <div className="flex items-center gap-2">
//         <input 
//           type="checkbox" 
//           checked={autoRotate} 
//           onChange={(e) => setAutoRotate(e.target.checked)}
//           className="rounded"
//         />
//         <label className="text-sm text-gray-300">Auto Rotate</label>
//       </div>
      
//       <div className="flex items-center gap-2">
//         <input 
//           type="checkbox" 
//           checked={followPlants} 
//           onChange={(e) => setFollowPlants(e.target.checked)}
//           className="rounded"
//         />
//         <label className="text-sm text-gray-300">Follow Plants</label>
//       </div>
//     </div>
//   );
// }

// // Main ThreeDeeViewer Component
// function ThreeDeeViewer({ dailyLog, currentDay, onDayChange }) {
//   const [weatherCondition, setWeatherCondition] = useState('sunny');
//   const [timeOfDay, setTimeOfDay] = useState('day');
//   const [autoRotate, setAutoRotate] = useState(false);
//   const [followPlants, setFollowPlants] = useState(false);
//   const [showStats, setShowStats] = useState(true);

//   // Auto-adjust weather based on data if available
//   useEffect(() => {
//     if (dailyLog && dailyLog[currentDay - 1]) {
//       const entry = dailyLog[currentDay - 1];
//       if (entry.weather_condition) {
//         setWeatherCondition(entry.weather_condition.toLowerCase());
//       }
//     }
//   }, [dailyLog, currentDay]);

//   const farmStats = useMemo(() => {
//     if (!dailyLog || !dailyLog[currentDay - 1]) return null;
    
//     const entry = dailyLog[currentDay - 1];
//     return {
//       health: entry.crop_health || 0,
//       height: entry.crop_height || 0,
//       stage: entry.growth_stage || 'Unknown',
//       moisture: entry.soil_moisture || 0,
//       pests: entry.pest_activity || 0,
//       weather: entry.weather_condition || 'Unknown'
//     };
//   }, [dailyLog, currentDay]);

//   return (
//     <div className="w-full mt-8 p-4 bg-gray-700/50 rounded-lg shadow-lg">
//       <h3 className="text-xl font-semibold text-center text-gray-300 mb-4">
//         🌾 Realistic 3D Digital Twin Farm
//       </h3>
      
//       {/* Control Panel */}
//       <ControlPanel 
//         weatherCondition={weatherCondition}
//         setWeatherCondition={setWeatherCondition}
//         timeOfDay={timeOfDay}
//         setTimeOfDay={setTimeOfDay}
//         autoRotate={autoRotate}
//         setAutoRotate={setAutoRotate}
//         followPlants={followPlants}
//         setFollowPlants={setFollowPlants}
//       />
      
//       {/* 3D Canvas */}
//       <div className="bg-black rounded-md h-[500px] mb-4 relative overflow-hidden">
//         <Canvas 
//           camera={{ position: [0, 25, 50], fov: 60 }}
//           shadows
//           gl={{ 
//             antialias: true, 
//             alpha: false,
//             powerPreference: "high-performance"
//           }}
//         >
//           <Suspense fallback={<LoadingFarm />}>
//             {/* Enhanced Environment */}
//             <Environment 
//               files="/venice_sunset_1k.hdr" 
//               background={timeOfDay === 'day'} 
//               blur={0.8} 
//             />
            
//             {/* Main Farm Scene */}
//             <FarmScene 
//               dailyLog={dailyLog}
//               currentDay={currentDay}
//               weatherCondition={weatherCondition}
//               timeOfDay={timeOfDay}
//             />
            
//             {/* Enhanced Camera Controls */}
//             <CameraController 
//               autoRotate={autoRotate}
//               followPlants={followPlants}
//             />
//           </Suspense>
//         </Canvas>
        
//         {/* Stats Overlay */}
//         {showStats && farmStats && (
//           <div className="absolute top-4 left-4 bg-black/70 text-white p-3 rounded-lg text-sm">
//             <div className="grid grid-cols-2 gap-2">
//               <div>Health: <span className="text-green-400">{farmStats.health.toFixed(1)}%</span></div>
//               <div>Height: <span className="text-blue-400">{farmStats.height.toFixed(2)}m</span></div>
//               <div>Stage: <span className="text-yellow-400">{farmStats.stage}</span></div>
//               <div>Moisture: <span className="text-cyan-400">{farmStats.moisture.toFixed(1)}%</span></div>
//               <div>Pests: <span className="text-red-400">{farmStats.pests.toFixed(0)}</span></div>
//               <div>Weather: <span className="text-purple-400">{farmStats.weather}</span></div>
//             </div>
//           </div>
//         )}
        
//         {/* Toggle Stats Button */}
//         <button
//           onClick={() => setShowStats(!showStats)}
//           className="absolute top-4 right-4 bg-gray-800/80 text-white p-2 rounded-lg hover:bg-gray-700/80 transition-colors"
//         >
//           📊
//         </button>
//       </div>

//       {/* Day Control Slider */}
//       <div className="flex items-center justify-center gap-4 mb-4">
//         <span className="text-lg font-mono text-white w-32 text-center">
//           Day: {currentDay} / {dailyLog ? dailyLog.length : 0}
//         </span>
//         <input 
//           type="range"
//           min="1"
//           max={dailyLog ? dailyLog.length : 1}
//           value={currentDay}
//           onChange={(e) => onDayChange(Number(e.target.value))}
//           className="flex-1 h-3 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
//           style={{
//             background: `linear-gradient(to right, #22c55e 0%, #22c55e ${(currentDay / (dailyLog?.length || 1)) * 100}%, #4b5563 ${(currentDay / (dailyLog?.length || 1)) * 100}%, #4b5563 100%)`
//           }}
//         />
//       </div>
      
//       {/* Farm Information */}
//       <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-300">
//         <div className="bg-gray-800/50 p-3 rounded-lg">
//           <h4 className="font-semibold text-green-400 mb-2">🌱 Growth Features</h4>
//           <ul className="space-y-1">
//             <li>• Dynamic plant growth stages</li>
//             <li>• Health-based color variations</li>
//             <li>• Realistic wind animations</li>
//             <li>• Multiple plant varieties</li>
//           </ul>
//         </div>
        
//         <div className="bg-gray-800/50 p-3 rounded-lg">
//           <h4 className="font-semibold text-blue-400 mb-2">🌦️ Weather Effects</h4>
//           <ul className="space-y-1">
//             <li>• Dynamic rain particles</li>
//             <li>• Volumetric clouds</li>
//             <li>• Weather-based lighting</li>
//             <li>• Day/night cycles</li>
//           </ul>
//         </div>
        
//         <div className="bg-gray-800/50 p-3 rounded-lg">
//           <h4 className="font-semibold text-yellow-400 mb-2">🏞️ Environment</h4>
//           <ul className="space-y-1">
//             <li>• Procedural soil textures</li>
//             <li>• Surrounding trees & fences</li>
//             <li>• Pest & disease indicators</li>
//             <li>• Realistic shadows & lighting</li>
//           </ul>
//         </div>
//       </div>
      
//       {/* Controls Info */}
//       <div className="mt-4 text-xs text-gray-400 text-center">
//         💡 Use mouse to orbit • Scroll to zoom • Drag to pan • Toggle settings above for different experiences
//       </div>
//     </div>
//   );
// }

// export default ThreeDeeViewer;














import React, { useMemo, useRef, useEffect, Suspense, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment, Stars, Cloud, Text } from '@react-three/drei';
import * as THREE from 'three';

// Import our realistic farm components with GLTF support
import { 
  WeatherSystem, 
  SoilSystem, 
  PlantSystem, 
  EnvironmentDetails, 
  FarmAnimations,
  PestIndicators,
  DiseaseIndicators 
} from './farm3d';

// Enhanced Camera Controller
function CameraController({ autoRotate = false, followPlants = false }) {
  const controlsRef = useRef();
  
  useFrame((state, delta) => {
    if (!controlsRef.current) return;
    
    if (autoRotate) {
      controlsRef.current.azimuthAngle += delta * 0.1;
    }
    
    if (followPlants) {
      const time = state.clock.elapsedTime;
      controlsRef.current.target.set(
        Math.sin(time * 0.2) * 10,
        0,
        Math.cos(time * 0.2) * 10
      );
    }
  });
  
  return (
    <OrbitControls 
      ref={controlsRef}
      minDistance={15} 
      maxDistance={100} 
      enablePan={true}
      maxPolarAngle={Math.PI / 2.2}
      minPolarAngle={Math.PI / 6}
    />
  );
}

// Loading placeholder component
function LoadingFarm() {
  const meshRef = useRef();
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.elapsedTime;
    }
  });
  
  return (
    <group>
      <mesh ref={meshRef} position={[0, 2, 0]}>
        <torusGeometry args={[2, 0.5, 8, 16]} />
        <meshBasicMaterial color="#4ade80" wireframe />
      </mesh>
      <Text
        position={[0, -2, 0]}
        fontSize={1}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
      >
        Loading Farm Models...
      </Text>
    </group>
  );
}

// Main Farm Scene Component
function FarmScene({ dailyLog, currentDay, weatherCondition, timeOfDay, cameraSettings, cropType }) {
  const sceneRef = useRef();
  
  // Calculate derived values from dailyLog
  const farmData = useMemo(() => {
    if (!dailyLog || !dailyLog[currentDay - 1]) {
      return {
        moistureLevel: 50,
        fertility: 75,
        plantCount: 500,
        pestActivity: 0,
        diseaseLevel: 0
      };
    }
    
    const entry = dailyLog[currentDay - 1];
    return {
      moistureLevel: entry.soil_moisture || 50,
      fertility: 75 + (entry.crop_health - 50) * 0.5,
      plantCount: Math.max(100, 500 - (entry.pest_activity || 0) * 10),
      pestActivity: entry.pest_activity || 0,
      diseaseLevel: 100 - (entry.crop_health || 100)
    };
  }, [dailyLog, currentDay]);
  
  return (
    <FarmAnimations enabled={true}>
      <group ref={sceneRef}>
        {/* Weather and Lighting */}
        <WeatherSystem 
          weatherCondition={weatherCondition}
          intensity={timeOfDay === 'night' ? 0.3 : 1.0}
        />
        
        {/* Environment */}
        <EnvironmentDetails timeOfDay={timeOfDay} />
        
        {/* Stars for night time */}
        {timeOfDay === 'night' && (
          <Stars 
            radius={100} 
            depth={50} 
            count={5000} 
            factor={4} 
            saturation={0} 
            fade 
          />
        )}
        
        {/* Soil System */}
        <SoilSystem 
          moistureLevel={farmData.moistureLevel}
          fertility={farmData.fertility}
          size={[100, 100]}
        />
        
        {/* Plant System with GLTF Models */}
        <PlantSystem 
          dailyLog={dailyLog}
          currentDay={currentDay}
          plantCount={farmData.plantCount}
          cropType={cropType}
        />
        
        {/* Pest indicators (flying particles) */}
        {farmData.pestActivity > 0 && (
          <PestIndicators count={farmData.pestActivity * 5} />
        )}
        
        {/* Disease indicators (brown patches) */}
        {farmData.diseaseLevel > 20 && (
          <DiseaseIndicators severity={farmData.diseaseLevel} />
        )}
      </group>
    </FarmAnimations>
  );
}

// Control Panel Component
function ControlPanel({ 
  weatherCondition, setWeatherCondition,
  timeOfDay, setTimeOfDay,
  autoRotate, setAutoRotate,
  followPlants, setFollowPlants,
  cropType, setCropType
}) {
  return (
    <div className="flex flex-wrap gap-4 mb-4 p-4 bg-gray-800 rounded-lg">
      <div className="flex flex-col">
        <label className="text-sm text-gray-300 mb-1">Crop Type</label>
        <select 
          value={cropType} 
          onChange={(e) => setCropType(e.target.value)}
          className="bg-gray-700 text-white px-3 py-1 rounded"
        >
          <option value="wheat">Wheat</option>
          <option value="rice">Rice</option>
          <option value="sugarcane">Sugarcane</option>
        </select>
      </div>
      
      <div className="flex flex-col">
        <label className="text-sm text-gray-300 mb-1">Weather</label>
        <select 
          value={weatherCondition} 
          onChange={(e) => setWeatherCondition(e.target.value)}
          className="bg-gray-700 text-white px-3 py-1 rounded"
        >
          <option value="sunny">Sunny</option>
          <option value="cloudy">Cloudy</option>
          <option value="rainy">Rainy</option>
        </select>
      </div>
      
      <div className="flex flex-col">
        <label className="text-sm text-gray-300 mb-1">Time</label>
        <select 
          value={timeOfDay} 
          onChange={(e) => setTimeOfDay(e.target.value)}
          className="bg-gray-700 text-white px-3 py-1 rounded"
        >
          <option value="day">Day</option>
          <option value="night">Night</option>
        </select>
      </div>
      
      <div className="flex items-center gap-2">
        <input 
          type="checkbox" 
          checked={followPlants} 
          onChange={(e) => setFollowPlants(e.target.checked)}
          className="rounded"
        />
        <label className="text-sm text-gray-300">Follow Plants</label>
      </div>
    </div>
  );
}

// Main ThreeDeeViewer Component
function ThreeDeeViewer({ dailyLog, currentDay, onDayChange, simulationConfig }) {
  const [weatherCondition, setWeatherCondition] = useState('sunny');
  const [timeOfDay, setTimeOfDay] = useState('day');
  const [autoRotate, setAutoRotate] = useState(false);
  const [followPlants, setFollowPlants] = useState(false);
  const [showStats, setShowStats] = useState(true);
  
  // Get crop type from simulation config or default to wheat
  const [cropType, setCropType] = useState(
    simulationConfig?.crop_type?.toLowerCase() || 'wheat'
  );

  // Update crop type when simulation config changes
  useEffect(() => {
    if (simulationConfig?.crop_type) {
      setCropType(simulationConfig.crop_type.toLowerCase());
    }
  }, [simulationConfig]);

  // Auto-adjust weather based on data if available
  useEffect(() => {
    if (dailyLog && dailyLog[currentDay - 1]) {
      const entry = dailyLog[currentDay - 1];
      if (entry.weather_condition) {
        setWeatherCondition(entry.weather_condition.toLowerCase());
      }
    }
  }, [dailyLog, currentDay]);

  const farmStats = useMemo(() => {
    if (!dailyLog || !dailyLog[currentDay - 1]) return null;
    
    const entry = dailyLog[currentDay - 1];
    return {
      health: entry.crop_health || 0,
      height: entry.crop_height || 0,
      stage: entry.growth_stage || 'Unknown',
      moisture: entry.soil_moisture || 0,
      pests: entry.pest_activity || 0,
      weather: entry.weather_condition || 'Unknown'
    };
  }, [dailyLog, currentDay]);

  // Crop stage descriptions for better understanding
  const getStageDescription = (stage) => {
    const descriptions = {
      'seedling': 'Young shoots emerging from soil',
      'germination': 'Seeds beginning to sprout',
      'vegetative': 'Active growth and leaf development',
      'flowering': 'Plant producing flowers/heads',
      'mature': 'Ready for harvest',
      'harvest': 'Harvesting stage'
    };
    return descriptions[stage?.toLowerCase()] || stage;
  };

  return (
    <div className="w-full mt-8 p-4 bg-gray-700/50 rounded-lg shadow-lg">
      <h3 className="text-xl font-semibold text-center text-gray-300 mb-4">
        🌾 Realistic 3D Digital Twin Farm - {cropType.charAt(0).toUpperCase() + cropType.slice(1)} Crop
      </h3>
      
      {/* Control Panel */}
      <ControlPanel 
        weatherCondition={weatherCondition}
        setWeatherCondition={setWeatherCondition}
        timeOfDay={timeOfDay}
        setTimeOfDay={setTimeOfDay}
        autoRotate={autoRotate}
        setAutoRotate={setAutoRotate}
        followPlants={followPlants}
        setFollowPlants={setFollowPlants}
        cropType={cropType}
        setCropType={setCropType}
      />
      
      {/* GLTF Model Requirements Notice */}
      <div className="mb-4 p-3 bg-blue-900/30 rounded-lg border border-blue-500/30">
        <div className="text-sm text-blue-300">
          <strong>GLTF Model Structure Required:</strong>
          <div className="mt-2 font-mono text-xs">
            /public/models/<br/>
            ├── wheat/<br/>
            │   ├── wheat_stage1.gltf (Seedling)<br/>
            │   ├── wheat_stage2.gltf (Vegetative)<br/>
            │   └── wheat_stage3.gltf (Mature)<br/>
            ├── rice/<br/>
            │   ├── rice_stage1.gltf (Seedling)<br/>
            │   ├── rice_stage2.gltf (Vegetative)<br/>
            │   └── rice_stage3.gltf (Mature)<br/>
            └── sugarcane/<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;├── sugarcane_stage1.gltf (Young)<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;├── sugarcane_stage2.gltf (Growing)<br/>
            &nbsp;&nbsp;&nbsp;&nbsp;└── sugarcane_stage3.gltf (Mature)
          </div>
        </div>
      </div>
      
      {/* 3D Canvas */}
      <div className="bg-black rounded-md h-[500px] mb-4 relative overflow-hidden">
        <Canvas 
          camera={{ position: [0, 25, 50], fov: 60 }}
          shadows
          gl={{ 
            antialias: true, 
            alpha: false,
            powerPreference: "high-performance"
          }}
        >
          <Suspense fallback={<LoadingFarm />}>
            {/* Enhanced Environment */}
            <Environment 
              files="/venice_sunset_1k.hdr" 
              background={timeOfDay === 'day'} 
              blur={0.8} 
            />
            
            {/* Main Farm Scene with Crop Type */}
            <FarmScene 
              dailyLog={dailyLog}
              currentDay={currentDay}
              weatherCondition={weatherCondition}
              timeOfDay={timeOfDay}
              cropType={cropType}
            />
            
            {/* Enhanced Camera Controls */}
            <CameraController 
              autoRotate={autoRotate}
              followPlants={followPlants}
            />
          </Suspense>
        </Canvas>
        
        {/* Stats Overlay */}
        {showStats && farmStats && (
          <div className="absolute top-4 left-4 bg-black/70 text-white p-3 rounded-lg text-sm">
            <div className="grid grid-cols-2 gap-2">
              <div>Health: <span className="text-green-400">{farmStats.health.toFixed(1)}%</span></div>
              <div>Height: <span className="text-blue-400">{farmStats.height.toFixed(2)}m</span></div>
              <div>Stage: <span className="text-yellow-400">{farmStats.stage}</span></div>
              <div>Moisture: <span className="text-cyan-400">{farmStats.moisture.toFixed(1)}%</span></div>
              <div>Pests: <span className="text-red-400">{farmStats.pests.toFixed(0)}</span></div>
              <div>Weather: <span className="text-purple-400">{farmStats.weather}</span></div>
            </div>
            <div className="mt-2 text-xs text-gray-400">
              {getStageDescription(farmStats.stage)}
            </div>
          </div>
        )}
        
        {/* Crop Type Indicator */}
        <div className="absolute top-4 right-16 bg-green-900/80 text-white p-2 rounded-lg text-sm">
          🌾 {cropType.charAt(0).toUpperCase() + cropType.slice(1)}
        </div>
        
        {/* Toggle Stats Button */}
        <button
          onClick={() => setShowStats(!showStats)}
          className="absolute top-4 right-4 bg-gray-800/80 text-white p-2 rounded-lg hover:bg-gray-700/80 transition-colors"
        >
          📊
        </button>
      </div>

      {/* Day Control Slider */}
      <div className="flex items-center justify-center gap-4 mb-4">
        <span className="text-lg font-mono text-white w-32 text-center">
          Day: {currentDay} / {dailyLog ? dailyLog.length : 0}
        </span>
        <input 
          type="range"
          min="1"
          max={dailyLog ? dailyLog.length : 1}
          value={currentDay}
          onChange={(e) => onDayChange(Number(e.target.value))}
          className="flex-1 h-3 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
          style={{
            background: `linear-gradient(to right, #22c55e 0%, #22c55e ${(currentDay / (dailyLog?.length || 1)) * 100}%, #4b5563 ${(currentDay / (dailyLog?.length || 1)) * 100}%, #4b5563 100%)`
          }}
        />
      </div>
      
      {/* Farm Information - Updated for GLTF Models */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-300">
        <div className="bg-gray-800/50 p-3 rounded-lg">
          <h4 className="font-semibold text-green-400 mb-2">🌱 GLTF Model Features</h4>
          <ul className="space-y-1">
            <li>• Realistic 3D crop models</li>
            <li>• 3 growth stages per crop</li>
            <li>• Dynamic model switching</li>
            <li>• Health-based scaling</li>
          </ul>
        </div>
        
        <div className="bg-gray-800/50 p-3 rounded-lg">
          <h4 className="font-semibold text-blue-400 mb-2">🌦️ Weather Effects</h4>
          <ul className="space-y-1">
            <li>• Dynamic rain particles</li>
            <li>• Volumetric clouds</li>
            <li>• Weather-based lighting</li>
            <li>• Day/night cycles</li>
          </ul>
        </div>
        
        <div className="bg-gray-800/50 p-3 rounded-lg">
          <h4 className="font-semibold text-yellow-400 mb-2">🏞️ Environment</h4>
          <ul className="space-y-1">
            <li>• Procedural soil textures</li>
            <li>• Wind animations</li>
            <li>• Pest & disease indicators</li>
            <li>• Realistic shadows & lighting</li>
          </ul>
        </div>
      </div>
      
      {/* Crop Stages Information */}
      <div className="mt-4 p-3 bg-gray-800/50 rounded-lg">
        <h4 className="font-semibold text-orange-400 mb-2">📈 Growth Stages for {cropType.charAt(0).toUpperCase() + cropType.slice(1)}</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-gray-400">
          <div className="text-center">
            <div className="font-semibold text-green-400">Stage 1</div>
            <div>{cropType === 'wheat' ? 'Seedling' : cropType === 'rice' ? 'Seedling' : 'Young Shoots'}</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-yellow-400">Stage 2</div>
            <div>{cropType === 'wheat' ? 'Vegetative' : cropType === 'rice' ? 'Tillering' : 'Growing Stalks'}</div>
          </div>
          <div className="text-center">
            <div className="font-semibold text-orange-400">Stage 3</div>
            <div>{cropType === 'wheat' ? 'Mature/Harvest' : cropType === 'rice' ? 'Mature Grain' : 'Full Height'}</div>
          </div>
        </div>
      </div>
      
      {/* Controls Info */}
      <div className="mt-4 text-xs text-gray-400 text-center">
        💡 Use mouse to orbit • Scroll to zoom • Drag to pan • Toggle settings above for different experiences<br/>
        🔄 Models load automatically based on growth stage and crop type
      </div>
    </div>
  );
}

export default ThreeDeeViewer;