import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # 프로젝트 루트를 path에 추가

from app import create_app

app = create_app()
