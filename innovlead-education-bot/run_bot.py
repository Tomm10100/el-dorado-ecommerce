"""
Simple launcher for InnovLead Education Bot
Run this file to start the bot
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Change to bot directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import and run the bot
from bot.main import main

if __name__ == '__main__':
    print("Starting InnovLead Education Bot...")
    print("=" * 70)
    main()
