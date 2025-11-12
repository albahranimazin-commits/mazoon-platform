# مزون - ملف المشروع الشامل
# Mazoon - Complete Project Summary

## 📋 نظرة عامة | Overview

**مزون** هي منصة عمانية شاملة تجمع كل ما يحتاجه المواطن العماني في مكان واحد.

**Mazoon** is a comprehensive Omani platform that brings everything an Omani citizen needs in one place.

---

## 📁 الملفات المتضمنة | Included Files

### 1. قاعدة البيانات | Database Files

#### `mazoon_database.sql` (قاعدة البيانات الكاملة)
- 37 جدول شامل | 37 comprehensive tables
- يشمل جميع الأنظمة: أخبار، فعاليات، وظائف، سوق، سياحة، وأكثر
- Includes all systems: news, events, jobs, marketplace, tourism, and more
- فهارس محسّنة للأداء | Optimized indexes for performance
- محفزات تلقائية | Automatic triggers

#### `mazoon.db` (قاعدة البيانات الجاهزة)
- قاعدة بيانات SQLite جاهزة للاستخدام مع بيانات تجريبية
- Ready-to-use SQLite database with sample data
- حجم: ~100 KB | Size: ~100 KB

### 2. البرمجيات | Scripts

#### `init_database.py` (برنامج التهيئة)
```bash
python init_database.py
```
- إنشاء قاعدة بيانات جديدة | Creates new database
- إضافة بيانات تجريبية | Adds sample data
- التحقق من البنية | Verifies structure

#### `verify_database.py` (برنامج التحقق)
```bash
python verify_database.py
```
- عرض محتويات قاعدة البيانات | Displays database contents
- إحصائيات شاملة | Comprehensive statistics
- معاينة البيانات | Data preview

#### `api_example.py` (مثال للواجهة البرمجية)
```bash
python api_example.py
```
- Flask API كامل الوظائف | Fully functional Flask API
- نقاط نهاية RESTful | RESTful endpoints
- أمثلة على الاستعلامات | Query examples

### 3. التوثيق | Documentation

#### `DATABASE_README.md`
- دليل شامل لقاعدة البيانات | Comprehensive database guide
- أمثلة على الاستعلامات | Query examples
- أفضل الممارسات | Best practices

#### `requirements.txt`
- قائمة المتطلبات | Dependencies list
- للتثبيت: `pip install -r requirements.txt`
- For installation: `pip install -r requirements.txt`

---

## 🚀 البدء السريع | Quick Start

### الخطوة 1: إنشاء قاعدة البيانات
```bash
python init_database.py
```

### الخطوة 2: التحقق من قاعدة البيانات
```bash
python verify_database.py
```

### الخطوة 3: تشغيل الواجهة البرمجية (اختياري)
```bash
# تثبيت المتطلبات
pip install flask flask-cors

# تشغيل الخادم
python api_example.py
```

---

## 🗂️ هيكل قاعدة البيانات | Database Structure

### الأنظمة الرئيسية | Main Systems

1. **إدارة المستخدمين | User Management**
   - users
   - user_preferences

2. **نظام الأخبار | News System**
   - news_categories (7 تصنيفات)
   - news_articles
   - news_tags
   - news_article_tags

3. **نظام الفعاليات | Events System**
   - event_categories (6 تصنيفات)
   - events
   - event_registrations

4. **نظام التوظيف | Jobs System**
   - job_categories (8 تصنيفات)
   - companies
   - jobs
   - job_applications

5. **السوق الإلكتروني | Marketplace**
   - marketplace_categories (6 تصنيفات)
   - marketplace_listings
   - marketplace_images

6. **السياحة | Tourism**
   - tourism_categories (6 تصنيفات)
   - tourism_places (3 أماكن تجريبية)
   - tourism_images
   - tourism_reviews

7. **الوصفات | Recipes**
   - recipe_categories (5 تصنيفات)
   - recipes (2 وصفات تجريبية)

8. **التعليم | Education**
   - education_institutions
   - education_programs

9. **دليل الأعمال | Business Directory**
   - business_categories (6 تصنيفات)
   - businesses (2 أعمال تجريبية)
   - business_reviews

10. **المنتديات | Forums**
    - forum_categories (4 تصنيفات)
    - forum_topics
    - forum_replies

11. **الطقس | Weather**
    - weather_locations (5 مدن)
    - weather_data

12. **التفاعل | Engagement**
    - notifications
    - user_favorites
    - user_views
    - comments

---

## 📊 البيانات التجريبية | Sample Data

### الأخبار | News
- 3 مقالات إخبارية | 3 news articles
- 7 تصنيفات | 7 categories

### الفعاليات | Events
- 2 فعاليات قادمة | 2 upcoming events
- مهرجان مسقط | Muscat Festival
- معرض عمان للكتاب | Oman Book Fair

### الوظائف | Jobs
- 2 وظيفة متاحة | 2 available jobs
- 3 شركات | 3 companies

### السياحة | Tourism
- 3 أماكن سياحية | 3 tourist places
- قلعة نزوى | Nizwa Fort
- شاطئ القرم | Qurum Beach
- سوق مطرح | Mutrah Souq

### الوصفات | Recipes
- 2 وصفة تقليدية | 2 traditional recipes
- الشواء العماني | Omani Shuwa
- الحلوى العمانية | Omani Halwa

### المحافظات | Governorates
- 11 محافظة عمانية | 11 Omani governorates
- 5 مواقع للطقس | 5 weather locations

---

## 🔌 نقاط النهاية البرمجية | API Endpoints

### الأخبار | News
```
GET /api/news                    # جميع الأخبار
GET /api/news/<slug>             # خبر محدد
GET /api/news/categories         # التصنيفات
```

### الفعاليات | Events
```
GET /api/events                  # جميع الفعاليات
GET /api/events/<slug>           # فعالية محددة
```

### الوظائف | Jobs
```
GET /api/jobs                    # جميع الوظائف
GET /api/jobs/<slug>             # وظيفة محددة
```

### السياحة | Tourism
```
GET /api/tourism/places          # الأماكن السياحية
GET /api/tourism/places/<slug>  # مكان محدد
```

### الوصفات | Recipes
```
GET /api/recipes                 # جميع الوصفات
```

### الأعمال | Businesses
```
GET /api/businesses              # دليل الأعمال
```

### البحث | Search
```
GET /api/search?q=مسقط          # البحث الشامل
```

---

## 💡 أمثلة على الاستخدام | Usage Examples

### Python - الاتصال بقاعدة البيانات
```python
import sqlite3

conn = sqlite3.connect('mazoon.db')
cursor = conn.cursor()

# استرجاع جميع الأخبار
cursor.execute("""
    SELECT a.title_ar, c.name_ar 
    FROM news_articles a
    JOIN news_categories c ON a.category_id = c.id
    WHERE a.is_published = 1
    ORDER BY a.published_at DESC
""")

articles = cursor.fetchall()
for article in articles:
    print(f"{article[0]} - {article[1]}")

conn.close()
```

### cURL - اختبار الواجهة البرمجية
```bash
# استرجاع الأخبار
curl http://localhost:5000/api/news

# استرجاع الفعاليات القادمة
curl http://localhost:5000/api/events?upcoming=true

# البحث
curl http://localhost:5000/api/search?q=مسقط
```

---

## 🛠️ التطوير المستقبلي | Future Development

### المرحلة 1 - الأساسيات ✅
- [x] قاعدة بيانات شاملة
- [x] بيانات تجريبية
- [x] واجهة برمجية أساسية

### المرحلة 2 - التحسينات
- [ ] نظام المصادقة والتفويض
- [ ] رفع الملفات والصور
- [ ] نظام الإشعارات الفورية
- [ ] التخزين المؤقت

### المرحلة 3 - المميزات المتقدمة
- [ ] البحث بالنص الكامل
- [ ] التوصيات الذكية
- [ ] التحليلات والإحصائيات
- [ ] التكامل مع خدمات خارجية

### المرحلة 4 - التطبيقات
- [ ] تطبيق الويب الكامل
- [ ] تطبيق الهاتف المحمول
- [ ] لوحة التحكم الإدارية
- [ ] واجهة المستخدم بالذكاء الاصطناعي

---

## 📱 المنصات المدعومة | Supported Platforms

- ✅ الويب | Web (React, Vue, Angular)
- ✅ الهاتف المحمول | Mobile (React Native, Flutter)
- ✅ سطح المكتب | Desktop (Electron)
- ✅ الواجهة البرمجية | API (REST)

---

## 🔒 الأمان | Security

### التوصيات | Recommendations
1. استخدم معلمات للاستعلامات | Use parameterized queries
2. قم بتجزئة كلمات المرور | Hash passwords (bcrypt)
3. نفذ التحقق من الصلاحيات | Implement authorization
4. استخدم HTTPS في الإنتاج | Use HTTPS in production
5. قم بالنسخ الاحتياطي المنتظم | Regular backups

---

## 📈 الأداء | Performance

### التحسينات المطبقة | Applied Optimizations
- ✅ فهارس على الأعمدة الأساسية | Indexes on key columns
- ✅ علاقات خارجية محسّنة | Optimized foreign keys
- ✅ استعلامات محسّنة | Optimized queries

### توصيات إضافية | Additional Recommendations
- استخدم Redis للتخزين المؤقت | Use Redis for caching
- نفذ الترقيم | Implement pagination
- استخدم CDN للملفات الثابتة | Use CDN for static files
- راقب الأداء بانتظام | Monitor performance regularly

---

## 🌍 التعريب | Localization

- ✅ دعم اللغة العربية والإنجليزية
- ✅ Arabic and English support
- ✅ أسماء الأعمدة بالعربية والإنجليزية
- ✅ Column names in Arabic and English
- ✅ التنسيق من اليمين إلى اليسار (RTL)
- ✅ Right-to-Left (RTL) formatting

---

## 📞 الدعم | Support

للمساعدة والاستفسارات:
For help and inquiries:

- 📧 البريد الإلكتروني | Email: support@mazoon.om
- 🌐 الموقع | Website: https://mazoon.om
- 📱 تويتر | Twitter: @mazoon_om

---

## 📄 الترخيص | License

© 2025 Mazoon Platform. All rights reserved.

---

## 🙏 شكر وتقدير | Acknowledgments

شكراً لكل من ساهم في هذا المشروع الذي يهدف لخدمة المجتمع العماني.

Thanks to everyone who contributed to this project aimed at serving the Omani community.

---

**صُنع بكل ♥ في عُمان | Made with ♥ in Oman**

---

## 📝 ملاحظات إضافية | Additional Notes

### المتطلبات التقنية | Technical Requirements
- Python 3.7+
- SQLite3
- Flask (للواجهة البرمجية | for API)

### التثبيت | Installation
```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# إنشاء قاعدة البيانات
python init_database.py

# التحقق من النجاح
python verify_database.py
```

### الاختبار | Testing
```bash
# تشغيل الواجهة البرمجية
python api_example.py

# في نافذة أخرى، اختبر النقاط
curl http://localhost:5000/api/news
```

---

**انتهى | END**
