import pickle
from flask import Flask, flash, redirect, render_template, request, session, url_for
import numpy as np
import tempfile
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Use environment variable for secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement your user creation logic here
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Implement your authentication logic here
        session['username'] = username
        session['user_authenticated'] = True
        return redirect(url_for('profile'))
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_authenticated', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('user_info/profile.html', username=username)
    else:
        return redirect(url_for('login'))
@app.route('/new_purchasing')
def new_purchasing():
    return render_template('services/new_purchasing.html')  # Use a specific template if available

@app.route('/settings')
def settings():
    return render_template('user_info/settings.html')  # Use a specific template if available


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    # Implement your search logic here
    return render_template('search_results.html', query=query)

@app.route('/service')
def service():
    return render_template('service.html')  # Use a specific template if available

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Use a specific template if available



@app.route('/ready_construction')
def ready_construction():
    return render_template('services/ready_construction.html')  # Use a specific template if available

@app.route('/new_construction')
def new_construction():
    return render_template('services/new_construction.html')  # Use a specific template if available
@app.route('/property_listings')
def property_listings():
    return render_template('services/property_listings.html')
# Load the trained model and label encoders
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
        # Handle GET request (e.g., initial page load)
        prediction_text = 'Please submit the form to get predictions.'

    return render_template('index.html', prediction_text=prediction_text, temp_file_content=temp_file_content)

if __name__ == '__main__':
    app.run(debug=True)
