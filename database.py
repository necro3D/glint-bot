import sqlite3


#------------make all tables------------

def initialize_db():
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guilds (
            guild_id INTEGER PRIMARY KEY,
            guild_name TEXT,
            setup_complete INTEGER DEFAULT 0,
            admin_role_id INTEGER,
            admin_role_auto_created INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_modules (
            guild_id INTEGER,
            module_name TEXT,
            PRIMARY KEY (guild_id, module_name)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_moderation (
            guild_id INTEGER PRIMARY KEY,
            unspoiler_keywords TEXT DEFAULT '[]'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guild_counters (
            guild_id INTEGER PRIMARY KEY,
            channel_id INTEGER,
            api_endpoint TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            guild_id INTEGER,
            user_id INTEGER,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            PRIMARY KEY (guild_id, user_id)
        )
    """)
    
    conn.commit()
    conn.close()
    


#------------add all callable functions------------
def add_guild(guild_id, guild_name):
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO guilds (guild_id, guild_name) VALUES (?, ?)", (guild_id, guild_name))
    conn.commit()
    conn.close()
    
def set_admin_role(guild_id, role_id):
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE guilds SET admin_role_id = ? WHERE guild_id = ?", (role_id, guild_id))
    conn.commit()
    conn.close()

def complete_setup(guild_id):
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE guilds SET setup_complete = 1 WHERE guild_id = ?", (guild_id,))
    conn.commit()
    conn.close()

def set_modules(guild_id, modules):
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    for module in modules:
        cursor.execute("INSERT OR IGNORE INTO guild_modules (guild_id, module_name) VALUES (?, ?)", (guild_id, module))
    conn.commit()
    conn.close()
    
def get_guild(guild_id):
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_modules(guild_id):
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM guild_modules WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def reset_guild_setup(guild_id):
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE guilds SET admin_role_id = NULL, admin_role_auto_created = 0 WHERE guild_id = ?", (guild_id,))
    cursor.execute("DELETE FROM guild_modules WHERE guild_id = ?", (guild_id,))
    conn.commit()
    conn.close()

def set_role_autocreated(guild_id):
    conn = sqlite3.connect('glint.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE guilds SET admin_role_auto_created = 1 WHERE guild_id = ?", (guild_id,))
    conn.commit()
    conn.close()


