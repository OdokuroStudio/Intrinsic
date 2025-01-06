import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
from collections import deque

# ====================
# 1) The BotNet
# ====================
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
        return self.output_layer(x)  # Q-values


# =========================
# 2) Replay Buffer
# =========================
class ReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        import random
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.buffer)


# =========================
# 3) Hyperparameters
# =========================
BOT_COUNT = 6

INPUT_SIZE = 25
HIDDEN_SIZE = 128
OUTPUT_SIZE = 35
NUM_HIDDEN_LAYERS = 3

GAMMA = 0.99
EPSILON = 0.2
EPSILON_DECAY = 0.995
EPSILON_MIN = 0.01
BATCH_SIZE = 32
REPLAY_CAPACITY = 5000
UPDATE_TARGET_INTERVAL = 50

# =========================
# 4) Actions list
# =========================
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


# =========================
# 5) Create networks & optimizer
# =========================
model = BotNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_HIDDEN_LAYERS)
target_model = BotNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_HIDDEN_LAYERS)
target_model.load_state_dict(model.state_dict())

optimizer = optim.Adam(model.parameters(), lr=0.001)
replay_buffer = ReplayBuffer(REPLAY_CAPACITY)


# =========================
# 6) Extract state
# =========================
def extract_state(msg):
    px = msg["position"]["x"]
    py = msg["position"]["y"]
    pz = msg["position"]["z"]

    vx = msg["velocity"]["x"]
    vy = msg["velocity"]["y"]
    vz = msg["velocity"]["z"]

    yaw = msg.get("yaw", 0)
    pitch = msg.get("pitch", 0)

    health = msg.get("health", 20)
    food = msg.get("food", 20)

    surroundings = msg.get("surroundings", [])
    coords_list = []
    for i in range(5):
        if i < len(surroundings):
            bx = surroundings[i]["x"]
            by = surroundings[i]["y"]
            bz = surroundings[i]["z"]
            coords_list.extend([bx, by, bz])
        else:
            coords_list.extend([0, 0, 0])

    state_list = [
        px, py, pz,
        vx, vy, vz,
        yaw, pitch,
        health, food
    ] + coords_list

    return torch.tensor(state_list, dtype=torch.float32)


# =========================
# 7) get_action
# =========================
def get_action(state_tensor):
    global EPSILON
    if random.random() < EPSILON:
        return random.randint(0, OUTPUT_SIZE - 1)  # Random action
    else:
        with torch.no_grad():
            q_values = model(state_tensor.unsqueeze(0))
            return q_values.argmax(dim=1).item()


# =========================
# 8) dqn_update
# =========================
def dqn_update(batch):
    states, actions_idx, rewards, next_states, dones = batch

    states_tensor = torch.stack(states)
    next_states_tensor = torch.stack(next_states)
    actions_tensor = torch.tensor(actions_idx, dtype=torch.long)
    rewards_tensor = torch.tensor(rewards, dtype=torch.float32)
    dones_tensor = torch.tensor(dones, dtype=torch.float32)

    q_values = model(states_tensor)
    q_action = q_values.gather(1, actions_tensor.unsqueeze(1)).squeeze(1)

    with torch.no_grad():
        next_q_values = target_model(next_states_tensor).max(1)[0]

    target = rewards_tensor + GAMMA * (1 - dones_tensor) * next_q_values

    loss = F.smooth_l1_loss(q_action, target)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()
