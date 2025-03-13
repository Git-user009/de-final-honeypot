import pandas as pd
import os

# Print current working directory for debugging
print("Current working directory:", os.getcwd())

# Load raw logs
try:
    logs = pd.read_json('/home/kabangi/Desktop/de-final/ai-module/data/raw_logs/cowrie.json', lines=True)
    print("Raw logs loaded successfully.")
except FileNotFoundError:
    print("Error: Raw logs file not found. Please ensure 'cowrie.json' exists in the 'raw_logs' folder.")
    exit(1)
except Exception as e:
    print(f"Error loading raw logs: {e}")
    exit(1)

# Print available columns for debugging
print("Available columns:", logs.columns)

# Check if the required columns exist
required_columns = ['src_ip', 'eventid']
if not all(column in logs.columns for column in required_columns):
    print(f"Error: Raw logs are missing required columns. Expected: {required_columns}")
    exit(1)

# Create a new DataFrame for features to avoid SettingWithCopyWarning
features = logs[['src_ip', 'eventid']].copy()

# Add a label column (1 = attack, 0 = normal)
features['label'] = logs['eventid'].apply(lambda x: 1 if 'cowrie.login.failed' in x or 'cowrie.session.closed' in x else 0)

# Save processed logs
try:
    features.to_csv('/home/kabangi/Desktop/de-final/ai-module/data/processed_logs/attack_data.csv', index=False)
    print("Processed logs saved successfully.")
except Exception as e:
    print(f"Error saving processed logs: {e}")
    exit(1)