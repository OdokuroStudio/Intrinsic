#!/usr/bin/env python3

import os
import re
from uuid import uuid4
from argparse import ArgumentParser

import gymnasium as gym
import craftium

from stable_baselines3 import PPO, A2C
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.logger import configure
from stable_baselines3.common.callbacks import CheckpointCallback


def parse_args():
    parser = ArgumentParser()
    # --------------------------------------------------------------------
    # General training/run arguments
    # --------------------------------------------------------------------
    parser.add_argument("--run-name", type=str, default=None,
                        help="Unique name for the run. Defaults to a random uuid.")
    parser.add_argument("--runs-dir", type=str, default="./run-room/",
                        help="Directory to store this run's logs and model.")
    parser.add_argument("--method", type=str, default="ppo", choices=["ppo", "a2c"],
                        help="RL algorithm to use.")
    parser.add_argument("--total-timesteps", type=int, default=1000000,
                        help="Number of total timesteps to train for.")
    parser.add_argument("--device", type=str, default="cuda",
                        help="Device to run on (e.g. 'cuda' or 'cpu').")
    parser.add_argument("--checkpoint-freq", type=int, default=10000,
                        help="How often (in steps) to save a checkpoint during training.")

    # --------------------------------------------------------------------
    # Environment-specific arguments
    # --------------------------------------------------------------------
    parser.add_argument("--env-id", type=str, default="Craftium/Room-v0",
                        help="Name (registered) of the environment.")
    parser.add_argument("--render-mode", type=str, default="human",
                        help="Render mode (e.g. 'human', 'rgb_array', etc.).")
    parser.add_argument("--obs-width", type=int, default=64,
                        help="Observation width in pixels.")
    parser.add_argument("--obs-height", type=int, default=64,
                        help="Observation height in pixels.")
    parser.add_argument("--init-frames", type=int, default=100,
                        help="Number of 'wait frames' for Minetest to load.")
    parser.add_argument("--frameskip", type=int, default=5,
                        help="Number of frames skipped between steps (only if Craftium supports).")
    parser.add_argument("--max-timesteps", type=int, default=10000,
                        help="Max timesteps per episode.")
    parser.add_argument("--mt-listen-timeout", type=int, default=12000,
                        help="Timeout in ms for Minetest to connect via TCP.")
    parser.add_argument("--num-envs", type=int, default=4,
                        help="Number of parallel environments.")

    return parser.parse_args()


def make_env(args):
    """
    Returns a function that, when called, creates a fresh Monitor-wrapped instance
    of the Craftium environment. We can pass it to SubprocVecEnv.
    """
    def _init():
        env = gym.make(
            args.env_id,
            render_mode=args.render_mode,
            # obs_width=args.obs_width,
            # obs_height=args.obs_height,
            init_frames=args.init_frames,
            max_timesteps=args.max_timesteps,
            mt_listen_timeout=args.mt_listen_timeout,
            frameskip=args.frameskip,
        )
        return Monitor(env)  # logs episode rewards, lengths, etc.
    return _init


def find_latest_checkpoint(log_path, method):
    """
    Search the log_path directory for the most recently saved model checkpoint
    for the given method (ppo/a2c). Return its full file path or None if not found.

    We look for files named like:
      - "<method>_model_final.zip"
      - "<method>_<steps>_steps.zip"
    and pick whichever is "latest".

    By 'latest', we prioritize a final model if it exists, otherwise
    the largest step count. If none found, return None.
    """
    # Candidate patterns:
    #   <method>_model_final.zip
    #   <method>_XXXX_steps.zip
    # We'll parse step counts from the second pattern.

    final_model_name = f"{method}_model_final.zip"
    final_model_path = os.path.join(log_path, final_model_name)

    # If final model already exists, use that first
    if os.path.isfile(final_model_path):
        return final_model_path

    # Otherwise, look for checkpoint files named e.g. ppo_10000_steps.zip
    checkpoint_regex = re.compile(rf"^{method}_(\d+)_steps\.zip$")
    max_steps = -1
    chosen_path = None

    if not os.path.isdir(log_path):
        return None

    for f in os.listdir(log_path):
        match = checkpoint_regex.match(f)
        if match:
            steps = int(match.group(1))
            if steps > max_steps:
                max_steps = steps
                chosen_path = os.path.join(log_path, f)

    return chosen_path


def main():
    args = parse_args()

    # Generate a run name if none is provided
    if args.run_name is None:
        run_name = f"{args.env_id.replace('/', '-')}-{args.method}--{uuid4()}"
    else:
        run_name = args.run_name

    # Create the logging directory
    log_path = os.path.join(args.runs_dir, run_name)
    os.makedirs(log_path, exist_ok=True)
    print(f"** Logging to: {log_path}")

    # Configure SB3 logger (stdout, CSV, and tensorboard)
    new_logger = configure(log_path, ["stdout", "csv", "tensorboard"])

    # Create a vectorized environment
    env_fns = [make_env(args) for _ in range(args.num_envs)]
    if args.num_envs > 1:
        venv = SubprocVecEnv(env_fns)
    else:
        # No need for SubprocVecEnv overhead if there's only 1 env
        venv = env_fns[0]()

    # Pick the algorithm class
    if args.method == "ppo":
        model_cls = PPO
        default_kwargs = dict(
            n_steps=2048,
            batch_size=64,
            gae_lambda=0.95,
            gamma=0.99,
            ent_coef=0.01,
            learning_rate=3e-4,
            vf_coef=0.5,
            max_grad_norm=0.5,
        )
    else:
        model_cls = A2C
        default_kwargs = dict(
            n_steps=5,
            gamma=0.99,
            gae_lambda=1.0,
            ent_coef=0.01,
            learning_rate=3e-4,
            vf_coef=0.25,
            max_grad_norm=0.5,
        )

    # ----------------------------------------------------------------------
    # 1) Check if there's a previously saved checkpoint/final model:
    # ----------------------------------------------------------------------
    latest_model_path = find_latest_checkpoint(log_path, args.method)

    if latest_model_path is not None:
        print(f"** Found existing model checkpoint: {latest_model_path}")
        # Load the model and attach the newly created venv
        model = model_cls.load(latest_model_path, env=venv, device=args.device)
        model.set_logger(new_logger)  # re-set the logger
    else:
        print("** No existing model found, creating a new model from scratch.")
        model = model_cls(
            "CnnPolicy",
            venv,
            verbose=1,
            device=args.device,
            **default_kwargs
        )
        model.set_logger(new_logger)

    # ----------------------------------------------------------------------
    # 2) Set up checkpoint callback
    # ----------------------------------------------------------------------
    checkpoint_callback = CheckpointCallback(
        save_freq=args.checkpoint_freq,  # e.g. every 10k steps
        save_path=log_path,
        name_prefix=f"{args.method}",
        verbose=1
    )

    # ----------------------------------------------------------------------
    # 3) Start or continue training
    # ----------------------------------------------------------------------
    model.learn(
        total_timesteps=args.total_timesteps,
        callback=checkpoint_callback,
        reset_num_timesteps=False  # Keep counting from existing step if continuing
    )

    # ----------------------------------------------------------------------
    # 4) Save final model at the end
    # ----------------------------------------------------------------------
    final_path = os.path.join(log_path, f"{args.method}_model_final.zip")
    model.save(final_path)
    print(f"** Final model saved to {final_path}")

    venv.close()
    print("Done.")


if __name__ == "__main__":
    main()
