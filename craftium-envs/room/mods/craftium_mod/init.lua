-- We can track the old distance in a global or in a table keyed by each player's name.
-- For a single-player environment, it's simplest to store in a single variable.

local old_distance = nil
local target_pos = nil

-- Utility function to get a random float in [lower, greater]
function rand(lower, greater)
    return lower + math.random() * (greater - lower)
end

reset_environment = function()
    local player = minetest.get_connected_players()[1]
    if not player then
        return
    end

    -- Place the player in a random position inside the room
    player:set_pos({
        x = rand(-13.2, 4.2),
        z = rand(-15.2, -10.0),
        y = 6
    })

    -- Remove the previously spawned block (if any)
    if target_pos ~= nil then
        minetest.remove_node(target_pos)
    end

    -- Spawn a red block inside the room at a random position
    target_pos = {
        x = rand(-13.2, 4.2),
        z = rand(-9.0, -0.8),
        y = 5.5
    }
    minetest.set_node(target_pos, {name = "default:coral_orange"})

    -- Disable HUD elements
    player:hud_set_flags({
        hotbar = false,
        crosshair = false,
        healthbar = false,
    })

    -- Reset the distance record
    old_distance = nil
end

-- Called once when the player joins
minetest.register_on_joinplayer(function(player, last_login)
    reset_environment()
end)

minetest.register_globalstep(function(dtime)
    -- Keep the world at midday
    minetest.set_timeofday(0.5)

    local player = minetest.get_connected_players()[1]
    if not player then return end

    -- Check if Python side wants a reset
    if get_soft_reset() == 1 then
        reset_environment()
        reset_termination()
    end

    -- Calculate new distance (linear, not squared)
    local player_pos = player:get_pos()
    local dx = target_pos.x - player_pos.x
    local dz = target_pos.z - player_pos.z
    local new_distance = math.sqrt(dx*dx + dz*dz)

    -- Sanity check
    if not new_distance or new_distance ~= new_distance then
        set_reward(-100)  -- punish hard if something breaks
        set_termination()
        return
    end

    -- First-time setup
    if not old_distance then
        old_distance = new_distance
    end

    -- Shaping reward parameters
    local step_penalty = 0.01
    local distance_bonus_scale = 1.0
    local success_threshold = 2.0  -- lowered since this is linear distance
    local success_reward = 10.0

    if new_distance < success_threshold then
        set_reward(success_reward)
        set_termination()
    else
        -- distance improvement (clamped)
        local distance_improvement = old_distance - new_distance
        distance_improvement = math.max(-1, math.min(1, distance_improvement))

        local reward = distance_bonus_scale * distance_improvement - step_penalty
        set_reward(reward)
    end

    old_distance = new_distance
end)
