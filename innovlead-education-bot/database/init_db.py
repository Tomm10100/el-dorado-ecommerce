"""
Database initialization script
Run this to create all tables and seed initial data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import init_db

if __name__ == '__main__':
    print("🚀 Initializing InnovLead Education Bot Database...")
    init_db()
    print("✅ Database setup complete!")
