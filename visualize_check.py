import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 한글 폰트 설정 (그래프 깨짐 방지 - 윈도우용)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기
try:
    users = pd.read_csv('users.csv')
    logs = pd.read_csv('campaign_logs.csv')
    # 두 테이블을 user_id 기준으로 합치기
    df = pd.merge(logs, users, on='user_id')
    print("✅ 데이터 로드 성공!")
except FileNotFoundError:
    print("❌ 파일이 없어요! users.csv가 있는 폴더에서 실행해주세요.")
    exit()

# 그래프 스타일 설정
sns.set(style="whitegrid")
# seaborn 설정 후 폰트가 초기화될 수 있어서 다시 설정
plt.rcParams['font.family'] = 'Malgun Gothic'

# 3. 그래프 그리기 (화면을 두 개로 쪼개서 비교)
plt.figure(figsize=(12, 5))

# [왼쪽] 전체 고객 대상 성공률 (A안 vs B안)
plt.subplot(1, 2, 1)
sns.barplot(x='group', y='password_changed', data=df, errorbar=None, palette='Blues')
plt.title("전체 고객 성공률 (B안_Reward가 높아야 함)")
plt.ylim(0, 0.6) # Y축 고정

# [오른쪽] VIP 고객 대상 성공률 (여기가 반전 포인트!)
vip_data = df[df['segment'] == 'VIP']
plt.subplot(1, 2, 2)
sns.barplot(x='group', y='password_changed', data=vip_data, errorbar=None, palette='Reds')
plt.title("★VIP 고객★ 성공률 (A안_Transparency가 높아야 함)")
plt.ylim(0, 0.6)

plt.tight_layout()
plt.show()