import sqlite3
from datetime import datetime

def init_database():
    conn = sqlite3.connect('romantic_website.db')
    cursor = conn.cursor()
    
    # Create daily messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_name TEXT NOT NULL,
            image1_path TEXT NOT NULL,
            image2_path TEXT NOT NULL,
            image3_path TEXT NOT NULL,
            romantic_message TEXT NOT NULL
        )
    ''')
    
    # Create love letters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS love_letters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create memory boxes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_boxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            type TEXT NOT NULL,
            unlocked BOOLEAN DEFAULT 0,
            unlock_day INTEGER
        )
    ''')
    
    # Insert sample daily messages
    daily_messages = [
        ('Monday', 'static/img/monday1.jpg', 'static/img/monday2.jpg', 'static/img/monday3.jpg', 
         'Aapki muskurahat se mera Monday bhi Sunday jaisa lagta hai. Aap har din ko khaas banati hain.'),
        
        ('Tuesday', 'static/img/tuesday1.jpg', 'static/img/tuesday2.jpg', 'static/img/tuesday3.jpg',
         'Aapki yaadon ke bina Tuesday bhi ajeeb sa lagta hai. Aap mere har din ki roshni ho.'),
        
        ('Wednesday', 'static/img/wednesday1.jpg', 'static/img/wednesday2.jpg', 'static/img/wednesday3.jpg',
         'Beech ka din hai par aapki yaad hamesha mere dil mein hai. Aap mere liye poore hafte ki khushi ho.'),
        
        ('Thursday', 'static/img/thursday1.jpg', 'static/img/thursday2.jpg', 'static/img/thursday3.jpg',
         'Aapki aankhon mein jo pyaar hai, woh mere liye har din Thursday ko bhi khaas bana deta hai.'),
        
        ('Friday', 'static/img/friday1.jpg', 'static/img/friday2.jpg', 'static/img/friday3.jpg',
         'Aapke bina Friday bhi koi Friday nahi lagta. Aap meri har Friday date ho.'),
        
        ('Saturday', 'static/img/saturday1.jpg', 'static/img/saturday2.jpg', 'static/img/saturday3.jpg',
         'Saturday a gaya, par aapki yaad ka mausam to har din rehta hai. Aap meri weekend ki shuruaat ho.'),
        
        ('Sunday', 'static/img/sunday1.jpg', 'static/img/sunday2.jpg', 'static/img/sunday3.jpg',
         'Aapke bina Sunday bhi adhura lagta hai. Aap meri har Sunday ki subah ki pehli kiran ho.')
    ]
    
    cursor.executemany('''
        INSERT INTO daily_messages (day_name, image1_path, image2_path, image3_path, romantic_message)
        VALUES (?, ?, ?, ?, ?)
    ''', daily_messages)
    
    # Insert sample love letters
    love_letters = [
        ('Aapke Naam Khat', 
         '''Pyaari [Her Name],
         
Aaj phir aapki yaad aayi, aapki muskurahat ki tasveer mere dimaag mein ghoom rahi hai. Aapko dekhkar lagta hai jaise zindagi ki har khushi mere saamne khadi hai.

Aapki har ada, har baat, har lehar mere liye ek naya geet hai. Aapke bina har din adhura sa lagta hai, jaise kuch kho gaya ho.

Aap mere liye sirf ek pyaar nahi, aap to meri duaon ka jawab ho, meri har khwahish ka anjaam ho, meri zindagi ki sabse khoobsurat shuruaat ho.

Hamesha aapka,
[Your Name]'''),
        
        ('Aapki Yaad Ka Mausam',
         '''Meri Jaan,
         
Aaj bahar barish ho rahi hai, aur har boond aapki yaad le kar aa rahi hai. Aapki yaadon ke bina har mausam bejaan sa lagta hai.

Aapki aankhon mein woh jaadu hai jo mujhe har pal aapke kareeb khicha laata hai. Aapki hansi ki awaz mere liye sabse pyaari dhun hai.

Aap mere liye woh khushi ho jo har gum ko bhula deti hai, woh aas ho jo har andhere ko roshan kar deti hai.

Aapse pyaar karta hoon,
[Your Name]''')
    ]
    
    cursor.executemany('''
        INSERT INTO love_letters (title, content)
        VALUES (?, ?)
    ''', love_letters)
    
    # Insert memory boxes
    memory_boxes = [
        ('Pehli Mulaqat', 'static/img/first_meet.jpg', 'Woh pehla pal jab maine aapko dekha, meri duniya badal gayi. Aapki aankhon mein maine apna aaina dekha.', 'image', 0, 1),
        ('Aapki Muskurahat', 'Aapki muskurahat mere liye sabse khoobsurat tohfa hai. Iski chamak se meri poori duniya roshan ho jaati hai.', 'text', 0, 2),
        ('Pyaar Bhara Sandesh', 'Aap meri zindagi ki sabse khoobsurat kahani ho, aur main is kahani ka sabse khushnaseeb patra hoon.', 'text', 0, 3)
    ]
    
    cursor.executemany('''
        INSERT INTO memory_boxes (title, content, type, unlocked, unlock_day)
        VALUES (?, ?, ?, ?, ?)
    ''', memory_boxes)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()