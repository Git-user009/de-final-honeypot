import pandas as pd
import joblib
import os

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Load the trained model
try:
    model_path = '/home/kabangi/Desktop/de-final/ai-module/models/attack_detection_model.pkl'
    model = joblib.load(model_path)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}. Please train the model first.")
    exit(1)
except Exception as e:
    print(f"Error loading the model: {e}")
    exit(1)

def preprocess_log(log_entry):
    # Convert log entry to DataFrame
    log_df = pd.DataFrame([log_entry])

    # Extract and encode features
    log_df['src_ip'] = log_df['src_ip'].astype('category').cat.codes
    log_df['eventid'] = log_df['eventid'].astype('category').cat.codes
    return log_df[['src_ip', 'eventid']]

def detect_attack(log_entry):
    # Preprocess the log entry
    features = preprocess_log(log_entry)

    # Predict using the trained model
    prediction = model.predict(features)
    return prediction[0]  # 0 = normal, 1 = attack

# Example usage
log_entry = {
    "src_ip": "192.168.1.100",
    "eventid": "cowrie.login.failed"
}

if detect_attack(log_entry) == 1:
    print(f"Attack detected from {log_entry['src_ip']}")
else:
    print(f"No attack detected from {log_entry['src_ip']}")