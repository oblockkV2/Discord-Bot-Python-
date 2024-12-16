@echo off
REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the bot script
echo Starting the bot...
python bot.py

pause
