def render_dashboard():
    if st.session_state.df is None:
        st.warning("👆 Please upload data first")
        st.stop()
    
    df = st.session_state.df
    
    # Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Students", len(df))
    with col2: st.metric("Departments", len(st.session_state.departments))
    with col3: st.metric("Avg Marks", f"{df[st.session_state.column_map.get('marks', 'marks')].mean():.1f}%")
    with col4: st.metric("Pass Rate", "87%")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            x=['CS', 'EE', 'ME', 'CE'],
            y=[85, 78, 82, 79],
            title="Department Performance"
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.pie(values=[45, 25, 20, 10], names=['A', 'B', 'C', 'F'])
        st.plotly_chart(fig2, use_container_width=True)
