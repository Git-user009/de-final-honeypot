import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Debugging: Print current working directory
print("Current working directory:", os.getcwd())

# Load processed logs
try:
    data = pd.read_csv('/home/kabangi/Desktop/de-final/ai-module/data/processed_logs/attack_data.csv')
    print("Processed logs loaded successfully.")
except FileNotFoundError:
    print("Error: Processed logs file not found. Please ensure 'attack_data.csv' exists in the 'processed_logs' folder.")
    exit(1)
except Exception as e:
    print(f"Error loading processed logs: {e}")
    exit(1)

# Check if the required columns exist
required_columns = ['src_ip', 'eventid', 'label']
if not all(column in data.columns for column in required_columns):
    print(f"Error: Processed logs are missing required columns. Expected: {required_columns}")
    print("Available columns:", data.columns)
    exit(1)

# Encode categorical features (e.g., 'src_ip' and 'eventid')
data['src_ip'] = data['src_ip'].astype('category').cat.codes
data['eventid'] = data['eventid'].astype('category').cat.codes

# Split into features (X) and labels (y)
X = data.drop('label', axis=1)  # Features
y = data['label']  # Labels (0 = normal, 1 = attack)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
print("Training the model...")
try:
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Model trained successfully.")
except Exception as e:
    print(f"Error training the model: {e}")
    exit(1)

# Test the model
print("Testing the model...")
try:
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", classification_report(y_test, y_pred))
except Exception as e:
    print(f"Error testing the model: {e}")
    exit(1)

# Save the trained model
try:
    model_path = '/home/kabangi/Desktop/de-final/ai-module/models/attack_detection_model.pkl'
    joblib.dump(model, model_path)
    print(f"Model saved successfully at {model_path}")
except Exception as e:
    print(f"Error saving the model: {e}")
    exit(1)