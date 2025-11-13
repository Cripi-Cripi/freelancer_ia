import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Express", layout="wide")
st.title("Sube tu Excel → Dashboard en 10 segundos")
st.markdown("*Sin instalación. Solo sube tu archivo.*")

uploaded = st.file_uploader("Sube Excel o CSV", type=["xlsx", "csv"])
if uploaded:
    try:
        df = pd.read_excel(uploaded) if uploaded.name.endswith('.xlsx') else pd.read_csv(uploaded)
        st.success(f"¡Listo! {len(df)} filas cargadas")
        
        col1, col2, col3 = st.columns(3)
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            col1.metric("Total", f"£{df[numeric_cols[0]].sum():,.0f}")
            col2.metric("Filas", len(df))
            col3.metric("Promedio", f"£{df[numeric_cols[0]].mean():.1f}")
        
        if len(numeric_cols) >= 2:
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], color=df.columns[0])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(df[numeric_cols[0]] if len(numeric_cols) > 0 else df.iloc[:, 0])
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Sube un archivo para ver el dashboard")