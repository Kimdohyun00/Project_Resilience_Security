import pandas as pd
import numpy as np
import random
import os

# 1. 설정: 데이터 규모 (일단 시범용으로 1만 명만 생성)
NUM_USERS = 10000
START_DATE = '2023-12-01'

print(f"[{NUM_USERS}명]의 가상 고객 데이터를 생성합니다...")

# ---------------------------------------------------------
# [Table 1] users.csv : 고객 프로필 데이터
# ---------------------------------------------------------
# ID 생성 (U_00001 ~ U_10000)
user_ids = [f"U_{i:05d}" for i in range(1, NUM_USERS + 1)]

# 고객 등급 (VIP: 10%, Loyal: 30%, New: 60%)
segments = np.random.choice(['VIP', 'Loyal', 'New'], size=NUM_USERS, p=[0.1, 0.3, 0.6])

# 주 사용 기기
devices = np.random.choice(['Mobile', 'PC'], size=NUM_USERS, p=[0.65, 0.35])

df_users = pd.DataFrame({
    'user_id': user_ids,
    'segment': segments,
    'device': devices,
    'join_date': pd.date_range(start='2020-01-01', end='2023-11-30', periods=NUM_USERS)
})

# ---------------------------------------------------------
# [Table 2] campaign_logs.csv : 보안 안내 메시지 반응 로그
# ---------------------------------------------------------
# A/B 그룹 배정 (50:50)
groups = np.random.choice(['A_Transparency', 'B_Reward'], size=NUM_USERS, p=[0.5, 0.5])

# 데이터프레임 병합 (로직 적용을 위해 잠시 합침)
df_logs = pd.DataFrame({
    'user_id': user_ids,
    'group': groups
})
df_combined = pd.merge(df_logs, df_users, on='user_id')

# ★ 시나리오 로직 적용 함수 (여기가 핵심!) ★
def simulate_reaction(row):
    # 기본 확률
    open_prob = 0.4      # 메일 열람 확률
    click_prob = 0.2     # 링크 클릭 확률
    convert_prob = 0.1   # 비밀번호 변경(성공) 확률
    churn_prob = 0.01    # 탈퇴 확률
    
    # 1. 그룹별 효과 (B안: 보상형은 전환율이 높지만, 탈퇴율도 높음)
    if row['group'] == 'B_Reward':
        open_prob += 0.15     # "쿠폰 드려요" 제목이라 많이 열어봄
        convert_prob += 0.20  # 보상 때문에 비번 많이 바꿈
        churn_prob += 0.03    # "내 정보 털렸어?" 놀라서 탈퇴도 증가
        
    # 2. 세그먼트별 반전 (VIP는 보상보다 신뢰를 중시)
    if row['segment'] == 'VIP':
        if row['group'] == 'B_Reward':
            convert_prob -= 0.25 # VIP: "돈으로 때우나?" (오히려 역효과)
        else: # A_Transparency
            convert_prob += 0.15 # VIP: "솔직해서 좋네" (신뢰 상승)

    # 확률에 따른 행동 결정 (0 또는 1)
    is_opened = 1 if random.random() < open_prob else 0
    is_clicked = 1 if (is_opened and random.random() < click_prob) else 0
    is_changed = 1 if (is_clicked and random.random() < convert_prob) else 0 # 이게 KPI
    is_withdrawn = 1 if random.random() < churn_prob else 0
    
    return is_opened, is_clicked, is_changed, is_withdrawn

# 로직 적용
results = df_combined.apply(simulate_reaction, axis=1, result_type='expand')
df_combined[['opened', 'clicked', 'password_changed', 'withdrawn']] = results

# 날짜 랜덤 배정 (12월 1일 ~ 7일 사이)
random_days = np.random.randint(0, 7, size=NUM_USERS)
df_combined['event_date'] = pd.to_datetime(START_DATE) + pd.to_timedelta(random_days, unit='D')

# 최종 로그 테이블 정리
df_final_logs = df_combined[['user_id', 'event_date', 'group', 'opened', 'clicked', 'password_changed', 'withdrawn']]

# ---------------------------------------------------------
# [Output] CSV 파일 저장
# ---------------------------------------------------------
df_users.to_csv('users.csv', index=False)
df_final_logs.to_csv('campaign_logs.csv', index=False)

print("✅ 생성 완료!")
print(f"1. users.csv : {len(df_users)}명 (고객 정보)")
print(f"2. campaign_logs.csv : {len(df_final_logs)}건 (실험 결과)")
print("=> 이제 이 파일을 열어서 내용을 확인해보세요.")