#!/usr/bin/env python3
"""
Fix database schema by adding missing video consultation columns
"""

import sqlite3
import os

def fix_database_schema():
    """Add missing video consultation columns to appointments table"""
    
    db_path = 'hospital.db'
    
    if not os.path.exists(db_path):
        print("Database not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current table structure
        cursor.execute("PRAGMA table_info(appointments)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"Current columns: {columns}")
        
        # Add missing columns
        columns_to_add = [
            ('consultation_type', 'VARCHAR(20) DEFAULT "In-Person"'),
            ('video_room_id', 'VARCHAR(100)'),
            ('video_link', 'VARCHAR(500)'),
            ('video_enabled', 'VARCHAR(10) DEFAULT "false"')
        ]
        
        for column_name, column_def in columns_to_add:
            if column_name not in columns:
                try:
                    sql = f'ALTER TABLE appointments ADD COLUMN {column_name} {column_def}'
                    cursor.execute(sql)
                    print(f"✅ Added column: {column_name}")
                except Exception as e:
                    print(f"❌ Error adding {column_name}: {e}")
            else:
                print(f"✅ Column already exists: {column_name}")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Database schema fixed successfully!")
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")

if __name__ == '__main__':
    fix_database_schema()
