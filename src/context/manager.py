from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.now()

class Context(BaseModel):
    session_id: str
    messages: List[Message] = []
    metadata: Dict = {}
    created_at: datetime = datetime.now()
    last_updated: datetime = datetime.now()

class ContextManager:
    def __init__(self):
        self.contexts: Dict[str, Context] = {}

    def create_context(self, session_id: str) -> Context:
        """Create a new context for a session."""
        if session_id in self.contexts:
            return self.contexts[session_id]
        
        context = Context(session_id=session_id)
        self.contexts[session_id] = context
        return context

    def get_context(self, session_id: str) -> Optional[Context]:
        """Get context for a session if it exists."""
        return self.contexts.get(session_id)

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to the context."""
        context = self.get_context(session_id)
        if not context:
            context = self.create_context(session_id)
        
        message = Message(role=role, content=content)
        context.messages.append(message)
        context.last_updated = datetime.now()

    def update_metadata(self, session_id: str, metadata: Dict) -> None:
        """Update metadata for a session."""
        context = self.get_context(session_id)
        if not context:
            context = self.create_context(session_id)
        
        context.metadata.update(metadata)
        context.last_updated = datetime.now()

    def clear_context(self, session_id: str) -> None:
        """Clear context for a session."""
        if session_id in self.contexts:
            del self.contexts[session_id]