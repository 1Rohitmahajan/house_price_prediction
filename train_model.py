from sklearn.linear_model import LinearRegression
import pickle
import numpy as np

# Example training data
X_train = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
y_train = np.array([1, 2, 3])

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
with open('model/model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model trained and saved successfully.")
