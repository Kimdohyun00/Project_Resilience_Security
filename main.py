from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uuid
import random
import datetime

app = FastAPI()

# ==========================================
# 1. 데이터 형식 정의 (팀원이 준 코드 기반)
# ==========================================

# [입력] 팀원(대시보드)이 보낼 데이터
class TriageRequest(BaseModel):
    patient_id: str         # 환자 ID
    current_symptoms: str   # 현재 증상 (예: 가슴 통증)

class DrugConsultRequest(BaseModel):
    patient_id: str
    prescribe_drug: str     # 처방하려는 약 (예: 아스피린)

# [출력] 우리가 팀원에게 줄 데이터 (JSON 구조 그대로 반영)
class AiTriageResponse(BaseModel):
    triage_level: str
    suspected_diagnosis: str
    recommended_action: List[str]
    destination_type: str

# ==========================================
# 2. API 기능 구현
# ==========================================

# 기능 1: 응급 환자 분류 (A/B 테스트 적용)
@app.post("/get_ai_triage")
def get_ai_triage(req: TriageRequest):
    
    # 1. 세션 ID 발급 (나중에 시간 잴 때 추적용)
    session_id = str(uuid.uuid4())
    
    # 2. A/B 테스트: 50% 확률로 AI 켜기
    # True = B그룹 (AI 대시보드), False = A그룹 (그냥 빈 화면)
    show_ai = random.random() > 0.5

    response_data = None

    if show_ai:
        # [B그룹 - AI 작동] 
        # ★여기가 나중에 팀원2의 코드가 들어올 자리입니다.
        # 지금은 팀원이 준 예시랑 똑같은 '가짜 정답'을 보냅니다.
        response_data = {
            "triage_level": "KTAS 1등급 (즉각 처치 필요)",
            "suspected_diagnosis": "급성 심근경색(AMI) 의심",
            "recommended_action": [
                "즉시 산소 공급 (O2 4L/min)",
                "아스피린 300mg 저작 투여 (유전적 위험 확인 필요)"
            ],
            "destination_type": "심혈관 중재술(PCI) 가능한 권역응급의료센터"
        }
    else:
        # [A그룹 - 통제군]
        # AI 도움 없이 의사가 알아서 판단해야 하므로 데이터 안 줌
        response_data = None

    # 3. 결과 전송
    return {
        "session_id": session_id,
        "group_type": "B_Group_AI" if show_ai else "A_Group_Control",
        "data": response_data
    }


# 기능 2: 약물 처방 상담 (팀원이 준 두 번째 함수)
@app.post("/get_drug_consultation")
def get_drug_consultation(req: DrugConsultRequest):
    
    # [가짜 응답 - 나중에 팀원 코드 연결]
    fake_llm_response = f"""
    [AI 분석 결과]
    환자({req.patient_id})에게 '{req.prescribe_drug}' 처방 시 주의사항:
    - 신장 기능(GFR)이 55로 낮아 용량 조절이 필요합니다.
    - 유전자 검사 결과 출혈 위험이 있으니 모니터링하세요.
    """
    
    return {
        "status": "success",
        "consultation_result": fake_llm_response
    }


# ==========================================
# 3. [핵심] 성과 측정 (검정용)
# ==========================================
class DecisionLog(BaseModel):
    session_id: str
    action_taken: str  # 의사가 실제로 내린 처방
    time_taken_sec: float # 걸린 시간 (초)

@app.post("/submit_result")
def submit_result(log: DecisionLog):
    # 나중에 이 로그들이 쌓이면 '검정'을 할 수 있습니다.
    print(f"✅ [검정 데이터 확보] 세션: {log.session_id} | 시간: {log.time_taken_sec}초 | 처방: {log.action_taken}")
    return {"msg": "저장 완료"}