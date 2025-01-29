// rewards.js

// 1) Some config object for item-based rewards:
const itemRewards = {
  diamond_ore: { baseReward: 1.0, craftingValue: 2.0 },
  iron_ore: { baseReward: 0.5, craftingValue: 1.5 },
  cobblestone: { baseReward: 0.1, craftingValue: 0.5 },
  beef: { baseReward: 0.8, craftingValue: 0.8 },
  bread: { baseReward: 0.8, craftingValue: 0.6 },
}

// 2) Initialization on spawn
function onSpawn(bot) {
  bot._currentReward = 0
  bot._lastPosition = bot.entity.position.clone()
  bot._lastHealth = bot.health
  bot._collectedCount = {}   // Track how many times we've collected items
}

// 3) Simple movement-based reward
function onMove(bot) {
  if (!bot._lastPosition) return
  const currPos = bot.entity.position
  if (!currPos.equals(bot._lastPosition)) {
    bot._currentReward += Math.abs(currPos.x - bot._lastPosition.x) + Math.abs(currPos.z - bot._lastPosition.z)
    console.log(Math.abs(currPos.x - bot._lastPosition.x) + Math.abs(currPos.z - bot._lastPosition.z))
    bot._lastPosition = currPos.clone()
  }
}

// 4) Breaking blocks
function onDiggingCompleted(bot, block) {
  const blockName = block.name
  if (!blockName || blockName === 'air') return

  const base = itemRewards[blockName]?.baseReward ?? .1
  bot._currentReward += base
  console.log(`${bot.username} broke block: ${blockName}, +${base} reward`)
}

// 5) Health damage penalty
function onHealth(bot) {
  if (bot._lastHealth !== null && bot.health < bot._lastHealth) {
    bot._currentReward -= 0.5
    console.log(`${bot.username} took damage, -0.5 reward`)
  }
  bot._lastHealth = bot.health
}

// 6) Idle penalty
function onIdle(bot) {
  bot._currentReward -= 10
  console.log(`${bot.username} idle, -10 reward`)
}

// 7) Increment count & use config for item-based reward
function onItemCollected(bot, itemName) {
  if (!bot._collectedCount[itemName]) {
    bot._collectedCount[itemName] = 0
  }
  bot._collectedCount[itemName]++

  const timesCollected = bot._collectedCount[itemName]
  const base = itemRewards[itemName]?.baseReward ?? 0.1
  const craftVal = itemRewards[itemName]?.craftingValue ?? 0.2

  const rewardForItem = base + craftVal * Math.log(timesCollected + 1)
  bot._currentReward += rewardForItem

  console.log(
    `${bot.username} collected ${itemName}, count=${timesCollected}, +${rewardForItem.toFixed(2)}`
  )
}

// 8) Death penalty
function onDeath(bot) {
  bot._currentReward -= 2.0
  console.log(`${bot.username} died, -2.0 reward`)
}

// 9) Eating event
function onEat(bot, itemName) {
  // Check if rewards are not set
  const base = itemRewards[itemName]?.baseReward ?? 0.2
  const craftVal = itemRewards[itemName]?.craftingValue ?? 0.5

  const rewardForFood = base + craftVal * 0.5
  bot._currentReward += rewardForFood

  console.log(`${bot.username} ate ${itemName}, +${rewardForFood.toFixed(2)} reward`)
}

// 10) Killing animals
function onEntityKilled(bot, entityName) {
  const animalRewards = {
    pig: 40,
    cow: 50,
    sheep: 40,
    chicken: 30,
  }
  const reward = animalRewards[entityName] || 0
  if (reward > 0) {
    bot._currentReward += reward
    console.log(`${bot.username} killed ${entityName}, +${reward} reward`)
  }
}

// 11) Reset
function getAndResetReward(bot) {
  const r = bot._currentReward
  bot._currentReward = 0
  return r
}

module.exports = {
  itemRewards,
  onSpawn,
  onMove,
  onDiggingCompleted,
  onHealth,
  onIdle,
  onItemCollected,
  onDeath,
  onEat,
  onEntityKilled,
  getAndResetReward
}
