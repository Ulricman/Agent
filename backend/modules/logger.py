import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    def __init__(self, log_file: str = "data/system.log"):
        self.log_file = log_file
        self.json_log_file = "data/system_log.json"
        
        # Ensure log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Setup standard logger
        self.logger = logging.getLogger("TaxSystem")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def log_info(self, message: str, extra_data: Dict[str, Any] = None):
        """Log info level message with structured data"""
        self.logger.info(message)
        self._log_structured("INFO", message, extra_data)

    def log_warning(self, message: str, extra_data: Dict[str, Any] = None):
        """Log warning level message with structured data"""
        self.logger.warning(message)
        self._log_structured("WARNING", message, extra_data)

    def log_error(self, message: str, extra_data: Dict[str, Any] = None):
        """Log error level message with structured data"""
        self.logger.error(message)
        self._log_structured("ERROR", message, extra_data)

    def log_debug(self, message: str, extra_data: Dict[str, Any] = None):
        """Log debug level message with structured data"""
        self.logger.debug(message)
        self._log_structured("DEBUG", message, extra_data)

    def _log_structured(self, level: str, message: str, extra_data: Dict[str, Any] = None):
        """Log structured data to JSON file"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "level": level,
                "message": message,
                "extra_data": extra_data or {}
            }
            
            # Load existing logs
            logs = []
            if os.path.exists(self.json_log_file):
                try:
                    with open(self.json_log_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Ensure data is a list
                        if isinstance(data, list):
                            logs = data
                        else:
                            # If it's not a list, start fresh
                            logs = []
                except (json.JSONDecodeError, TypeError):
                    logs = []
            
            # Add new log entry
            logs.append(log_entry)
            
            # Keep only last 10000 entries to prevent file from getting too large
            if len(logs) > 10000:
                logs = logs[-10000:]
            
            # Save logs
            with open(self.json_log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            # Fallback to standard logger if JSON logging fails
            self.logger.error(f"Failed to write structured log: {e}")

    def get_recent_logs(self, count: int = 100) -> list:
        """Get recent log entries"""
        try:
            if not os.path.exists(self.json_log_file):
                return []
            
            with open(self.json_log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure data is a list
                if isinstance(data, list):
                    logs = data
                else:
                    return []
            
            return logs[-count:] if len(logs) > count else logs
            
        except Exception as e:
            self.logger.error(f"Failed to read logs: {e}")
            return []

    def get_logs_by_level(self, level: str) -> list:
        """Get logs filtered by level"""
        try:
            if not os.path.exists(self.json_log_file):
                return []
            
            with open(self.json_log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure data is a list
                if isinstance(data, list):
                    logs = data
                else:
                    return []
            
            return [log for log in logs if log.get('level') == level.upper()]
            
        except Exception as e:
            self.logger.error(f"Failed to filter logs: {e}")
            return []

    def clear_logs(self):
        """Clear all logs"""
        try:
            if os.path.exists(self.json_log_file):
                os.remove(self.json_log_file)
            self.log_info("Logs cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear logs: {e}") 