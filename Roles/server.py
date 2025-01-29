import asyncio
import json
from websockets import connect

# Import everything from our DQN file
from serf import *

# Initialize EPSILON with the initial exploration rate
EPSILON = 1.0  # Starting exploration rate
step_count = 0

async def control_bots():
    global step_count, EPSILON

    uri = "ws://localhost:3000"
    async with connect(uri) as websocket:
        print("Connected to WebSocket server")

        # Keep track of last state and action per bot
        last_state = [None] * BOT_COUNT
        last_action = [None] * BOT_COUNT

        async def send_actions():
            global step_count, EPSILON

            while True:
                for bot_id in range(BOT_COUNT):
                    if last_state[bot_id] is not None:
                        action_idx = get_action(last_state[bot_id])
                        last_action[bot_id] = action_idx

                        action_message = {
                            "botId": bot_id,
                            "type": actions[action_idx],
                            "data": {}
                        }
                        await websocket.send(json.dumps(action_message))

                # Update target network periodically
                if step_count % UPDATE_TARGET_INTERVAL == 0:
                    # TODO add random telport so models can train on new locations
                    target_model.load_state_dict(model.state_dict())
                    save_model()

                # Decay epsilon
                EPSILON = max(EPSILON * EPSILON_DECAY, EPSILON_MIN)

                # ~10 actions per second
                await asyncio.sleep(0.5)

        async def receive_messages():
            while True:
                try:
                    message = await websocket.recv()
                    msg_data = json.loads(message)

                    bot_id = msg_data.get("botId", 0)
                    reward = msg_data.get("reward", 0.0)
                    done = 0.0  # or detect end-of-episode

                    next_state = extract_state(msg_data)

                    if last_state[bot_id] is not None and last_action[bot_id] is not None:
                        replay_buffer.push(
                            last_state[bot_id],
                            last_action[bot_id],
                            float(reward),
                            next_state,
                            done
                        )

                    last_state[bot_id] = next_state

                    # If buffer is large enough, train
                    if len(replay_buffer) >= BATCH_SIZE:
                        batch_data = replay_buffer.sample(BATCH_SIZE)
                        loss_val = dqn_update(batch_data)

                        print(f"Loss={loss_val:.4f}, Reward={reward:.2f}")

                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Error receiving message: {e}")

        send_task = asyncio.create_task(send_actions())
        recv_task = asyncio.create_task(receive_messages())

        try:
            await asyncio.gather(send_task, recv_task)
        except Exception as e:
            print(f"Main control loop error: {e}")
        finally:
            send_task.cancel()
            recv_task.cancel()


if __name__ == "__main__":
    asyncio.run(control_bots())
