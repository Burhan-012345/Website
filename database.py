import sqlite3
import os
from datetime import datetime
from flask import g

class RomanticDatabase:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        app.teardown_appcontext(self.close_connection)
    
    def get_connection(self):
        if 'db_connection' not in g:
            g.db_connection = sqlite3.connect(
                self.app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db_connection.row_factory = sqlite3.Row
        return g.db_connection
    
    def close_connection(self, exception=None):
        connection = g.pop('db_connection', None)
        if connection is not None:
            connection.close()
    
    def init_database(self):
        """Initialize the database with all required tables and sample data"""
        connection = self.get_connection()
        
        try:
            # Enable foreign keys
            connection.execute('PRAGMA foreign_keys = ON')
            
            self.create_tables(connection)
            self.insert_sample_data(connection)
            
            connection.commit()
            print("✅ Romantic database initialized successfully!")
            
        except Exception as e:
            connection.rollback()
            print(f"❌ Error initializing database: {e}")
            raise
    
    def create_tables(self, connection):
        """Create all required tables for the romantic website"""
        
        # Daily messages with images table
        connection.execute('''
            CREATE TABLE IF NOT EXISTS daily_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_name TEXT NOT NULL UNIQUE,
                image1_path TEXT NOT NULL,
                image2_path TEXT NOT NULL,
                image3_path TEXT NOT NULL,
                romantic_message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Love letters table
        connection.execute('''
            CREATE TABLE IF NOT EXISTS love_letters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'romantic',
                is_favorite BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Memory boxes table
        connection.execute('''
            CREATE TABLE IF NOT EXISTS memory_boxes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                content TEXT NOT NULL,
                content_type TEXT NOT NULL, -- 'text', 'image', 'audio', 'combo'
                box_type TEXT NOT NULL, -- 'memory', 'surprise', 'dream', 'compliment'
                icon TEXT NOT NULL,
                is_locked BOOLEAN DEFAULT 1,
                is_special BOOLEAN DEFAULT 0,
                unlock_day INTEGER, -- Specific day to unlock
                unlock_chance REAL DEFAULT 0.3, -- Random chance to unlock
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Reasons I love you table
        connection.execute('''
            CREATE TABLE IF NOT EXISTS love_reasons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reason_number INTEGER NOT NULL,
                icon TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Quiz questions table
        connection.execute('''
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                correct_option CHAR(1) NOT NULL,
                points INTEGER DEFAULT 2,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Quiz results table
        connection.execute('''
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                result_message TEXT NOT NULL,
                min_score INTEGER NOT NULL,
                max_score INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User sessions table (for future enhancements)
        connection.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_token TEXT UNIQUE NOT NULL,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Romantic compliments table
        connection.execute('''
            CREATE TABLE IF NOT EXISTS romantic_compliments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compliment_text TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Special dates table
        connection.execute('''
            CREATE TABLE IF NOT EXISTS special_dates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_name TEXT NOT NULL,
                date_date TEXT NOT NULL, -- YYYY-MM-DD format
                description TEXT,
                importance_level INTEGER DEFAULT 1, -- 1-5 scale
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        print("✅ All tables created successfully!")
    
    def insert_sample_data(self, connection):
        """Insert sample romantic data into the database"""
        
        # Insert daily messages
        daily_messages = [
            (
                'Monday', 
                'static/img/monday1.jpg', 
                'static/img/monday2.jpg', 
                'static/img/monday3.jpg',
                'Aapki muskurahat se mera Monday bhi Sunday jaisa lagta hai. Aap har din ko khaas banati hain, aapke bina har din adhura lagta hai.'
            ),
            (
                'Tuesday',
                'static/img/tuesday1.jpg',
                'static/img/tuesday2.jpg',
                'static/img/tuesday3.jpg',
                'Aapki yaadon ke bina Tuesday bhi ajeeb sa lagta hai. Aap mere har din ki roshni ho, aapke saath har pal khaas ban jaata hai.'
            ),
            (
                'Wednesday',
                'static/img/wednesday1.jpg',
                'static/img/wednesday2.jpg',
                'static/img/wednesday3.jpg',
                'Beech ka din hai par aapki yaad hamesha mere dil mein hai. Aap mere liye poore hafte ki khushi ho, aapke pyaar ne meri zindagi badal di.'
            ),
            (
                'Thursday',
                'static/img/thursday1.jpg',
                'static/img/thursday2.jpg',
                'static/img/thursday3.jpg',
                'Aapki aankhon mein jo pyaar hai, woh mere liye har din Thursday ko bhi khaas bana deta hai. Aap bin har din bemaani sa lagta hai.'
            ),
            (
                'Friday',
                'static/img/friday1.jpg',
                'static/img/friday2.jpg',
                'static/img/friday3.jpg',
                'Aapke bina Friday bhi koi Friday nahi lagta. Aap meri har Friday date ho, aapke saath bitaya har pal sona hai.'
            ),
            (
                'Saturday',
                'static/img/saturday1.jpg',
                'static/img/saturday2.jpg',
                'static/img/saturday3.jpg',
                'Saturday a gaya, par aapki yaad ka mausam to har din rehta hai. Aap meri weekend ki shuruaat ho, aapke saath har din celebration hai.'
            ),
            (
                'Sunday',
                'static/img/sunday1.jpg',
                'static/img/sunday2.jpg',
                'static/img/sunday3.jpg',
                'Aapke bina Sunday bhi adhura lagta hai. Aap meri har Sunday ki subah ki pehli kiran ho, aapki mohabbat meri har subah ko roshan karti hai.'
            )
        ]
        
        connection.executemany('''
            INSERT OR REPLACE INTO daily_messages 
            (day_name, image1_path, image2_path, image3_path, romantic_message)
            VALUES (?, ?, ?, ?, ?)
        ''', daily_messages)
        
        # Insert love letters
        love_letters = [
            (
                'Aapke Naam Pyaar Bhara Khat',
                '''Pyaari [Her Name],

Aaj phir aapki yaad aayi, aapki muskurahat ki tasveer mere dimaag mein ghoom rahi hai. Aapko dekhkar lagta hai jaise zindagi ki har khushi mere saamne khadi hai.

Aapki har ada, har baat, har lehar mere liye ek naya geet hai. Aapke bina har din adhura sa lagta hai, jaise kuch kho gaya ho.

Aap mere liye sirf ek pyaar nahi, aap to meri duaon ka jawab ho, meri har khwahish ka anjaam ho, meri zindagi ki sabse khoobsurat shuruaat ho.

Aapki har yaad dil ko chhoo jaati hai, aapki har baat dil ko sukoon deti hai. Aap bin yeh zindagi adhoori hai, aapke saath har pal poora lagta hai.

Hamesha aapka,
Forever Your's 💖'''
            ),
            (
                'Aapki Yaadon Ka Mausam',
                '''Meri Jaan,

Aaj bahar barish ho rahi hai, aur har boond aapki yaad le kar aa rahi hai. Aapki yaadon ke bina har mausam bejaan sa lagta hai.

Aapki aankhon mein woh jaadu hai jo mujhe har pal aapke kareeb khicha laata hai. Aapki hansi ki awaz mere liye sabse pyaari dhun hai.

Aap mere liye woh khushi ho jo har gum ko bhula deti hai, woh aas ho jo har andhere ko roshan kar deti hai.

Kabhi kabhi lagta hai ki aapko paana meri zindagi ki sabse badi kamiyabi hai. Aapke saath bitaya har pal mere liye anmol hai.

Aapse pyaar karna meri zindagi ka sabse khoobsurat faisla tha, aur aaj bhi hai, aur hamesha rahega...

Aapse pyaar karta hoon,
Forever Your's 🌹'''
            ),
            (
                'Mere Dil Ki Dhadkan',
                '''Meri Mohabbat,

Aaj phir aapki yaad ne mujhe jagaya, aapki muskurahat ne meri duniya roshan kar di. Aapke bina har pal adhura lagta hai.

Aapki har baat dil ko chhoo jaati hai, aapki har nazar dil ko sukoon deti hai. Aap bin yeh zindagi bemaani si lagti hai.

Aap ho meri har khushi ka sabaab, aap ho meri har muskurahat ki wajah. Aapke saath har pal khaas ban jaata hai.

Main dua karta hoon ki aap hamesha khush rahein, aapki zindagi mein har khushi aaye. Aap mere liye sabse khaas ho.

Aapki yaadon ke saath,
Forever Your's 💫'''
            ),
            (
                'Aapki Aankhon Mein Base Ho',
                '''Meri Duniya,

Aapki aankhon mein jo pyaar hai, woh mere liye sab kuch hai. Aapki har nazar mere dil ko sukoon deti hai.

Aapki muskurahat meri duniya ki sabse khoobsurat cheez hai, aapki har ada mere liye ek naya pyaar hai.

Aap bin yeh zindagi adhoori hai, aapke saath har pal poora lagta hai. Aap mere liye sabse khaas ho.

Main chahta hoon ki aap hamesha mere saath rahein, aapki har khushi mein saath rahun. Aap meri zindagi ki sabse khoobsurat haqeeqat ho.

Aapke pyaar ke saath,
Forever Your's 🌟'''
            )
        ]
        
        connection.executemany('''
            INSERT INTO love_letters (title, content)
            VALUES (?, ?)
        ''', love_letters)
        
        # Insert memory boxes
        memory_boxes = [
            (
                'Pehli Mulaqat',
                'Woh khoobsurat din jab hum mile the',
                'static/img/first_meet.jpg',
                'image',
                'memory',
                '💫',
                0,  # unlocked
                1   # special
            ),
            (
                'Aapki Muskurahat',
                'Meri duniya ki sabse khoobsurat cheez',
                'Aapki muskurahat mere liye sabse khoobsurat tohfa hai. Jab aap muskurate hain, lagta hai jaise poori duniya roshan ho gayi hai. Aapki har muskurahat mere dil ko chhoo jaati hai, har hansi meri duniya ko khushiyon se bhar deti hai.',
                'text',
                'compliment',
                '😊',
                0,  # unlocked
                0   # not special
            ),
            (
                'Pyaar Bhari Raatein',
                'Lamhe jo kabhi nahi bhoolenge',
                'static/img/night_memory.jpg',
                'image',
                'memory',
                '🌙',
                1,  # locked
                0   # not special
            ),
            (
                'Surprise Moments',
                'Anokhe pal jo dil ko chho gaye',
                'static/img/surprise_memory.jpg',
                'image',
                'surprise',
                '🎁',
                1,  # locked
                0   # not special
            ),
            (
                'Sapno Ki Udaan',
                'Humare shared dreams aur hopes',
                'Aapke saath bitane waale kal jaise humare sabse khoobsurat sapne hain. Har sapna aapke saath poora karna chahta hoon, har manzil aapke saath tay karna chahta hoon. Aap bin yeh sapne adhure hain.',
                'text',
                'dream',
                '🌈',
                1,  # locked
                1   # special
            ),
            (
                'Chhoti Chhoti Khushiyan',
                'Wo chhote pal jo bade hai',
                'static/img/small_joys.jpg',
                'image',
                'memory',
                '✨',
                1,  # locked
                0   # not special
            )
        ]
        
        connection.executemany('''
            INSERT INTO memory_boxes 
            (title, description, content, content_type, box_type, icon, is_locked, is_special)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', memory_boxes)
        
        # Insert love reasons
        love_reasons = [
            (1, '😊', 'Aapki Muskurahat', 'Aapki muskurahat dekhkar meri poori duniya roshan ho jaati hai. Woh pyaar bhali hansi mere dil ko chhoo jaati hai, har gum ko door kar deti hai.'),
            (2, '💖', 'Aapka Dil', 'Aapka dil itna saaf hai, itna pyaar se bhara hua hai. Aapki har baat, har ehsaas mein sachcha pyaar jhalakta hai.'),
            (3, '🌟', 'Aapki Soch', 'Aapki soch itni khoobsurat hai, aap har cheez ko itne pyaar se dekhti hain. Aapki har baat mein gehraai hoti hai.'),
            (4, '🤗', 'Aapka Sahara', 'Har mushkil waqt mein aapka sahana milna, aapka haath thamna... yeh sabse bada reason hai aapse pyaar karne ka.'),
            (5, '🎨', 'Aapki Kala', 'Aap har cheez ko itni khoobsurati se karti hain, jaise zindagi ek canvas ho aur aap uspe pyaar ki painting bana rahi hain.'),
            (6, '💫', 'Aapka Andaaz', 'Aapka baat karne ka andaaz, chalne ka tareeka, har cheez mein ek alag hi jaadu hai. Aapki har ada dil chura leti hai.'),
            (7, '🌹', 'Aapki Mohabbat', 'Aapki mohabbat mein woh jaadu hai jo har dard ko bhula deti hai, har pal ko khoobsurat bana deti hai.'),
            (8, '📚', 'Aapki Samajh', 'Aap har baat ko itni acchi tarah samajhti hain, aapki understanding mere liye sabse khoobsurat tohfa hai.'),
            (9, '🎵', 'Aapki Aawaz', 'Aapki aawaz mein woh madhurta hai jo dil ko sukoon deti hai, jaise koi pyaari si dhun ho.'),
            (10, '💝', 'Bas Aap Ho', 'Sabse bada reason yehi hai ki aap aap hain. Aapke andar woh sab kuch hai jo ek perfect partner mein hona chahiye.')
        ]
        
        connection.executemany('''
            INSERT INTO love_reasons (reason_number, icon, title, description)
            VALUES (?, ?, ?, ?)
        ''', love_reasons)
        
        # Insert quiz questions
        quiz_questions = [
            (
                'Pehli mulaqat mein aapko dekhkar mera pehla khayal kya tha?',
                '"Waah! Kitni khoobsurat hain!" 😍',
                '"Inse baat karni chahiye" 🤔',
                '"Yahi meri life partner hai" 💖',
                'A',
                2
            ),
            (
                'Aapki sabse pasandeed cheez mere andar kya hai?',
                'Aapki muskurahat 😊',
                'Aapka pyaar bhara vyavahar 🤗',
                'Aapka dekhne ka tareeka 💕',
                'A',
                2
            ),
            (
                'Humari relationship ki sabse khoobsurat baat kya hai?',
                'Ek dusre ki understanding 🤝',
                'Behad pyaar 💞',
                'Trust aur respect 🌟',
                'B',
                2
            ),
            (
                'Aapke liye meri sabse pyaari aadat kya hai?',
                'Aapki chai banane ki aadat ☕',
                'Regular call karna 📞',
                'Surprise dena 💝',
                'C',
                2
            ),
            (
                'Hum dono ka sapna kya hai?',
                'Ek sundar sa ghar banana 🏡',
                'Duniya ghumna 🌍',
                'Hamesha saath rehna 💑',
                'A',
                2
            )
        ]
        
        connection.executemany('''
            INSERT INTO quiz_questions 
            (question_text, option_a, option_b, option_c, correct_option, points)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', quiz_questions)
        
        # Insert quiz results
        quiz_results = [
            (10, 5, 'Waah! Aap to perfect couple ho! Aap dono ka pyaar dekhkar lagta hai jaise aap ek dusre ke liye hi bane ho. Aapki understanding aur pyaar sabse alag hai. Aap dono hamesha khush rahein! 💑', 8, 10),
            (7, 5, 'Bahut khoob! Aap dono ka rishta bahut gehara hai. Aap ek dusre ko acchi tarah samajhte hain aur aapka pyaar har roz badhta ja raha hai. Yeh rishta hamesha qayam rahe! 🌟', 6, 7),
            (5, 5, 'Achha score hai! Aap dono mein accha understanding hai. Thoda aur time dijiye, aap dono ka rishta aur bhi gehara ho jayega. Pyaar badhta rahe! 💕', 4, 5),
            (3, 5, 'Aap dono abhi ek dusre ko samajh rahe hain. Koi baat nahi, pyaar mein time lagta hai. Aap dono ka rishta zaroor age badhega! 🌹', 2, 3)
        ]
        
        connection.executemany('''
            INSERT INTO quiz_results 
            (score, total_questions, result_message, min_score, max_score)
            VALUES (?, ?, ?, ?, ?)
        ''', quiz_results)
        
        # Insert romantic compliments
        romantic_compliments = [
            ('Aap bohot pyaari hain 💖', 'general'),
            ('Aapki smile sabse khoobsurat hai 😊', 'smile'),
            ('Aap meri jaan hain 🌹', 'love'),
            ('Aapse hi mera har din behtar hota hai ✨', 'daily'),
            ('Aapki aankhon mein sara pyaar hai 👀', 'eyes'),
            ('Aap mere sapnon ki rani hain 👑', 'dreams'),
            ('Aapki har ada dil chura leti hai 💕', 'charm'),
            ('Aap bin meri duniya adhuri hai 🌍', 'completeness'),
            ('Aapki aawaz meri favorite dhun hai 🎵', 'voice'),
            ('Aap mere liye sabse khaas ho 💫', 'special')
        ]
        
        connection.executemany('''
            INSERT INTO romantic_compliments (compliment_text, category)
            VALUES (?, ?)
        ''', romantic_compliments)
        
        # Insert special dates
        special_dates = [
            ('Pehli Mulaqat', '2008-09-16', 'Woh khoobsurat din jab hum pehli baar mile the', 5),
            ('Pehli Date', '2008-10-01', 'Humari pehli official date', 4),
            ('Relationship Anniversary', '2009-01-01', 'Official relationship start date', 5),
            ('Aapka Birthday', '1990-03-15', 'Meri jaan ka janamdin', 5),
            ('Mera Birthday', '1989-07-20', 'Mera janamdin', 3)
        ]
        
        connection.executemany('''
            INSERT INTO special_dates (date_name, date_date, description, importance_level)
            VALUES (?, ?, ?, ?)
        ''', special_dates)
        
        print("✅ Sample data inserted successfully!")
    
    # Database query methods
    
    def get_daily_message(self, day_name):
        """Get daily message and images for specific day"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM daily_messages WHERE day_name = ?',
            (day_name,)
        )
        return cursor.fetchone()
    
    def get_random_love_letter(self):
        """Get a random love letter"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM love_letters ORDER BY RANDOM() LIMIT 1'
        )
        return cursor.fetchone()
    
    def get_love_letter_by_id(self, letter_id):
        """Get specific love letter by ID"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM love_letters WHERE id = ?',
            (letter_id,)
        )
        return cursor.fetchone()
    
    def get_memory_boxes(self, include_locked=False):
        """Get memory boxes, optionally including locked ones"""
        connection = self.get_connection()
        if include_locked:
            cursor = connection.execute(
                'SELECT * FROM memory_boxes ORDER BY is_locked, id'
            )
        else:
            cursor = connection.execute(
                'SELECT * FROM memory_boxes WHERE is_locked = 0 ORDER BY id'
            )
        return cursor.fetchall()
    
    def get_memory_box_by_id(self, box_id):
        """Get specific memory box by ID"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM memory_boxes WHERE id = ?',
            (box_id,)
        )
        return cursor.fetchone()
    
    def unlock_memory_box(self, box_id):
        """Unlock a memory box"""
        connection = self.get_connection()
        connection.execute(
            'UPDATE memory_boxes SET is_locked = 0 WHERE id = ?',
            (box_id,)
        )
        connection.commit()
    
    def get_love_reasons(self):
        """Get all active love reasons"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM love_reasons WHERE is_active = 1 ORDER BY reason_number'
        )
        return cursor.fetchall()
    
    def get_quiz_questions(self):
        """Get all active quiz questions"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM quiz_questions WHERE is_active = 1 ORDER BY id'
        )
        return cursor.fetchall()
    
    def get_quiz_result(self, score):
        """Get quiz result message based on score"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM quiz_results WHERE ? BETWEEN min_score AND max_score ORDER BY min_score DESC LIMIT 1',
            (score,)
        )
        return cursor.fetchone()
    
    def get_random_compliment(self):
        """Get a random romantic compliment"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM romantic_compliments WHERE is_active = 1 ORDER BY RANDOM() LIMIT 1'
        )
        return cursor.fetchone()
    
    def get_special_dates(self):
        """Get all special dates"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM special_dates ORDER BY importance_level DESC, date_date'
        )
        return cursor.fetchall()
    
    def get_upcoming_special_dates(self, days=30):
        """Get special dates in the next specified days"""
        connection = self.get_connection()
        cursor = connection.execute('''
            SELECT * FROM special_dates 
            WHERE date(date_date) BETWEEN date('now') AND date('now', ?)
            ORDER BY date_date
        ''', (f'+{days} days',))
        return cursor.fetchall()
    
    def add_new_love_letter(self, title, content):
        """Add a new love letter to the database"""
        connection = self.get_connection()
        cursor = connection.execute(
            'INSERT INTO love_letters (title, content) VALUES (?, ?)',
            (title, content)
        )
        connection.commit()
        return cursor.lastrowid
    
    def add_new_memory_box(self, title, description, content, content_type, box_type, icon, is_special=False):
        """Add a new memory box to the database"""
        connection = self.get_connection()
        cursor = connection.execute('''
            INSERT INTO memory_boxes 
            (title, description, content, content_type, box_type, icon, is_special)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, content, content_type, box_type, icon, is_special))
        connection.commit()
        return cursor.lastrowid
    
    def mark_love_letter_favorite(self, letter_id, is_favorite=True):
        """Mark a love letter as favorite or unfavorite"""
        connection = self.get_connection()
        connection.execute(
            'UPDATE love_letters SET is_favorite = ? WHERE id = ?',
            (1 if is_favorite else 0, letter_id)
        )
        connection.commit()
    
    def get_favorite_love_letters(self):
        """Get all favorite love letters"""
        connection = self.get_connection()
        cursor = connection.execute(
            'SELECT * FROM love_letters WHERE is_favorite = 1 ORDER BY created_at DESC'
        )
        return cursor.fetchall()
    
    def get_todays_special(self):
        """Get today's special message or memory based on date"""
        today = datetime.now().strftime('%m-%d')
        connection = self.get_connection()
        
        # Check if today is a special date
        cursor = connection.execute('''
            SELECT * FROM special_dates 
            WHERE strftime('%m-%d', date_date) = ?
        ''', (today,))
        
        special_date = cursor.fetchone()
        if special_date:
            return {
                'type': 'special_date',
                'data': special_date,
                'message': f'Aaj hai {special_date["date_name"]}! {special_date["description"]}'
            }
        
        # If no special date, return random compliment
        compliment = self.get_random_compliment()
        return {
            'type': 'compliment',
            'data': compliment,
            'message': compliment['compliment_text'] if compliment else 'Aap aaj bhi utni hi khoobsurat hain! 💖'
        }
    
    def get_database_stats(self):
        """Get database statistics for admin panel"""
        connection = self.get_connection()
        
        stats = {}
        
        # Count love letters
        cursor = connection.execute('SELECT COUNT(*) as count FROM love_letters')
        stats['love_letters'] = cursor.fetchone()['count']
        
        # Count memory boxes
        cursor = connection.execute('SELECT COUNT(*) as count FROM memory_boxes')
        stats['memory_boxes'] = cursor.fetchone()['count']
        
        # Count unlocked memory boxes
        cursor = connection.execute('SELECT COUNT(*) as count FROM memory_boxes WHERE is_locked = 0')
        stats['unlocked_boxes'] = cursor.fetchone()['count']
        
        # Count love reasons
        cursor = connection.execute('SELECT COUNT(*) as count FROM love_reasons')
        stats['love_reasons'] = cursor.fetchone()['count']
        
        # Count special dates
        cursor = connection.execute('SELECT COUNT(*) as count FROM special_dates')
        stats['special_dates'] = cursor.fetchone()['count']
        
        return stats

# Create database instance
romantic_db = RomanticDatabase()

def init_db_command():
    """Initialize the database (can be called from Flask CLI)"""
    romantic_db.init_database()
    return "Database initialized successfully!"

if __name__ == '__main__':
    # Test the database initialization
    romantic_db.init_database()
    print("✅ Romantic website database is ready!")