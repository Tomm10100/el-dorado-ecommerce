"""
Initialize the InnovLead Bot Database
Creates all tables
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from database.models import Base
from config import get_settings

def main():
    print("="*70)
    print("InnovLead Education Bot - Database Initialization")
    print("="*70)
    
    try:
        settings = get_settings()
        print(f"\n[1/2] Connecting to database: {settings.database_url}")
        
        # Create engine
        engine = create_engine(settings.database_url, echo=False)
        
        # Create all tables
        print("[2/2] Creating database tables...")
        Base.metadata.create_all(engine)
        print("  -> Tables created successfully!")
        
        print("\n" + "="*70)
        print("[SUCCESS] Database initialized and ready to use!")
        print("="*70)
        print("\nThe bot will create modules and lessons on first run.")
        print("Now restart the bot to test it!")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to initialize database: {e}")
        print("Make sure your .env file is configured correctly")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
