from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Caregiver(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: str
    relationship: str

    users: List["User"] = Relationship(back_populates="caregiver")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    language: str = "English"
    emergency_contact: str

    caregiver_id: Optional[int] = Field(default=None, foreign_key="caregiver.id")
    caregiver: Optional[Caregiver] = Relationship(back_populates="users")

    reminders: List["Reminder"] = Relationship(back_populates="user")
    checkins: List["DailyCheckin"] = Relationship(back_populates="user")
    alerts: List["Alert"] = Relationship(back_populates="user")


class Reminder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    time: str
    dosage: Optional[str] = None

    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="reminders")


class DailyCheckin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    orientation_score: int
    mood_score: int
    response_time: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="checkins")


class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = False

    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="alerts")