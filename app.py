from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages, jsonify
import sqlite3
import os
import uuid
from werkzeug.utils import secure_filename
import bcrypt
from functools import wraps
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
app.config['UPLOAD_FOLDER'] = 'static/uploaded'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------- Helper Functions ----------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Login required to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ---------- LOGIN ----------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# ---------- DASHBOARD ----------
@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images")
    images = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', images=images)

# ---------- UPLOAD IMAGE ----------
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        image = request.files['image']
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']

        if image and allowed_file(image.filename):
            unique_filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            image.save(filepath)

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO images (filename, title, description, category) VALUES (?, ?, ?, ?)",
                           (unique_filename, title, description, category))
            conn.commit()
            conn.close()

            flash('Image uploaded successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid file type. Please upload a valid image.', 'danger')
            return redirect(url_for('upload'))

    return render_template('upload.html')

# ---------- EDIT IMAGE ----------
@app.route('/edit/<int:image_id>', methods=['GET', 'POST'])
@login_required
def edit_image(image_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        cursor.execute("UPDATE images SET title = ?, description = ?, category = ? WHERE id = ?",
                       (title, description, category, image_id))
        conn.commit()
        conn.close()
        flash('Image updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    # GET request - show current data
    cursor.execute("SELECT * FROM images WHERE id = ?", (image_id,))
    image = cursor.fetchone()
    conn.close()
    return render_template('edit_image.html', image=image)

# ---------- DELETE IMAGE ----------
@app.route('/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM images WHERE id = ?", (image_id,))
        file = cursor.fetchone()
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file[0])
            if os.path.exists(filepath):
                os.remove(filepath)
        cursor.execute("DELETE FROM images WHERE id = ?", (image_id,))
        conn.commit()
        conn.close()
        flash('Image deleted successfully.', 'success')
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        logger.error(f"Error deleting image {image_id}: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

# ---------- FLASH MESSAGES AUTO-HIDE ----------
@app.context_processor
def utility_processor():
    return dict(flash_messages=get_flashed_messages(with_categories=True))

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
