// // frontend/src/components/farm3d/index.js
// // Complete realistic 3D farm components - All in one file for easy implementation

// import React, { useRef, useMemo } from 'react';
// import { useFrame } from '@react-three/fiber';
// import * as THREE from 'three';

// // Weather System Component
// export function WeatherSystem({ weatherCondition = 'sunny', intensity = 1.0 }) {
//   const rainRef = useRef();
//   const cloudsRef = useRef();
  
//   const rainGeometry = useMemo(() => {
//     const geometry = new THREE.BufferGeometry();
//     const rainCount = weatherCondition === 'rainy' ? 2000 : 0;
//     const positions = new Float32Array(rainCount * 3);
//     const velocities = new Float32Array(rainCount * 3);
    
//     for (let i = 0; i < rainCount; i++) {
//       positions[i * 3] = (Math.random() - 0.5) * 200;
//       positions[i * 3 + 1] = Math.random() * 100 + 50;
//       positions[i * 3 + 2] = (Math.random() - 0.5) * 200;
      
//       velocities[i * 3] = (Math.random() - 0.5) * 2;
//       velocities[i * 3 + 1] = -Math.random() * 20 - 10;
//       velocities[i * 3 + 2] = (Math.random() - 0.5) * 2;
//     }
    
//     geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
//     geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));
//     return geometry;
//   }, [weatherCondition]);

//   useFrame((state, delta) => {
//     if (rainRef.current && weatherCondition === 'rainy') {
//       const positions = rainRef.current.geometry.attributes.position.array;
//       const velocities = rainRef.current.geometry.attributes.velocity.array;
      
//       for (let i = 0; i < positions.length; i += 3) {
//         positions[i] += velocities[i] * delta;
//         positions[i + 1] += velocities[i + 1] * delta;
//         positions[i + 2] += velocities[i + 2] * delta;
        
//         if (positions[i + 1] < 0) {
//           positions[i + 1] = 100;
//           positions[i] = (Math.random() - 0.5) * 200;
//           positions[i + 2] = (Math.random() - 0.5) * 200;
//         }
//       }
//       rainRef.current.geometry.attributes.position.needsUpdate = true;
//     }
    
//     if (cloudsRef.current) {
//       cloudsRef.current.rotation.y += delta * 0.1;
//     }
//   });

//   const getWeatherLighting = () => {
//     switch (weatherCondition) {
//       case 'rainy':
//         return { ambient: 0.3, directional: 0.4, color: '#6B7280' };
//       case 'cloudy':
//         return { ambient: 0.5, directional: 0.6, color: '#9CA3AF' };
//       case 'sunny':
//       default:
//         return { ambient: 0.7, directional: 1.0, color: '#FEF3C7' };
//     }
//   };

//   const lighting = getWeatherLighting();

//   return (
//     <group>
//       <ambientLight intensity={lighting.ambient} color={lighting.color} />
//       <directionalLight 
//         position={[100, 100, 50]} 
//         intensity={lighting.directional}
//         color={lighting.color}
//         castShadow
//         shadow-mapSize-width={4096}
//         shadow-mapSize-height={4096}
//         shadow-camera-far={200}
//         shadow-camera-left={-100}
//         shadow-camera-right={100}
//         shadow-camera-top={100}
//         shadow-camera-bottom={-100}
//       />
      
//       {/* Rain particles */}
//       {weatherCondition === 'rainy' && (
//         <points ref={rainRef}>
//           <primitive object={rainGeometry} />
//           <pointsMaterial
//             color="#87CEEB"
//             size={0.1}
//             transparent
//             opacity={0.6}
//           />
//         </points>
//       )}
      
//       {/* Clouds */}
//       {(weatherCondition === 'cloudy' || weatherCondition === 'rainy') && (
//         <group ref={cloudsRef} position={[0, 80, 0]}>
//           {[...Array(8)].map((_, i) => (
//             <mesh key={i} position={[
//               Math.cos(i * Math.PI / 4) * 60,
//               Math.random() * 20,
//               Math.sin(i * Math.PI / 4) * 60
//             ]}>
//               <sphereGeometry args={[15 + Math.random() * 10, 8, 6]} />
//               <meshLambertMaterial 
//                 color={weatherCondition === 'rainy' ? '#4B5563' : '#E5E7EB'} 
//                 transparent 
//                 opacity={0.8} 
//               />
//             </mesh>
//           ))}
//         </group>
//       )}
//     </group>
//   );
// }

// // Soil System Component
// export function SoilSystem({ moistureLevel = 50, fertility = 75, size = [100, 100] }) {
//   const soilTexture = useMemo(() => {
//     // Create a procedural soil texture based on moisture and fertility
//     const canvas = document.createElement('canvas');
//     const ctx = canvas.getContext('2d');
//     canvas.width = 512;
//     canvas.height = 512;
    
//     // Base soil color varies with moisture and fertility
//     const baseR = Math.max(50, 139 - moistureLevel);
//     const baseG = Math.max(30, 69 + fertility * 0.5);
//     const baseB = Math.max(20, 19 + moistureLevel * 0.3);
    
//     for (let x = 0; x < canvas.width; x++) {
//       for (let y = 0; y < canvas.height; y++) {
//         const noise = Math.random() * 40 - 20;
//         const r = Math.max(0, Math.min(255, baseR + noise));
//         const g = Math.max(0, Math.min(255, baseG + noise));
//         const b = Math.max(0, Math.min(255, baseB + noise));
        
//         ctx.fillStyle = `rgb(${r},${g},${b})`;
//         ctx.fillRect(x, y, 1, 1);
//       }
//     }
    
//     const texture = new THREE.CanvasTexture(canvas);
//     texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
//     texture.repeat.set(4, 4);
//     return texture;
//   }, [moistureLevel, fertility]);

//   return (
//     <group>
//       {/* Main soil plane */}
//       <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
//         <planeGeometry args={size} />
//         <meshLambertMaterial map={soilTexture} />
//       </mesh>
      
//       {/* Soil variation patches */}
//       {[...Array(20)].map((_, i) => (
//         <mesh 
//           key={i}
//           rotation={[-Math.PI / 2, 0, Math.random() * Math.PI]}
//           position={[
//             (Math.random() - 0.5) * size[0] * 0.8,
//             0.01,
//             (Math.random() - 0.5) * size[1] * 0.8
//           ]}
//           receiveShadow
//         >
//           <planeGeometry args={[3 + Math.random() * 5, 3 + Math.random() * 5]} />
//           <meshLambertMaterial 
//             color={new THREE.Color().setHSL(0.1, 0.3 + Math.random() * 0.4, 0.2 + Math.random() * 0.3)}
//             transparent
//             opacity={0.7}
//           />
//         </mesh>
//       ))}
//     </group>
//   );
// }

// // Plant System Component
// export function PlantSystem({ dailyLog, currentDay, plantCount = 500 }) {
//   const meshRefs = useRef({});
//   const plantsData = useMemo(() => {
//     const plants = [];
//     for (let i = 0; i < plantCount; i++) {
//       plants.push({
//         id: i,
//         basePosition: [
//           (Math.random() - 0.5) * 80,
//           0,
//           (Math.random() - 0.5) * 80
//         ],
//         baseScale: 0.7 + Math.random() * 0.6,
//         plantType: Math.random() > 0.8 ? 'variant' : 'normal',
//         healthVariation: 0.8 + Math.random() * 0.4,
//       });
//     }
//     return plants;
//   }, [plantCount]);

//   const createPlantGeometry = (stage, variant = false) => {
//     if (stage === 'seedling' || stage === 'germination') {
//       return new THREE.ConeGeometry(0.1, 0.3, 6);
//     } else if (stage === 'vegetative') {
//       return new THREE.ConeGeometry(0.2, 0.8, 7);
//     } else if (stage === 'mature') {
//       if (variant) {
//         // Wheat head geometry
//         return new THREE.CylinderGeometry(0.15, 0.1, 1.5, 8);
//       }
//       return new THREE.ConeGeometry(0.25, 1.2, 8);
//     }
//     return new THREE.ConeGeometry(0.3, 1, 8);
//   };

//   React.useEffect(() => {
//     if (!dailyLog || !dailyLog[currentDay - 1]) return;
    
//     const logEntry = dailyLog[currentDay - 1];
//     const { crop_health, crop_height, growth_stage } = logEntry;
    
//     // Update each plant type
//     ['normal', 'variant'].forEach(plantType => {
//       const meshRef = meshRefs.current[plantType];
//       if (!meshRef) return;
      
//       const tempObject = new THREE.Object3D();
//       const color = new THREE.Color();
//       const healthyColor = new THREE.Color('#22c55e');
//       const unhealthyColor = new THREE.Color('#8B4513');
//       const bloomColor = new THREE.Color('#FFD700');
      
//       const filteredPlants = plantsData.filter(p => p.plantType === plantType);
      
//       filteredPlants.forEach((plant, i) => {
//         // Position with slight wind sway
//         const time = Date.now() * 0.001;
//         const swayX = Math.sin(time + plant.id * 0.1) * 0.1;
//         const swayZ = Math.cos(time + plant.id * 0.15) * 0.1;
        
//         tempObject.position.set(
//           plant.basePosition[0] + swayX,
//           plant.basePosition[1],
//           plant.basePosition[2] + swayZ
//         );
        
//         // Scale based on growth and health
//         const healthFactor = (crop_health / 100) * plant.healthVariation;
//         const heightFactor = crop_height * plant.baseScale * healthFactor;
//         tempObject.scale.set(
//           plant.baseScale * healthFactor,
//           Math.max(0.1, heightFactor),
//           plant.baseScale * healthFactor
//         );
        
//         tempObject.updateMatrix();
//         meshRef.setMatrixAt(i, tempObject.matrix);
        
//         // Color based on health and growth stage
//         let targetColor = healthyColor;
//         if (growth_stage === 'mature' && plant.plantType === 'variant') {
//           targetColor = bloomColor;
//         }
//         color.lerpColors(unhealthyColor, targetColor, healthFactor);
//         meshRef.setColorAt(i, color);
//       });
      
//       meshRef.instanceMatrix.needsUpdate = true;
//       if (meshRef.instanceColor) {
//         meshRef.instanceColor.needsUpdate = true;
//       }
//     });
//   }, [currentDay, dailyLog, plantsData]);

//   const normalPlants = plantsData.filter(p => p.plantType === 'normal');
//   const variantPlants = plantsData.filter(p => p.plantType === 'variant');
  
//   const currentStage = dailyLog && dailyLog[currentDay - 1] ? 
//     dailyLog[currentDay - 1].growth_stage.toLowerCase() : 'seedling';

//   return (
//     <group>
//       {/* Normal plants */}
//       {normalPlants.length > 0 && (
//         <instancedMesh 
//           ref={ref => { if (ref) meshRefs.current.normal = ref; }}
//           args={[
//             createPlantGeometry(currentStage, false),
//             new THREE.MeshLambertMaterial({ vertexColors: true }),
//             normalPlants.length
//           ]}
//           castShadow
//           receiveShadow
//         />
//       )}
      
//       {/* Variant plants */}
//       {variantPlants.length > 0 && (
//         <instancedMesh 
//           ref={ref => { if (ref) meshRefs.current.variant = ref; }}
//           args={[
//             createPlantGeometry(currentStage, true),
//             new THREE.MeshLambertMaterial({ vertexColors: true }),
//             variantPlants.length
//           ]}
//           castShadow
//           receiveShadow
//         />
//       )}
//     </group>
//   );
// }

// // Environment Details Component
// export function EnvironmentDetails({ timeOfDay = 'day' }) {
//   const treesRef = useRef();
  
//   const createTree = (position, scale = 1) => (
//     <group key={`tree-${position.join('-')}`} position={position} scale={scale}>
//       {/* Trunk */}
//       <mesh position={[0, 2, 0]} castShadow>
//         <cylinderGeometry args={[0.3, 0.4, 4, 8]} />
//         <meshLambertMaterial color="#8B4513" />
//       </mesh>
//       {/* Leaves */}
//       <mesh position={[0, 5, 0]} castShadow>
//         <sphereGeometry args={[2.5, 8, 6]} />
//         <meshLambertMaterial color="#228B22" />
//       </mesh>
//     </group>
//   );

//   const trees = useMemo(() => {
//     const treePositions = [
//       [-60, 0, -60], [60, 0, -60], [-60, 0, 60], [60, 0, 60],
//       [-40, 0, -70], [40, 0, -70], [-70, 0, -40], [70, 0, -40],
//       [-70, 0, 40], [70, 0, 40], [-40, 0, 70], [40, 0, 70]
//     ];
    
//     return treePositions.map(pos => createTree(pos, 0.8 + Math.random() * 0.4));
//   }, []);

//   return (
//     <group ref={treesRef}>
//       {/* Trees around the perimeter */}
//       {trees}
      
//       {/* Fence posts */}
//       {[...Array(20)].map((_, i) => {
//         const angle = (i / 20) * Math.PI * 2;
//         const radius = 55;
//         const x = Math.cos(angle) * radius;
//         const z = Math.sin(angle) * radius;
        
//         return (
//           <mesh key={`fence-${i}`} position={[x, 1, z]} castShadow>
//             <cylinderGeometry args={[0.1, 0.1, 2, 6]} />
//             <meshLambertMaterial color="#8B4513" />
//           </mesh>
//         );
//       })}
      
//       {/* Rocks scattered around */}
//       {[...Array(15)].map((_, i) => (
//         <mesh 
//           key={`rock-${i}`}
//           position={[
//             (Math.random() - 0.5) * 90,
//             0,
//             (Math.random() - 0.5) * 90
//           ]}
//           rotation={[0, Math.random() * Math.PI, 0]}
//           castShadow
//         >
//           <dodecahedronGeometry args={[0.3 + Math.random() * 0.5, 0]} />
//           <meshLambertMaterial color="#696969" />
//         </mesh>
//       ))}
      
//       {/* Sky box color based on time */}
//       <mesh>
//         <sphereGeometry args={[200, 32, 16]} />
//         <meshBasicMaterial 
//           color={timeOfDay === 'night' ? '#1a1a2e' : '#87CEEB'} 
//           side={THREE.BackSide}
//         />
//       </mesh>
//     </group>
//   );
// }

// // Farm Animations Component
// export function FarmAnimations({ children, enabled = true }) {
//   const groupRef = useRef();
  
//   useFrame((state, delta) => {
//     if (!enabled || !groupRef.current) return;
    
//     // Gentle overall scene breathing
//     const breathe = Math.sin(state.clock.elapsedTime * 0.5) * 0.002;
//     groupRef.current.scale.setScalar(1 + breathe);
    
//     // Subtle rotation for dynamic feel
//     groupRef.current.rotation.y += delta * 0.005;
//   });
  
//   return (
//     <group ref={groupRef}>
//       {children}
//     </group>
//   );
// }

// // Pest Indicators Component
// export function PestIndicators({ count = 10 }) {
//   const pestsRef = useRef();
  
//   const pestPositions = useMemo(() => {
//     const positions = new Float32Array(count * 3);
//     for (let i = 0; i < count; i++) {
//       positions[i * 3] = (Math.random() - 0.5) * 80;
//       positions[i * 3 + 1] = 2 + Math.random() * 8;
//       positions[i * 3 + 2] = (Math.random() - 0.5) * 80;
//     }
//     return positions;
//   }, [count]);
  
//   useFrame((state, delta) => {
//     if (!pestsRef.current) return;
    
//     const positions = pestsRef.current.geometry.attributes.position.array;
//     const time = state.clock.elapsedTime;
    
//     for (let i = 0; i < count; i++) {
//       const i3 = i * 3;
//       positions[i3] += Math.sin(time * 2 + i) * delta * 2;
//       positions[i3 + 1] += Math.cos(time * 3 + i) * delta;
//       positions[i3 + 2] += Math.sin(time * 1.5 + i) * delta * 2;
      
//       // Keep pests within bounds
//       if (Math.abs(positions[i3]) > 40) positions[i3] *= 0.9;
//       if (Math.abs(positions[i3 + 2]) > 40) positions[i3 + 2] *= 0.9;
//       if (positions[i3 + 1] > 15) positions[i3 + 1] = 2;
//       if (positions[i3 + 1] < 1) positions[i3 + 1] = 15;
//     }
    
//     pestsRef.current.geometry.attributes.position.needsUpdate = true;
//   });
  
//   return (
//     <points ref={pestsRef}>
//       <bufferGeometry>
//         <bufferAttribute
//           attach="attributes-position"
//           count={count}
//           array={pestPositions}
//           itemSize={3}
//         />
//       </bufferGeometry>
//       <pointsMaterial
//         color="#8B4513"
//         size={0.2}
//         sizeAttenuation={true}
//       />
//     </points>
//   );
// }

// // Disease Indicators Component
// export function DiseaseIndicators({ severity = 50 }) {
//   const patchCount = Math.floor(severity / 10);
  
//   return (
//     <group>
//       {[...Array(patchCount)].map((_, i) => (
//         <mesh 
//           key={`disease-${i}`}
//           rotation={[-Math.PI / 2, 0, Math.random() * Math.PI]}
//           position={[
//             (Math.random() - 0.5) * 60,
//             0.02,
//             (Math.random() - 0.5) * 60
//           ]}
//         >
//           <circleGeometry args={[2 + Math.random() * 3, 16]} />
//           <meshLambertMaterial 
//             color="#654321"
//             transparent
//             opacity={0.6}
//           />
//         </mesh>
//       ))}
//     </group>
//   );
// }








import React, { useRef, useMemo, useState, useEffect } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import * as THREE from 'three';

// Weather System Component
export function WeatherSystem({ weatherCondition = 'sunny', intensity = 1.0 }) {
  const rainRef = useRef();
  const cloudsRef = useRef();
  
  const rainGeometry = useMemo(() => {
    const geometry = new THREE.BufferGeometry();
    const rainCount = weatherCondition === 'rainy' ? 2000 : 0;
    const positions = new Float32Array(rainCount * 3);
    const velocities = new Float32Array(rainCount * 3);
    
    for (let i = 0; i < rainCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 200;
      positions[i * 3 + 1] = Math.random() * 100 + 50;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 200;
      
      velocities[i * 3] = (Math.random() - 0.5) * 2;
      velocities[i * 3 + 1] = -Math.random() * 20 - 10;
      velocities[i * 3 + 2] = (Math.random() - 0.5) * 2;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));
    return geometry;
  }, [weatherCondition]);

  useFrame((state, delta) => {
    if (rainRef.current && weatherCondition === 'rainy') {
      const positions = rainRef.current.geometry.attributes.position.array;
      const velocities = rainRef.current.geometry.attributes.velocity.array;
      
      for (let i = 0; i < positions.length; i += 3) {
        positions[i] += velocities[i] * delta;
        positions[i + 1] += velocities[i + 1] * delta;
        positions[i + 2] += velocities[i + 2] * delta;
        
        if (positions[i + 1] < 0) {
          positions[i + 1] = 100;
          positions[i] = (Math.random() - 0.5) * 200;
          positions[i + 2] = (Math.random() - 0.5) * 200;
        }
      }
      rainRef.current.geometry.attributes.position.needsUpdate = true;
    }
    
    if (cloudsRef.current) {
      cloudsRef.current.rotation.y += delta * 0.1;
    }
  });

  const getWeatherLighting = () => {
    switch (weatherCondition) {
      case 'rainy':
        return { ambient: 0.3, directional: 0.4, color: '#6B7280' };
      case 'cloudy':
        return { ambient: 0.5, directional: 0.6, color: '#9CA3AF' };
      case 'sunny':
      default:
        return { ambient: 0.7, directional: 1.0, color: '#FEF3C7' };
    }
  };

  const lighting = getWeatherLighting();

  return (
    <group>
      <ambientLight intensity={lighting.ambient} color={lighting.color} />
      <directionalLight 
        position={[100, 100, 50]} 
        intensity={lighting.directional}
        color={lighting.color}
        castShadow
        shadow-mapSize-width={4096}
        shadow-mapSize-height={4096}
        shadow-camera-far={200}
        shadow-camera-left={-100}
        shadow-camera-right={100}
        shadow-camera-top={100}
        shadow-camera-bottom={-100}
      />
      
      {/* Rain particles */}
      {weatherCondition === 'rainy' && (
        <points ref={rainRef}>
          <primitive object={rainGeometry} />
          <pointsMaterial
            color="#87CEEB"
            size={0.1}
            transparent
            opacity={0.6}
          />
        </points>
      )}
      
      {/* Clouds */}
      {(weatherCondition === 'cloudy' || weatherCondition === 'rainy') && (
        <group ref={cloudsRef} position={[0, 80, 0]}>
          {[...Array(8)].map((_, i) => (
            <mesh key={i} position={[
              Math.cos(i * Math.PI / 4) * 60,
              Math.random() * 20,
              Math.sin(i * Math.PI / 4) * 60
            ]}>
              <sphereGeometry args={[15 + Math.random() * 10, 8, 6]} />
              <meshLambertMaterial 
                color={weatherCondition === 'rainy' ? '#4B5563' : '#E5E7EB'} 
                transparent 
                opacity={0.8} 
              />
            </mesh>
          ))}
        </group>
      )}
    </group>
  );
}

// Soil System Component
export function SoilSystem({ moistureLevel = 50, fertility = 75, size = [100, 100] }) {
  const soilTexture = useMemo(() => {
    // Create a procedural soil texture based on moisture and fertility
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 512;
    canvas.height = 512;
    
    // Base soil color varies with moisture and fertility
    const baseR = Math.max(50, 139 - moistureLevel);
    const baseG = Math.max(30, 69 + fertility * 0.5);
    const baseB = Math.max(20, 19 + moistureLevel * 0.3);
    
    for (let x = 0; x < canvas.width; x++) {
      for (let y = 0; y < canvas.height; y++) {
        const noise = Math.random() * 40 - 20;
        const r = Math.max(0, Math.min(255, baseR + noise));
        const g = Math.max(0, Math.min(255, baseG + noise));
        const b = Math.max(0, Math.min(255, baseB + noise));
        
        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(x, y, 1, 1);
      }
    }
    
    const texture = new THREE.CanvasTexture(canvas);
    texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
    texture.repeat.set(4, 4);
    return texture;
  }, [moistureLevel, fertility]);

  return (
    <group>
      {/* Main soil plane */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={size} />
        <meshLambertMaterial map={soilTexture} />
      </mesh>
      
      {/* Soil variation patches */}
      {[...Array(20)].map((_, i) => (
        <mesh 
          key={i}
          rotation={[-Math.PI / 2, 0, Math.random() * Math.PI]}
          position={[
            (Math.random() - 0.5) * size[0] * 0.8,
            0.01,
            (Math.random() - 0.5) * size[1] * 0.8
          ]}
          receiveShadow
        >
          <planeGeometry args={[3 + Math.random() * 5, 3 + Math.random() * 5]} />
          <meshLambertMaterial 
            color={new THREE.Color().setHSL(0.1, 0.3 + Math.random() * 0.4, 0.2 + Math.random() * 0.3)}
            transparent
            opacity={0.7}
          />
        </mesh>
      ))}
    </group>
  );
}

// GLTF Model Loader Hook
function useGLTFModels(cropType) {
  const [models, setModels] = useState({ stage1: null, stage2: null, stage3: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loader = new GLTFLoader();
    const cropLower = cropType.toLowerCase();
    
    const modelPaths = {
      stage1: `/models/${cropLower}/${cropLower}_stage1.glb`,
      stage2: `/models/${cropLower}/${cropLower}_stage2.glb`,
      stage3: `/models/${cropLower}/${cropLower}_stage3.glb`
    };

    setLoading(true);
    setError(null);

    const loadPromises = Object.entries(modelPaths).map(([stage, path]) =>
      new Promise((resolve, reject) => {
        loader.load(
          path,
          (gltf) => {
            // Clone the scene to allow multiple instances
            const model = gltf.scene.clone();
            model.traverse((child) => {
              if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
                // Ensure materials are properly set
                if (child.material) {
                  child.material = child.material.clone();
                }
              }
            });
            resolve({ stage, model });
          },
          (progress) => {
            console.log(`Loading ${stage}: ${(progress.loaded / progress.total * 100)}%`);
          },
          (error) => {
            console.error(`Error loading ${stage}:`, error);
            reject(error);
          }
        );
      })
    );

    Promise.all(loadPromises)
      .then((results) => {
        const modelMap = {};
        results.forEach(({ stage, model }) => {
          modelMap[stage] = model;
        });
        setModels(modelMap);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error loading GLTF models:', err);
        setError(err);
        setLoading(false);
      });
  }, [cropType]);

  return { models, loading, error };
}

// Plant System Component with GLTF Models
export function PlantSystem({ dailyLog, currentDay, plantCount = 500, cropType = 'wheat' }) {
  const groupRef = useRef();
  const { models, loading, error } = useGLTFModels(cropType);
  
  const plantsData = useMemo(() => {
    const plants = [];
    for (let i = 0; i < plantCount; i++) {
      plants.push({
        id: i,
        basePosition: [
          (Math.random() - 0.5) * 80,
          0,
          (Math.random() - 0.5) * 80
        ],
        baseScale: 0.8 + Math.random() * 0.4,
        healthVariation: 0.8 + Math.random() * 0.4,
        windOffset: Math.random() * Math.PI * 2,
      });
    }
    return plants;
  }, [plantCount]);

  // Determine which model to use based on growth stage
  const getCurrentModel = (growthStage) => {
    if (!models.stage1) return null;
    
    const stage = growthStage?.toLowerCase() || 'seedling';
    
    if (stage.includes('seedling') || stage.includes('germination')) {
      return models.stage1;
    } else if (stage.includes('vegetative') || stage.includes('flowering')) {
      return models.stage2;
    } else if (stage.includes('mature') || stage.includes('harvest')) {
      return models.stage3;
    }
    
    return models.stage1; // Default to stage 1
  };

  useFrame((state, delta) => {
    if (!groupRef.current) return;
    
    // Apply gentle wind animation to all plants
    const windStrength = 0.05;
    const windSpeed = state.clock.elapsedTime * 2;
    
    groupRef.current.children.forEach((plantGroup, index) => {
      if (plantGroup && plantsData[index]) {
        const plant = plantsData[index];
        const swayX = Math.sin(windSpeed + plant.windOffset) * windStrength;
        const swayZ = Math.cos(windSpeed * 0.7 + plant.windOffset) * windStrength * 0.5;
        
        plantGroup.rotation.x = swayX;
        plantGroup.rotation.z = swayZ;
      }
    });
  });

  if (loading) {
    return (
      <group>
        <mesh position={[0, 1, 0]}>
          <boxGeometry args={[1, 1, 1]} />
          <meshBasicMaterial color="#4ade80" wireframe />
        </mesh>
      </group>
    );
  }

  if (error) {
    console.error('Failed to load plant models:', error);
    // Fallback to simple geometry
    return (
      <group ref={groupRef}>
        {plantsData.map((plant, index) => (
          <mesh
            key={plant.id}
            position={plant.basePosition}
            scale={plant.baseScale}
            castShadow
            receiveShadow
          >
            <coneGeometry args={[0.2, 1, 8]} />
            <meshLambertMaterial color="#22c55e" />
          </mesh>
        ))}
      </group>
    );
  }

  const currentLogEntry = dailyLog && dailyLog[currentDay - 1] ? dailyLog[currentDay - 1] : null;
  const currentModel = getCurrentModel(currentLogEntry?.growth_stage);
  
  if (!currentModel) {
    return <group ref={groupRef} />;
  }

  return (
    <group ref={groupRef}>
      {plantsData.map((plant, index) => {
        const healthFactor = currentLogEntry ? 
          (currentLogEntry.crop_health / 100) * plant.healthVariation : 
          plant.healthVariation;
        
        const heightFactor = currentLogEntry ? 
          currentLogEntry.crop_height * plant.baseScale * healthFactor : 
          plant.baseScale;

        return (
          <group
            key={plant.id}
            position={plant.basePosition}
            scale={[
              plant.baseScale * healthFactor,
              Math.max(0.1, heightFactor),
              plant.baseScale * healthFactor
            ]}
          >
            <primitive
              object={currentModel.clone()}
              castShadow
              receiveShadow
            />
          </group>
        );
      })}
    </group>
  );
}

// Environment Details Component
export function EnvironmentDetails({ timeOfDay = 'day' }) {
  const treesRef = useRef();
  
  const createTree = (position, scale = 1) => (
    <group key={`tree-${position.join('-')}`} position={position} scale={scale}>
      {/* Trunk */}
      <mesh position={[0, 2, 0]} castShadow>
        <cylinderGeometry args={[0.3, 0.4, 4, 8]} />
        <meshLambertMaterial color="#8B4513" />
      </mesh>
      {/* Leaves */}
      <mesh position={[0, 5, 0]} castShadow>
        <sphereGeometry args={[2.5, 8, 6]} />
        <meshLambertMaterial color="#228B22" />
      </mesh>
    </group>
  );

  const trees = useMemo(() => {
    const treePositions = [
      [-60, 0, -60], [60, 0, -60], [-60, 0, 60], [60, 0, 60],
      [-40, 0, -70], [40, 0, -70], [-70, 0, -40], [70, 0, -40],
      [-70, 0, 40], [70, 0, 40], [-40, 0, 70], [40, 0, 70]
    ];
    
    return treePositions.map(pos => createTree(pos, 0.8 + Math.random() * 0.4));
  }, []);

  return (
    <group ref={treesRef}>
      {/* Trees around the perimeter */}
      {trees}
      
      {/* Fence posts */}
      {[...Array(20)].map((_, i) => {
        const angle = (i / 20) * Math.PI * 2;
        const radius = 55;
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
        
        return (
          <mesh key={`fence-${i}`} position={[x, 1, z]} castShadow>
            <cylinderGeometry args={[0.1, 0.1, 2, 6]} />
            <meshLambertMaterial color="#8B4513" />
          </mesh>
        );
      })}
      
      {/* Rocks scattered around */}
      {[...Array(15)].map((_, i) => (
        <mesh 
          key={`rock-${i}`}
          position={[
            (Math.random() - 0.5) * 90,
            0,
            (Math.random() - 0.5) * 90
          ]}
          rotation={[0, Math.random() * Math.PI, 0]}
          castShadow
        >
          <dodecahedronGeometry args={[0.3 + Math.random() * 0.5, 0]} />
          <meshLambertMaterial color="#696969" />
        </mesh>
      ))}
      
      {/* Sky box color based on time */}
      <mesh>
        <sphereGeometry args={[200, 32, 16]} />
        <meshBasicMaterial 
          color={timeOfDay === 'night' ? '#1a1a2e' : '#87CEEB'} 
          side={THREE.BackSide}
        />
      </mesh>
    </group>
  );
}

// Farm Animations Component
export function FarmAnimations({ children, enabled = true }) {
  const groupRef = useRef();
  
  useFrame((state, delta) => {
    if (!enabled || !groupRef.current) return;
    
    // Gentle overall scene breathing
    const breathe = Math.sin(state.clock.elapsedTime * 0.5) * 0.002;
    groupRef.current.scale.setScalar(1 + breathe);
    
    // Subtle rotation for dynamic feel
    groupRef.current.rotation.y += delta * 0.005;
  });
  
  return (
    <group ref={groupRef}>
      {children}
    </group>
  );
}

// Pest Indicators Component
export function PestIndicators({ count = 10 }) {
  const pestsRef = useRef();
  
  const pestPositions = useMemo(() => {
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 80;
      positions[i * 3 + 1] = 2 + Math.random() * 8;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 80;
    }
    return positions;
  }, [count]);
  
  useFrame((state, delta) => {
    if (!pestsRef.current) return;
    
    const positions = pestsRef.current.geometry.attributes.position.array;
    const time = state.clock.elapsedTime;
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      positions[i3] += Math.sin(time * 2 + i) * delta * 2;
      positions[i3 + 1] += Math.cos(time * 3 + i) * delta;
      positions[i3 + 2] += Math.sin(time * 1.5 + i) * delta * 2;
      
      // Keep pests within bounds
      if (Math.abs(positions[i3]) > 40) positions[i3] *= 0.9;
      if (Math.abs(positions[i3 + 2]) > 40) positions[i3 + 2] *= 0.9;
      if (positions[i3 + 1] > 15) positions[i3 + 1] = 2;
      if (positions[i3 + 1] < 1) positions[i3 + 1] = 15;
    }
    
    pestsRef.current.geometry.attributes.position.needsUpdate = true;
  });
  
  return (
    <points ref={pestsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={pestPositions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        color="#8B4513"
        size={0.2}
        sizeAttenuation={true}
      />
    </points>
  );
}

// Disease Indicators Component
export function DiseaseIndicators({ severity = 50 }) {
  const patchCount = Math.floor(severity / 10);
  
  return (
    <group>
      {[...Array(patchCount)].map((_, i) => (
        <mesh 
          key={`disease-${i}`}
          rotation={[-Math.PI / 2, 0, Math.random() * Math.PI]}
          position={[
            (Math.random() - 0.5) * 60,
            0.02,
            (Math.random() - 0.5) * 60
          ]}
        >
          <circleGeometry args={[2 + Math.random() * 3, 16]} />
          <meshLambertMaterial 
            color="#654321"
            transparent
            opacity={0.6}
          />
        </mesh>
      ))}
    </group>
  );
}