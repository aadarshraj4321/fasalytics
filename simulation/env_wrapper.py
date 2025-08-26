# simulation/env_wrapper.py

import gymnasium as gym
from gymnasium import spaces

class MultiAgentActionWrapper(gym.ActionWrapper):
    def __init__(self, env):
        super(MultiAgentActionWrapper, self).__init__(env)
        
        # The agent now sees a single action space with 50 actions.
        # This represents every combination of:
        # 5 water levels * 5 fertilizer levels * 2 pesticide choices (Yes/No)
        self.action_space = spaces.Discrete(5 * 5 * 2)

    def action(self, action):
        """
        This method decodes the agent's single action (an integer from 0 to 49)
        back into the dictionary format that our complex FarmEnv expects.
        
        We use a sequence of mathematical operations to decode the action.
        Example: if the agent chooses action `action = 37`
        - pesticide_action = 37 // 25 = 1 (meaning "Yes, apply pesticide")
        - temp_action = 37 % 25 = 12
        - irrigation_action = 12 // 5 = 2
        - fertilizer_action = 12 % 5 = 2
        This translates to: {"pesticide": 1, "irrigation": 2, "fertilizer": 2}
        """
        
        # First, decode the pesticide action (the highest level)
        pesticide_action = action // (5 * 5)
        
        # Get the remainder to decode the other two actions
        temp_action = action % (5 * 5)
        
        # Now, decode irrigation and fertilizer from the remainder
        irrigation_action = temp_action // 5
        fertilizer_action = temp_action % 5
        
        return {
            "irrigation": irrigation_action,
            "fertilizer": fertilizer_action,
            "pesticide": pesticide_action
        }