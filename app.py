import streamlit as st
import pandas as pd
import os

st.title('筋トレ成長記録・管理アプリ')
st.image('画像.jpg',use_container_width=true)

exercises = ['インクラインダンベルプレス', 'デッドリフト', 'ショルダープレス', 'Tバーロウ']
selected_exercise = st.sidebar.selectbox('トレーニング種目を選択', exercises)
file_name = f'{selected_exercise}.csv'

# 型変換などをなくして、ただ読み込むだけのシンプルな形に戻す
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=['日付', '重量(kg)', '回数'])

st.header(f'【{selected_exercise}】の記録管理')

# カレンダー設定（column_config）を丸ごと削除して、一番シンプルな1行に戻す
edited_df = st.data_editor(df, num_rows='dynamic', key=f'editor_{selected_exercise}')

if st.button('この内容で保存する'):
    edited_df.to_csv(file_name, index=False)
    st.success(f'{selected_exercise} のデータを保存したよ！')
    st.rerun()

if not edited_df.empty:
    st.subheader('成長グラフ')
    chart_data = edited_df.copy()
    chart_data['日付'] = pd.to_datetime(chart_data['日付'])
    chart_data = chart_data.sort_values('日付')
    chart_data = chart_data.set_index('日付')
    st.line_chart(chart_data['重量(kg)'])
