import streamlit as st
import pandas as pd
import os
import base64

def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# 君がアップロードした画像ファイル名に書き換えてね！
set_background('画像.jpg')

st.title('Managemanet Of Training')

exercises = ['Incline Dumbell Press', 'latpulldawn', 'shoulderpress', 'Tbarrow']
selected_exercise = st.sidebar.selectbox('トレーニング種目を選択', exercises)
file_name = f'{selected_exercise}.csv'

# 型変換などをなくして、ただ読み込むだけのシンプルな形に戻す
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=['日付', '重量(kg)', '回数'])

st.header(f'【{selected_exercise}】')

# カレンダー設定（column_config）を丸ごと削除して、一番シンプルな1行に戻す
df['日付'] = df['日付'].astype(str)
edited_df = st.data_editor(df, num_rows='dynamic', key=f'editor_{selected_exercise}')

if st.button('この内容で保存する'):
    edited_df.to_csv(file_name, index=False)
    st.success(f'{selected_exercise} のデータを保存したよ！')
    st.rerun()

if not edited_df.empty:
    st.subheader('Growing Graph')
    chart_data = edited_df.copy()
    chart_data['日付'] = pd.to_datetime(chart_data['日付'])
    chart_data = chart_data.sort_values('日付')
 　　st.scatter_chart(chart_data, x='日付', y='重量(kg)', size='回数')
