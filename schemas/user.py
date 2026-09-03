from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict



class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
    
    
    
    
    
    
    
    
    
    # class for updating  admin password 
    
    




class Changepassword(BaseModel):
      current_password:str
      new_password:str
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    