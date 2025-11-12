"""
Mazoon Platform - Production API
مزون - واجهة برمجية للإنتاج

Full CRUD operations for all major entities
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'mazoon.db'

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    """Convert database row to dictionary"""
    return {key: row[key] for key in row.keys()}

def response_success(data=None, message="Success", status=200):
    """Standard success response"""
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    }), status

def response_error(message="Error", status=400):
    """Standard error response"""
    return jsonify({
        'success': False,
        'message': message,
        'data': None
    }), status

# ============================================
# NEWS CRUD OPERATIONS
# ============================================

@app.route('/api/news', methods=['GET'])
def get_all_news():
    """Get all news articles"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        category = request.args.get('category')
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = """
            SELECT a.*, c.name_ar as category_name, c.name_en as category_name_en
            FROM news_articles a
            JOIN news_categories c ON a.category_id = c.id
            WHERE a.is_published = 1
        """
        params = []
        
        if category:
            query += " AND c.slug = ?"
            params.append(category)
        
        query += " ORDER BY a.published_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        articles = [dict_from_row(row) for row in cursor.fetchall()]
        
        # Get total count
        count_query = "SELECT COUNT(*) FROM news_articles WHERE is_published = 1"
        if category:
            count_query += " AND category_id = (SELECT id FROM news_categories WHERE slug = ?)"
            cursor.execute(count_query, [category])
        else:
            cursor.execute(count_query)
        
        total = cursor.fetchone()[0]
        conn.close()
        
        return response_success({
            'articles': articles,
            'total': total,
            'limit': limit,
            'offset': offset
        })
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/news/<slug>', methods=['GET'])
def get_news_article(slug):
    """Get single news article"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.*, c.name_ar as category_name, c.name_en as category_name_en
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
            conn.close()
            return response_success(result)
        else:
            conn.close()
            return response_error('Article not found', 404)
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/news', methods=['POST'])
def create_news_article():
    """Create new news article"""
    try:
        data = request.get_json()
        
        required_fields = ['category_id', 'title_ar', 'slug', 'content_ar']
        for field in required_fields:
            if field not in data:
                return response_error(f'Missing required field: {field}', 400)
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO news_articles 
            (category_id, title_ar, title_en, slug, summary_ar, summary_en, 
             content_ar, content_en, image_url, is_published, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            data['category_id'],
            data['title_ar'],
            data.get('title_en'),
            data['slug'],
            data.get('summary_ar'),
            data.get('summary_en'),
            data['content_ar'],
            data.get('content_en'),
            data.get('image_url'),
            data.get('is_published', 1)
        ))
        
        article_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return response_success({'id': article_id}, 'Article created successfully', 201)
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/news/<int:article_id>', methods=['PUT'])
def update_news_article(article_id):
    """Update news article"""
    try:
        data = request.get_json()
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Build update query dynamically
        update_fields = []
        params = []
        
        allowed_fields = ['title_ar', 'title_en', 'summary_ar', 'summary_en', 
                         'content_ar', 'content_en', 'image_url', 'is_published']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = ?")
                params.append(data[field])
        
        if not update_fields:
            return response_error('No valid fields to update', 400)
        
        params.append(article_id)
        query = f"UPDATE news_articles SET {', '.join(update_fields)}, updated_at = datetime('now') WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return response_error('Article not found', 404)
        
        conn.close()
        return response_success({'id': article_id}, 'Article updated successfully')
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/news/<int:article_id>', methods=['DELETE'])
def delete_news_article(article_id):
    """Delete news article"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM news_articles WHERE id = ?", (article_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return response_error('Article not found', 404)
        
        conn.close()
        return response_success(message='Article deleted successfully')
    except Exception as e:
        return response_error(str(e), 500)

# ============================================
# NEWS CATEGORIES
# ============================================

@app.route('/api/news/categories', methods=['GET'])
def get_news_categories():
    """Get all news categories"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*, COUNT(a.id) as article_count
            FROM news_categories c
            LEFT JOIN news_articles a ON c.id = a.category_id AND a.is_published = 1
            WHERE c.is_active = 1
            GROUP BY c.id
            ORDER BY c.display_order
        """)
        
        categories = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        
        return response_success(categories)
    except Exception as e:
        return response_error(str(e), 500)

# ============================================
# EVENTS CRUD OPERATIONS
# ============================================

@app.route('/api/events', methods=['GET'])
def get_all_events():
    """Get all events"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        upcoming = request.args.get('upcoming', 'true').lower() == 'true'
        category = request.args.get('category')
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = """
            SELECT e.*, c.name_ar as category_name, c.name_en as category_name_en
            FROM events e
            JOIN event_categories c ON e.category_id = c.id
            WHERE e.is_published = 1
        """
        params = []
        
        if upcoming:
            query += " AND e.start_date > datetime('now')"
        
        if category:
            query += " AND c.slug = ?"
            params.append(category)
        
        query += " ORDER BY e.start_date ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        events = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        
        return response_success({'events': events})
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/events/<slug>', methods=['GET'])
def get_event(slug):
    """Get single event"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT e.*, c.name_ar as category_name, c.name_en as category_name_en
            FROM events e
            JOIN event_categories c ON e.category_id = c.id
            WHERE e.slug = ? AND e.is_published = 1
        """, (slug,))
        
        event = cursor.fetchone()
        conn.close()
        
        if event:
            return response_success(dict_from_row(event))
        else:
            return response_error('Event not found', 404)
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/events', methods=['POST'])
def create_event():
    """Create new event"""
    try:
        data = request.get_json()
        
        required_fields = ['category_id', 'title_ar', 'slug', 'description_ar', 
                          'start_date', 'end_date', 'venue']
        for field in required_fields:
            if field not in data:
                return response_error(f'Missing required field: {field}', 400)
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO events 
            (category_id, title_ar, title_en, slug, description_ar, description_en,
             venue, city, governorate, start_date, end_date, organizer, is_free, is_published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['category_id'],
            data['title_ar'],
            data.get('title_en'),
            data['slug'],
            data['description_ar'],
            data.get('description_en'),
            data['venue'],
            data.get('city'),
            data.get('governorate'),
            data['start_date'],
            data['end_date'],
            data.get('organizer'),
            data.get('is_free', 1),
            data.get('is_published', 1)
        ))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return response_success({'id': event_id}, 'Event created successfully', 201)
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update event"""
    try:
        data = request.get_json()
        
        conn = get_db()
        cursor = conn.cursor()
        
        update_fields = []
        params = []
        
        allowed_fields = ['title_ar', 'title_en', 'description_ar', 'description_en',
                         'venue', 'city', 'start_date', 'end_date', 'is_published']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = ?")
                params.append(data[field])
        
        if not update_fields:
            return response_error('No valid fields to update', 400)
        
        params.append(event_id)
        query = f"UPDATE events SET {', '.join(update_fields)}, updated_at = datetime('now') WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return response_error('Event not found', 404)
        
        conn.close()
        return response_success({'id': event_id}, 'Event updated successfully')
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete event"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return response_error('Event not found', 404)
        
        conn.close()
        return response_success(message='Event deleted successfully')
    except Exception as e:
        return response_error(str(e), 500)

# ============================================
# EVENT CATEGORIES
# ============================================

@app.route('/api/events/categories', methods=['GET'])
def get_event_categories():
    """Get all event categories"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*, COUNT(e.id) as event_count
            FROM event_categories c
            LEFT JOIN events e ON c.id = e.category_id AND e.is_published = 1
            GROUP BY c.id
            ORDER BY c.name_ar
        """)
        
        categories = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        
        return response_success(categories)
    except Exception as e:
        return response_error(str(e), 500)

# ============================================
# JOBS CRUD OPERATIONS
# ============================================

@app.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    """Get all jobs"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        category = request.args.get('category')
        employment_type = request.args.get('type')
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = """
            SELECT j.*, c.name as company_name, c.logo_url as company_logo,
                   cat.name_ar as category_name, cat.name_en as category_name_en
            FROM jobs j
            JOIN companies c ON j.company_id = c.id
            JOIN job_categories cat ON j.category_id = cat.id
            WHERE j.is_active = 1
        """
        params = []
        
        if category:
            query += " AND cat.slug = ?"
            params.append(category)
        
        if employment_type:
            query += " AND j.employment_type = ?"
            params.append(employment_type)
        
        query += " ORDER BY j.posted_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        jobs = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        
        return response_success({'jobs': jobs})
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/jobs/<slug>', methods=['GET'])
def get_job(slug):
    """Get single job"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT j.*, c.name as company_name, c.logo_url, c.website, c.description as company_description,
                   cat.name_ar as category_name, cat.name_en as category_name_en
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
            conn.close()
            return response_success(result)
        else:
            conn.close()
            return response_error('Job not found', 404)
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create new job"""
    try:
        data = request.get_json()
        
        required_fields = ['category_id', 'company_id', 'title_ar', 'slug', 
                          'description_ar', 'employment_type']
        for field in required_fields:
            if field not in data:
                return response_error(f'Missing required field: {field}', 400)
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO jobs 
            (category_id, company_id, title_ar, title_en, slug, description_ar, description_en,
             requirements_ar, employment_type, location, min_salary, max_salary, is_active, posted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            data['category_id'],
            data['company_id'],
            data['title_ar'],
            data.get('title_en'),
            data['slug'],
            data['description_ar'],
            data.get('description_en'),
            data.get('requirements_ar'),
            data['employment_type'],
            data.get('location'),
            data.get('min_salary'),
            data.get('max_salary'),
            data.get('is_active', 1)
        ))
        
        job_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return response_success({'id': job_id}, 'Job created successfully', 201)
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update job"""
    try:
        data = request.get_json()
        
        conn = get_db()
        cursor = conn.cursor()
        
        update_fields = []
        params = []
        
        allowed_fields = ['title_ar', 'title_en', 'description_ar', 'description_en',
                         'requirements_ar', 'location', 'min_salary', 'max_salary', 'is_active']
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = ?")
                params.append(data[field])
        
        if not update_fields:
            return response_error('No valid fields to update', 400)
        
        params.append(job_id)
        query = f"UPDATE jobs SET {', '.join(update_fields)}, updated_at = datetime('now') WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return response_error('Job not found', 404)
        
        conn.close()
        return response_success({'id': job_id}, 'Job updated successfully')
    except Exception as e:
        return response_error(str(e), 500)

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete job"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return response_error('Job not found', 404)
        
        conn.close()
        return response_success(message='Job deleted successfully')
    except Exception as e:
        return response_error(str(e), 500)

# ============================================
# JOB CATEGORIES
# ============================================

@app.route('/api/jobs/categories', methods=['GET'])
def get_job_categories():
    """Get all job categories"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*, COUNT(j.id) as job_count
            FROM job_categories c
            LEFT JOIN jobs j ON c.id = j.category_id AND j.is_active = 1
            GROUP BY c.id
            ORDER BY c.name_ar
        """)
        
        categories = [dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        
        return response_success(categories)
    except Exception as e:
        return response_error(str(e), 500)

# ============================================
# SEARCH
# ============================================

@app.route('/api/search', methods=['GET'])
def search():
    """Global search"""
    try:
        query = request.args.get('q', '')
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return response_error('Query parameter required', 400)
        
        conn = get_db()
        cursor = conn.cursor()
        
        results = {
            'news': [],
            'events': [],
            'jobs': []
        }
        
        # Search news
        cursor.execute("""
            SELECT id, title_ar, slug, 'news' as type, published_at as date
            FROM news_articles
            WHERE (title_ar LIKE ? OR content_ar LIKE ?)
            AND is_published = 1
            ORDER BY published_at DESC
            LIMIT ?
        """, (f'%{query}%', f'%{query}%', limit))
        results['news'] = [dict_from_row(row) for row in cursor.fetchall()]
        
        # Search events
        cursor.execute("""
            SELECT id, title_ar, slug, 'event' as type, start_date as date
            FROM events
            WHERE (title_ar LIKE ? OR description_ar LIKE ?)
            AND is_published = 1
            ORDER BY start_date DESC
            LIMIT ?
        """, (f'%{query}%', f'%{query}%', limit))
        results['events'] = [dict_from_row(row) for row in cursor.fetchall()]
        
        # Search jobs
        cursor.execute("""
            SELECT id, title_ar, slug, 'job' as type, posted_at as date
            FROM jobs
            WHERE (title_ar LIKE ? OR description_ar LIKE ?)
            AND is_active = 1
            ORDER BY posted_at DESC
            LIMIT ?
        """, (f'%{query}%', f'%{query}%', limit))
        results['jobs'] = [dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        total = len(results['news']) + len(results['events']) + len(results['jobs'])
        
        return response_success({
            'results': results,
            'total': total,
            'query': query
        })
    except Exception as e:
        return response_error(str(e), 500)

# ============================================
# STATISTICS
# ============================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get platform statistics"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        stats = {}
        
        # News count
        cursor.execute("SELECT COUNT(*) FROM news_articles WHERE is_published = 1")
        stats['news_count'] = cursor.fetchone()[0]
        
        # Events count
        cursor.execute("SELECT COUNT(*) FROM events WHERE is_published = 1")
        stats['events_count'] = cursor.fetchone()[0]
        
        # Jobs count
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
        stats['jobs_count'] = cursor.fetchone()[0]
        
        # Tourism places count
        cursor.execute("SELECT COUNT(*) FROM tourism_places WHERE is_active = 1")
        stats['tourism_count'] = cursor.fetchone()[0]
        
        # Recipes count
        cursor.execute("SELECT COUNT(*) FROM recipes WHERE is_published = 1")
        stats['recipes_count'] = cursor.fetchone()[0]
        
        conn.close()
        
        return response_success(stats)
    except Exception as e:
        return response_error(str(e), 500)

# ============================================
# MAIN & ROOT
# ============================================

@app.route('/')
def index():
    """API root with HTML interface"""
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mazoon API - مزون</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 800px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 1.2em;
            }
            .status {
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
                font-weight: bold;
            }
            .endpoints {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .endpoints h2 {
                color: #667eea;
                margin-bottom: 15px;
            }
            .endpoint {
                background: white;
                padding: 12px;
                margin: 8px 0;
                border-radius: 8px;
                border-right: 4px solid #667eea;
            }
            .endpoint a {
                color: #667eea;
                text-decoration: none;
                font-weight: bold;
            }
            .endpoint a:hover {
                text-decoration: underline;
            }
            .method {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                font-weight: bold;
                margin-left: 10px;
            }
            .get { background: #28a745; color: white; }
            .post { background: #007bff; color: white; }
            .put { background: #ffc107; color: white; }
            .delete { background: #dc3545; color: white; }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .stat-card h3 {
                font-size: 2em;
                margin-bottom: 5px;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌟 مزون</h1>
            <div class="subtitle">Mazoon Platform API - منصة لكل عماني</div>
            
            <div class="status">
                ✅ API يعمل بشكل صحيح | API is Running Successfully
            </div>

            <div class="endpoints">
                <h2>📋 نقاط النهاية المتاحة | Available Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/health" target="_blank">/health</a>
                    - فحص صحة النظام
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/api/stats" target="_blank">/api/stats</a>
                    - إحصائيات المنصة
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/api/news" target="_blank">/api/news</a>
                    - جميع الأخبار
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/api/news/categories" target="_blank">/api/news/categories</a>
                    - تصنيفات الأخبار
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/api/events" target="_blank">/api/events</a>
                    - جميع الفعاليات
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/api/events/categories" target="_blank">/api/events/categories</a>
                    - تصنيفات الفعاليات
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/api/jobs" target="_blank">/api/jobs</a>
                    - جميع الوظائف
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/api/jobs/categories" target="_blank">/api/jobs/categories</a>
                    - تصنيفات الوظائف
                </div>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <a href="/api/search?q=مسقط" target="_blank">/api/search?q=مسقط</a>
                    - البحث الشامل
                </div>
            </div>

            <div id="stats" class="stats"></div>

            <div class="footer">
                <p><strong>Made with ♥ in Oman | صُنع بكل ♥ في عُمان</strong></p>
                <p style="margin-top: 10px; font-size: 0.9em;">
                    📚 <a href="https://github.com/YOUR_USERNAME/mazoon-platform" target="_blank" style="color: #667eea;">GitHub Repository</a>
                </p>
            </div>
        </div>

        <script>
            // Load and display stats
            fetch('/api/stats')
                .then(res => res.json())
                .then(data => {
                    const stats = data.data;
                    const statsHtml = `
                        <div class="stat-card">
                            <h3>${stats.news_count || 0}</h3>
                            <p>📰 أخبار</p>
                        </div>
                        <div class="stat-card">
                            <h3>${stats.events_count || 0}</h3>
                            <p>📅 فعاليات</p>
                        </div>
                        <div class="stat-card">
                            <h3>${stats.jobs_count || 0}</h3>
                            <p>💼 وظائف</p>
                        </div>
                        <div class="stat-card">
                            <h3>${stats.tourism_count || 0}</h3>
                            <p>🏖️ سياحة</p>
                        </div>
                    `;
                    document.getElementById('stats').innerHTML = statsHtml;
                })
                .catch(err => console.error('Error loading stats:', err));
        </script>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("=" * 60)
    print("مزون - واجهة برمجية")
    print("Mazoon Platform API")
    print("=" * 60)
    print()
    
    # Get port from environment variable (for production) or use 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') != 'production'
    
    print(f"✓ Server starting on http://0.0.0.0:{port}")
    print(f"✓ Health check: http://0.0.0.0:{port}/health")
    print()
    print("Available CRUD endpoints:")
    print("  📰 News:   /api/news")
    print("  📅 Events: /api/events")
    print("  💼 Jobs:   /api/jobs")
    print("  🔍 Search: /api/search?q=مسقط")
    print("  📊 Stats:  /api/stats")
    print()
    print("=" * 60)
    
    app.run(debug=debug, host='0.0.0.0', port=port)
