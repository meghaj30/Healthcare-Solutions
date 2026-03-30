#!/usr/bin/env python3
"""
Database migration script to add video consultation fields to appointments table
"""

import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Add video consultation fields to the appointments table"""
    
    db_path = 'hospital.db'
    
    if not os.path.exists(db_path):
        print("Database not found. Creating new database...")
        from app import app, db
        with app.app_context():
            db.create_all()
        print("Database created successfully!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if consultation_type column exists
        cursor.execute("PRAGMA table_info(appointments)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add missing columns if they don't exist
        if 'consultation_type' not in columns:
            cursor.execute("""
                ALTER TABLE appointments 
                ADD COLUMN consultation_type VARCHAR(20) DEFAULT 'In-Person'
            """)
            print("Added consultation_type column")
        
        if 'video_room_id' not in columns:
            cursor.execute("""
                ALTER TABLE appointments 
                ADD COLUMN video_room_id VARCHAR(100)
            """)
            print("Added video_room_id column")
        
        if 'video_link' not in columns:
            cursor.execute("""
                ALTER TABLE appointments 
                ADD COLUMN video_link VARCHAR(500)
            """)
            print("Added video_link column")
        
        if 'video_enabled' not in columns:
            cursor.execute("""
                ALTER TABLE appointments 
                ADD COLUMN video_enabled VARCHAR(10) DEFAULT 'false'
            """)
            print("Added video_enabled column")
        
        conn.commit()
        conn.close()
        
        print("Database migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        if conn:
            conn.close()

if __name__ == '__main__':
    migrate_database()
