# Reinforcement Learning

A collection of reinforcement learning experiments, starting simple and building up.

## CartPole (DQN)

Started with a random agent that picks left or right with no logic, just to understand how states, actions, rewards and episodes work in Gymnasium.

Then trained a DQN using Stable Baselines 3 on the MlpPolicy for 200,000 timesteps. The trained agent went from averaging ~30 (basically random) to 200-500, a 7-10x improvement.

**Stack:** Python, Gymnasium, Stable Baselines 3, PyTorch

## What is next

More environments and algorithms will be added to this repo over time. This is an ongoing project.
