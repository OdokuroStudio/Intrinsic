@echo off
echo Starting bot.js...
start cmd /k "cd minecraft_bot && node bot.js"
echo Starting main.py...
start cmd /k "python agent.py"