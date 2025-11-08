from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    userId: str
    scratchCardId: str
    transactionAmount: float
    dateOfTransaction: datetime = datetime.utcnow()
