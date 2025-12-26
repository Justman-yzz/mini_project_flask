"""
서비스 계층 (Service Layer)
- 라우트에서 직접 DB 조작하지 않고
- 이 모듈을 거쳐서 DB CRUD 실행
"""

from app import SessionLocal
from app.models import Review
from sqlalchemy import func


def get_all_reviews():
    """모든 리뷰 조회"""
    db = SessionLocal()
    return db.query(Review).order_by(Review.created_at.desc()).all()      # desc 내림차순(최신순)



def create_review(title, content, rating):
    """리뷰 생성"""
    db = SessionLocal()
    review = Review(title=title, content=content, rating=rating)
    db.add(review)
    db.commit()
    db.refresh(review) # 🔥 DB가 id 또는 created_at 채워줬을 때, 확실하게 채워지게 하기
    return review


def get_review_by_id(review_id):
    """ID로 리뷰 조회"""
    db = SessionLocal()
    return db.get(Review, review_id) # db.get(Model, pk) → pk로 바로 찾아오기


def update_review(review_id, title, content, rating):
    """리뷰 수정"""
    db = SessionLocal()
    review = db.get(Review, review_id)
    if review is None: # 수정하려는 리뷰 없으면 None 반환
        return None
    # 필드수정하기 
    review.title = title  
    review.content = content
    review.rating = rating

    db.commit()
    db.refresh(review) 
    return review


def delete_review(review_id):
    """리뷰 삭제"""
    db = SessionLocal()
    review = db.get(Review, review_id)
    if review is None: # 삭제하려는 리뷰 없으면 None 반환
        return None
    # 리뷰 삭제
    db.delete(review)
    db.commit()

def get_average_rating():
    """전체 리뷰의 rating 평균"""
    db = SessionLocal()
    avg = db.query(func.avg(Review.rating)).scalar() # scalar() → 결과 한개 값만 꺼내기
    if avg is None:
        return 0  # 리뷰 0개일 시, 평균 = 0
    return round(avg, 2) # 반올림 소수 2자리