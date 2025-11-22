from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from database import romantic_db
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)
app.secret_key = 'romantic_website_secret_key_2024'  # Change this to a secure secret key
app.config['DATABASE'] = 'romantic_website.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session lasts 7 days

# Initialize database with app
romantic_db.init_app(app)

# Check if user is authenticated
def is_authenticated():
    return session.get('authenticated', False)

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    return redirect(url_for('home'))

@app.route('/unlock', methods=['GET', 'POST'])
def unlock():
    if request.method == 'POST':
        try:
            data = request.get_json()
            password = data.get('password', '') if data else ''
            
            print(f"Password received: {password}")  # Debug log
            
            if password == '16-09-2008':
                session['authenticated'] = True
                session['unlock_time'] = datetime.now().isoformat()
                print("Unlock successful! Session set.")  # Debug log
                return jsonify({'success': True, 'message': 'Welcome to our romantic world! 💖'})
            else:
                print("Unlock failed: wrong password")  # Debug log
                return jsonify({'success': False, 'message': 'Invalid password. Please try again.'})
                
        except Exception as e:
            print(f"Unlock error: {e}")  # Debug log
            return jsonify({'success': False, 'message': 'Server error. Please try again.'})
    
    # If already authenticated, redirect to home
    if is_authenticated():
        return redirect(url_for('home'))
        
    return render_template('unlock.html')

@app.route('/loading')
def loading():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    return render_template('loading.html')

@app.route('/home')
def home():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    
    current_day = datetime.now().strftime('%A')
    
    # Get daily message and images
    daily_data = romantic_db.get_daily_message(current_day)
    
    # Get random love letter
    love_letter = romantic_db.get_random_love_letter()
    
    # Get today's special
    todays_special = romantic_db.get_todays_special()
    
    if daily_data:
        # Randomly select one of the three images
        images = [daily_data['image1_path'], daily_data['image2_path'], daily_data['image3_path']]
        selected_image = random.choice(images)
        romantic_message = daily_data['romantic_message']
    else:
        selected_image = 'static/img/placeholder1.jpg'
        romantic_message = "Aap har din mere liye khaas hain, aaj bhi aur hamesha bhi."
    
    return render_template('home.html', 
                         image=selected_image,
                         message=romantic_message,
                         love_letter=love_letter,
                         todays_special=todays_special,
                         now=datetime.now())

@app.route('/love_letter')
def love_letter():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    
    letter = romantic_db.get_random_love_letter()
    return render_template('love_letter.html', letter=letter, now=datetime.now())

@app.route('/love_letter/<int:letter_id>')
def specific_love_letter(letter_id):
    if not is_authenticated():
        return redirect(url_for('unlock'))
    
    letter = romantic_db.get_love_letter_by_id(letter_id)
    if not letter:
        return redirect(url_for('love_letter'))
    
    return render_template('love_letter.html', letter=letter, now=datetime.now())

@app.route('/reasons')
def reasons():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    return render_template('reasons.html')

@app.route('/star')
def star():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    return render_template('star.html')

@app.route('/gift')
def gift():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    return render_template('gift.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    
    if request.method == 'POST':
        answers = request.json
        score = calculate_quiz_score(answers)
        result = romantic_db.get_quiz_result(score)
        return jsonify({
            'score': score, 
            'message': result['result_message'] if result else generate_quiz_result(score)
        })
    
    return render_template('quiz.html')

@app.route('/memory')
def memory():
    if not is_authenticated():
        return redirect(url_for('unlock'))
    
    boxes = romantic_db.get_memory_boxes(include_locked=True)
    return render_template('memory.html', boxes=boxes)

@app.route('/unlock_memory/<int:box_id>')
def unlock_memory(box_id):
    if not is_authenticated():
        return redirect(url_for('unlock'))
    
    box = romantic_db.get_memory_box_by_id(box_id)
    if box and box['is_locked']:
        romantic_db.unlock_memory_box(box_id)
    
    return jsonify({
        'title': box['title'],
        'content': box['content'],
        'type': box['content_type']
    })

@app.route('/logout')
def logout():
    """Clear session and logout"""
    session.clear()
    return redirect(url_for('unlock'))

@app.route('/api/compliment')
def random_compliment():
    """API endpoint to get random compliment"""
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    compliment = romantic_db.get_random_compliment()
    return jsonify({
        'compliment': compliment['compliment_text'] if compliment else 'Aap bohot khoobsurat hain! 💖'
    })

@app.route('/api/special_dates')
def special_dates():
    """API endpoint to get special dates"""
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    dates = romantic_db.get_special_dates()
    return jsonify({
        'dates': [dict(date) for date in dates]
    })

@app.route('/api/database_stats')
def database_stats():
    """API endpoint to get database statistics"""
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    stats = romantic_db.get_database_stats()
    return jsonify(stats)

def calculate_quiz_score(answers):
    score = 0
    for answer in answers.values():
        if answer in ['a', 'A']:
            score += 2
        elif answer in ['b', 'B']:
            score += 1
    return min(score, 10)

def generate_quiz_result(score):
    messages = {
        8: "Aap mere liye sab kuch ho! Aapki har ada, har baat, har muskurahat meri duniya ko roshan karti hai.",
        6: "Aap meri jaan ho, aur main aapke bina soch bhi nahi sakta. Aapse pyaar har roz badhta hai.",
        4: "Aapki mohabbat meri zindagi ki sabse khoobsurat cheez hai. Main aapko hamesha pyaar karta rahunga.",
        2: "Aapse milkar meri zindagi ko nayi roshni mili hai. Aap mere liye bahut khaas ho."
    }
    
    for threshold, message in messages.items():
        if score >= threshold:
            return message
    return "Aap meri duniya ho, aur main aapke saath har pal jeena chahta hoon."

# CLI command to initialize database
@app.cli.command('init-db')
def init_db_command():
    """Initialize the database."""
    romantic_db.init_database()
    print("Initialized the database.")

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(app.config['DATABASE']):
        with app.app_context():
            romantic_db.init_database()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
