import sqlite3
from datetime import datetime, timedelta
import random

def create_database():
    """Create the Mazoon database and initialize it with sample data"""
    
    # Connect to database
    conn = sqlite3.connect('mazoon.db')
    cursor = conn.cursor()
    
    # Read and execute the schema file
    with open('mazoon_database.sql', 'r', encoding='utf-8') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    print("✓ Database schema created successfully")
    
    # Insert sample data
    insert_sample_data(conn, cursor)
    
    conn.commit()
    conn.close()
    
    print("\n✓ Database initialization complete!")
    print("Database file: mazoon.db")

def insert_sample_data(conn, cursor):
    """Insert sample data for testing"""
    
    # Insert governorates and cities for reference
    governorates = [
        'مسقط', 'ظفار', 'مسندم', 'البريمي', 'الداخلية', 
        'شمال الباطنة', 'جنوب الباطنة', 'شمال الشرقية', 'جنوب الشرقية', 'الظاهرة', 'الوسطى'
    ]
    
    # News Categories
    news_categories = [
        ('أخبار محلية', 'Local News', 'local', 'newspaper', 1),
        ('أخبار عالمية', 'World News', 'world', 'globe', 2),
        ('اقتصاد', 'Economy', 'economy', 'chart-line', 3),
        ('رياضة', 'Sports', 'sports', 'football', 4),
        ('تقنية', 'Technology', 'technology', 'laptop', 5),
        ('صحة', 'Health', 'health', 'heart', 6),
        ('ثقافة وفن', 'Culture & Arts', 'culture', 'palette', 7),
    ]
    
    cursor.executemany('''
        INSERT INTO news_categories (name_ar, name_en, slug, icon, display_order)
        VALUES (?, ?, ?, ?, ?)
    ''', news_categories)
    print("✓ News categories inserted")
    
    # Event Categories
    event_categories = [
        ('مهرجانات', 'Festivals', 'festivals', 'calendar-star', '#FF6B6B'),
        ('معارض', 'Exhibitions', 'exhibitions', 'building', '#4ECDC4'),
        ('ورش عمل', 'Workshops', 'workshops', 'users', '#45B7D1'),
        ('رياضة', 'Sports', 'sports', 'trophy', '#FFA07A'),
        ('ثقافة', 'Culture', 'culture', 'book', '#98D8C8'),
        ('تعليم', 'Education', 'education', 'graduation-cap', '#F7DC6F'),
    ]
    
    cursor.executemany('''
        INSERT INTO event_categories (name_ar, name_en, slug, icon, color)
        VALUES (?, ?, ?, ?, ?)
    ''', event_categories)
    print("✓ Event categories inserted")
    
    # Job Categories
    job_categories = [
        ('تقنية المعلومات', 'Information Technology', 'it', 'laptop-code'),
        ('هندسة', 'Engineering', 'engineering', 'cog'),
        ('طب وصحة', 'Healthcare', 'healthcare', 'stethoscope'),
        ('تعليم', 'Education', 'education', 'chalkboard-teacher'),
        ('مبيعات وتسويق', 'Sales & Marketing', 'sales-marketing', 'chart-line'),
        ('مالية ومحاسبة', 'Finance & Accounting', 'finance', 'dollar-sign'),
        ('إدارة', 'Management', 'management', 'briefcase'),
        ('قانون', 'Legal', 'legal', 'gavel'),
    ]
    
    cursor.executemany('''
        INSERT INTO job_categories (name_ar, name_en, slug, icon)
        VALUES (?, ?, ?, ?)
    ''', job_categories)
    print("✓ Job categories inserted")
    
    # Marketplace Categories
    marketplace_categories = [
        ('إلكترونيات', 'Electronics', 'electronics', None, 'phone'),
        ('سيارات', 'Vehicles', 'vehicles', None, 'car'),
        ('عقارات', 'Real Estate', 'real-estate', None, 'home'),
        ('أثاث', 'Furniture', 'furniture', None, 'couch'),
        ('أزياء', 'Fashion', 'fashion', None, 'tshirt'),
        ('رياضة', 'Sports', 'sports', None, 'dumbbell'),
    ]
    
    cursor.executemany('''
        INSERT INTO marketplace_categories (name_ar, name_en, slug, parent_id, icon)
        VALUES (?, ?, ?, ?, ?)
    ''', marketplace_categories)
    print("✓ Marketplace categories inserted")
    
    # Tourism Categories
    tourism_categories = [
        ('قلاع وحصون', 'Forts & Castles', 'forts-castles', 'fort-awesome'),
        ('شواطئ', 'Beaches', 'beaches', 'umbrella-beach'),
        ('جبال وأودية', 'Mountains & Wadis', 'mountains-wadis', 'mountain'),
        ('متاحف', 'Museums', 'museums', 'landmark'),
        ('أسواق تقليدية', 'Traditional Souqs', 'souqs', 'store'),
        ('منتجعات', 'Resorts', 'resorts', 'hotel'),
    ]
    
    cursor.executemany('''
        INSERT INTO tourism_categories (name_ar, name_en, slug, icon)
        VALUES (?, ?, ?, ?)
    ''', tourism_categories)
    print("✓ Tourism categories inserted")
    
    # Recipe Categories
    recipe_categories = [
        ('أطباق رئيسية', 'Main Dishes', 'main-dishes', 'utensils'),
        ('مقبلات', 'Appetizers', 'appetizers', 'bowl'),
        ('حلويات', 'Desserts', 'desserts', 'ice-cream'),
        ('مشروبات', 'Beverages', 'beverages', 'mug-hot'),
        ('أطباق عمانية', 'Omani Dishes', 'omani-dishes', 'flag'),
    ]
    
    cursor.executemany('''
        INSERT INTO recipe_categories (name_ar, name_en, slug, icon)
        VALUES (?, ?, ?, ?)
    ''', recipe_categories)
    print("✓ Recipe categories inserted")
    
    # Business Categories
    business_categories = [
        ('مطاعم', 'Restaurants', 'restaurants', None, 'utensils'),
        ('فنادق', 'Hotels', 'hotels', None, 'hotel'),
        ('تسوق', 'Shopping', 'shopping', None, 'shopping-bag'),
        ('خدمات', 'Services', 'services', None, 'tools'),
        ('صحة', 'Health', 'health', None, 'heartbeat'),
        ('تعليم', 'Education', 'education', None, 'book'),
    ]
    
    cursor.executemany('''
        INSERT INTO business_categories (name_ar, name_en, slug, parent_id, icon)
        VALUES (?, ?, ?, ?, ?)
    ''', business_categories)
    print("✓ Business categories inserted")
    
    # Forum Categories
    forum_categories = [
        ('نقاش عام', 'General Discussion', 'general', 'عام', 'comments', 1),
        ('تقنية', 'Technology', 'technology', 'تقنية', 'laptop', 2),
        ('سفر وسياحة', 'Travel & Tourism', 'travel', 'سياحة', 'plane', 3),
        ('صحة ورياضة', 'Health & Fitness', 'health-fitness', 'رياضة', 'heartbeat', 4),
    ]
    
    cursor.executemany('''
        INSERT INTO forum_categories (name_ar, name_en, slug, description_ar, icon, display_order)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', forum_categories)
    print("✓ Forum categories inserted")
    
    # Weather Locations
    weather_locations = [
        ('مسقط', 'Muscat', 'مسقط', 'Muscat', 23.588, 58.383, 1),
        ('صلالة', 'Salalah', 'ظفار', 'Dhofar', 17.015, 54.091, 0),
        ('صحار', 'Sohar', 'شمال الباطنة', 'North Al Batinah', 24.341, 56.709, 0),
        ('نزوى', 'Nizwa', 'الداخلية', 'Ad Dakhiliyah', 22.933, 57.529, 0),
        ('صور', 'Sur', 'جنوب الشرقية', 'South Al Sharqiyah', 22.566, 59.528, 0),
    ]
    
    cursor.executemany('''
        INSERT INTO weather_locations (city_ar, city_en, governorate_ar, governorate_en, 
                                       latitude, longitude, is_default)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', weather_locations)
    print("✓ Weather locations inserted")
    
    # Sample Companies
    companies = [
        ('شركة أوكيو', 'OOQYU', 'شركة عمانية رائدة في مجال التقنية', 
         'Technology', 'Large', 'https://ooqyu.com', 'مسقط', 'مسقط', 1),
        ('بنك مسقط', 'Bank Muscat', 'أكبر بنك في سلطنة عمان',
         'Banking', 'Large', 'https://bankmuscat.com', 'مسقط', 'مسقط', 1),
        ('شركة النفط العمانية', 'Petroleum Development Oman', 'شركة رائدة في قطاع النفط والغاز',
         'Oil & Gas', 'Large', 'https://pdo.co.om', 'مسقط', 'مسقط', 1),
    ]
    
    cursor.executemany('''
        INSERT INTO companies (name, name_ar, description, industry, company_size, 
                              website, city, governorate, is_verified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', companies)
    print("✓ Sample companies inserted")
    
    # Sample News Articles
    sample_news = [
        (1, 'افتتاح مشروع تطوير جديد في مسقط', 'new-development-project-muscat',
         'تم افتتاح مشروع تطوير حضري جديد في محافظة مسقط يهدف إلى تحسين البنية التحتية',
         'افتتح صباح اليوم مشروع تطوير حضري كبير في محافظة مسقط بحضور عدد من المسؤولين...', 1, 1),
        
        (4, 'منتخبنا الوطني يستعد لبطولة كأس الخليج', 'national-team-gulf-cup',
         'يواصل منتخبنا الوطني لكرة القدم استعداداته لبطولة كأس الخليج القادمة',
         'يخوض منتخبنا الوطني معسكراً تدريبياً مكثفاً استعداداً للبطولة...', 1, 1),
        
        (5, 'إطلاق تطبيق جديد لتسهيل الخدمات الحكومية', 'new-gov-services-app',
         'أطلقت الحكومة تطبيقاً جديداً يهدف إلى تسهيل الوصول للخدمات الحكومية',
         'في خطوة نحو التحول الرقمي، تم إطلاق تطبيق متكامل للخدمات الحكومية...', 1, 1),
    ]
    
    for article in sample_news:
        cursor.execute('''
            INSERT INTO news_articles (category_id, title_ar, slug, summary_ar, content_ar, 
                                      is_featured, is_published, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', article)
    print("✓ Sample news articles inserted")
    
    # Sample Events
    base_date = datetime.now()
    sample_events = [
        (1, 'مهرجان مسقط', 'muscat-festival', 
         'مهرجان سنوي يحتفل بالثقافة والتراث العماني',
         'منظمة مهرجان مسقط', 'حديقة القرم', 'مسقط', 'مسقط',
         (base_date + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
         (base_date + timedelta(days=60)).strftime('%Y-%m-%d %H:%M:%S'), 1, 1),
        
        (2, 'معرض عمان للكتاب', 'oman-book-fair',
         'معرض سنوي للكتب والثقافة',
         'وزارة الثقافة', 'مركز عمان للمؤتمرات والمعارض', 'مسقط', 'مسقط',
         (base_date + timedelta(days=15)).strftime('%Y-%m-%d %H:%M:%S'),
         (base_date + timedelta(days=20)).strftime('%Y-%m-%d %H:%M:%S'), 1, 1),
    ]
    
    for event in sample_events:
        cursor.execute('''
            INSERT INTO events (category_id, title_ar, slug, description_ar, organizer, 
                              venue, city, governorate, start_date, end_date, 
                              is_free, is_published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', event)
    print("✓ Sample events inserted")
    
    # Sample Jobs
    sample_jobs = [
        (1, 1, 'مطور برمجيات', 'software-developer',
         'نبحث عن مطور برمجيات موهوب للانضمام لفريقنا',
         'خبرة في تطوير تطبيقات الويب', 'full-time', 'mid', 800, 1200, 1),
        
        (5, 2, 'مدير تسويق رقمي', 'digital-marketing-manager',
         'فرصة رائعة للعمل في بيئة ديناميكية',
         'خبرة في التسويق الرقمي ووسائل التواصل الاجتماعي', 'full-time', 'senior', 1000, 1500, 1),
    ]
    
    for job in sample_jobs:
        cursor.execute('''
            INSERT INTO jobs (category_id, company_id, title_ar, slug, description_ar, 
                            requirements_ar, employment_type, experience_level, 
                            min_salary, max_salary, is_active, posted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', job)
    print("✓ Sample jobs inserted")
    
    # Sample Tourism Places
    sample_places = [
        (1, 'قلعة نزوى', 'nizwa-fort',
         'قلعة تاريخية شهيرة بتصميمها المعماري الفريد',
         'نزوى', 'الداخلية', 'شارع السوق', 22.933, 57.529, 2.0, 1, 1),
        
        (2, 'شاطئ القرم', 'qurum-beach',
         'شاطئ جميل مع مرافق متكاملة',
         'مسقط', 'مسقط', 'القرم', 23.588, 58.383, 0.0, 1, 1),
        
        (5, 'سوق مطرح', 'mutrah-souq',
         'سوق تقليدي عريق يعكس التراث العماني',
         'مطرح', 'مسقط', 'كورنيش مطرح', 23.620, 58.565, 0.0, 1, 1),
    ]
    
    for place in sample_places:
        cursor.execute('''
            INSERT INTO tourism_places (category_id, name_ar, slug, description_ar, 
                                       city, governorate, address, latitude, longitude, 
                                       entry_fee, is_featured, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', place)
    print("✓ Sample tourism places inserted")
    
    # Sample Recipes
    sample_recipes = [
        (5, 'الشواء العماني', 'omani-shuwa',
         'طبق تقليدي عماني شهير',
         'لحم، بهارات عمانية، أوراق موز',
         'يتم تحضير اللحم بالبهارات ولفه بأوراق الموز وطبخه تحت الأرض...',
         240, 720, 10, 'hard', 1, 1),
        
        (3, 'الحلوى العمانية', 'omani-halwa',
         'حلوى تقليدية عمانية',
         'سكر، نشا، ماء الورد، زعفران، مكسرات',
         'يتم خلط المكونات وطبخها على نار هادئة مع التحريك المستمر...',
         30, 60, 20, 'medium', 1, 1),
    ]
    
    for recipe in sample_recipes:
        cursor.execute('''
            INSERT INTO recipes (category_id, title_ar, slug, description_ar,
                               ingredients_ar, instructions_ar, prep_time, cook_time, 
                               servings, difficulty, is_traditional, is_published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', recipe)
    print("✓ Sample recipes inserted")
    
    # Sample Businesses
    sample_businesses = [
        (1, 'مطعم الأنغام', 'al-angham-restaurant',
         'مطعم متخصص في المأكولات العمانية التقليدية',
         'مسقط', 'مسقط', 1, 1, 1),
        
        (2, 'فندق شيراتون مسقط', 'sheraton-muscat-hotel',
         'فندق فاخر بإطلالة على البحر',
         'مسقط', 'مسقط', 1, 1, 1),
    ]
    
    for business in sample_businesses:
        cursor.execute('''
            INSERT INTO businesses (category_id, name_ar, slug, description_ar, 
                                  city, governorate, is_verified, is_featured, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', business)
    print("✓ Sample businesses inserted")

if __name__ == '__main__':
    print("=" * 50)
    print("مزون - تهيئة قاعدة البيانات")
    print("Mazoon - Database Initialization")
    print("=" * 50)
    print()
    
    create_database()
    
    print()
    print("=" * 50)
    print("Database ready to use!")
    print("File: mazoon.db")
    print("=" * 50)
