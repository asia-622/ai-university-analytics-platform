def render_department_analytics():
    if st.session_state.df is None:
        st.warning("👆 Please upload data first")
        st.stop()
    
    st.markdown("## 🏛️ Department Analytics")
    
    df = st.session_state.df
    column_map = st.session_state.column_map
    
    # FIXED: Dynamic Department Dropdown
    dept_col = column_map.get('department', df.columns[0])
    departments = sorted(df[dept_col].dropna().unique())[:10]  # Top 10
    
    selected_dept = st.selectbox(
        "Select Department",
        options=departments,
        index=0
    )
    
    if selected_dept:
        # Filter data
        dept_data = df[df[dept_col] == selected_dept]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### 📊 {selected_dept} Overview")
            st.metric("Students", len(dept_data))
            st.metric("Avg Performance", f"{dept_data[column_map.get('marks', 'marks')].mean():.1f}%")
        
        with col2:
            # Semesters (FIXED - Dynamic detection)
            semester_cols = [col for col in df.columns if any(x in col.lower() for x in ['semester', 'sem', 'term'])]
            if semester_cols:
                semesters = sorted(dept_data[semester_cols[0]].dropna().unique())
                selected_sem = st.selectbox("Semester", options=semesters)
                
                sem_data = dept_data[dept_data[semester_cols[0]] == selected_sem]
                
                fig = px.bar(
                    x=sem_data.head(10)[column_map.get('student', 'student')],
                    y=sem_data.head(10)[column_map.get('marks', 'marks')],
                    title=f"{selected_dept} - {selected_sem} Performance"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Student List Table
        st.markdown("### 👥 Top Students")
        student_col = column_map.get('student', 'student')
        marks_col = column_map.get('marks', 'marks')
        
        top_students = dept_data.nlargest(10, marks_col)[[student_col, marks_col]]
        top_students.columns = ['Student', 'Marks']
        st.dataframe(top_students, use_container_width=True)
