from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict











class EnquiryCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    course: Optional[str] = None
    qualification: Optional[str] = None
    message: Optional[str] = None



class EnquiryStatusUpdate(BaseModel):
    status: str


class EnquiryResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    course: Optional[str] = None
    qualification: Optional[str] = None
    message: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)




