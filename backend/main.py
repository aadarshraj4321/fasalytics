# # backend/main.py

# from fastapi import FastAPI, BackgroundTasks, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import sys
# import os
# from fastapi.staticfiles import StaticFiles 
# import time
# import shutil
# # Subprocess is no longer needed as we are removing the 2D image rendering
# # import subprocess 

# # --- Path Setup ---
# this_file_path = os.path.abspath(__file__)
# project_root_path = os.path.dirname(os.path.dirname(this_file_path))
# sys.path.append(project_root_path)

# # --- Project Imports ---
# from simulation.farm_env import FarmEnv
# from simulation.env_wrapper import MultiAgentActionWrapper
# from stable_baselines3 import PPO

# # --- In-memory storage for tracking background tasks ---
# SIMULATION_STATUS = {}
# SIMULATION_RESULTS = {}

# # --- FastAPI App Initialization ---
# app = FastAPI(
#     title="AI digital twin farm api",
#     description="An api to run farm simulations using a trained reinforcement learning agent.",
#     version="5.0.0"
# )

# # --- Static Files and CORS ---
# STATIC_DIR = os.path.join(project_root_path, "static")
# os.makedirs(STATIC_DIR, exist_ok=True)
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# origins = [
#     "http://localhost",
#     "http://localhost:5173",
#     "http://localhost:3000"
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = origins,
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"]
# )

# # --- AI Model Loading ---
# # Create a dictionary to hold our specialist AI models
# models = {}
# # This should point to your final, prescient champion models for each crop
# CROP_MODELS = {
#     "Wheat": "ppo_PRESCIENT_WHEAT_champion.zip",
#     "Rice": "ppo_PRESCIENT_RICE_champion.zip",
#     "Sugarcane": "ppo_PRESCIENT_SUGARCANE_champion.zip"
# }

# print("--- Loading Specialist Prescient AI Models ---")
# for crop, model_file in CROP_MODELS.items():
#     model_path = os.path.join(project_root_path, "models", model_file)
#     if os.path.exists(model_path):
#         # creating dummy environment for loading the model, it MUST be wrapped
#         base_env_for_loading = FarmEnv(crop_type=crop)
#         wrapped_env_for_loading = MultiAgentActionWrapper(base_env_for_loading)
#         models[crop] = PPO.load(model_path, env=wrapped_env_for_loading)
#         print(f"Successfully loaded model for: {crop}")
#     else:
#         print(f"Warning: Model file not found for {crop} at {model_path}. This crop will not be available.")

# if not models:
#     raise RuntimeError("No AI models were loaded. Please train at least one agent.")

# print("Backend is ready. All available AI models loaded successfully.")


# # --- Background Task Definition ---
# def run_simulation_task(sim_id: str, request_data: dict):
#     try:
#         SIMULATION_STATUS[sim_id] = "processing: Running simulation..."
        
#         crop_type = request_data.get('crop_type', 'Wheat')
        
#         # --- Dynamic Model Selection ---
#         model = models.get(crop_type)
#         if model is None:
#             raise ValueError(f"No trained model available for the selected crop: {crop_type}")
        
#         # for every request we creating the fresh new environment, with dynamic location
#         base_env_sim = FarmEnv(
#             crop_type=request_data['crop_type'],
#             soil_type=request_data['soil_type'],
#             simulation_days=request_data.get('simulation_days'),
#             latitude=request_data['latitude'],
#             longitude=request_data['longitude']
#         )
#         env = MultiAgentActionWrapper(base_env_sim)
        
#         obs, _ = env.reset()
#         done = False
        
#         # store the result
#         daily_results = []
#         total_irrigation, total_fertilizer, total_pesticide_apps = 0, 0, 0
#         total_days = base_env_sim.simulation_days

#         while not done:
#             action, _ = model.predict(obs, deterministic=True)
#             obs, reward, done, _, info = env.step(action)

#             original_env = env.unwrapped
#             decoded_action = env.action(action)
#             irrigation_amount = original_env.irrigation_map[decoded_action["irrigation"]]
#             fertilizer_amount = original_env.fertilizer_map[decoded_action["fertilizer"]]
#             pesticide_applied = original_env.pesticide_map[decoded_action["pesticide"]]

#             total_irrigation += irrigation_amount
#             total_fertilizer += fertilizer_amount
#             if pesticide_applied == 1:
#                 total_pesticide_apps += 1

#             # Update status for frontend polling
#             SIMULATION_STATUS[sim_id] = f"processing: Simulating Day {original_env.current_day}/{total_days}"

#             # Get data directly from the environment for the log
#             daily_results.append({
#                 "day": original_env.current_day,
#                 "soil_moisture": info.get('moisture'),
#                 "soil_nitrogen": info.get('nitrogen'),
#                 "crop_health": info.get('health'),
#                 "yield_kg_per_ha": info.get('yield'),
#                 "irrigation_mm": irrigation_amount,
#                 "fertilizer_kg_per_ha": fertilizer_amount,
#                 "pesticide_applied": pesticide_applied,
#                 "rust_risk": info.get('rust_risk', 0.0),
#                 "crop_height": original_env.crop.height,
#                 "growth_stage": original_env.crop.growth_stage
#             })
        
#         final_yield = daily_results[-1]["yield_kg_per_ha"] if daily_results else 0
#         final_profit = info.get('profit', 0)

#         # The slow 2D image rendering subprocess loop has been completely removed.
#         print("Simulation data generation complete.")
        
#         # Prepare final results package
#         final_data = {
#             "status": "complete",
#             "simulation_parameters": request_data,
#             "results_summary": {
#                 "final_yield_kg_per_ha": round(final_yield, 2),
#                 "total_irrigation_applied_mm": round(total_irrigation, 2),
#                 "total_fertilizer_applied_kg_per_ha": round(total_fertilizer, 2),
#                 "total_pesticide_applications": total_pesticide_apps,
#                 "final_profit": round(final_profit, 2)
#             },
#             # The visualization key is removed, frontend will handle 3D rendering
#             "daily_log": daily_results
#         }
        
#         # Store results and update final status
#         SIMULATION_RESULTS[sim_id] = final_data
#         SIMULATION_STATUS[sim_id] = "complete"
#         print(f"Simulation {sim_id} completed.")

#     except Exception as e:
#         print(f"Error in background task for {sim_id}: {e}")
#         SIMULATION_STATUS[sim_id] = f"error: {str(e)}"

# # --- API Data Models ---
# class SimulationRequest(BaseModel):
#     crop_type: str = "Wheat"
#     soil_type: str = "Alluvial"
#     simulation_days: int = None
#     latitude: float = 30.9010
#     longitude: float = 75.8573





# # --- API Endpoints ---
# @app.post("/simulate/start")
# def start_simulation_endpoint(request: SimulationRequest, background_tasks: BackgroundTasks):
#     print(f"Received simulation start request: {request}")
#     sim_id = f"sim_{int(time.time())}"
#     SIMULATION_STATUS[sim_id] = "pending"
#     SIMULATION_RESULTS[sim_id] = None
#     background_tasks.add_task(run_simulation_task, sim_id, request.dict())
#     return {"message": "Simulation started in background", "simulation_id": sim_id}

# @app.get("/simulate/status/{sim_id}")
# def get_simulation_status(sim_id: str):
#     status = SIMULATION_STATUS.get(sim_id)
#     if status is None:
#         raise HTTPException(status_code=404, detail="Simulation ID not found")
#     return {"simulation_id": sim_id, "status": status}

# @app.get("/simulate/results/{sim_id}")
# def get_simulation_results(sim_id: str):
#     status = SIMULATION_STATUS.get(sim_id)
#     results = SIMULATION_RESULTS.get(sim_id)
#     if status != "complete" or results is None:
#         raise HTTPException(status_code=404, detail=f"Results not available. Status: {status}")
#     return results





















# # backend/main.py

# from fastapi import FastAPI, BackgroundTasks, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import sys
# import os
# from fastapi.staticfiles import StaticFiles 
# import time
# import shutil
# import subprocess

# # --- Path Setup ---
# this_file_path = os.path.abspath(__file__)
# project_root_path = os.path.dirname(os.path.dirname(this_file_path))
# sys.path.append(project_root_path)

# # --- Project Imports ---
# from simulation.farm_env import FarmEnv
# from simulation.env_wrapper import MultiAgentActionWrapper
# from stable_baselines3 import PPO

# # --- In-memory storage for tracking background tasks ---
# SIMULATION_STATUS = {}
# SIMULATION_RESULTS = {}

# # --- FastAPI App Initialization ---
# app = FastAPI(
#     title="AI digital twin farm api",
#     description="An api to run farm simulations using a trained reinforcement learning agent.",
#     version="5.0.0"
# )

# # --- Static Files and CORS ---
# STATIC_DIR = os.path.join(project_root_path, "static")
# os.makedirs(STATIC_DIR, exist_ok=True)
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# origins = [
#     "http://localhost",
#     "http://localhost:5173",
#     "http://localhost:3000"
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = origins,
#     allow_credentials = True,
#     allow_methods = ["*"],
#     allow_headers = ["*"]
# )

# # --- AI Model Loading ---
# # Create a dictionary to hold our specialist AI models
# models = {}
# # This should point to your final, prescient champion models for each crop
# CROP_MODELS = {
#     "Wheat": "one_million_ppo_ULTIMATE_CHAMPION_WHEAT.zip",
#     "Rice": "ppo_ULTIMATE_CHAMPION_Rice.zip",
#     "Sugarcane": "ppo_ULTIMATE_CHAMPION_Sugarcane.zip"
# }

# print("--- Loading Specialist Prescient AI Models ---")
# for crop, model_file in CROP_MODELS.items():
#     model_path = os.path.join(project_root_path, "models", model_file)
#     if os.path.exists(model_path):
#         # creating dummy environment for loading the model, it MUST be wrapped
#         base_env_for_loading = FarmEnv(crop_type=crop)
#         wrapped_env_for_loading = MultiAgentActionWrapper(base_env_for_loading)
#         models[crop] = PPO.load(model_path, env=wrapped_env_for_loading)
#         print(f"Successfully loaded model for: {crop}")
#     else:
#         print(f"Warning: Model file not found for {crop} at {model_path}. This crop will not be available.")

# if not models:
#     raise RuntimeError("No AI models were loaded. Please train at least one agent.")

# print("Backend is ready. All available AI models loaded successfully.")


# # --- Background Task Definition ---
# def run_simulation_and_render_task(sim_id: str, request_data: dict):
#     try:
#         SIMULATION_STATUS[sim_id] = "processing: Running simulation..."
        
#         crop_type = request_data.get('crop_type', 'Wheat')
        
#         # --- Dynamic Model Selection ---
#         model = models.get(crop_type)
#         if model is None:
#             raise ValueError(f"No trained model available for the selected crop: {crop_type}")
        
#         # for every request we creating the fresh new environment, with dynamic location
#         base_env_sim = FarmEnv(
#             crop_type=request_data['crop_type'],
#             soil_type=request_data['soil_type'],
#             simulation_days=request_data.get('simulation_days'),
#             latitude=request_data['latitude'],
#             longitude=request_data['longitude']
#         )
#         env = MultiAgentActionWrapper(base_env_sim)
        
#         obs, _ = env.reset()
#         done = False
        
#         # store the result
#         daily_results = []
#         total_irrigation, total_fertilizer, total_pesticide_apps = 0, 0, 0
#         total_days = base_env_sim.simulation_days
#         # Track extreme weather events
#         heat_wave_days = 0
#         heavy_rain_days = 0

#         while not done:
#             action, _ = model.predict(obs, deterministic=True)
#             obs, reward, done, _, info = env.step(action)

#             original_env = env.unwrapped
#             decoded_action = env.action(action)
#             irrigation_amount = original_env.irrigation_map[decoded_action["irrigation"]]
#             fertilizer_amount = original_env.fertilizer_map[decoded_action["fertilizer"]]
#             pesticide_applied = original_env.pesticide_map[decoded_action["pesticide"]]

#             total_irrigation += irrigation_amount
#             total_fertilizer += fertilizer_amount
#             if pesticide_applied == 1:
#                 total_pesticide_apps += 1

#             # Update status for frontend polling
#             SIMULATION_STATUS[sim_id] = f"processing: Simulating Day {original_env.current_day}/{total_days}"

#             # Check for extreme weather alerts from the info dictionary
#             alerts = info.get('extreme_weather_alerts', [])
#             if "High risk of HEAT WAVE" in alerts:
#                 heat_wave_days += 1
#             if "High risk of HEAVY RAIN" in alerts:
#                 heavy_rain_days += 1

#             # Get data directly from the environment's info dictionary
#             # daily_results.append({
#             #     "day": original_env.current_day,
#             #     "soil_moisture": info.get('moisture'),
#             #     "soil_nitrogen": info.get('nitrogen'),
#             #     "crop_health": info.get('health'),
#             #     "yield_kg_per_ha": info.get('yield'),
#             #     "irrigation_mm": irrigation_amount,
#             #     "fertilizer_kg_per_ha": fertilizer_amount,
#             #     "pesticide_applied": pesticide_applied,
#             #     "disease_risks": info.get('disease_risks', {}),
#             #     "extreme_weather_alerts": alerts
#             # })

#             daily_results.append({
#                 "day": original_env.current_day,
#                 "soil_moisture": info.get('moisture'),
#                 "soil_nitrogen": info.get('nitrogen'),
#                 "crop_health": info.get('health'),
#                 "yield_kg_per_ha": info.get('yield'),
#                 "irrigation_mm": irrigation_amount,
#                 "fertilizer_kg_per_ha": fertilizer_amount,
#                 "pesticide_applied": pesticide_applied,
#                 "disease_risks": info.get('disease_risks', {}),
#                 "extreme_weather_alerts": alerts,
#                 # Add these missing fields:
#                 "growth_stage": original_env.growth_stage,
#                 "crop_height": original_env.crop_height, 
#                 "weather_condition": original_env.weather_condition,
#                 "pest_activity": original_env.pest_activity
#             })
        
#         final_yield = daily_results[-1]["yield_kg_per_ha"] if daily_results else 0
#         final_profit = info.get('profit', 0)

#         # The image rendering part is removed as we move to real-time 3D
#         print("Simulation data generation complete.")
        
#         # Prepare final results package
#         final_data = {
#             "status": "complete",
#             "simulation_parameters": request_data,
#             "results_summary": {
#                 "final_yield_kg_per_ha": round(final_yield, 2),
#                 "total_irrigation_applied_mm": round(total_irrigation, 2),
#                 "total_fertilizer_applied_kg_per_ha": round(total_fertilizer, 2),
#                 "total_pesticide_applications": total_pesticide_apps,
#                 "final_profit": round(final_profit, 2),
#                 "heat_wave_alert_days": heat_wave_days,
#                 "heavy_rain_alert_days": heavy_rain_days,
#             },
#             "daily_log": daily_results
#         }
        
#         # Store results and update final status
#         SIMULATION_RESULTS[sim_id] = final_data
#         SIMULATION_STATUS[sim_id] = "complete"
#         print(f"Simulation {sim_id} completed.")

#     except Exception as e:
#         print(f"Error in background task for {sim_id}: {e}")
#         SIMULATION_STATUS[sim_id] = f"error: {str(e)}"

# # --- API Data Models ---
# class SimulationRequest(BaseModel):
#     crop_type: str = "Wheat"
#     soil_type: str = "Alluvial"
#     simulation_days: int = None
#     latitude: float = 30.9010 # Default to Ludhiana
#     longitude: float = 75.8573

# # --- API Endpoints ---
# @app.post("/simulate/start")
# def start_simulation_endpoint(request: SimulationRequest, background_tasks: BackgroundTasks):
#     print(f"Received simulation start request: {request}")
#     sim_id = f"sim_{int(time.time())}"
#     SIMULATION_STATUS[sim_id] = "pending"
#     SIMULATION_RESULTS[sim_id] = None
#     background_tasks.add_task(run_simulation_and_render_task, sim_id, request.dict())
#     return {"message": "Simulation started in background", "simulation_id": sim_id}

# @app.get("/simulate/status/{sim_id}")
# def get_simulation_status(sim_id: str):
#     status = SIMULATION_STATUS.get(sim_id)
#     if status is None:
#         raise HTTPException(status_code=404, detail="Simulation ID not found")
#     return {"simulation_id": sim_id, "status": status}

# @app.get("/simulate/results/{sim_id}")
# def get_simulation_results(sim_id: str):
#     status = SIMULATION_STATUS.get(sim_id)
#     results = SIMULATION_RESULTS.get(sim_id)
#     if status != "complete" or results is None:
#         raise HTTPException(status_code=404, detail=f"Results not available. Status: {status}")
#     return results


















# backend/main.py

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from fastapi.staticfiles import StaticFiles 
import time
import shutil

import sys
import numpy.core.numeric as numeric
sys.modules['numpy._core.numeric'] = numeric

# Subprocess is no longer needed as the 3D rendering is on the frontend
# import subprocess 

# --- Path Setup ---
this_file_path = os.path.abspath(__file__)
project_root_path = os.path.dirname(os.path.dirname(this_file_path))
sys.path.append(project_root_path)

# --- Project Imports ---
from simulation.farm_env import FarmEnv
from simulation.env_wrapper import MultiAgentActionWrapper
from stable_baselines3 import PPO

# --- In-memory storage for tracking background tasks ---
SIMULATION_STATUS = {}
SIMULATION_RESULTS = {}

# --- FastAPI App Initialization ---
app = FastAPI(
    title="AI digital twin farm api",
    description="An api to run farm simulations using a trained reinforcement learning agent.",
    version="6.0.0" # Final version with all advanced features
)

# --- Static Files and CORS ---
STATIC_DIR = os.path.join(project_root_path, "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# --- AI Model Loading ---
# Create a dictionary to hold our specialist AI models
models = {}
# This should point to your final champion models
CROP_MODELS = {
    "Wheat": "one_million_ppo_ULTIMATE_CHAMPION_WHEAT.zip",
    "Rice": "ppo_ULTIMATE_CHAMPION_Rice.zip",
    "Sugarcane": "ppo_ULTIMATE_CHAMPION_Sugarcane.zip"
}

print("--- Loading Specialist ULTIMATE AI Models ---")
for crop, model_file in CROP_MODELS.items():
    model_path = os.path.join(project_root_path, "models", model_file)
    if os.path.exists(model_path):
        # creating dummy environment for loading the model, it MUST be wrapped
        base_env_for_loading = FarmEnv(crop_type=crop)
        wrapped_env_for_loading = MultiAgentActionWrapper(base_env_for_loading)
        models[crop] = PPO.load(model_path, env=wrapped_env_for_loading)
        print(f"Successfully loaded ULTIMATE model for: {crop}")
    else:
        print(f"Warning: ULTIMATE model file not found for {crop} at {model_path}. This crop will not be available.")

if not models:
    raise RuntimeError("No AI models were loaded. Please train at least one agent.")

print("Backend is ready. All available AI models loaded successfully.")


# --- Background Task Definition ---
def run_simulation_and_render_task(sim_id: str, request_data: dict):
    try:
        SIMULATION_STATUS[sim_id] = "processing: Running simulation..."
        
        crop_type = request_data.get('crop_type', 'Wheat')
        
        # --- Dynamic Model Selection ---
        model = models.get(crop_type)
        if model is None:
            raise ValueError(f"No trained model available for the selected crop: {crop_type}")
        
        # for every request we creating the fresh new environment, with dynamic location
        base_env_sim = FarmEnv(
            crop_type=request_data['crop_type'],
            soil_type=request_data['soil_type'],
            simulation_days=request_data.get('simulation_days'),
            latitude=request_data['latitude'],
            longitude=request_data['longitude']
        )
        env = MultiAgentActionWrapper(base_env_sim)
        
        obs, _ = env.reset()
        done = False
        
        # store the result
        daily_results = []
        total_irrigation, total_fertilizer, total_pesticide_apps = 0, 0, 0
        total_days = base_env_sim.simulation_days
        heat_wave_days = 0
        heavy_rain_days = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _, info = env.step(action)

            original_env = env.unwrapped
            decoded_action = env.action(action)
            irrigation_amount = original_env.irrigation_map[decoded_action["irrigation"]]
            fertilizer_amount = original_env.fertilizer_map[decoded_action["fertilizer"]]
            pesticide_applied = original_env.pesticide_map[decoded_action["pesticide"]]

            total_irrigation += irrigation_amount
            total_fertilizer += fertilizer_amount
            if pesticide_applied == 1:
                total_pesticide_apps += 1

            SIMULATION_STATUS[sim_id] = f"processing: Simulating Day {original_env.current_day}/{total_days}"

            alerts = info.get('extreme_weather_alerts', [])
            # Using .upper() makes the check case-insensitive and more robust
            if any("HEAT WAVE" in s.upper() for s in alerts):
                heat_wave_days += 1
            if any("HEAVY RAIN" in s.upper() for s in alerts):
                heavy_rain_days += 1

            # Get data from the correct objects (info dict and original_env.crop)
            daily_results.append({
                "day": original_env.current_day,
                "soil_moisture": info.get('moisture'),
                "soil_nitrogen": info.get('nitrogen'),
                "crop_health": info.get('health'),
                "yield_kg_per_ha": info.get('yield'),
                "irrigation_mm": irrigation_amount,
                "fertilizer_kg_per_ha": fertilizer_amount,
                "pesticide_applied": pesticide_applied,
                "disease_risks": info.get('disease_risks', {}),
                "extreme_weather_alerts": alerts,
                "growth_stage": original_env.crop.growth_stage,
                "crop_height": original_env.crop.height, 
            })
        
        final_yield = daily_results[-1]["yield_kg_per_ha"] if daily_results else 0
        final_profit = info.get('profit', 0)

        # The image rendering part is removed as we move to real-time 3D
        print("Simulation data generation complete.")
        
        # Prepare final results package
        final_data = {
            "status": "complete",
            "simulation_parameters": request_data,
            "results_summary": {
                "final_yield_kg_per_ha": round(final_yield, 2),
                "total_irrigation_applied_mm": round(total_irrigation, 2),
                "total_fertilizer_applied_kg_per_ha": round(total_fertilizer, 2),
                "total_pesticide_applications": total_pesticide_apps,
                "final_profit": round(final_profit, 2),
                "heat_wave_alert_days": heat_wave_days,
                "heavy_rain_alert_days": heavy_rain_days,
            },
            "daily_log": daily_results
        }
        
        # Store results and update final status
        SIMULATION_RESULTS[sim_id] = final_data
        SIMULATION_STATUS[sim_id] = "complete"
        print(f"Simulation {sim_id} completed.")

    except Exception as e:
        print(f"Error in background task for {sim_id}: {e}")
        SIMULATION_STATUS[sim_id] = f"error: {str(e)}"

# --- API Data Models ---
class SimulationRequest(BaseModel):
    crop_type: str = "Wheat"
    soil_type: str = "Alluvial"
    simulation_days: int = None
    latitude: float = 30.9010
    longitude: float = 75.8573

# --- API Endpoints ---
@app.post("/simulate/start")
def start_simulation_endpoint(request: SimulationRequest, background_tasks: BackgroundTasks):
    print(f"Received simulation start request: {request}")
    sim_id = f"sim_{int(time.time())}"
    SIMULATION_STATUS[sim_id] = "pending"
    SIMULATION_RESULTS[sim_id] = None
    background_tasks.add_task(run_simulation_and_render_task, sim_id, request.dict())
    return {"message": "Simulation started in background", "simulation_id": sim_id}

@app.get("/simulate/status/{sim_id}")
def get_simulation_status(sim_id: str):
    status = SIMULATION_STATUS.get(sim_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Simulation ID not found")
    return {"simulation_id": sim_id, "status": status}

@app.get("/simulate/results/{sim_id}")
def get_simulation_results(sim_id: str):
    status = SIMULATION_STATUS.get(sim_id)
    results = SIMULATION_RESULTS.get(sim_id)
    if status != "complete" or results is None:
        raise HTTPException(status_code=404, detail=f"Results not available. Status: {status}")
    return results