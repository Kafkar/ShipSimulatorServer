from flask_socketio import SocketIO
from datetime import datetime

COLOR_MAP = {
    'info': '\033[96m',  # Cyan
    'warning': '\033[93m',  # Yellow
    'error': '\033[91m',  # Red
    'success': '\033[92m',  # Green
    'reset': '\033[0m'  # Reset color
}

class Logger:
    def __init__(self, app):
        self.socketio = SocketIO(app)

    def emit_log(self, message, log_type='info'):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = COLOR_MAP.get(log_type, '')
        colored_message = f"{color}[{timestamp}] [{log_type.upper()}] {message}{COLOR_MAP['reset']}"
        print(colored_message)
        self.socketio.emit('debug_log', {'timestamp': timestamp, 'message': message, 'type': log_type})
