from datetime import datetime, timedelta

def should_deactivate_conversation(updated_at: datetime, threshold_minutes=1):
    return (datetime.utcnow() - updated_at) > timedelta(minutes=threshold_minutes)
