import joblib

class AIModel:
    def __init__(self, model_path):
        try:
            self.model = joblib.load(model_path)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def classify_log(self, log):
        # Preprocess the log (e.g., extract features like src_ip, eventid)
        features = self.preprocess_log(log)
        # Predict using the model
        prediction = self.model.predict([features])
        return prediction[0]

    def preprocess_log(self, log):
        # Example: Convert log to feature vector
        return [log['src_ip'], log['eventid']]