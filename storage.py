"""
Local storage manager using SQLite
Handles API keys and content history
"""

import sqlite3
import json
from datetime import datetime
import os


class StorageManager:
    """Manages local SQLite database for app data"""
    
    def __init__(self):
        self.db_path = self._get_db_path()
        self._init_database()
    
    def _get_db_path(self):
        """Get database path (app data directory on Android)"""
        try:
            # Try to use Android app data directory
            from android.storage import app_storage_path
            db_dir = app_storage_path()
        except ImportError:
            # Fallback for development on desktop
            db_dir = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(db_dir, 'ai_content_generator.db')
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # API keys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                provider TEXT PRIMARY KEY,
                api_key TEXT NOT NULL
            )
        ''')
        
        # Content history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                content TEXT NOT NULL,
                platform TEXT,
                tone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_api_keys(self, keys):
        """Save API keys to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for provider, key in keys.items():
            if key:  # Only save non-empty keys
                cursor.execute('''
                    INSERT OR REPLACE INTO api_keys (provider, api_key)
                    VALUES (?, ?)
                ''', (provider, key))
        
        conn.commit()
        conn.close()
    
    def get_api_keys(self):
        """Retrieve all API keys"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT provider, api_key FROM api_keys')
        rows = cursor.fetchall()
        conn.close()
        
        return {provider: key for provider, key in rows}
    
    def save_post(self, prompt, content, platform, tone):
        """Save generated content to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO content_history (prompt, content, platform, tone)
            VALUES (?, ?, ?, ?)
        ''', (prompt, content, platform, tone))
        
        conn.commit()
        conn.close()
    
    def get_history(self, limit=50):
        """Retrieve content history"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM content_history
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def clear_history(self):
        """Clear all content history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM content_history')
        conn.commit()
        conn.close()
