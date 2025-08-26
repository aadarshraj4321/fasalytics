// frontend/src/components/Plant.jsx

import React from 'react';
// useGLTF is a helper from drei that makes loading .gltf or .glb models easy
import { useGLTF } from '@react-three/drei';

function Plant(props) {
  // --- IMPORTANT ---
  // Replace 'wheat_mature.glb' with the EXACT filename of your 3D model
  // that is inside the `frontend/public/models/` folder.
  const modelPath = '/models/wheatA.glb'; 
  
  // useGLTF hook loads the model and gives us access to its contents
  const { scene } = useGLTF(modelPath);

  // We need to traverse the model to make sure every part casts and receives shadows
  scene.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });

  // 'primitive' is a special JSX tag from React Three Fiber.
  // It allows us to render a complex, pre-existing three.js object like our 'scene'.
  // We pass all other props (like position, scale) down to it.
  return <primitive object={scene} {...props} />;
}

// Preloading the model so it's ready when the component mounts
useGLTF.preload('/models/wheatA.glb');

export default Plant;