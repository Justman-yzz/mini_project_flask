# 📌 테이블 설계서
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime # 💡 🔥"created_at 기준 최신순"🔥 설정
from . import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key = True, index = True) # index로 검색 시, 용이하도록
    title = Column(String(80), nullable = False) # Text 대신 String(80)으로 제한, 프론트 관련 
    content = Column(Text, nullable = False)
    rating = Column(Integer, nullable = False)
    created_at = Column(DateTime, default = datetime.now) # 🔥"created_at 기준 최신순"🔥 설정

    def __repr__(self):
        return f"<Review {self.title}>"