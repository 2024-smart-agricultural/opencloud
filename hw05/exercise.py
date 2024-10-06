import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.font_manager as fm
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows


# 운동 기록을 저장할 DataFrame 초기화
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = pd.DataFrame(columns=['날짜', '운동 종류', '운동 시간', '소모 칼로리', '일지'])

# 사이드바 제목
st.sidebar.title("운동 기록 추가")

# 운동 목표 설정
goal_calories = st.sidebar.number_input("주간 소모 칼로리 목표", min_value=1)

# 운동 기록 입력
date = st.sidebar.date_input("날짜", pd.to_datetime("today"))
exercise = st.sidebar.selectbox("운동 종류", ["달리기", "수영", "자전거", "웨이트", "요가", "기타"])
duration = st.sidebar.number_input("운동 시간 (분)", min_value=1)
calories = st.sidebar.number_input("소모 칼로리", min_value=1)
journal_entry = st.sidebar.text_area("운동 일지")

# 기록 추가 버튼
if st.sidebar.button("기록 추가"):
    new_record = pd.DataFrame([[date, exercise, duration, calories, journal_entry]], 
                               columns=['날짜', '운동 종류', '운동 시간', '소모 칼로리', '일지'])
    st.session_state.workout_data = pd.concat([st.session_state.workout_data, new_record], ignore_index=True)
    st.success("운동 기록이 추가되었습니다!")

# 기록 보기
st.title("운동 트래킹 앱")
st.write("기록된 운동 내용:")
st.dataframe(st.session_state.workout_data)

# 운동 목표 달성 여부
if not st.session_state.workout_data.empty:
    total_calories = st.session_state.workout_data['소모 칼로리'].sum()
    if total_calories >= goal_calories:
        st.success(f"축하합니다! 목표 달성! 총 소모 칼로리: {total_calories}")
    else:
        st.warning(f"아직 목표에 도달하지 못했습니다. 현재 총 소모 칼로리: {total_calories}")

# 데이터 시각화
st.subheader("운동 기록 시각화")

# 운동 종류별 소모 칼로리 시각화
calories_per_exercise = st.session_state.workout_data.groupby('운동 종류')['소모 칼로리'].sum().reset_index()

fig, ax = plt.subplots()
ax.bar(calories_per_exercise['운동 종류'], calories_per_exercise['소모 칼로리'], color='skyblue')
ax.set_xlabel("운동 종류")
ax.set_ylabel("소모 칼로리")
ax.set_title("운동 종류별 소모 칼로리")
st.pyplot(fig)

# 날짜별 소모 칼로리 시각화
calories_per_date = st.session_state.workout_data.groupby('날짜')['소모 칼로리'].sum().reset_index()

fig, ax = plt.subplots()
ax.plot(calories_per_date['날짜'], calories_per_date['소모 칼로리'], marker='o', color='orange')
ax.set_xlabel("날짜")
ax.set_ylabel("소모 칼로리")
ax.set_title("날짜별 소모 칼로리")
st.pyplot(fig)

# 데이터 내보내기
st.sidebar.title("데이터 내보내기")
if st.sidebar.button("CSV로 내보내기"):
    csv = st.session_state.workout_data.to_csv(index=False, encoding="utf-8-sig").encode('utf-8-sig')
    st.sidebar.download_button("다운로드", csv, "workout_data.csv", "text/csv")
