`app/database.py`:

```python
"""SQLite database setup using SQLAlchemy ORM."""

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    """Stores user profile and their generated workout plan."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(String(20), nullable=False)
    goal = Column(String(200), nullable=False)
    intensity = Column(String(50), nullable=False, default="Moderate")
    workout_plan = Column(Text, nullable=True)
    nutrition_tips = Column(Text, nullable=True)


def init_db() -> None:
    """Create all tables if they don't exist yet."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This file sets up the SQLite database connection, defines the `User` table with all the fields (ID, Name, Age, Weight, Goal, Intensity, Workout Plan, Nutrition Tips), and provides the `get_db` helper that FastAPI uses to hand a database session to each route. Let me know which file you'd like next.