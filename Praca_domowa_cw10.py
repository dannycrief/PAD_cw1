import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_option('deprecation.showPyplotGlobalUse', False)

st.header('Homework 10')

page = st.sidebar.selectbox('Select page:', ['Survey', 'Stats'])

if page == 'Survey':
    show_surname = False

    name = st.text_input("Name:")
    if len(name) > 0:
        show_surname = True
        st.success('Name accepted')
    if show_surname:
        surname = st.text_input("Surname:")
        if len(surname) > 0:
            st.success('Surname accepted')
else:
    data = st.file_uploader("Upload your dataset", type=['csv'])
    if data is not None:
        df = pd.read_csv(data)
        st.dataframe(df.head(20))
        selected_col = st.multiselect("Select columns to plot", df.columns.tolist())
        chart_type = st.radio("Select chart type (for pie plot select 2 values)", ['Pie Plot', 'Histogram'])
        if chart_type == 'Pie Plot' and len(selected_col) == 2:
            fig = go.Figure(
                go.Pie(
                    labels=df[selected_col[0]].unique(),
                    values=df.groupby(selected_col[0])[selected_col[1]].count(),
                ))
            st.plotly_chart(fig)
        if chart_type == 'Histogram' and len(selected_col) > 0:
            plot_data = df[selected_col].plot(kind='hist')
            st.write(plot_data)
            st.pyplot()
