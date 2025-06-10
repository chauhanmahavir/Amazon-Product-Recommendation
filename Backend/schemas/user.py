from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserResponse(BaseModel):
    message: Optional[str] = None
    user_id: Optional[str] = None
    random_user_ids: Optional[List[str]] = None
    prediction: Optional[dict] = None
    purchased: Optional[List[str]] = None