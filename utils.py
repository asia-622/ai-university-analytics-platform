import pandas as pd
import numpy as np

def detect_columns(df):
    """Smart column detection"""
    cols_lower = [col.lower() for col in df.columns]
    column_map = {}
    
    # Student patterns
    student_patterns = ['student', 'name', 'id', 'roll']
    for i, col in enumerate(cols_lower):
        if any(pattern in col for pattern in student_patterns):
            column_map['student'] = df.columns[i]
            break
    
    # Department patterns  
    dept_patterns = ['dept', 'department', 'branch']
    for i, col in enumerate(cols_lower):
        if any(pattern in col for pattern in dept_patterns):
            column_map['department'] = df.columns[i]
            break
    
    # Marks patterns
    marks_patterns = ['marks', 'score', 'grade']
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if numeric_cols.size > 0:
        column_map['marks'] = numeric_cols[0]
    
    return column_map

def safe_load_data(file):
    """Safe file loading"""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)
