from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, Memo, Notification
from .approval import ApprovalRequest, ApprovalHistory, QAItem, KnowledgeItem 