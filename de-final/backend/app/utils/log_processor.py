from .ai_model import AIModel
from ..models import AttackLog
from .. import db

class LogProcessor:
    def __init__(self, model_path):
        self.ai_model = AIModel(model_path)

    def process_log(self, log):
        # Classify the log
        attack_type = self.ai_model.classify_log(log)
        # Save to database
        attack_log = AttackLog(src_ip=log['src_ip'], timestamp=log['timestamp'], attack_type=attack_type)
        db.session.add(attack_log)
        db.session.commit()
        return attack_log