// bot.js
const mineflayer = require('mineflayer')
const WebSocket = require('ws')
const Vec3 = require('vec3').Vec3
const {
  pathfinder,
  Movements,
  goals: { GoalFollow, GoalBlock }
} = require('mineflayer-pathfinder')

const rewards = require('./rewards')
const { handleAction } = require('./actions')  // <-- Import our handleAction function

const BOT_COUNT = 6
const bots = []
const ws = new WebSocket.Server({ port: 3000 })
console.log("WebSocket server started on port 3000")

function createBot(username) {
  const bot = mineflayer.createBot({
    host: 'localhost',
    port: 25565,
    username: username
  })

  bot.loadPlugin(pathfinder)

  bot.on('spawn', () => {
    console.log(`${username} has spawned in the world`)

    const defaultMovements = new Movements(bot, bot.world)
    bot.pathfinder.setMovements(defaultMovements)

    // Initialize for rewards
    rewards.onSpawn(bot)
  })

  bot.on('move', () => rewards.onMove(bot))

  bot.on('diggingCompleted', (block) => rewards.onDiggingCompleted(bot, block))

  bot.on('health', () => rewards.onHealth(bot))

  bot.on('consume', (foodItem) => {
    if (foodItem?.name) {
      rewards.onEat(bot, foodItem.name)
    }
  })

  setInterval(() => rewards.onIdle(bot), 5000)
  bot.on('playerCollect', (collector, itemDrop) => {
    if (collector.username === bot.username) rewards.onItemCollected(bot)
  })
  bot.on('death', () => rewards.onDeath(bot))

  bot.getAndResetReward = () => rewards.getAndResetReward(bot)

  bot.on('kicked', (reason) => console.log(`${username} was kicked: ${reason}`))
  bot.on('error', (err) => console.log(`${username} encountered an error: ${err}`))

  return bot
}

for (let i = 0; i < BOT_COUNT; i++) {
  bots.push(createBot(`Bot_${i}`))
}

ws.on('connection', (socket) => {
  console.log('WebSocket connection established')

  // Listen for action commands from Python server
  socket.on('message', async (data) => {
    try {
      const message = JSON.parse(data)
      const { botId, type, data: actionData } = message

      if (botId < 0 || botId >= bots.length) {
        console.log(`Invalid botId: ${botId}`)
        return
      }

      const bot = bots[botId]
      await handleAction(bot, type, actionData)  // <-- The call to actions.js
    } catch (err) {
      console.error(`Error handling action: ${err.message}`)
    }
  })

  // Send bot state + reward to Python
  setInterval(() => {
    bots.forEach((bot, botId) => {
      if (socket.readyState === WebSocket.OPEN) {
        const surroundings = bot.findBlocks({
          matching: block => block.name !== 'air',
          maxDistance: 10,
          count: 5
        }).map(coord => {
          const b = bot.blockAt(coord)
          return {
            x: coord.x,
            y: coord.y,
            z: coord.z,
            name: b?.name
          }
        })

        const state = {
          botId: botId,
          position: {
            x: bot.entity.position.x,
            y: bot.entity.position.y,
            z: bot.entity.position.z
          },
          yaw: bot.entity.yaw,
          pitch: bot.entity.pitch,
          health: bot.health,
          food: bot.food,
          surroundings: surroundings,
          velocity: {
            x: bot.entity.velocity.x,
            y: bot.entity.velocity.y,
            z: bot.entity.velocity.z
          },
          reward: bot.getAndResetReward()
        }

        socket.send(JSON.stringify(state))
      }
    })
  }, 100)
})
