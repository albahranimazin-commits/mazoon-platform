-- Mazoon Platform Database Schema
-- مزون - منصة لكل عماني

-- ============================================
-- USER MANAGEMENT
-- ============================================

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(255),
    bio TEXT,
    location VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(10),
    is_verified BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    role VARCHAR(20) DEFAULT 'user', -- user, admin, moderator
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    language VARCHAR(10) DEFAULT 'ar',
    theme VARCHAR(20) DEFAULT 'light',
    notifications_enabled BOOLEAN DEFAULT 1,
    email_notifications BOOLEAN DEFAULT 1,
    newsletter_subscription BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- NEWS SYSTEM
-- ============================================

CREATE TABLE news_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    title_ar VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    slug VARCHAR(255) UNIQUE NOT NULL,
    summary_ar TEXT,
    summary_en TEXT,
    content_ar TEXT NOT NULL,
    content_en TEXT,
    author_id INTEGER,
    source VARCHAR(100),
    source_url VARCHAR(500),
    image_url VARCHAR(500),
    video_url VARCHAR(500),
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT 0,
    is_breaking BOOLEAN DEFAULT 0,
    is_published BOOLEAN DEFAULT 1,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES news_categories(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);

CREATE TABLE news_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(50) NOT NULL,
    name_en VARCHAR(50) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE news_article_tags (
    article_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (article_id, tag_id),
    FOREIGN KEY (article_id) REFERENCES news_articles(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES news_tags(id) ON DELETE CASCADE
);

-- ============================================
-- EVENTS SYSTEM
-- ============================================

CREATE TABLE event_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(50),
    color VARCHAR(20)
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    title_ar VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    slug VARCHAR(255) UNIQUE NOT NULL,
    description_ar TEXT NOT NULL,
    description_en TEXT,
    organizer VARCHAR(100),
    venue VARCHAR(200),
    address TEXT,
    city VARCHAR(100),
    governorate VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    registration_deadline TIMESTAMP,
    max_attendees INTEGER,
    current_attendees INTEGER DEFAULT 0,
    ticket_price DECIMAL(10, 2) DEFAULT 0,
    image_url VARCHAR(500),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    website_url VARCHAR(500),
    is_free BOOLEAN DEFAULT 1,
    is_online BOOLEAN DEFAULT 0,
    is_featured BOOLEAN DEFAULT 0,
    is_published BOOLEAN DEFAULT 1,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES event_categories(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

CREATE TABLE event_registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    attendee_name VARCHAR(100),
    attendee_email VARCHAR(100),
    attendee_phone VARCHAR(20),
    number_of_tickets INTEGER DEFAULT 1,
    total_amount DECIMAL(10, 2),
    payment_status VARCHAR(20) DEFAULT 'pending', -- pending, paid, refunded
    registration_status VARCHAR(20) DEFAULT 'confirmed', -- confirmed, cancelled, waitlist
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(event_id, user_id)
);

-- ============================================
-- JOBS SYSTEM
-- ============================================

CREATE TABLE job_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(50)
);

CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    name_ar VARCHAR(200),
    logo_url VARCHAR(500),
    description TEXT,
    industry VARCHAR(100),
    company_size VARCHAR(50),
    website VARCHAR(500),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    governorate VARCHAR(100),
    is_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    title_ar VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    slug VARCHAR(255) UNIQUE NOT NULL,
    description_ar TEXT NOT NULL,
    description_en TEXT,
    requirements_ar TEXT,
    requirements_en TEXT,
    responsibilities_ar TEXT,
    responsibilities_en TEXT,
    employment_type VARCHAR(50) NOT NULL, -- full-time, part-time, contract, internship
    experience_level VARCHAR(50), -- entry, mid, senior, executive
    min_experience INTEGER, -- years
    max_experience INTEGER,
    min_salary DECIMAL(10, 2),
    max_salary DECIMAL(10, 2),
    salary_currency VARCHAR(10) DEFAULT 'OMR',
    salary_period VARCHAR(20) DEFAULT 'monthly', -- monthly, yearly
    location VARCHAR(200),
    city VARCHAR(100),
    governorate VARCHAR(100),
    is_remote BOOLEAN DEFAULT 0,
    application_deadline DATE,
    application_email VARCHAR(100),
    application_url VARCHAR(500),
    views_count INTEGER DEFAULT 0,
    applications_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    is_featured BOOLEAN DEFAULT 0,
    posted_by INTEGER,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (category_id) REFERENCES job_categories(id),
    FOREIGN KEY (posted_by) REFERENCES users(id)
);

CREATE TABLE job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    applicant_name VARCHAR(100) NOT NULL,
    applicant_email VARCHAR(100) NOT NULL,
    applicant_phone VARCHAR(20),
    cover_letter TEXT,
    resume_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending', -- pending, reviewed, shortlisted, rejected, hired
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(job_id, user_id)
);

-- ============================================
-- MARKETPLACE SYSTEM
-- ============================================

CREATE TABLE marketplace_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    parent_id INTEGER,
    icon VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    FOREIGN KEY (parent_id) REFERENCES marketplace_categories(id)
);

CREATE TABLE marketplace_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    title_ar VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    slug VARCHAR(255) UNIQUE NOT NULL,
    description_ar TEXT NOT NULL,
    description_en TEXT,
    price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'OMR',
    condition VARCHAR(20), -- new, like-new, good, fair
    location VARCHAR(200),
    city VARCHAR(100),
    governorate VARCHAR(100),
    is_negotiable BOOLEAN DEFAULT 1,
    is_featured BOOLEAN DEFAULT 0,
    is_sold BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    views_count INTEGER DEFAULT 0,
    favorites_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES marketplace_categories(id),
    FOREIGN KEY (seller_id) REFERENCES users(id)
);

CREATE TABLE marketplace_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    display_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT 0,
    FOREIGN KEY (listing_id) REFERENCES marketplace_listings(id) ON DELETE CASCADE
);

-- ============================================
-- TOURISM SYSTEM
-- ============================================

CREATE TABLE tourism_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(50)
);

CREATE TABLE tourism_places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name_ar VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    slug VARCHAR(255) UNIQUE NOT NULL,
    description_ar TEXT NOT NULL,
    description_en TEXT,
    governorate VARCHAR(100),
    city VARCHAR(100),
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    opening_hours TEXT,
    entry_fee DECIMAL(10, 2) DEFAULT 0,
    contact_phone VARCHAR(20),
    website_url VARCHAR(500),
    rating DECIMAL(3, 2) DEFAULT 0,
    reviews_count INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES tourism_categories(id)
);

CREATE TABLE tourism_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    caption_ar VARCHAR(255),
    caption_en VARCHAR(255),
    display_order INTEGER DEFAULT 0,
    is_primary BOOLEAN DEFAULT 0,
    FOREIGN KEY (place_id) REFERENCES tourism_places(id) ON DELETE CASCADE
);

CREATE TABLE tourism_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    review_text TEXT,
    visit_date DATE,
    is_verified BOOLEAN DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES tourism_places(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(place_id, user_id)
);

-- ============================================
-- RECIPES SYSTEM
-- ============================================

CREATE TABLE recipe_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(50)
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    author_id INTEGER,
    title_ar VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    slug VARCHAR(255) UNIQUE NOT NULL,
    description_ar TEXT,
    description_en TEXT,
    ingredients_ar TEXT NOT NULL,
    ingredients_en TEXT,
    instructions_ar TEXT NOT NULL,
    instructions_en TEXT,
    prep_time INTEGER, -- minutes
    cook_time INTEGER, -- minutes
    servings INTEGER,
    difficulty VARCHAR(20), -- easy, medium, hard
    image_url VARCHAR(500),
    video_url VARCHAR(500),
    rating DECIMAL(3, 2) DEFAULT 0,
    reviews_count INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    favorites_count INTEGER DEFAULT 0,
    is_traditional BOOLEAN DEFAULT 0,
    is_featured BOOLEAN DEFAULT 0,
    is_published BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES recipe_categories(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- ============================================
-- EDUCATION SYSTEM
-- ============================================

CREATE TABLE education_institutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(200) NOT NULL,
    name_en VARCHAR(200),
    type VARCHAR(50), -- university, college, school, institute
    governorate VARCHAR(100),
    city VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(500),
    logo_url VARCHAR(500),
    description_ar TEXT,
    description_en TEXT,
    is_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE education_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institution_id INTEGER NOT NULL,
    name_ar VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    degree_level VARCHAR(50), -- bachelor, master, doctorate, diploma
    field_of_study VARCHAR(100),
    duration_years DECIMAL(3, 1),
    description_ar TEXT,
    description_en TEXT,
    requirements_ar TEXT,
    requirements_en TEXT,
    tuition_fee DECIMAL(10, 2),
    application_deadline DATE,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (institution_id) REFERENCES education_institutions(id)
);

-- ============================================
-- BUSINESS DIRECTORY
-- ============================================

CREATE TABLE business_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    parent_id INTEGER,
    icon VARCHAR(50),
    FOREIGN KEY (parent_id) REFERENCES business_categories(id)
);

CREATE TABLE businesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    owner_id INTEGER,
    name_ar VARCHAR(200) NOT NULL,
    name_en VARCHAR(200),
    slug VARCHAR(255) UNIQUE NOT NULL,
    description_ar TEXT,
    description_en TEXT,
    logo_url VARCHAR(500),
    cover_image_url VARCHAR(500),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(500),
    address TEXT,
    city VARCHAR(100),
    governorate VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    opening_hours TEXT,
    rating DECIMAL(3, 2) DEFAULT 0,
    reviews_count INTEGER DEFAULT 0,
    views_count INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT 0,
    is_featured BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES business_categories(id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE business_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    review_text TEXT,
    is_verified BOOLEAN DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ============================================
-- COMMUNITY FEATURES
-- ============================================

CREATE TABLE forum_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description_ar TEXT,
    description_en TEXT,
    icon VARCHAR(50),
    display_order INTEGER DEFAULT 0
);

CREATE TABLE forum_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    title_ar VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    slug VARCHAR(255) UNIQUE NOT NULL,
    content_ar TEXT NOT NULL,
    content_en TEXT,
    views_count INTEGER DEFAULT 0,
    replies_count INTEGER DEFAULT 0,
    is_pinned BOOLEAN DEFAULT 0,
    is_locked BOOLEAN DEFAULT 0,
    is_published BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES forum_categories(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE forum_replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    parent_reply_id INTEGER,
    content TEXT NOT NULL,
    likes_count INTEGER DEFAULT 0,
    is_solution BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES forum_topics(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_reply_id) REFERENCES forum_replies(id)
);

-- ============================================
-- WEATHER DATA
-- ============================================

CREATE TABLE weather_locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_ar VARCHAR(100) NOT NULL,
    city_en VARCHAR(100) NOT NULL,
    governorate_ar VARCHAR(100),
    governorate_en VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_default BOOLEAN DEFAULT 0
);

CREATE TABLE weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    temperature DECIMAL(5, 2),
    feels_like DECIMAL(5, 2),
    humidity INTEGER,
    wind_speed DECIMAL(5, 2),
    pressure INTEGER,
    visibility INTEGER,
    weather_condition VARCHAR(50),
    weather_description_ar VARCHAR(100),
    weather_description_en VARCHAR(100),
    icon VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES weather_locations(id)
);

-- ============================================
-- NOTIFICATIONS SYSTEM
-- ============================================

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type VARCHAR(50) NOT NULL, -- news, event, job, message, etc.
    title_ar VARCHAR(255),
    title_en VARCHAR(255),
    content_ar TEXT,
    content_en TEXT,
    link_url VARCHAR(500),
    is_read BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- ENGAGEMENT TRACKING
-- ============================================

CREATE TABLE user_favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_type VARCHAR(50) NOT NULL, -- article, event, job, recipe, place, etc.
    item_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, item_type, item_id)
);

CREATE TABLE user_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_type VARCHAR(50) NOT NULL,
    item_id INTEGER NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    item_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    parent_comment_id INTEGER,
    likes_count INTEGER DEFAULT 0,
    is_approved BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_comment_id) REFERENCES comments(id) ON DELETE CASCADE
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_news_articles_category ON news_articles(category_id);
CREATE INDEX idx_news_articles_published ON news_articles(is_published, published_at);
CREATE INDEX idx_events_dates ON events(start_date, end_date);
CREATE INDEX idx_events_category ON events(category_id);
CREATE INDEX idx_jobs_category ON jobs(category_id);
CREATE INDEX idx_jobs_company ON jobs(company_id);
CREATE INDEX idx_jobs_active ON jobs(is_active, posted_at);
CREATE INDEX idx_marketplace_category ON marketplace_listings(category_id);
CREATE INDEX idx_marketplace_seller ON marketplace_listings(seller_id);
CREATE INDEX idx_marketplace_active ON marketplace_listings(is_active, is_sold);
CREATE INDEX idx_tourism_category ON tourism_places(category_id);
CREATE INDEX idx_recipes_category ON recipes(category_id);
CREATE INDEX idx_recipes_author ON recipes(author_id);
CREATE INDEX idx_businesses_category ON businesses(category_id);
CREATE INDEX idx_forum_topics_category ON forum_topics(category_id);
CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX idx_user_favorites_user ON user_favorites(user_id);
CREATE INDEX idx_comments_item ON comments(item_type, item_id);

-- ============================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- ============================================

-- Update timestamps on user changes
CREATE TRIGGER update_users_timestamp 
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Update timestamps on article changes
CREATE TRIGGER update_news_articles_timestamp 
AFTER UPDATE ON news_articles
FOR EACH ROW
BEGIN
    UPDATE news_articles SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Update timestamps on event changes
CREATE TRIGGER update_events_timestamp 
AFTER UPDATE ON events
FOR EACH ROW
BEGIN
    UPDATE events SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Update timestamps on job changes
CREATE TRIGGER update_jobs_timestamp 
AFTER UPDATE ON jobs
FOR EACH ROW
BEGIN
    UPDATE jobs SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;
