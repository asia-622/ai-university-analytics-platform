import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Custom CSS - Professional SaaS Design
st.markdown("""
<style>
    /* Main Background */
    .main {background-color: #F8FAFC;}
    
    /* Sidebar */
    .css-1d391kg {background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);}
    .css-h5rgaw {background: linear-gradient(180deg, #ffffff 0%, #f1f5f9 100%);}
    
    /* Navigation Menu */
    .nav-link {color: #64748b !important; font-weight: 500; padding: 8px 12px;}
    .nav-link:hover {color: #2563EB !important; background-color: #EFF6FF;}
    
    /* Active Page */
    .nav-link[data-baseweb="tab-list"] [data-baseweb="tab"][aria-selected="true"] {
        color: #2563EB !important; 
        background-color: #EFF6FF;
        border-radius: 8px;
    }
    
    /* Cards */
    .metric-container {background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
    
    /* Headers */
    h1 {color: #1E293B !important; font-size: 2.5rem; font-weight: 700;}
    h2 {color: #1E293B !important; font-size: 1.75rem; font-weight: 600;}
    h3 {color: #334155 !important; font-size: 1.25rem; font-weight: 600;}
    
    /* Text */
    .stMarkdown {color: #1E293B;}
    
    /* Buttons */
    .stButton > button {background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); 
                       color: white; border-radius: 8px; font-weight: 500;}
    .stButton > button:hover {background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);}
    
    /* Dataframe */
    .dataframe {background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
    .dataframe th {background: #F8FAFC; color: #1E293B; font-weight: 600;}
    
    /* Selectbox */
    .stSelectbox > div > div > div {background: white; border: 1px solid #E2E8F0;}
    
    /* File Uploader */
    .uploadedFile {background: #EFF6FF; border: 2px dashed #2563EB; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

# Page Config
st.set_page_config(
    page_title="AI University Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'df' not in st.session_state:
    st.session_state.df = None
if 'column_map' not in st.session_state:
    st.session_state.column_map = {}
if 'departments' not in st.session_state:
    st.session_state.departments = []
if 'semesters' not in st.session_state:
    st.session_state.semesters = []

# Sidebar Navigation
st.sidebar.title("🎓 AI University Analytics")
st.sidebar.markdown("---")

# Navigation Menu
nav_options = [
    "🏠 Home",
    "📤 Upload & Analyze", 
    "📊 Dashboard",
    "📚 Subject Analysis",
    "🏛️ Department Analytics",
    "👤 Student Search",
    "⚖️ Comparison Tool",
    "🤖 AI Chat Assistant"
]

selected_page = st.sidebar.radio(
    "Navigation",
    options=nav_options,
    index=0,
    format_func=lambda x: x
)

# Header
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("# 🎓 AI University Analytics Platform")
    st.markdown("**Professional SaaS Dashboard for University Data Analysis**")
with col2:
    if st.session_state.df is not None:
        st.metric("Total Students", f"{len(st.session_state.df):,}")
with col3:
    if st.session_state.df is not None:
        st.metric("Departments", len(set(st.session_state.departments)))

st.markdown("---")

# Page Routing
if selected_page == "🏠 Home":
    st.session_state.current_page = "home"
    exec(open('pages/1_Home.py').read())
elif selected_page == "📤 Upload & Analyze":
    st.session_state.current_page = "upload"
    exec(open('pages/2_Upload_Analyze.py').read())
elif selected_page == "📊 Dashboard":
    st.session_state.current_page = "dashboard"
    exec(open('pages/3_Dashboard.py').read())
elif selected_page == "📚 Subject Analysis":
    st.session_state.current_page = "subjects"
    exec(open('pages/4_Subject_Analysis.py').read())
elif selected_page == "🏛️ Department Analytics":
    st.session_state.current_page = "departments"
    exec(open('pages/5_Department_Analytics.py').read())
elif selected_page == "👤 Student Search":
    st.session_state.current_page = "student"
    exec(open('pages/6_Student_Search.py').read())
elif selected_page == "⚖️ Comparison Tool":
    st.session_state.current_page = "comparison"
    exec(open('pages/7_Comparison.py').read())
elif selected_page == "🤖 AI Chat Assistant":
    st.session_state.current_page = "chat"
    exec(open('pages/8_AI_Chat.py').read())
