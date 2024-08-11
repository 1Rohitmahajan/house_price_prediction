import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('housing.csv')

# Initialize label encoders for categorical features
label_encoders = {}
categorical_columns = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']

# Encode categorical variables
for column in categorical_columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Feature selection
X = df[['area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea', 'furnishingstatus']]
y = df['price']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple Linear Regression model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Evaluate the model
predictions = regressor.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Save the model and label encoders
model_dir = 'model'
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'model.pkl')
encoders_path = os.path.join(model_dir, 'label_encoders.pkl')

with open(model_path, 'wb') as model_file:
    pickle.dump(regressor, model_file)
    print("Model saved successfully.")

with open(encoders_path, 'wb') as encoders_file:
    pickle.dump(label_encoders, encoders_file)
    print("Label encoders saved successfully.")
