// rewards.js
function onSpawn(bot) {
  // Initialize the bot's reward or other properties here
  bot._currentReward = 0
  bot._lastPosition = bot.entity.position.clone()
  bot._lastHealth = bot.health
}

function onMove(bot) {
  if (!bot._lastPosition) return
  const currPos = bot.entity.position
  if (!currPos.equals(bot._lastPosition)) {
    bot._currentReward += 0.05
    bot._lastPosition = currPos.clone()
  }
}

function onDiggingCompleted(bot, block) {
  if (block.name === 'diamond_ore') {
    bot._currentReward += 1.0
  } else {
    bot._currentReward += 0.2
  }
}

function onHealth(bot) {
  // If the bot took damage
  if (bot._lastHealth !== null && bot.health < bot._lastHealth) {
    bot._currentReward -= 0.5
  }
  bot._lastHealth = bot.health
}

function onIdle(bot) {
  bot._currentReward -= 0.1
}

function onItemCollected(bot) {
  bot._currentReward += 0.3
}

function onDeath(bot) {
  bot._currentReward -= 2.0
}

// Utility function for retrieving and resetting the reward:
function getAndResetReward(bot) {
  const r = bot._currentReward
  bot._currentReward = 0
  return r
}

module.exports = {
  onSpawn,
  onMove,
  onDiggingCompleted,
  onHealth,
  onIdle,
  onItemCollected,
  onDeath,
  getAndResetReward
}
