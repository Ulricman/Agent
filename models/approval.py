from . import db
from datetime import datetime

class ApprovalRequest(db.Model):
    __tablename__ = 'approval_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(20), nullable=False)  # 'qa' or 'knowledge'
    content_id = db.Column(db.Integer)  # Reference to original content if updating
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    tags = db.Column(db.String(500))
    submitter_id = db.Column(db.Integer, nullable=False)
    submitter_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    priority = db.Column(db.String(10), default='normal')  # 'low', 'normal', 'high', 'urgent'
    reviewer_id = db.Column(db.Integer)
    reviewer_name = db.Column(db.String(100))
    review_comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    action_type = db.Column(db.String(20), nullable=False)  # 'create', 'update', 'delete'
    
    # Additional fields for QA content
    question = db.Column(db.Text)  # For QA content type
    answer = db.Column(db.Text)    # For QA content type
    
    # Relationship to approval history
    history = db.relationship('ApprovalHistory', backref='request', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, content_type, title, content, submitter_id, submitter_name, action_type, **kwargs):
        self.content_type = content_type
        self.title = title
        self.content = content
        self.submitter_id = submitter_id
        self.submitter_name = submitter_name
        self.action_type = action_type
        
        # Set optional fields
        self.content_id = kwargs.get('content_id')
        self.category = kwargs.get('category')
        self.tags = kwargs.get('tags')
        self.priority = kwargs.get('priority', 'normal')
        self.question = kwargs.get('question')
        self.answer = kwargs.get('answer')
    
    def to_dict(self):
        return {
            'id': self.id,
            'content_type': self.content_type,
            'content_id': self.content_id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.tags,
            'submitter_id': self.submitter_id,
            'submitter_name': self.submitter_name,
            'status': self.status,
            'priority': self.priority,
            'reviewer_id': self.reviewer_id,
            'reviewer_name': self.reviewer_name,
            'review_comment': self.review_comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'action_type': self.action_type,
            'question': self.question,
            'answer': self.answer
        }

class ApprovalHistory(db.Model):
    __tablename__ = 'approval_history'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('approval_requests.id'), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # 'submitted', 'approved', 'rejected', 'modified'
    actor_id = db.Column(db.Integer, nullable=False)
    actor_name = db.Column(db.String(100), nullable=False)
    actor_role = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, request_id, action, actor_id, actor_name, actor_role, comment=None):
        self.request_id = request_id
        self.action = action
        self.actor_id = actor_id
        self.actor_name = actor_name
        self.actor_role = actor_role
        self.comment = comment
    
    def to_dict(self):
        return {
            'id': self.id,
            'request_id': self.request_id,
            'action': self.action,
            'actor_id': self.actor_id,
            'actor_name': self.actor_name,
            'actor_role': self.actor_role,
            'comment': self.comment,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

# Mock QA and Knowledge models for the approval system
class QAItem(db.Model):
    __tablename__ = 'qa_items'
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    tags = db.Column(db.String(500))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'tags': self.tags,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }

class KnowledgeItem(db.Model):
    __tablename__ = 'knowledge_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    tags = db.Column(db.String(500))
    created_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': self.tags,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        } 