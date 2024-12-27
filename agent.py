import asyncio
import json
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from websockets import connect
from collections import deque


# A simple DQN network acts as the key survival mechanism
class BotNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_hidden_layers=2):
        super(BotNet, self).__init__()
        self.input_layer = nn.Linear(input_size, hidden_size)
        self.hidden_layers = nn.ModuleList([
            nn.Linear(hidden_size, hidden_size) for _ in range(num_hidden_layers)
        ])
        self.output_layer = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = self.relu(self.input_layer(x))
        for hidden_layer in self.hidden_layers:
            x = self.dropout(self.relu(hidden_layer(x)))
        return self.output_layer(x)  # Returns Q-values for each action


# Replay Buffer to store past events
class ReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.buffer)


# Hyperparameters
BOT_COUNT = 6
# We have position (3), velocity (3), yaw/pitch (2), health + food (2),
# plus 5 blocks * (x,y,z + maybe an encoding for name).
# IE: 3 (pos) + 3 (vel) + 2 (angles) + 2 (health+food) + (5 * 3 coords) = 3+3+2+2+(5*3)=3+3+2+2+15=25
INPUT_SIZE = 25
HIDDEN_SIZE = 128
OUTPUT_SIZE = 35  # Matches the number of actions
NUM_HIDDEN_LAYERS = 3

GAMMA = 0.99
EPSILON = 0.2
EPSILON_DECAY = 0.995
EPSILON_MIN = 0.01
BATCH_SIZE = 32
REPLAY_CAPACITY = 5000
UPDATE_TARGET_INTERVAL = 50  # Steps after which the target network is updated

# Creates the main (online) network and the target network
model = BotNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_HIDDEN_LAYERS)
target_model = BotNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_HIDDEN_LAYERS)
target_model.load_state_dict(model.state_dict())  # Initializes the target same as model

optimizer = optim.Adam(model.parameters(), lr=0.001)
replay_buffer = ReplayBuffer(REPLAY_CAPACITY)

# Action space mapping
actions = [
    "MOVE_FORWARD", "STOP_FORWARD", "MOVE_BACK", "STOP_BACK",
    "JUMP", "LOOK_AT", "BREAK_BLOCK",
    "PLACE_BLOCK", "ATTACK", "PICKUP_ITEM", "USE_ITEM",
    "TURN_LEFT", "TURN_RIGHT", "STRAFE_LEFT", "STRAFE_RIGHT",
    "DROP_ITEM", "DROP_ALL", "SWAP_HANDS", "CRAFT",
    "PLACE_LADDER", "INTERACT_ENTITY", "USE_DOOR",
    "ACTIVATE_LEVER", "COLLECT_ITEM", "SHOOT_BOW",
    "BLOCK_WITH_SHIELD", "CHASE_ENTITY", "NAVIGATE_TO",
    "CLIMB", "FIND_BLOCK", "EAT", "SLEEP", "RESPAWN",
    "USE_FURNACE", "USE_CHEST"
]


# DQN update
def dqn_update(batch, gamma=GAMMA):
    states, actions_idx, rewards, next_states, dones = batch

    # Convert to tensors
    states_tensor = torch.stack(states)  # shape: [batch_size, input_size]
    next_states_tensor = torch.stack(next_states)
    actions_tensor = torch.tensor(actions_idx, dtype=torch.long)  # [batch_size]
    rewards_tensor = torch.tensor(rewards, dtype=torch.float32)  # [batch_size]
    dones_tensor = torch.tensor(dones, dtype=torch.float32)  # [batch_size]

    # Current Q-values
    q_values = model(states_tensor)  # [batch_size, OUTPUT_SIZE]
    q_action = q_values.gather(1, actions_tensor.unsqueeze(1)).squeeze(1)  # [batch_size]

    # Next Q-values (from target network)
    with torch.no_grad():
        next_q_values = target_model(next_states_tensor).max(1)[0]  # [batch_size]

    # Target: r + gamma * max Q(next_state) * (1 - done)
    target = rewards_tensor + gamma * (1 - dones_tensor) * next_q_values

    # Loss
    loss = F.smooth_l1_loss(q_action, target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()


# Extracts states from message
# Same logic as INPUT_SIZE = 25
def extract_state(msg):
    # position(3)
    px = msg["position"]["x"]
    py = msg["position"]["y"]
    pz = msg["position"]["z"]

    # velocity(3)
    vx = msg["velocity"]["x"]
    vy = msg["velocity"]["y"]
    vz = msg["velocity"]["z"]

    # yaw/pitch(2)
    yaw = msg.get("yaw", 0)
    pitch = msg.get("pitch", 0)

    # health + food(2)
    health = msg.get("health", 20)
    food = msg.get("food", 20)

    # surroundings: up to 5 blocks (3 coords each)
    # ignoring block name for now, just the coords
    surroundings = msg.get("surroundings", [])
    coords_list = []
    for i in range(5):
        if i < len(surroundings):
            bx = surroundings[i]["x"]
            by = surroundings[i]["y"]
            bz = surroundings[i]["z"]
            coords_list.extend([bx, by, bz])
        else:
            # If fewer than 5 blocks found, pad with zeros
            coords_list.extend([0, 0, 0])

    # Combine
    state_list = [
                     px, py, pz,
                     vx, vy, vz,
                     yaw, pitch,
                     health, food
                 ] + coords_list  # 5 * 3 = 15 here

    # Convert to PyTorch tensor
    return torch.tensor(state_list, dtype=torch.float32)


def get_action(state_tensor):
    global EPSILON
    if random.random() < EPSILON:
        # Explore
        return random.randint(0, OUTPUT_SIZE - 1)
    else:
        # Exploit
        with torch.no_grad():
            q_values = model(state_tensor.unsqueeze(0))  # shape: [1, OUTPUT_SIZE]
            return q_values.argmax(dim=1).item()


async def control_bots():
    uri = "ws://localhost:3000"
    async with connect(uri) as websocket:
        print("Connected to WebSocket server")

        # Keep track of last state and action per bot
        last_state = [None] * BOT_COUNT
        last_action = [None] * BOT_COUNT

        step_count = 0

        async def send_actions():
            nonlocal step_count
            while True:
                # For each bot, if we have a state, pick an action
                for bot_id in range(BOT_COUNT):
                    if last_state[bot_id] is not None:
                        action_idx = get_action(last_state[bot_id])
                        last_action[bot_id] = action_idx
                        # Prepare the message
                        action_message = {
                            "botId": bot_id,
                            "type": actions[action_idx],
                            "data": {}
                        }
                        await websocket.send(json.dumps(action_message))

                step_count += 1

                # Periodically update the target network
                if step_count % UPDATE_TARGET_INTERVAL == 0:
                    target_model.load_state_dict(model.state_dict())

                # Decay epsilon
                global EPSILON
                EPSILON = max(EPSILON * EPSILON_DECAY, EPSILON_MIN)

                # Send actions ~10 times a second
                await asyncio.sleep(0.1)

        async def receive_messages():
            while True:
                try:
                    message = await websocket.recv()
                    msg_data = json.loads(message)

                    bot_id = msg_data.get("botId", 0)
                    reward = msg_data.get("reward", 0.0)
                    # If you have a 'done' condition (e.g., death or something),
                    # set done = 1.0, else 0.0.
                    done = 0.0

                    # Next state
                    next_state = extract_state(msg_data)

                    # If there is a last state/action, add to replay
                    if last_state[bot_id] is not None and last_action[bot_id] is not None:
                        replay_buffer.push(
                            last_state[bot_id],
                            last_action[bot_id],
                            float(reward),
                            next_state,
                            done
                        )

                    # Update last_state for this bot
                    last_state[bot_id] = next_state

                    # If buffer is large enough, train
                    if len(replay_buffer) >= BATCH_SIZE:
                        batch_data = replay_buffer.sample(BATCH_SIZE)
                        loss_val = dqn_update(batch_data, gamma=GAMMA)
                        print(f"Loss={loss_val:.4f}, Reward={reward:.2f}")
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Error receiving message: {e}")

        # Launch tasks
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
