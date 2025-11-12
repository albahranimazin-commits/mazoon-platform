"""
Mazoon Platform - Sample API
مزون - نموذج واجهة برمجية

This is a simple Flask API demonstrating how to interact with the Mazoon database.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE = 'mazoon.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    """Convert database row to dictionary"""
    return {key: row[key] for key in row.keys()}

# ============================================
# NEWS ENDPOINTS
# ============================================

@app.route('/api/news', methods=['GET'])
def get_news():
    """Get all news articles"""
    conn = get_db()
    cursor = conn.cursor()
    
    category = request.args.get('category')
    limit = request.args.get('limit', 10, type=int)
    
    query = """
        SELECT a.*, c.name_ar as category_name
        FROM news_articles a
        JOIN news_categories c ON a.category_id = c.id
        WHERE a.is_published = 1
    """
    
    if category:
        query += f" AND c.slug = '{category}'"
    
    query += " ORDER BY a.published_at DESC LIMIT ?"
    
    cursor.execute(query, (limit,))
    articles = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'data': articles,
        'count': len(articles)
    })

@app.route('/api/news/<slug>', methods=['GET'])
def get_news_article(slug):
    """Get single news article"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT a.*, c.name_ar as category_name
        FROM news_articles a
        JOIN news_categories c ON a.category_id = c.id
        WHERE a.slug = ? AND a.is_published = 1
    """, (slug,))
    
    article = cursor.fetchone()
    
    if article:
        # Increment views
        cursor.execute("""
            UPDATE news_articles 
            SET views_count = views_count + 1 
            WHERE slug = ?
        """, (slug,))
        conn.commit()
        
        result = dict_from_row(article)
    else:
        result = None
    
    conn.close()
    
    if result:
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'error': 'Article not found'}), 404

@app.route('/api/news/categories', methods=['GET'])
def get_news_categories():
    """Get all news categories"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM news_categories 
        WHERE is_active = 1 
        ORDER BY display_order
    """)
    
    categories = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'success': True, 'data': categories})

# ============================================
# EVENTS ENDPOINTS
# ============================================

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    conn = get_db()
    cursor = conn.cursor()
    
    upcoming = request.args.get('upcoming', 'true').lower() == 'true'
    category = request.args.get('category')
    limit = request.args.get('limit', 10, type=int)
    
    query = """
        SELECT e.*, c.name_ar as category_name
        FROM events e
        JOIN event_categories c ON e.category_id = c.id
        WHERE e.is_published = 1
    """
    
    if upcoming:
        query += " AND e.start_date > datetime('now')"
    
    if category:
        query += f" AND c.slug = '{category}'"
    
    query += " ORDER BY e.start_date ASC LIMIT ?"
    
    cursor.execute(query, (limit,))
    events = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'data': events,
        'count': len(events)
    })

@app.route('/api/events/<slug>', methods=['GET'])
def get_event(slug):
    """Get single event"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.*, c.name_ar as category_name
        FROM events e
        JOIN event_categories c ON e.category_id = c.id
        WHERE e.slug = ? AND e.is_published = 1
    """, (slug,))
    
    event = cursor.fetchone()
    conn.close()
    
    if event:
        return jsonify({'success': True, 'data': dict_from_row(event)})
    else:
        return jsonify({'success': False, 'error': 'Event not found'}), 404

# ============================================
# JOBS ENDPOINTS
# ============================================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs"""
    conn = get_db()
    cursor = conn.cursor()
    
    category = request.args.get('category')
    employment_type = request.args.get('type')
    limit = request.args.get('limit', 10, type=int)
    
    query = """
        SELECT j.*, c.name as company_name, cat.name_ar as category_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        JOIN job_categories cat ON j.category_id = cat.id
        WHERE j.is_active = 1
    """
    
    if category:
        query += f" AND cat.slug = '{category}'"
    
    if employment_type:
        query += f" AND j.employment_type = '{employment_type}'"
    
    query += " ORDER BY j.posted_at DESC LIMIT ?"
    
    cursor.execute(query, (limit,))
    jobs = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'data': jobs,
        'count': len(jobs)
    })

@app.route('/api/jobs/<slug>', methods=['GET'])
def get_job(slug):
    """Get single job"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT j.*, c.name as company_name, c.logo_url, c.website,
               cat.name_ar as category_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.id
        JOIN job_categories cat ON j.category_id = cat.id
        WHERE j.slug = ? AND j.is_active = 1
    """, (slug,))
    
    job = cursor.fetchone()
    
    if job:
        # Increment views
        cursor.execute("""
            UPDATE jobs 
            SET views_count = views_count + 1 
            WHERE slug = ?
        """, (slug,))
        conn.commit()
        
        result = dict_from_row(job)
    else:
        result = None
    
    conn.close()
    
    if result:
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'error': 'Job not found'}), 404

# ============================================
# TOURISM ENDPOINTS
# ============================================

@app.route('/api/tourism/places', methods=['GET'])
def get_tourism_places():
    """Get tourism places"""
    conn = get_db()
    cursor = conn.cursor()
    
    category = request.args.get('category')
    governorate = request.args.get('governorate')
    limit = request.args.get('limit', 10, type=int)
    
    query = """
        SELECT p.*, c.name_ar as category_name
        FROM tourism_places p
        JOIN tourism_categories c ON p.category_id = c.id
        WHERE p.is_active = 1
    """
    
    if category:
        query += f" AND c.slug = '{category}'"
    
    if governorate:
        query += f" AND p.governorate = '{governorate}'"
    
    query += " ORDER BY p.rating DESC, p.reviews_count DESC LIMIT ?"
    
    cursor.execute(query, (limit,))
    places = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'data': places,
        'count': len(places)
    })

@app.route('/api/tourism/places/<slug>', methods=['GET'])
def get_tourism_place(slug):
    """Get single tourism place"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, c.name_ar as category_name
        FROM tourism_places p
        JOIN tourism_categories c ON p.category_id = c.id
        WHERE p.slug = ? AND p.is_active = 1
    """, (slug,))
    
    place = cursor.fetchone()
    
    if place:
        # Increment views
        cursor.execute("""
            UPDATE tourism_places 
            SET views_count = views_count + 1 
            WHERE slug = ?
        """, (slug,))
        conn.commit()
        
        result = dict_from_row(place)
    else:
        result = None
    
    conn.close()
    
    if result:
        return jsonify({'success': True, 'data': result})
    else:
        return jsonify({'success': False, 'error': 'Place not found'}), 404

# ============================================
# RECIPES ENDPOINTS
# ============================================

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get recipes"""
    conn = get_db()
    cursor = conn.cursor()
    
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    limit = request.args.get('limit', 10, type=int)
    
    query = """
        SELECT r.*, c.name_ar as category_name
        FROM recipes r
        JOIN recipe_categories c ON r.category_id = c.id
        WHERE r.is_published = 1
    """
    
    if category:
        query += f" AND c.slug = '{category}'"
    
    if difficulty:
        query += f" AND r.difficulty = '{difficulty}'"
    
    query += " ORDER BY r.rating DESC, r.created_at DESC LIMIT ?"
    
    cursor.execute(query, (limit,))
    recipes = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'data': recipes,
        'count': len(recipes)
    })

# ============================================
# BUSINESSES ENDPOINTS
# ============================================

@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    """Get businesses"""
    conn = get_db()
    cursor = conn.cursor()
    
    category = request.args.get('category')
    city = request.args.get('city')
    limit = request.args.get('limit', 10, type=int)
    
    query = """
        SELECT b.*, c.name_ar as category_name
        FROM businesses b
        JOIN business_categories c ON b.category_id = c.id
        WHERE b.is_active = 1
    """
    
    if category:
        query += f" AND c.slug = '{category}'"
    
    if city:
        query += f" AND b.city = '{city}'"
    
    query += " ORDER BY b.rating DESC, b.is_featured DESC LIMIT ?"
    
    cursor.execute(query, (limit,))
    businesses = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'success': True,
        'data': businesses,
        'count': len(businesses)
    })

# ============================================
# WEATHER ENDPOINTS
# ============================================

@app.route('/api/weather/locations', methods=['GET'])
def get_weather_locations():
    """Get weather locations"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM weather_locations ORDER BY is_default DESC, city_ar")
    locations = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'success': True, 'data': locations})

# ============================================
# SEARCH ENDPOINT
# ============================================

@app.route('/api/search', methods=['GET'])
def search():
    """Global search across content"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    
    if not query:
        return jsonify({'success': False, 'error': 'Query parameter required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    results = {
        'news': [],
        'events': [],
        'jobs': [],
        'places': [],
        'recipes': [],
        'businesses': []
    }
    
    # Search news
    cursor.execute("""
        SELECT id, title_ar, slug, 'news' as type
        FROM news_articles
        WHERE title_ar LIKE ? OR content_ar LIKE ?
        AND is_published = 1
        LIMIT ?
    """, (f'%{query}%', f'%{query}%', limit))
    results['news'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Search events
    cursor.execute("""
        SELECT id, title_ar, slug, 'event' as type
        FROM events
        WHERE title_ar LIKE ? OR description_ar LIKE ?
        AND is_published = 1
        LIMIT ?
    """, (f'%{query}%', f'%{query}%', limit))
    results['events'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Search jobs
    cursor.execute("""
        SELECT id, title_ar, slug, 'job' as type
        FROM jobs
        WHERE title_ar LIKE ? OR description_ar LIKE ?
        AND is_active = 1
        LIMIT ?
    """, (f'%{query}%', f'%{query}%', limit))
    results['jobs'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({'success': True, 'data': results})

# ============================================
# MAIN
# ============================================

@app.route('/')
def index():
    """API root"""
    return jsonify({
        'name': 'Mazoon API - مزون',
        'version': '1.0.0',
        'description': 'A platform for every Omani - منصة لكل عماني',
        'endpoints': {
            'news': '/api/news',
            'events': '/api/events',
            'jobs': '/api/jobs',
            'tourism': '/api/tourism/places',
            'recipes': '/api/recipes',
            'businesses': '/api/businesses',
            'weather': '/api/weather/locations',
            'search': '/api/search?q=query'
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("مزون - واجهة برمجية")
    print("Mazoon Platform API")
    print("=" * 60)
    print()
    print("Server starting on http://localhost:5000")
    print()
    print("Available endpoints:")
    print("  • http://localhost:5000/api/news")
    print("  • http://localhost:5000/api/events")
    print("  • http://localhost:5000/api/jobs")
    print("  • http://localhost:5000/api/tourism/places")
    print("  • http://localhost:5000/api/recipes")
    print("  • http://localhost:5000/api/businesses")
    print("  • http://localhost:5000/api/search?q=مسقط")
    print()
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
