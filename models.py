from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import os


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5431')

PG_DSN = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
         f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Ads(Base):
    __tablename__ = 'Ads'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user: Mapped[str] = mapped_column(String(120), nullable=False)
    heading: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    
    
    @property
    def dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'heading': self.heading,
            'description': self.description,
            'date': self.date,
            }
        
        
Base.metadata.create_all(bind=engine)