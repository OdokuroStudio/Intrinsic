from argparse import ArgumentParser
from uuid import uuid4
import os

import gymnasium as gym
import craftium

from stable_baselines3 import A2C, PPO
from stable_baselines3.common import logger
from stable_baselines3.common.monitor import Monitor


def parse_args():
    parser = ArgumentParser()

    # General training/run arguments
    parser.add_argument(
        "--run-name", type=str, default=None,
        help="Unique name for the run. Defaults to a random uuid."
    )
    parser.add_argument(
        "--runs-dir", type=str, default="./run-room/",
        help="Directory to store this run's logs and model."
    )
    parser.add_argument(
        "--method", type=str, default="a2c", choices=["ppo", "a2c"],
        help="RL algorithm to use."
    )
    parser.add_argument(
        "--total-timesteps", type=int, default=10_000_000,
        help="Number of total timesteps to train for."
    )

    # Environment-specific arguments
    parser.add_argument(
        "--env-id", type=str, default="Craftium/Room-v0",
        help="Name (registered) of the environment."
    )
    parser.add_argument(
        "--render-mode", type=str, default="human",
        help="Render mode (e.g. 'human' or 'rgb_array')."
    )
    parser.add_argument(
        "--obs-width", type=int, default=200,
        help="Observation width in pixels."
    )
    parser.add_argument(
        "--obs-height", type=int, default=200,
        help="Observation height in pixels."
    )
    parser.add_argument(
        "--init-frames", type=int, default=100,
        help="Number of 'wait frames' for Minetest to load."
    )
    parser.add_argument(
        "--max-timesteps", type=int, default=10000,
        help="Max timesteps per episode."
    )
    parser.add_argument(
        "--mt-listen-timeout", type=int, default=12000,
        help="Timeout in ms for Minetest to connect via TCP."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Generate a run name if none is provided
    if args.run_name is None:
        run_name = f"{args.env_id.replace('/', '-')}-{args.method}--{uuid4()}"
    else:
        run_name = args.run_name

    # Configure the logger so your logs and model go into the specified directory
    log_path = os.path.join(args.runs_dir, run_name)
    print(f"** Logging to: {log_path}")
    new_logger = logger.configure(log_path, ["stdout", "csv"])

    # Create a single environment instance
    env = gym.make(
        args.env_id,
        render_mode=args.render_mode,
        obs_width=args.obs_width,
        obs_height=args.obs_height,
        init_frames=args.init_frames,
        max_timesteps=args.max_timesteps,
        mt_listen_timeout=args.mt_listen_timeout,
    )

    # Wrap it with Monitor for basic logging of episodes
    env = Monitor(env, filename=log_path)

    # Pick the algorithm
    if args.method == "ppo":
        model_cls = PPO
    else:
        model_cls = A2C

    # Initialize model
    model = model_cls("CnnPolicy", env, verbose=1, n_steps=2048, learning_rate=3e-4, ent_coef=0.01, device="cuda")
    model.set_logger(new_logger)

    # Train
    model.learn(total_timesteps=args.total_timesteps)

    env.close()
