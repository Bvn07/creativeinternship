from pydantic import BaseModel
from datetime import datetime

class ScratchCard(BaseModel):
    discountAmount: float
    expiryDate: datetime
    isUsed: bool = False
