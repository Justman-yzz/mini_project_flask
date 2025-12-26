# 📌 config/DB/blueprint 등록 
# 📝 기본 초기화 세팅
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from .config import Config

# ☐ 1. 엔진 ☐ DB 연결엔진 생성
# app/__init__.py
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    echo=True,
    connect_args=Config.CONNECT_ARGS
)
# 📝 engine = "DB로 가는 도로" 📝 SessionLocal = "도로를 이용해 왕복하는 택시" 📝 Base = "이 클래스는 DB테이블로 만들거야 표시하는 도면틀" 
# 📝 connect_args={"check_same_thread": False} → 다른 사람도 다른 데이터의 접근권한 사용할 수 있도록
# ☐ 2. SesiionLocal ☐ 세션 객체 생성
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine) # 📝 bid=engine → 세션이 어느 DB 도로탈지 결정
) # 💡 commit 커밋(DB저장확정)  # 💡 flush 커밋전 임시전송으로 쿼리결과 자동 보이게하기(중간버전 튀어나오기)
## ✅ 커밋은 명시적으로, 플러시는 필요할 때만 해서 트랜잭션 안전하게 운영시키기

# ☐ 3. Base ☐ Base클래스 
Base = declarative_base() # 📝 declarative →  코드로 '이렇게 생긴 테이블 만들거야' 선언하는 방식

def create_app():
    """Flask 앱 생성 및 초기화"""
    app = Flask(__name__)

    app.config.from_object(Config)

    from . import models  # 📝 모델 먼저 로딩(등록)
    Base.metadata.create_all(bind=engine)

    from .routes.review_routes import review_bp
    app.register_blueprint(review_bp)
    # 요청이 끝날 때마다 세션 닫기( 📝 안전장치)
    # db.close 필요 X
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        SessionLocal.remove()

    return app

    # ☐ 4. config 적용 ☐
    # ☐ 5. 모델 로딩(테이블  설계서 등록) ☐     # 📝 Base가 어떤 테이블 있는지, create_all이 비어 버리지 않도록 !
    # ☐ 6. 테이블 생성 ☐
    # ☐ 7. 블루프린트 등록 ☐

