import pandas as pd
from utils import detect_columns, safe_load_data

def render_upload():
    st.markdown("## 📤 Upload & Analyze Dataset")
    
    # Drag & Drop Upload
    uploaded_file = st.file_uploader(
        "Choose CSV/Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Drag & drop or click to upload (Max 200MB)"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            with st.spinner("🔄 Analyzing dataset..."):
                df = safe_load_data(uploaded_file)
                column_map = detect_columns(df)
                
                st.session_state.df = df
                st.session_state.column_map = column_map
                st.session_state.departments = sorted(df[column_map.get('department', df.columns[0])].dropna().unique())
                
                st.success(f"✅ Dataset loaded: {len(df):,} rows × {len(df.columns)} columns")
                st.metric("Detected", f"{len(column_map)} column types")
        
        with col2:
            st.markdown("### 🧠 Auto-Detected Columns")
            for key, col in column_map.items():
                st.markdown(f"**{key.title()}**: `{col}`")
        
        # Preview Table
        st.markdown("### 📋 Data Preview")
        st.dataframe(st.session_state.df.head(10), use_container_width=True)
        
        if st.button("✨ Go to Dashboard", use_container_width=True):
            st.switch_page("pages/3_Dashboard.py")
