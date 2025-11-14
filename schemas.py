"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict

# Example schemas (you can keep these for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Personal profile app schemas

class Profile(BaseModel):
    """
    Public profile information
    Collection name: "profile"
    """
    name: str = Field(..., description="Full name")
    title: str = Field(..., description="Headline/title")
    bio: str = Field(..., description="Short biography")
    location: Optional[str] = Field(None, description="Location")
    photo_url: Optional[str] = Field(None, description="Profile photo URL")
    socials: Optional[Dict[str, str]] = Field(
        default=None,
        description="Map of social network to URL (e.g., linkedin, github)"
    )

class Project(BaseModel):
    """
    Portfolio projects
    Collection name: "project"
    """
    title: str
    description: str
    tags: List[str] = []
    link: Optional[str] = None

class Contactmessage(BaseModel):
    """
    Contact messages from site visitors
    Collection name: "contactmessage"
    """
    name: str
    email: EmailStr
    message: str
