# مزون - قاعدة البيانات | Mazoon Database

## نظرة عامة | Overview

قاعدة بيانات شاملة لمنصة مزون - منصة عمانية متكاملة تجمع الأخبار، الفعاليات، الوظائف، السوق، السياحة، وأكثر.

Comprehensive database for Mazoon platform - an integrated Omani platform featuring news, events, jobs, marketplace, tourism, and more.

## المميزات | Features

- ✅ إدارة المستخدمين والصلاحيات | User Management & Permissions
- 📰 نظام أخبار متكامل | Complete News System
- 📅 إدارة الفعاليات | Events Management
- 💼 نظام التوظيف | Job Listings System
- 🏪 السوق الإلكتروني | Marketplace
- 🏖️ دليل السياحة | Tourism Guide
- 👨‍🍳 وصفات الطبخ | Recipe System
- 🏢 دليل الأعمال | Business Directory
- 💬 المنتديات المجتمعية | Community Forums
- 🎓 التعليم | Education
- 🌤️ بيانات الطقس | Weather Data
- 🔔 نظام الإشعارات | Notifications System

## هيكل قاعدة البيانات | Database Structure

### Core Tables

#### 1. User Management
- `users` - معلومات المستخدمين | User information
- `user_preferences` - تفضيلات المستخدم | User preferences

#### 2. News System
- `news_categories` - تصنيفات الأخبار | News categories
- `news_articles` - المقالات الإخبارية | News articles
- `news_tags` - وسوم الأخبار | News tags
- `news_article_tags` - ربط المقالات بالوسوم | Article-tag relationships

#### 3. Events System
- `event_categories` - تصنيفات الفعاليات | Event categories
- `events` - الفعاليات | Events
- `event_registrations` - تسجيلات الفعاليات | Event registrations

#### 4. Jobs System
- `job_categories` - تصنيفات الوظائف | Job categories
- `companies` - الشركات | Companies
- `jobs` - الوظائف | Job listings
- `job_applications` - طلبات التوظيف | Job applications

#### 5. Marketplace System
- `marketplace_categories` - تصنيفات السوق | Marketplace categories
- `marketplace_listings` - الإعلانات | Listings
- `marketplace_images` - صور الإعلانات | Listing images

#### 6. Tourism System
- `tourism_categories` - تصنيفات السياحة | Tourism categories
- `tourism_places` - الأماكن السياحية | Tourist places
- `tourism_images` - صور الأماكن | Place images
- `tourism_reviews` - تقييمات الأماكن | Place reviews

#### 7. Recipe System
- `recipe_categories` - تصنيفات الوصفات | Recipe categories
- `recipes` - الوصفات | Recipes

#### 8. Education System
- `education_institutions` - المؤسسات التعليمية | Educational institutions
- `education_programs` - البرامج التعليمية | Educational programs

#### 9. Business Directory
- `business_categories` - تصنيفات الأعمال | Business categories
- `businesses` - دليل الأعمال | Business directory
- `business_reviews` - تقييمات الأعمال | Business reviews

#### 10. Community Features
- `forum_categories` - تصنيفات المنتدى | Forum categories
- `forum_topics` - مواضيع المنتدى | Forum topics
- `forum_replies` - الردود | Forum replies

#### 11. Weather System
- `weather_locations` - مواقع الطقس | Weather locations
- `weather_data` - بيانات الطقس | Weather data

#### 12. Engagement & Interaction
- `notifications` - الإشعارات | Notifications
- `user_favorites` - المفضلات | User favorites
- `user_views` - المشاهدات | Page views
- `comments` - التعليقات | Comments

## التثبيت والتشغيل | Installation & Setup

### المتطلبات | Requirements
- Python 3.7+
- SQLite3

### الخطوات | Steps

1. **إنشاء قاعدة البيانات | Create Database**
```bash
python init_database.py
```

2. **التحقق من قاعدة البيانات | Verify Database**
```bash
sqlite3 mazoon.db ".tables"
```

## الاستخدام | Usage

### الاتصال بقاعدة البيانات | Connecting to Database

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('mazoon.db')
cursor = conn.cursor()

# Execute queries
cursor.execute("SELECT * FROM users WHERE is_active = 1")
users = cursor.fetchall()

# Close connection
conn.close()
```

### أمثلة على الاستعلامات | Query Examples

#### إضافة مستخدم جديد | Add New User
```sql
INSERT INTO users (username, email, password_hash, full_name)
VALUES ('ahmed', 'ahmed@example.com', 'hashed_password', 'أحمد محمد');
```

#### البحث عن الأخبار | Search News
```sql
SELECT a.*, c.name_ar as category_name
FROM news_articles a
JOIN news_categories c ON a.category_id = c.id
WHERE a.is_published = 1
ORDER BY a.published_at DESC
LIMIT 10;
```

#### الفعاليات القادمة | Upcoming Events
```sql
SELECT *
FROM events
WHERE start_date > datetime('now')
  AND is_published = 1
ORDER BY start_date ASC;
```

#### الوظائف المتاحة | Available Jobs
```sql
SELECT j.*, c.name as company_name, cat.name_ar as category_name
FROM jobs j
JOIN companies c ON j.company_id = c.id
JOIN job_categories cat ON j.category_id = cat.id
WHERE j.is_active = 1
  AND j.application_deadline > date('now')
ORDER BY j.posted_at DESC;
```

#### الأماكن السياحية الأعلى تقييماً | Top-Rated Tourism Places
```sql
SELECT *
FROM tourism_places
WHERE is_active = 1
ORDER BY rating DESC, reviews_count DESC
LIMIT 10;
```

## الفهرسة | Indexing

تم إنشاء فهارس لتحسين الأداء على:
Indexes created for performance optimization on:

- البحث في الجداول الرئيسية | Primary table searches
- العلاقات بين الجداول | Table relationships
- الاستعلامات الشائعة | Common queries
- التصفية والفرز | Filtering and sorting

## المحفزات | Triggers

تم إنشاء محفزات تلقائية لـ:
Automatic triggers created for:

- تحديث الطوابع الزمنية | Timestamp updates
- صيانة سلامة البيانات | Data integrity maintenance

## أفضل الممارسات | Best Practices

### الأمان | Security
- استخدم معلمات للاستعلامات لتجنب حقن SQL | Use parameterized queries to prevent SQL injection
- قم بتجزئة كلمات المرور | Hash passwords before storing
- تحقق من صلاحيات المستخدم | Validate user permissions

### الأداء | Performance
- استخدم الفهارس للبحث السريع | Use indexes for fast searches
- قم بتحديد الأعمدة المطلوبة فقط | Select only needed columns
- استخدم الترقيم للنتائج الكبيرة | Use pagination for large result sets

### صيانة البيانات | Data Maintenance
- قم بنسخ احتياطي منتظم | Regular backups
- تنظيف البيانات القديمة | Clean old data
- مراقبة حجم قاعدة البيانات | Monitor database size

## معلومات إضافية | Additional Information

### المحافظات العمانية | Omani Governorates
القاعدة تدعم جميع المحافظات:
The database supports all governorates:

1. مسقط | Muscat
2. ظفار | Dhofar
3. مسندم | Musandam
4. البريمي | Al Buraimi
5. الداخلية | Ad Dakhiliyah
6. شمال الباطنة | North Al Batinah
7. جنوب الباطنة | South Al Batinah
8. شمال الشرقية | North Ash Sharqiyah
9. جنوب الشرقية | South Ash Sharqiyah
10. الظاهرة | Adh Dhahirah
11. الوسطى | Al Wusta

### أنواع المحتوى المدعومة | Supported Content Types

- النصوص العربية والإنجليزية | Arabic and English text
- الصور والفيديو | Images and videos
- التصنيفات والوسوم | Categories and tags
- التقييمات والمراجعات | Ratings and reviews
- الإحداثيات الجغرافية | Geographic coordinates

## الدعم الفني | Technical Support

للمساعدة والاستفسارات:
For help and inquiries:

- البريد الإلكتروني | Email: support@mazoon.om
- الموقع | Website: https://mazoon.om

## الترخيص | License

© 2025 Mazoon Platform. All rights reserved.

---

**صُنع بكل ♥ في عُمان | Made with ♥ in Oman**
