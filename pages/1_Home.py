def render_home():
    st.markdown("## 👋 Welcome to AI University Analytics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### 👥 Total Students
        **1,247**
        """)
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### 🏛️ Departments
        **8**
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Average GPA
        **3.45**
        """)
    
    with col4:
        st.markdown("""
        ### ✅ Pass Rate
        **87%**
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Quick Start")
        st.markdown("""
        1. **Upload** your CSV/Excel file
        2. **Auto-detect** columns (Student, Dept, Marks)
        3. **Explore** interactive dashboards
        4. **Get AI insights** instantly
        """)
        if st.button("📤 Upload Data Now", use_container_width=True):
            st.switch_page("pages/2_Upload_Analyze.py")
    
    with col2:
        st.markdown("### ✨ Features")
        st.markdown("""
        - **Auto Column Detection**
        - **Real-time Analytics**
        - **AI-Powered Insights**  
        - **Student Profiles**
        - **Department Comparison**
        """)
