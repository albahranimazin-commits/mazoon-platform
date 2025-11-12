import sqlite3

def verify_database():
    """Verify the database structure and show sample data"""
    
    conn = sqlite3.connect('mazoon.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("مزون - استعراض قاعدة البيانات")
    print("Mazoon - Database Explorer")
    print("=" * 60)
    print()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    tables = cursor.fetchall()
    
    print(f"📊 Total Tables: {len(tables)}")
    print("-" * 60)
    print()
    
    # Show table names with row counts
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"✓ {table_name:.<40} {count:>5} rows")
    
    print()
    print("=" * 60)
    print("Sample Data Preview")
    print("=" * 60)
    print()
    
    # Show sample news
    print("📰 NEWS ARTICLES:")
    print("-" * 60)
    cursor.execute("""
        SELECT a.title_ar, c.name_ar, a.published_at
        FROM news_articles a
        JOIN news_categories c ON a.category_id = c.id
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"  • {row[0]}")
        print(f"    Category: {row[1]} | Published: {row[2]}")
        print()
    
    # Show sample events
    print("📅 EVENTS:")
    print("-" * 60)
    cursor.execute("""
        SELECT title_ar, venue, start_date
        FROM events
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"  • {row[0]}")
        print(f"    Venue: {row[1]} | Date: {row[2]}")
        print()
    
    # Show sample jobs
    print("💼 JOBS:")
    print("-" * 60)
    cursor.execute("""
        SELECT j.title_ar, c.name, j.employment_type
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"  • {row[0]}")
        print(f"    Company: {row[1]} | Type: {row[2]}")
        print()
    
    # Show tourism places
    print("🏖️ TOURISM PLACES:")
    print("-" * 60)
    cursor.execute("""
        SELECT p.name_ar, c.name_ar, p.city
        FROM tourism_places p
        JOIN tourism_categories c ON p.category_id = c.id
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"  • {row[0]}")
        print(f"    Category: {row[1]} | City: {row[2]}")
        print()
    
    # Show recipes
    print("👨‍🍳 RECIPES:")
    print("-" * 60)
    cursor.execute("""
        SELECT r.title_ar, c.name_ar, r.difficulty
        FROM recipes r
        JOIN recipe_categories c ON r.category_id = c.id
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"  • {row[0]}")
        print(f"    Category: {row[1]} | Difficulty: {row[2]}")
        print()
    
    # Show weather locations
    print("🌤️ WEATHER LOCATIONS:")
    print("-" * 60)
    cursor.execute("""
        SELECT city_ar, governorate_ar
        FROM weather_locations
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  • {row[0]} ({row[1]})")
    print()
    
    print("=" * 60)
    print("Database Statistics")
    print("=" * 60)
    print()
    
    # Count categories
    stats = {
        'News Categories': 'news_categories',
        'Event Categories': 'event_categories',
        'Job Categories': 'job_categories',
        'Tourism Categories': 'tourism_categories',
        'Recipe Categories': 'recipe_categories',
        'Marketplace Categories': 'marketplace_categories',
        'Business Categories': 'business_categories',
        'Forum Categories': 'forum_categories'
    }
    
    for name, table in stats.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{name:.<40} {count:>5}")
    
    conn.close()
    
    print()
    print("=" * 60)
    print("✅ Database verification complete!")
    print("=" * 60)

if __name__ == '__main__':
    verify_database()
