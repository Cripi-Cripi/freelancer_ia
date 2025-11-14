import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive Excel Dashboard", layout="wide")

st.title("Turn your Excel/CSV into an Interactive Dashboard in 10 seconds")
st.markdown("**No installation needed · Instant charts, filters & export**")

st.sidebar.header("Upload your data")
st.sidebar.write("Supports Excel (.xlsx, .xls) and CSV files")

uploaded = st.file_uploader("Drag & drop your Excel or CSV file here", 
                           type=["xlsx", "xls", "csv"])

if uploaded:
    try:
        df = pd.read_excel(uploaded) if uploaded.name.endswith(('.xlsx', '.xls')) else pd.read_csv(uploaded)
        
        st.success(f"Success! {len(df):,} rows loaded")
        
        # Metrics
        numeric_cols = df.select_dtypes(include='number').columns
        col1, col2, col3 = st.columns(3)
        if len(numeric_cols) > 0:
            col1.metric("Total", f"${df[numeric_cols[0]].sum():,.0f}")
            col2.metric("Rows", f"{len(df):,}")
            col3.metric("Average", f"${df[numeric_cols[0]].mean():,.1f}")
        
        # Charts
        st.subheader("Interactive Charts")
        if len(numeric_cols) >= 2:
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], 
                           color=df.select_dtypes("object").columns[0] if len(df.select_dtypes("object").columns) > 0 else None,
                           hover_data=df.columns)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(df[numeric_cols[0]] if len(numeric_cols) > 0 else df.iloc[:, 0])
            
        st.download_button("Export data as CSV", 
                          data=df.to_csv(index=False).encode(), 
                          file_name="clean_data.csv", 
                          mime="text/csv")
                          
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Upload your Excel or CSV file to instantly generate your dashboard")
