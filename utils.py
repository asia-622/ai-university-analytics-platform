"""
Utility functions for AI University Analytics Agent
Auto Column Detection • Data Validation • Cleaning
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import re

def detect_columns(df: pd.DataFrame) -> Dict[str, str]:
    """
    AUTO COLUMN DETECTION - Production Critical
    Maps dataset columns to standard names using fuzzy matching
    """
    column_map = {}
    
    # All column names (lowercase for matching)
    cols_lower = {col.lower(): col for col in df.columns}
    
    # Smart detection patterns
    patterns = {
        'student': [
            'student', 'name', 'student_name', 'student_id', 'roll', 'roll_number', 
            'id', 'studentid', 'regno', 'reg_no', 'matric', 'enroll'
        ],
        'department': [
            'department', 'dept', 'program', 'course', 'branch', 'major', 'faculty'
        ],
        'subject': ['subject', 'course', 'paper', 'module'],
        'marks': ['marks', 'score', 'grade', 'percentage', 'mark', 'total'],
        'attendance': ['attendance', 'att', 'attn', 'present']
    }
    
    # Detect each column type
    for key, keywords in patterns.items():
        for col_lower, original_col in cols_lower.items():
            if any(keyword in col_lower for keyword in keywords):
                column_map[key] = original_col
                break
    
    # Fallback: use first numeric columns for marks
    if 'marks' not in column_map:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            column_map['marks'] = numeric_cols[0]
    
    return column_map

def safe_load_data(file) -> pd.DataFrame:
    """Safely load any file type with error handling"""
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file, low_memory=False)
        elif file.name.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file)
        elif file.name.endswith('.parquet'):
            return pd.read_parquet(file)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise ValueError(f"File loading failed: {str(e)}")

def validate_dataset(df: pd.DataFrame, column_map: Dict) -> None:
    """Production-grade dataset validation"""
    required = ['student', 'department']
    missing = [req for req in required if req not in column_map]
    
    if missing:
        raise ValueError(f"Missing critical columns: {missing}")
    
    if len(df) == 0:
        raise ValueError("Dataset is empty")
    
    # Check for basic data quality
    if df[column_map['student']].isnull().all():
        raise ValueError("Student column contains only null values")

def clean_data(df: pd.DataFrame, column_map: Dict) -> pd.DataFrame:
    """Production-grade data cleaning"""
    df_clean = df.copy()
    
    # Safe cleaning operations
    for col_type, col_name in column_map.items():
        if col_name in df_clean.columns:
            # Fill NaN with 0 for numeric columns
            if col_type in ['marks', 'attendance']:
                df_clean[col_name] = pd.to_numeric(df_clean[col_name], errors='coerce').fillna(0)
            # Strip whitespace for categorical
            else:
                df_clean[col_name] = df_clean[col_name].astype(str).str.strip()
    
    return df_clean

def get_departments(df: pd.DataFrame, column_map: Dict) -> List[str]:
    """Get unique departments safely"""
    if 'department' in column_map:
        return sorted(df[column_map['department']].dropna().unique().astype(str))
    return []

def get_semesters(df: pd.DataFrame, column_map: Dict, department: str) -> List[str]:
    """Get semesters for specific department"""
    dept_col = column_map.get('department')
    if dept_col and dept_col in df.columns:
        dept_data = df[df[dept_col] == department]
        semester_cols = [col for col in df.columns if 'semester' in col.lower() or 'sem' in col.lower()]
        if semester_cols:
            return sorted(dept_data[semester_cols[0]].dropna().unique().astype(str))
    return sorted(df.columns[df.columns.str.contains('semester|sem', case=False, na=False)])
