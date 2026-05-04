"""
AI University Agent - Smart Insights & Recommendations
Production-ready AI layer for analytics insights
"""

import pandas as pd
from typing import Dict, List
import numpy as np

class AIUniversityAgent:
    def __init__(self):
        self.insights = []
    
    def generate_insights(self, df: pd.DataFrame, column_map: Dict) -> List[str]:
        """AI-powered insights generation"""
        insights = []
        
        if 'department' in column_map and 'attendance' in column_map:
            avg_att = df[column_map['attendance']].mean()
            insights.append(f"📊 Average attendance across university: {avg_att:.1f}%")
        
        if 'marks' in column_map:
            avg_marks = df[column_map['marks']].mean()
            insights.append(f"📈 University average marks: {avg_marks:.1f}%")
            
            low_performers = len(df[df[column_map['marks']] < 40])
            insights.append(f"⚠️ Students needing attention (<40%): {low_performers}")
        
        return insights
    
    def risk_analysis(self, df: pd.DataFrame, column_map: Dict) -> Dict:
        """AI Risk Assessment"""
        risks = {
            'high_risk': 0,
            'medium_risk': 0,
            'low_risk': 0
        }
        
        if 'marks' in column_map and 'attendance' in column_map:
            for _, row in df.iterrows():
                marks = row[column_map['marks']]
                att = row[column_map['attendance']]
                
                if marks < 40 or att < 60:
                    risks['high_risk'] += 1
                elif marks < 60 or att < 75:
                    risks['medium_risk'] += 1
                else:
                    risks['low_risk'] += 1
        
        return risks
