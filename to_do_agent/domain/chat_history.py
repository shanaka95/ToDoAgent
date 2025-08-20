"""
Chat History Manager - Remembering Your Conversations

This module manages the conversation history for your AI task assistant.
Think of it as the AI's memory - it remembers what you've said before
so the AI can understand context like "also eggs" meaning "buy eggs"
from a previous shopping conversation.

The chat history system:
- Stores all your messages and the AI's responses
- Organizes conversations by unique IDs
- Provides context for the AI to understand references
- Keeps track of when messages were sent
- Allows the AI to remember what you've talked about

This is what makes your AI assistant seem smart and context-aware!
"""

import uuid
import logging
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    """
    A single message in a conversation.
    
    This represents one message - either from you or from the AI.
    It includes the message content, who sent it, and when it was sent.
    """
    
    id: str = Field(..., description="Unique identifier for this message")
    content: str = Field(..., description="The actual message text")
    role: str = Field(..., description="Who sent this: 'user' (you) or 'assistant' (AI)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When this message was sent")


class ChatConversation(BaseModel):
    """
    A complete conversation between you and the AI.
    
    This represents an entire chat session, including all the messages
    exchanged between you and the AI. Each conversation has a unique ID
    so the AI can remember different chat sessions separately.
    """
    
    conversation_id: str = Field(..., description="Unique identifier for this conversation")
    messages: List[ChatMessage] = Field(default_factory=list, description="All messages in this conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When this conversation started")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="When the last message was added")


class ChatHistoryManager:
    """
    The AI's Memory System - Managing All Your Conversations
    
    This class is responsible for storing and managing all your chat conversations
    with the AI. It's like the AI's brain that remembers what you've talked about
    so it can provide context-aware responses.
    
    The manager can:
    - Store new messages in conversations
    - Retrieve conversation history for context
    - Manage multiple separate conversations
    - Clean up old conversations when needed
    """
    
    def __init__(self):
        """
        Set up the conversation memory system.
        
        This initializes an empty storage area where all conversations
        will be kept in memory (like a digital filing cabinet).
        """
        # Store all conversations in a dictionary, organized by conversation ID
        self._conversations: Dict[str, ChatConversation] = {}
        self.logger = logging.getLogger(__name__)
    
    def add_message(self, conversation_id: str, content: str, role: str = "user") -> str:
        """
        Add a new message to a conversation.
        
        This is like adding a new entry to a chat log. The message gets
        stored with a unique ID and timestamp so the AI can reference it later.
        
        Args:
            conversation_id: Which conversation this message belongs to
            content: The actual message text
            role: Who sent this message ('user' for you, 'assistant' for AI)
            
        Returns:
            A unique ID for the message that was just added
        """
        # Create a unique identifier for this message
        message_id = str(uuid.uuid4())
        
        # Create the message object with all its details
        message = ChatMessage(
            id=message_id,
            content=content,
            role=role,
            timestamp=datetime.utcnow()
        )
        
        # If this is a new conversation, create it
        if conversation_id not in self._conversations:
            self._conversations[conversation_id] = ChatConversation(
                conversation_id=conversation_id
            )
        
        # Add the message to the conversation and update the timestamp
        conversation = self._conversations[conversation_id]
        conversation.messages.append(message)
        conversation.updated_at = datetime.utcnow()
        
        self.logger.info(f"Added message to conversation {conversation_id}")
        return message_id
    
    def get_conversation(self, conversation_id: str) -> Optional[ChatConversation]:
        """
        Retrieve a specific conversation by its ID.
        
        This is like looking up a specific chat session in the AI's memory.
        Useful when you want to see the full history of a particular conversation.
        
        Args:
            conversation_id: The ID of the conversation you want to find
            
        Returns:
            The complete conversation if found, or None if it doesn't exist
        """
        return self._conversations.get(conversation_id)
    
    def get_all_conversations(self) -> List[ChatConversation]:
        """
        Get a list of all conversations.
        
        This is like getting an overview of all your chat sessions with the AI.
        Useful for debugging or if you want to see all your conversation history.
        
        Returns:
            A list of all conversations the AI has stored
        """
        return list(self._conversations.values())
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Remove a specific conversation from memory.
        
        This is like deleting a chat history. Useful if you want to start
        fresh with the AI or if a conversation is no longer relevant.
        
        Args:
            conversation_id: The ID of the conversation to delete
            
        Returns:
            True if the conversation was found and deleted, False if it didn't exist
        """
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            self.logger.info(f"Deleted conversation {conversation_id}")
            return True
        return False
    
    def clear_all_conversations(self) -> int:
        """
        Clear all conversations from memory.
        
        This is like wiping the AI's memory clean. All conversation history
        will be lost, and the AI will start fresh with no context.
        
        Returns:
            How many conversations were cleared
        """
        count = len(self._conversations)
        self._conversations.clear()
        self.logger.info(f"Cleared {count} conversations")
        return count
    
    def get_conversation_messages(self, conversation_id: str) -> List[ChatMessage]:
        """
        Get all messages from a specific conversation.
        
        This is the most important method - it retrieves the conversation history
        that the AI uses to understand context. When you say "also eggs", the AI
        looks at previous messages to understand you mean "buy eggs".
        
        Args:
            conversation_id: The ID of the conversation to get messages from
            
        Returns:
            A list of all messages in that conversation, or empty list if not found
        """
        conversation = self.get_conversation(conversation_id)
        return conversation.messages if conversation else []
    
    def conversation_exists(self, conversation_id: str) -> bool:
        """
        Check if a conversation exists in memory.
        
        This is like checking if the AI remembers a particular chat session.
        Useful for determining if you're starting a new conversation or continuing an old one.
        
        Args:
            conversation_id: The ID of the conversation to check for
            
        Returns:
            True if the conversation exists, False if it doesn't
        """
        return conversation_id in self._conversations
