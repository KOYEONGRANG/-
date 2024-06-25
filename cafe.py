import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# 데이터 불러오기
file_path = 'cafe.xlsx'
cafe_data = pd.read_excel(file_path)

# order_date를 datetime 형식으로 변환
cafe_data['order_date'] = pd.to_datetime(cafe_data['order_date'])

# 연도와 월 컬럼 추가
cafe_data['year'] = cafe_data['order_date'].dt.year
cafe_data['month'] = cafe_data['order_date'].dt.month

# Streamlit 대시보드 설정
st.title('카페 매출 대시보드')

# 사이드바에서 연도와 제품 2개 선택
selected_year = st.sidebar.selectbox(
                  '연도 선택', sorted(cafe_data['year'].unique()))
selected_products = st.sidebar.multiselect(
                  '제품 선택', sorted(cafe_data['item'].unique()), default=sorted(cafe_data['item'].unique())[:2])

# 선택된 연도와 제품에 따라 데이터 필터링
filtered_data = cafe_data[(cafe_data['year'] == selected_year) & 
                          (cafe_data['item'].isin(selected_products))]

# 월별 매출 데이터 계산
monthly_sales = filtered_data.groupby(['month', 'item'])['price'].sum().reset_index()

# 매출 표 출력
st.write(f'{selected_year}년 선택된 제품 매출 데이터')
st.write(filtered_data)

# 월별 매출 데이터 출력
st.write(f'{selected_year}년 월별 매출 비교 및 총 매출 비교')
if len(selected_products) > 0:
    monthly_sales_pivot = monthly_sales.pivot(index='month', columns='item', values='price')
    total_sales = filtered_data.groupby('item')['price'].sum().reset_index()
    total_sales = total_sales.sort_values(by='price', ascending=False)
    
    # 월별 매출 데이터와 총 매출 데이터를 하나의 DataFrame으로 병합
    combined_data = pd.concat([monthly_sales_pivot, total_sales.set_index('item')['price']], axis=1)
    st.dataframe(combined_data)

# 막대 그래프 그리기
if len(selected_products) > 0:
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_sales.pivot(index='month', columns='item', values='price').plot(kind='bar', ax=ax)
    
    # 가로 줄 숫자를 세로로 기울어지지 않게 수정
    ax.tick_params(axis='x', rotation=0)
    
    ax.set_xlabel('월')
    ax.set_ylabel('매출')
    ax.set_title(f'{selected_year}년 월별 매출 비교')
    st.pyplot(fig)
else:
    st.write('제품을 선택해주세요.')
