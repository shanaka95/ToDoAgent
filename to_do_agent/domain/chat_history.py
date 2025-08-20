"""
Chat history manager for the ToDo Agent.

This module provides in-memory storage and management of chat conversations.
"""

import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """Represents a single message in a chat conversation."""
    
    id: str = Field(..., description="Unique message ID")
    content: str = Field(..., description="Message content")
    role: str = Field(..., description="Message role (user/assistant)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")


class ChatConversation(BaseModel):
    """Represents a chat conversation with its history."""
    
    conversation_id: str = Field(..., description="Unique conversation ID")
    messages: List[ChatMessage] = Field(default_factory=list, description="List of messages in the conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Conversation creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class ChatHistoryManager:
    """
    Manages in-memory chat history for conversations.
    
    This class provides methods to store, retrieve, and manage chat conversations
    in memory. Each conversation is identified by a unique conversation ID.
    """
    
    def __init__(self):
        """Initialize the chat history manager."""
        self._conversations: Dict[str, ChatConversation] = {}
        self.logger = logging.getLogger(__name__)
    
    def add_message(self, conversation_id: str, content: str, role: str = "user") -> str:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: The conversation ID
            content: The message content
            role: The message role (user/assistant)
            
        Returns:
            The message ID
        """
        message_id = str(uuid.uuid4())
        message = ChatMessage(
            id=message_id,
            content=content,
            role=role,
            timestamp=datetime.utcnow()
        )
        
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = ChatConversation(
                conversation_id=conversation_id
            )
        
        conversation = self._conversations[conversation_id]
        conversation.messages.append(message)
        conversation.updated_at = datetime.utcnow()
        
        self.logger.info(f"Added message to conversation {conversation_id}")
        return message_id
    
    def get_conversation(self, conversation_id: str) -> Optional[ChatConversation]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: The conversation ID
            
        Returns:
            The conversation or None if not found
        """
        return self._conversations.get(conversation_id)
    
    def get_all_conversations(self) -> List[ChatConversation]:
        """
        Get all conversations.
        
        Returns:
            List of all conversations
        """
        return list(self._conversations.values())
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation.
        
        Args:
            conversation_id: The conversation ID
            
        Returns:
            True if deleted, False if not found
        """
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            self.logger.info(f"Deleted conversation {conversation_id}")
            return True
        return False
    
    def clear_all_conversations(self) -> int:
        """
        Clear all conversations.
        
        Returns:
            Number of conversations cleared
        """
        count = len(self._conversations)
        self._conversations.clear()
        self.logger.info(f"Cleared {count} conversations")
        return count
    
    def get_conversation_messages(self, conversation_id: str) -> List[ChatMessage]:
        """
        Get all messages from a conversation.
        
        Args:
            conversation_id: The conversation ID
            
        Returns:
            List of messages or empty list if conversation not found
        """
        conversation = self.get_conversation(conversation_id)
        return conversation.messages if conversation else []
    
    def conversation_exists(self, conversation_id: str) -> bool:
        """
        Check if a conversation exists.
        
        Args:
            conversation_id: The conversation ID
            
        Returns:
            True if conversation exists, False otherwise
        """
        return conversation_id in self._conversations
