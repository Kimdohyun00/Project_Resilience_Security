from fastapi import FastAPI
from pydantic import BaseModel

# 1. API 앱 생성 (우리 가게 간판 달기)
app = FastAPI()

# 2. 데이터 형식 정의 (주문서 양식)
# 프론트엔드(웹/앱)에서 이런 형태로 데이터를 보내줘야 함
class UserInfo(BaseModel):
    user_id: str
    segment: str  # 여기에 "VIP" 또는 "Normal"이 들어옵니다.

# 3. 메인 로직 (우리가 찾은 Gold Data 규칙 적용!)
# 엔드포인트: /recommend
@app.post("/recommend")
def recommend_strategy(user: UserInfo):
    """
    고객 정보를 받아서, 어떤 사과문/보상을 띄울지 결정해주는 함수
    """
    
    # ★ 여기가 핵심! 우리가 분석으로 찾아낸 '승리 공식' ★
    if user.segment == "VIP":
        # VIP에게는 '투명성(Transparency)' 전략
        return {
            "user_id": user.user_id,
            "segment": "VIP",
            "popup_type": "Type_A",
            "message": "고객님, 심려를 끼쳐 죄송합니다. 정확한 사고 경위를 투명하게 설명드립니다...",
            "coupon_value": 0
        }
    else:
        # 일반(Normal) 고객에게는 '보상(Reward)' 전략
        return {
            "user_id": user.user_id,
            "segment": "Normal",
            "popup_type": "Type_B",
            "message": "비밀번호를 변경해주시면 감사 포인트 5,000원을 즉시 지급해 드립니다!",
            "coupon_value": 5000
        }

# 4. 헬스 체크용 (잘 살아있는지 확인)
@app.get("/")
def read_root():
    return {"status": "API is running", "version": "1.0"}