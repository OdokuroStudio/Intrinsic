// actions.js
const Vec3 = require('vec3').Vec3
const {
  pathfinder,
  Movements,
  goals: { GoalFollow, GoalBlock }
} = require('mineflayer-pathfinder')

async function handleAction(bot, type, actionData) {
  switch (type) {
    case "MOVE_FORWARD":
      bot.setControlState('forward', true)
      break
    case "STOP_FORWARD":
      bot.setControlState('forward', false)
      break
    case "MOVE_BACK":
      bot.setControlState('back', true)
      break
    case "STOP_BACK":
      bot.setControlState('back', false)
      break
    case "JUMP":
      bot.setControlState('jump', true)
      setTimeout(() => bot.setControlState('jump', false), 300)
      break
    case "LOOK_AT":
      {
        const { x, y, z } = actionData.pos || {}
        if (x !== undefined && y !== undefined && z !== undefined) {
          bot.lookAt(new Vec3(x, y, z))
        }
      }
      break
    case "BREAK_BLOCK":
      {
        const blockToBreak = bot.blockAt(bot.entity.position.offset(0, -1, 0))
        if (!blockToBreak || blockToBreak.name === "air") {
          console.error('No block to break or target is air.')
          return
        }
        try {
          await bot.dig(blockToBreak)
          console.log("Block broken successfully.")
        } catch (error) {
          console.error(`Failed to break block: ${error.message}`)
        }
      }
      break
    case "PLACE_BLOCK":
      {
        try {
          const targetPosition = bot.entity.position.offset(0, -1, 0)
          const referenceBlock = bot.blockAt(targetPosition)
          if (!referenceBlock) {
            console.error("No valid reference block to place against.")
            return
          }
          const itemToPlace = bot.inventory.items().find(item => item.name === "dirt")
          if (!itemToPlace) {
            console.error("No dirt in inventory to place.")
            return
          }
          await bot.equip(itemToPlace, "hand")
          await bot.placeBlock(referenceBlock, new Vec3(0, 1, 0))
          console.log("Block placed successfully.")
        } catch (error) {
          console.error(`Failed to place block: ${error.message}`)
        }
      }
      break
    case "ATTACK":
      {
        const entity = bot.nearestEntity()
        if (entity) {
          // Skip attacking friendly bots
          if (entity.type === 'player' && entity.username?.startsWith('Bot_')) {
            console.log(`Skipping attack on ${entity.username} (it's a friendly bot).`)
            break
          }
          bot.attack(entity)
        }
      }
      break
    case "PICKUP_ITEM":
      bot.activateItem()
      break
    case "USE_ITEM":
      bot.activateItem()
      break
    case "TURN_LEFT":
      bot.look(bot.entity.yaw - Math.PI / 8, bot.entity.pitch, true)
      break
    case "TURN_RIGHT":
      bot.look(bot.entity.yaw + Math.PI / 8, bot.entity.pitch, true)
      break
    case "STRAFE_LEFT":
      bot.setControlState('left', true)
      break
    case "STRAFE_RIGHT":
      bot.setControlState('right', true)
      break
    case "DROP_ITEM":
      if (bot.heldItem) {
        try {
          await bot.tossStack(bot.heldItem)
          console.log("Dropped the held item.")
        } catch (err) {
          console.error(`Failed to drop item: ${err.message}`)
        }
      } else {
        console.error("No item held to drop.")
      }
      break
    case "DROP_ALL":
      {
        for (const item of bot.inventory.items()) {
          try {
            // eslint-disable-next-line no-await-in-loop
            await bot.tossStack(item)
          } catch (err) {
            console.error(`Failed to drop item: ${err.message}`)
          }
        }
        console.log("Dropped all items.")
      }
      break
    case "SWAP_HANDS":
      bot.activateItem(true)
      console.log("Swapped hands.")
      break
    case "CRAFT":
      console.error("CRAFT action not implemented.")
      break
    case "PLACE_LADDER":
      console.error("PLACE_LADDER action not implemented.")
      break
    case "INTERACT_ENTITY":
      {
        const targetEntity = bot.nearestEntity()
        if (targetEntity) {
          bot.activateEntity(targetEntity)
          console.log(`Interacted with entity: ${targetEntity.name}`)
        } else {
          console.error("No entity nearby to interact with.")
        }
      }
      break
    case "USE_DOOR":
      {
        const door = bot.blockAtCursor()
        if (door && door.name.includes("door")) {
          bot.activateBlock(door)
          console.log("Used door.")
        } else {
          console.error("No door to use.")
        }
      }
      break
    case "ACTIVATE_LEVER":
      {
        const lever = bot.blockAtCursor()
        if (lever && lever.name.includes("lever")) {
          bot.activateBlock(lever)
          console.log("Activated lever.")
        } else {
          console.error("No lever to activate.")
        }
      }
      break
    case "COLLECT_ITEM":
      {
        const nearbyItem = bot.nearestEntity(entity => entity.kind === 'Drops')
        if (nearbyItem) {
          bot.pathfinder.setGoal(new GoalFollow(nearbyItem, 1))
          console.log("Moving to collect item.")
        } else {
          console.error("No item nearby to collect.")
        }
      }
      break
    case "SHOOT_BOW":
      console.error("SHOOT_BOW action not implemented.")
      break
    case "BLOCK_WITH_SHIELD":
      bot.setControlState('sneak', true)
      console.log("Blocking with shield.")
      break
    case "CHASE_ENTITY":
      {
        const targetToChase = bot.nearestEntity()
        if (targetToChase) {
          bot.pathfinder.setGoal(new GoalFollow(targetToChase, 1))
          console.log("Chasing entity.")
        } else {
          console.error("No entity nearby to chase.")
        }
      }
      break
    case "NAVIGATE_TO":
      {
        const { target } = actionData
        if (target && target.x !== undefined && target.y !== undefined && target.z !== undefined) {
          bot.pathfinder.setGoal(new GoalBlock(target.x, target.y, target.z))
          console.log(`Navigating to position: (${target.x}, ${target.y}, ${target.z})`)
        } else {
          console.error("Invalid target position for NAVIGATE_TO.")
        }
      }
      break
    case "CLIMB":
      bot.setControlState('jump', true)
      bot.setControlState('forward', true)
      console.log("Climbing.")
      break
    case "FIND_BLOCK":
      console.error("FIND_BLOCK action not implemented.")
      break
    case "EAT":
      {
        const food = bot.inventory.items().find(item => item.name === "bread")
        if (food) {
          try {
            await bot.equip(food, "hand")
            await bot.consume()
            console.log("Ate food.")
          } catch (err) {
            console.error(`Failed to eat: ${err.message}`)
          }
        } else {
          console.error("No food available to eat.")
        }
      }
      break
    case "SLEEP":
      {
        const bed = bot.findBlock({
          matching: block => block.name.includes('bed'),
          maxDistance: 5,
        })
        if (bed) {
          try {
            await bot.sleep(bed)
            console.log("Bot is now sleeping.")
          } catch (err) {
            console.error(`Failed to sleep: ${err.message}`)
          }
        } else {
          console.error("No bed found nearby to sleep.")
        }
      }
      break
    case "RESPAWN":
      console.log("Bot respawning.")
      break
    case "USE_FURNACE":
      console.error("USE_FURNACE action not implemented.")
      break
    case "USE_CHEST":
      console.error("USE_CHEST action not implemented.")
      break
    default:
      console.log(`Unknown command: ${type}`)
  }
}

module.exports = { handleAction }
