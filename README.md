# House Price Prediction

Welcome to the House Price Prediction project! This Flask-based web application allows users to predict house prices based on various features such as the number of bedrooms, bathrooms, size, and location. The application utilizes machine learning models to provide accurate predictions and features a user-friendly interface for seamless interaction.

## Features

- **Predict House Prices:** Enter house details and get price predictions based on machine learning models.
- **User Authentication:** Secure login and signup functionality.
- **Logout:** Easily log out of the application.
- **Responsive Design:** User-friendly interface with responsive design for both desktop and mobile devices.
- **Location Selection:** Choose location names for better clarity and understanding.
- **Machine Learning Integration:** Utilizes Python-based machine learning models for accurate predictions.

## Technologies Used

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Flask
- **Machine Learning:** Python (scikit-learn, pandas)
- **Database:** SQLite (or any other database if used)
- **Other Technologies:** Jinja2 for templating

## Installation

To set up and run the House Price Prediction application locally, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/1Rohitmahajan/house_price_prediction.git
Navigate to the Project Directory:

bash
Copy code
cd house_price_prediction
Create and Activate a Virtual Environment:

bash
Copy code
python -m venv venv
# On Windows use:
venv\Scripts\activate
# On Linux/Mac use:
source venv/bin/activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Application:

bash
Copy code
python app.py
The application will be accessible at http://127.0.0.1:5000/ by default.

Pages and Functionality
1. Login Page
URL: /login
Description: Allows users to log in to their account. The page includes fields for entering username and password. Upon successful login, users are redirected to the home page or their profile.
2. Signup Page
URL: /signup
Description: Allows new users to create an account by providing a username, email, and password. After signup, users are redirected to the login page.
3. Logout
URL: /logout
Description: Logs the user out of the application and redirects them to the home page. This action clears the session and any user-specific data.
4. Prediction Page
URL: /predict
Description: Users can enter details about a house (e.g., number of bedrooms, bathrooms, size, location) to receive a price prediction. The page uses a machine learning model to generate and display the predicted house price.
5. Home Page
URL: /
Description: The main page of the application that may include navigation links to other pages, information about the project, and an overview of features.
Authentication
The application uses Flask sessions for authentication. Users need to log in to access certain pages. The authentication mechanism includes:

Login: Validate user credentials and start a session.
Signup: Register new users and store their credentials securely.
Logout: End the user session and clear session data.
Contributing
Contributions are welcome! If you would like to contribute to this project, please follow these steps:

Fork the Repository

Create a New Branch:

bash
Copy code
git checkout -b feature-branch
Make Your Changes and Commit Them:

bash
Copy code
git commit -am 'Add new feature'
Push to the Branch:

bash
Copy code
git push origin feature-branch
Create a Pull Request

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contact
For any questions or feedback, please reach out to Rohit Mahajan at rohitam35@gmail.com.
