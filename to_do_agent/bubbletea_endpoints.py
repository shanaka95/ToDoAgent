# bubbletea_integration.py
from typing import Optional, List
from pydantic import BaseModel
import bubbletea_chat as bt
from bubbletea_chat import LLM

# ----  BubbleTea config the client reads at /config  ----
@bt.config()
def bubbletea_config():
    # IMPORTANT: if you deploy behind API Gateway with root_path="/prod/",
    # set url to your public base, e.g., "https://api.example.com/prod"
    return bt.BotConfig(
        name="todo-assistant",
        url="",               # fill in your public base URL (no trailing slash)
        is_streaming=True,    # BubbleTea supports streaming generators
        display_name="To-Do Assistant",
        subtitle="Task management via chat",
        initial_text="Hi! Tell me your task, e.g., 'add Buy milk due tomorrow'."
    )

# ----  Request model matching what BubbleTea sends to /chat  ----
class ChatRequest(BaseModel):
    message: str
    user_uuid: Optional[str] = None
    conversation_uuid: Optional[str] = None
    user_email: Optional[str] = None
    images: Optional[List[str]] = None   # BubbleTea may send image URLs/base64 for vision bots

# ----  Your bot logic. Yield BubbleTea components.  ----
@bt.chatbot(name="To-Do Assistant", stream=True)
async def todo_bot(message: str, user_uuid: str = None, conversation_uuid: str = None):
    # Example: hand off to your to_do_agent here, then format replies for BubbleTea
    # resp = await process_message_with_agent(message, user_uuid, conversation_uuid)
    # For now, a minimal echo + hint:
    if message.lower().startswith("help"):
        yield bt.Markdown("**Try:** `add Buy milk tomorrow 6pm` or `list tasks`")
        return
    yield bt.Text(f"You said: {message}")
    # You can also stream LLM output if you enable [llm] extra:
    # llm = LLM(model="gpt-4o-mini")   # or any LiteLLM-supported model with env keys set
    # async for chunk in llm.stream(f"Rephrase as a concise task: {message}"):
    #     yield bt.Text(chunk)

# ----  FastAPI-compatible handlers for /config and /chat  ----
# The SDK provides decorators for behavior; here we expose plain callables FastAPI can route to.
def fastapi_config_handler():
    # BubbleTea expects JSON of BotConfig at /config
    return bubbletea_config().__dict__

async def fastapi_chat_handler(req: ChatRequest):
    # The decorator makes todo_bot an async generator; collect its emitted components
    payload = []
    async for component in todo_bot(
        message=req.message,
        user_uuid=req.user_uuid,
        conversation_uuid=req.conversation_uuid,
        user_email=req.user_email
    ):
        # Components are dataclasses; convert to JSON-ish dicts BubbleTea understands
        payload.append(component.to_dict() if hasattr(component, "to_dict") else component.__dict__)
    return payload
