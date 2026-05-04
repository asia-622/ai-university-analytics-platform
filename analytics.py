"""
Analytics Engine - Production-grade calculations & visualizations
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Tuple, Dict
import numpy as np

def department_attendance(df: pd.DataFrame, column_map: Dict) -> go.Figure:
    """Department-wise Average Attendance - Bar Chart"""
    if 'department' not in column_map or 'attendance' not in column_map:
        return go.Figure().add_annotation(text="Attendance data not available")
    
    dept_att = df.groupby(column_map['department'])[column_map['attendance']].mean().reset_index()
    
    fig = px.bar(
        dept_att, 
        x=column_map['department'], 
        y=column_map['attendance'],
        title="Average Attendance by Department",
        color=column_map['department'],
        color_discrete_sequence=['#4FC3F7', '#81D4FA', '#B39DDB', '#4DB6AC', '#26A69A']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#EAEAEA',
        showlegend=False
    )
    return fig

def student_distribution(df: pd.DataFrame, column_map: Dict) -> go.Figure:
    """Student Distribution by Department - Pie Chart"""
    if 'department' not in column_map:
        return go.Figure().add_annotation(text="Department data not available")
    
    dept_count = df[column_map['department']].value_counts().reset_index()
    dept_count.columns = ['Department', 'Count']
    
    fig = px.pie(
        dept_count, 
        values='Count', 
        names='Department',
        color_discrete_sequence=['#4FC3F7', '#81D4FA', '#B39DDB', '#4DB6AC', '#26A69A']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#EAEAEA',
        title="Student Distribution by Department"
    )
    return fig

def grade_distribution(df: pd.DataFrame, column_map: Dict) -> go.Figure:
    """Grade Distribution - Smart Detection"""
    if 'marks' not in column_map:
        return go.Figure().add_annotation(text="Marks data not available")
    
    marks_col = column_map['marks']
    grades = pd.cut(df[marks_col], 
                   bins=[0, 40, 50, 60, 70, 100], 
                   labels=['F', 'D', 'C', 'B', 'A'],
                   right=False)
    
    grade_count = grades.value_counts().sort_index().reset_index()
    grade_count.columns = ['Grade', 'Count']
    
    fig = px.bar(
        grade_count,
        x='Grade', 
        y='Count',
        title="Grade Distribution",
        color='Grade',
        color_discrete_sequence=['#EF5350', '#FF9800', '#FFEB3B', '#4CAF50', '#2196F3']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#EAEAEA',
        showlegend=False
    )
    return fig

def department_subject_analysis(df: pd.DataFrame, column_map: Dict) -> go.Figure:
    """Department + Semester Subject Analysis"""
    if 'subject' not in column_map or 'marks' not in column_map:
        return go.Figure()
    
    subject_avg = df.groupby(column_map['subject'])[column_map['marks']].mean().reset_index()
    subject_avg.columns = ['Subject', 'Average Marks']
    subject_avg = subject_avg.sort_values('Average Marks', ascending=True)
    
    fig = px.bar(
        subject_avg,
        x='Average Marks',
        y='Subject',
        orientation='h',
        title="Subject-wise Average Marks",
        color='Average Marks',
        color_continuous_scale=['#EF5350', '#FF9800', '#4CAF50', '#2196F3']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#EAEAEA'
    )
    return fig

def student_profile_analysis(df: pd.DataFrame, column_map: Dict) -> Tuple[go.Figure, pd.DataFrame]:
    """Complete Student Profile Analysis"""
    if 'subject' not in column_map or 'marks' not in column_map:
        fig = go.Figure()
        table = pd.DataFrame()
        return fig, table
    
    # Table
    table = df[[column_map['subject'], column_map['marks']]].copy()
    table.columns = ['Subject', 'Marks']
    table = table.sort_values('Marks', ascending=False)
    
    # Bar Chart
    fig = px.bar(
        table, 
        x='Marks', 
        y='Subject',
        orientation='h',
        title="Student Performance by Subject",
        color='Marks',
        color_continuous_scale=['#EF5350', '#FF9800', '#4CAF50', '#2196F3']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#EAEAEA'
    )
    
    return fig, table
