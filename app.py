"""
AI University Analytics Agent - Production-Ready
Final Year University Project
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from utils import (
    detect_columns, validate_dataset, safe_load_data, 
    clean_data, get_departments, get_semesters
)
from analytics import (
    department_attendance, student_distribution, grade_distribution,
    department_subject_analysis, student_profile_analysis
)
from ai_agent import AIUniversityAgent

# Page config
st.set_page_config(
    page_title="AI University Analytics Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Professional Theme
st.markdown("""
    <style>
    /* Main background */
    .main {background-color: #0B1F3A;}
    
    /* Sidebar */
    .css-1d391kg {background-color: #1A2D4E;}
    .css-h5rgaw {background-color: #1A2D4E;}
    
    /* Headers */
    .st-emotion-cache-1gffh {color: #EAEAEA;}
    .st-emotion-cache-1gffh h1 {color: #4FC3F7;}
    .st-emotion-cache-1gffh h2 {color: #81D4FA;}
    .st-emotion-cache-1gffh h3 {color: #B39DDB;}
    
    /* Text */
    .stMarkdown {color: #EAEAEA;}
    
    /* Cards */
    .metric-container {background-color: #1A2D4E; padding: 1rem; border-radius: 10px;}
    
    /* Selectbox */
    .stSelectbox > div > div > div {background-color: #2A3F5F;}
    
    /* Buttons */
    .stButton > button {background-color: #4FC3F7; color: #0B1F3A;}
    .stButton > button:hover {background-color: #29B6F6;}
    
    /* Dataframe */
    .dataframe {background-color: #1A2D4E;}
    .dataframe th {background-color: #2A3F5F; color: #EAEAEA;}
    .dataframe td {color: #CFCFCF;}
    </style>
""", unsafe_allow_html=True)

class UniversityAnalyticsApp:
    def __init__(self):
        self.df = None
        self.column_map = {}
        self.ai_agent = AIUniversityAgent()
    
    def initialize_session(self):
        """Initialize session state"""
        if 'df' not in st.session_state:
            st.session_state.df = None
        if 'column_map' not in st.session_state:
            st.session_state.column_map = {}
        if 'departments' not in st.session_state:
            st.session_state.departments = []
    
    def sidebar_file_upload(self):
        """Professional sidebar file upload"""
        st.sidebar.markdown("## 📁 Upload Dataset")
        st.sidebar.markdown("**Supports: CSV, Excel, Parquet**")
        
        uploaded_file = st.sidebar.file_uploader(
            "Choose file", 
            type=['csv', 'xlsx', 'xls', 'parquet'],
            help="Upload your university dataset (max 200MB)"
        )
        
        if uploaded_file is not None:
            try:
                with st.spinner("🔄 Analyzing dataset structure..."):
                    self.df = safe_load_data(uploaded_file)
                    self.column_map = detect_columns(self.df)
                    validate_dataset(self.df, self.column_map)
                    
                    st.session_state.df = self.df
                    st.session_state.column_map = self.column_map
                    st.session_state.departments = get_departments(self.df, self.column_map)
                
                st.sidebar.success(f"✅ Loaded {len(self.df):,} rows")
                st.sidebar.metric("Columns", len(self.df.columns))
                st.sidebar.markdown(f"**Detected Columns:** {', '.join(self.column_map.keys())}")
                
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)}")
                st.sidebar.info("💡 Ensure your dataset has student/department/marks data")
        
        return uploaded_file is not None
    
    def display_header(self):
        """Display professional header"""
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("# 🎓 AI University Analytics Agent")
            st.markdown("### Production-Ready • Auto Column Detection • Scalable")
        with col2:
            if self.df is not None:
                st.metric("Total Students", f"{len(self.df):,}")
        with col3:
            if self.df is not None:
                st.metric("Departments", len(self.column_map.get('department', [])))
    
    def dashboard_page(self):
        """Main Dashboard - 3 metrics only"""
        if self.df is None:
            st.info("👆 Please upload a dataset first")
            return
        
        self.df_clean = clean_data(self.df, self.column_map)
        
        # 3 Column Layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Department-wise Attendance")
            fig1 = department_attendance(self.df_clean, self.column_map)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("### 👥 Student Distribution")
            fig2 = student_distribution(self.df_clean, self.column_map)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            st.markdown("### 📈 Grade Distribution")
            fig3 = grade_distribution(self.df_clean, self.column_map)
            st.plotly_chart(fig3, use_container_width=True)
    
    def department_analysis_page(self):
        """Department-wise Subject Analysis"""
        if self.df is None:
            st.warning("👆 Please upload dataset first")
            return
        
        st.markdown("## 🎯 Department-wise Subject Analysis")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            dept = st.selectbox(
                "Select Department",
                options=self.column_map.get('department', []),
                key="dept_select"
            )
            
            if dept:
                semesters = get_semesters(self.df, self.column_map, dept)
                semester = st.selectbox(
                    "Select Semester",
                    options=semesters,
                    key="semester_select"
                )
        
        if dept and 'semester_select' in st.session_state:
            filtered_df = self.df[
                (self.df[self.column_map['department']] == dept) &
                (self.df[self.column_map.get('semester', 'Semester')] == st.session_state.semester_select)
            ].copy()
            
            if not filtered_df.empty:
                fig = department_subject_analysis(filtered_df, self.column_map)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data found for selected filters")
    
    def student_search_page(self):
        """Student Profile Search"""
        if self.df is None:
            st.warning("👆 Please upload dataset first")
            return
        
        st.markdown("## 🔍 Student Profile Search")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            student_name = st.text_input(
                "Search Student Name/ID",
                placeholder="Enter student name or ID"
            )
        
        if student_name:
            student_data = self.df[
                self.df[self.column_map['student']].str.contains(student_name, case=False, na=False)
            ]
            
            if not student_data.empty:
                st.markdown(f"### 📋 {student_data.iloc[0][self.column_map['student']]}")
                
                fig, table = student_profile_analysis(student_data, self.column_map)
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(table, use_container_width=True)
            else:
                st.warning("Student not found")
    
    def run(self):
        """Main app runner"""
        self.initialize_session()
        
        # Check if data loaded
        if 'df' in st.session_state and st.session_state.df is not None:
            self.df = st.session_state.df
            self.column_map = st.session_state.column_map
        
        # Sidebar
        data_loaded = self.sidebar_file_upload()
        
        # Header
        self.display_header()
        
        # Navigation
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🎯 Dept Analysis", "🔍 Student Search"])
        
        with tab1:
            self.dashboard_page()
        
        with tab2:
            self.department_analysis_page()
        
        with tab3:
            self.student_search_page()
        
        # Footer
        st.markdown("---")
        st.markdown("*Built with ❤️ for Final Year Project | Production-Ready AI Analytics*")

def main():
    app = UniversityAnalyticsApp()
    app.run()

if __name__ == "__main__":
    main()
