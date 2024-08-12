# import crypt
import pickle
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
import numpy as np
import tempfile
import os
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,EmailField
from wtforms.validators import DataRequired,Email,ValidationError
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Use environment variable for secret key

class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])    
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])    
    submit = SubmitField("Signup")


@app.route('/')
def index():
    return render_template('index.html')

def get_db_connection():
    """Establish and return a database connection"""
    conn = sqlite3.connect(os.path.join('data', 'users.db'))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('auth/signup.html', form=form)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            with get_db_connection() as conn:
                c = conn.cursor()
                c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                          (name, email, hashed_password))
                conn.commit()
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please choose a different email.', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')

    return render_template('auth/signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with get_db_connection() as conn:
                c = conn.cursor()
                c.execute("SELECT password FROM users WHERE email = ?", (email,))
                result = c.fetchone()
                
                if result and check_password_hash(result[0], password):
                    session['email'] = email
                    session['user_authenticated'] = True
                    return redirect(url_for('profile'))
                else:
                    flash('Invalid email or password. Please try again.', 'danger')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('user_authenticated', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'email' in session:
        email = session['email']
        return render_template('user_info/profile.html', email=email)
    else:
        return redirect(url_for('login'))
@app.route('/new_purchasing')
def new_purchasing():
    return render_template('services/new_purchasing.html')  # plate if available

@app.route('/settings')
def settings():
    return render_template('user_info/settings.html')  


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    return render_template('search_results.html', query=query)

@app.route('/service')
def service():
    return render_template('service.html')  

@app.route('/contact')
def contact():
    return render_template('contact.html') 



@app.route('/ready_construction')
def ready_construction():
    return render_template('services/ready_construction.html') 

@app.route('/new_construction')
def new_construction():
    return render_template('services/new_construction.html')  
@app.route('/property_listings')
def property_listings():
    return render_template('services/property_listings.html')
# Load the trained model  encoders
model_path = 'model/model.pkl'
encoders_path = 'model/label_encoders.pkl'

try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    with open(encoders_path, 'rb') as file:
        label_encoders = pickle.load(file)
except Exception as e:
    print(f"Error loading model or encoders: {e}")
    model = None
    label_encoders = None

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction_text = ''
    temp_file_content = ''
    temp_file_path = ''  # Initialize to empty string

    if request.method == 'POST':
        if model is None or label_encoders is None:
            return render_template('index.html', prediction_text='Model or encoders not available.')

        try:
            # Get input features from the form
            area = float(request.form['area'])
            bedrooms = float(request.form['bedrooms'])
            bathrooms = float(request.form['bathrooms'])
            stories = float(request.form['stories'])
            mainroad = 1 if request.form['mainroad'] == 'yes' else 0
            guestroom = 1 if request.form['guestroom'] == 'yes' else 0
            basement = 1 if request.form['basement'] == 'yes' else 0
            hotwaterheating = 1 if request.form['hotwaterheating'] == 'yes' else 0
            airconditioning = 1 if request.form['airconditioning'] == 'yes' else 0
            parking = float(request.form['parking'])
            prefarea = 1 if request.form['prefarea'] == 'yes' else 0
            furnishingstatus = request.form['furnishingstatus']

            # Convert categorical feature
            furnishingstatus = label_encoders['furnishingstatus'].transform([furnishingstatus])[0]

            # Convert features to numpy array and reshape for prediction
            features = np.array([[area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea, furnishingstatus]])
            prediction = model.predict(features)

            # Convert the prediction to INR
            predicted_price_inr = prediction[0] 

            # Format the prediction text
            prediction_text = 'Estimated House Price: ₹ {:.2f}'.format(predicted_price_inr)

            # Save inputs to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='') as temp_file:
                temp_file.write(f'Area: {area}\n')
                temp_file.write(f'Bedrooms: {bedrooms}\n')
                temp_file.write(f'Bathrooms: {bathrooms}\n')
                temp_file.write(f'Stories: {stories}\n')
                temp_file.write(f'Mainroad: {mainroad}\n')
                temp_file.write(f'Guestroom: {guestroom}\n')
                temp_file.write(f'Basement: {basement}\n')
                temp_file.write(f'Hotwaterheating: {hotwaterheating}\n')
                temp_file.write(f'Airconditioning: {airconditioning}\n')
                temp_file.write(f'Parking: {parking}\n')
                temp_file.write(f'Prefarea: {prefarea}\n')
                temp_file.write(f'Furnishingstatus: {furnishingstatus}\n')
                temp_file_path = temp_file.name

            # Read the temporary file content
            with open(temp_file_path, 'r') as file:
                temp_file_content = file.read()

            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        except Exception as e:
            prediction_text = f'Error: {str(e)}'

    elif request.method == 'GET':
        prediction_text = 'Please submit the form to get predictions.'

    return render_template('index.html', prediction_text=prediction_text, temp_file_content=temp_file_content)

if __name__ == '__main__':
    app.run(debug=True)
