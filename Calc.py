import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="CECS Financial Analytics | UTK",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = []

def load_css():
    st.markdown("""
        <style>
        /* ========== GLOBAL STYLES ========== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Main background - dark */
        .main {
            background-color: #1a1a1a;
        }

        /* ========== SIDEBAR - GREY NOT WHITE ========== */
        section[data-testid="stSidebar"] {
            background-color: #2c2c2c !important;
            border-right: 1px solid #3a3a3a;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
            background-color: #2c2c2c;
        }

        /* Sidebar text colors */
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #e0e0e0 !important;
        }

        section[data-testid="stSidebar"] .stMarkdown {
            color: #e0e0e0 !important;
        }

        /* ========== TYPOGRAPHY ========== */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        /* Main title - WHITE not grey */
        h1 {
            color: #FFFFFF !important;
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* Subtitle - ORANGE */
        h3 {
            color: #FF8200 !important;
            font-size: 1.3rem !important;
        }

        h2 {
            color: #e0e0e0 !important;
            font-size: 1.8rem !important;
            margin-top: 1.5rem !important;
        }

        h4 {
            color: #FF8200 !important;
            font-size: 1.1rem !important;
        }

        /* Regular text on dark background */
        p, span, div {
            color: #e0e0e0;
        }

        /* ========== METRIC CARDS - DARK CARDS WITH ORANGE BORDER ========== */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #2c2c2c 0%, #3a3a3a 100%) !important;
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px solid #FF8200;
            box-shadow: 0 4px 12px rgba(255, 130, 0, 0.3);
            transition: all 0.3s ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(255, 130, 0, 0.5);
            border-color: #ff9f40;
            background: linear-gradient(135deg, #3a3a3a 0%, #4a4a4a 100%) !important;
        }

        /* Metric values - WHITE on dark cards */
        div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stMetricValue"] > div {
            color: #FFFFFF !important;
        }

        /* Metric labels - LIGHT GREY on dark cards */
        div[data-testid="stMetricLabel"] {
            color: #b0b0b0 !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem !important;
        }

        div[data-testid="stMetricLabel"] > div {
            color: #b0b0b0 !important;
        }

        /* Metric delta - BRIGHT ORANGE */
        div[data-testid="stMetricDelta"] {
            color: #ff9f40 !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
        }

        div[data-testid="stMetricDelta"] svg {
            fill: #ff9f40 !important;
        }

        /* ========== INPUT FIELDS ========== */
        div[data-testid="stNumberInput"] > div > div > input {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #e0e0e0 !important;
            background-color: #3a3a3a !important;
            border: 2px solid #4a4a4a !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            transition: all 0.2s ease;
        }

        div[data-testid="stNumberInput"] > div > div > input:focus {
            border-color: #FF8200 !important;
            box-shadow: 0 0 0 3px rgba(255, 130, 0, 0.2) !important;
            outline: none !important;
            background-color: #404040 !important;
        }

        /* ========== TEXT INPUTS ========== */
        input[type="text"], input[type="password"] {
            color: #e0e0e0 !important;
            background-color: #3a3a3a !important;
            border-color: #4a4a4a !important;
        }

        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #FF8200 !important;
            background-color: #404040 !important;
        }

        /* ========== SLIDERS ========== */
        .stSlider > div > div > div > div {
            background-color: #FF8200 !important;
        }

        .stSlider > div > div > div > div > div {
            color: #e0e0e0 !important;
            font-weight: 600 !important;
        }

        .stSlider [role="slider"] {
            background-color: #FF8200 !important;
        }

        .stSlider label {
            color: #e0e0e0 !important;
            font-weight: 600 !important;
        }

        /* ========== TABS ========== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #3a3a3a;
            border-radius: 8px;
            color: #b0b0b0 !important;
            font-weight: 600;
            padding: 0.75rem 1.5rem;
            border: 2px solid transparent;
            transition: all 0.2s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: #4a4a4a;
            color: #FF8200 !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: #FF8200 !important;
            color: white !important;
            border-color: #FF8200;
        }

        /* ========== BUTTONS ========== */
        .stButton > button {
            background-color: #FF8200;
            color: white !important;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 0.75rem 2rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px rgba(255, 130, 0, 0.3);
        }

        .stButton > button:hover {
            background-color: #e67700;
            box-shadow: 0 6px 12px rgba(255, 130, 0, 0.5);
            transform: translateY(-1px);
        }

        .stButton > button p {
            color: white !important;
        }

        /* ========== CUSTOM COMPONENTS ========== */
        .hero-banner {
            background: linear-gradient(135deg, #FF8200 0%, #ff9f40 100%);
            padding: 2rem;
            border-radius: 16px;
            color: white !important;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(255, 130, 0, 0.4);
        }

        .hero-banner h1, .hero-banner p {
            color: white !important;
        }

        .alert-success {
            background-color: #1e4620;
            border-left: 4px solid #28a745;
            padding: 1rem;
            border-radius: 8px;
            color: #8fd99c !important;
            font-weight: 600;
        }

        .alert-warning {
            background-color: #4a3b1a;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            border-radius: 8px;
            color: #ffd666 !important;
            font-weight: 600;
        }

        .alert-danger {
            background-color: #4a1a1a;
            border-left: 4px solid #dc3545;
            padding: 1rem;
            border-radius: 8px;
            color: #ff8888 !important;
            font-weight: 600;
        }

        /* ========== EXPANDER ========== */
        .streamlit-expanderHeader {
            background-color: #3a3a3a;
            border-radius: 8px;
            border: 1px solid #4a4a4a;
            font-weight: 600;
            color: #e0e0e0 !important;
        }

        details summary {
            color: #e0e0e0 !important;
        }

        /* ========== DATAFRAME ========== */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
            background-color: #2c2c2c;
        }

        .dataframe th {
            background-color: #FF8200 !important;
            color: white !important;
        }

        .dataframe td {
            color: #e0e0e0 !important;
            background-color: #3a3a3a !important;
        }

        .dataframe tr:hover td {
            background-color: #4a4a4a !important;
        }

        /* ========== CHECKBOX ========== */
        .stCheckbox label {
            color: #e0e0e0 !important;
        }

        /* ========== COLOR PICKER ========== */
        .stColorPicker label {
            color: #e0e0e0 !important;
        }

        /* ========== ANIMATIONS ========== */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }

        /* ========== PLOTLY CHARTS - DARK BACKGROUND ========== */
        .js-plotly-plot {
            border-radius: 12px;
            overflow: hidden;
            background: linear-gradient(135deg, #2c2c2c 0%, #3a3a3a 100%) !important;
            box-shadow: 0 4px 12px rgba(255, 130, 0, 0.3);
            border: 2px solid #FF8200;
            padding: 1rem;
        }

        /* ========== RADIO BUTTONS ========== */
        .stRadio label {
            color: #e0e0e0 !important;
        }

        /* ========== SELECT BOX ========== */
        .stSelectbox label {
            color: #e0e0e0 !important;
        }

        /* ========== DIVIDER ========== */
        hr {
            border-color: #3a3a3a !important;
        }

        /* ========== INFO BOXES ========== */
        .stAlert {
            background-color: #2c2c2c !important;
            color: #e0e0e0 !important;
            border: 1px solid #4a4a4a !important;
        }
        </style>
    """, unsafe_allow_html=True)

def login_page():
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
        }
        .login-container {
            background: #2c2c2c;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            max-width: 450px;
            margin: 5rem auto;
            border: 1px solid #3a3a3a;
        }
        .login-logo {
            text-align: center;
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        .login-title {
            color: #FF8200 !important;
            text-align: center;
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            color: #b0b0b0 !important;
            text-align: center;
            font-size: 1rem;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
            <div class="login-container">
                <div class="login-logo">🍊</div>
                <div class="login-title">CECS Analytics</div>
                <div class="login-subtitle">University of Tennessee, Knoxville</div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("🚀 Login", use_container_width=True)

            if submit:
                if username == "CECS" and password == "UTK":
                    st.session_state.logged_in = True
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

        st.markdown("---")
        st.markdown("""
            <p style='text-align: center; color: #b0b0b0; font-size: 0.875rem;'>
                <strong>Demo Credentials:</strong><br>
                Username: <code>CECS</code> | Password: <code>UTK</code>
            </p>
        """, unsafe_allow_html=True)

def main_dashboard():
    load_css()

    # HEADER
    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        st.markdown("<div style='font-size: 3rem;'>🍊</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h1 style='color: #FFFFFF !important;'>UNIVERSITY OF TENNESSEE</h1>", unsafe_allow_html=True)
        st.markdown(
            "<h3 style='color: #FF8200 !important;'>College of Emerging & Collaborative Studies | Financial Analytics Platform</h3>",
            unsafe_allow_html=True)

    with col3:
        if st.button("🚪 Logout", key="logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")

    # SIDEBAR
    with st.sidebar:
        st.markdown("## ⚙️ SCENARIO CONFIGURATION")
        st.markdown("---")

        st.markdown("### 📊 Enrollment Data")
        students = st.number_input(
            "Total Students Enrolled",
            min_value=0,
            max_value=50000,
            value=6000,
            step=100,
            help="Projected student enrollment"
        )

        st.markdown("### 💰 Revenue Parameters")
        tuition_per_student = st.number_input(
            "Average Tuition per Student",
            min_value=0,
            max_value=100000,
            value=12000,
            step=500,
            help="Annual tuition revenue per student"
        )

        other_revenue = st.number_input(
            "Other Revenue Sources",
            min_value=0,
            value=0,
            step=10000,
            help="Grants, donations, auxiliary revenue"
        )

        st.markdown("---")

        with st.expander("🔧 Advanced Settings"):
            inflation_rate = st.slider("Inflation Rate (%)", 0.0, 10.0, 3.0, 0.1)
            contingency_fund = st.slider("Contingency Fund (%)", 0, 20, 5, 1)
            show_detailed_breakdown = st.checkbox("Show Detailed Breakdown", value=True)

        st.markdown("---")

        st.markdown("### 💾 Scenario Management")
        scenario_name = st.text_input("Scenario Name", placeholder="e.g., Conservative 2025")
        if st.button("💾 Save Current Scenario", use_container_width=True):
            st.session_state.scenarios.append({
                'name': scenario_name if scenario_name else f"Scenario {len(st.session_state.scenarios) + 1}",
                'students': students,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("✅ Scenario saved!")

        if st.session_state.scenarios:
            st.markdown("**Saved Scenarios:**")
            for idx, scenario in enumerate(st.session_state.scenarios):
                st.markdown(
                    f"<p style='color: #b0b0b0;'>{idx + 1}. {scenario['name']} ({scenario['students']:,} students)</p>",
                    unsafe_allow_html=True)

    # HERO BANNER
    st.markdown(f"""
        <div class="hero-banner fade-in">
            <h1 style="color: white; margin: 0; font-size: 2.5rem;">FINANCIAL SCENARIO ANALYSIS</h1>
            <p style="font-size: 1.5rem; margin: 0.5rem 0 0 0; font-weight: 600; color: white;">
                {students:,} Students | Academic Year 2025-2026
            </p>
        </div>
    """, unsafe_allow_html=True)

    # TABS
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Executive Dashboard",
        "👥 Staffing Analysis",
        "💰 Financial Details",
        "📈 Advanced Analytics"
    ])

    with tab1:
        st.markdown("<h2 style='color: #e0e0e0;'>📊 Executive Summary</h2>", unsafe_allow_html=True)

        with st.expander("⚙️ Configure Staffing Ratios & Compensation"):
            st.markdown("### Staffing Ratios")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**👨‍🏫 Faculty**")
                faculty_ratio = st.slider("Students per FT Faculty", 10, 100, 50)
                adjunct_ratio = st.slider("Students per Adjunct", 20, 200, 100)

            with col2:
                st.markdown("**👔 Staff & Support**")
                staff_ratio = st.slider("Students per Staff", 50, 500, 200)
                ambassador_ratio = st.slider("Students per Ambassador", 100, 1000, 300)

            with col3:
                st.markdown("**🎓 Academic Support**")
                grader_ratio = st.slider("Students per Grader", 50, 300, 150)
                tutor_ratio = st.slider("Students per Tutor", 50, 300, 200)

            st.markdown("---")
            st.markdown("### Annual Compensation")

            col1, col2, col3 = st.columns(3)

            with col1:
                faculty_salary = st.number_input("FT Faculty Salary", value=75000, step=5000)
                adjunct_salary = st.number_input("Adjunct Salary", value=40000, step=2000)

            with col2:
                staff_salary = st.number_input("Staff Salary", value=50000, step=2000)
                ambassador_pay = st.number_input("Ambassador Pay", value=15000, step=1000)

            with col3:
                grader_pay = st.number_input("Grader Pay", value=10000, step=500)
                tutor_pay = st.number_input("Tutor Pay", value=12000, step=500)

            operating_per_student = st.number_input(
                "Operating Cost per Student",
                value=500,
                step=50
            )

        # CALCULATIONS
        full_time_faculty = max(1, int(students / faculty_ratio)) if faculty_ratio > 0 else 0
        adjunct_faculty = max(1, int(students / adjunct_ratio)) if adjunct_ratio > 0 else 0
        staff_members = max(1, int(students / staff_ratio)) if staff_ratio > 0 else 0
        ambassadors = int(students / ambassador_ratio) if ambassador_ratio > 0 else 0
        graders = int(students / grader_ratio) if grader_ratio > 0 else 0
        tutors = int(students / tutor_ratio) if tutor_ratio > 0 else 0

        faculty_cost = full_time_faculty * faculty_salary
        adjunct_cost = adjunct_faculty * adjunct_salary
        staff_cost = staff_members * staff_salary
        ambassador_cost = ambassadors * ambassador_pay
        grader_cost = graders * grader_pay
        tutor_cost = tutors * tutor_pay
        operating_cost = students * operating_per_student

        total_personnel = (full_time_faculty + adjunct_faculty + staff_members +
                           ambassadors + graders + tutors)
        total_personnel_cost = (faculty_cost + adjunct_cost + staff_cost +
                                ambassador_cost + grader_cost + tutor_cost)
        total_cost = total_personnel_cost + operating_cost

        total_revenue = (students * tuition_per_student) + other_revenue
        net_result = total_revenue - total_cost

        # KEY METRICS
        st.markdown("<h3 style='color: #e0e0e0;'>💎 Key Performance Indicators</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Revenue",
                f"${total_revenue:,.0f}",
                delta=f"{(other_revenue / total_revenue * 100):.1f}% other" if other_revenue > 0 else None
            )

        with col2:
            st.metric(
                "Total Expenses",
                f"${total_cost:,.0f}",
                delta=f"{(total_cost / total_revenue * 100):.1f}% of revenue" if total_revenue > 0 else None
            )

        with col3:
            delta_text = "Surplus" if net_result >= 0 else "Deficit"
            st.metric(
                "Net Position",
                f"${net_result:,.0f}",
                delta=delta_text,
                delta_color="normal" if net_result >= 0 else "inverse"
            )

        with col4:
            margin = (net_result / total_revenue * 100) if total_revenue > 0 else 0
            st.metric(
                "Profit Margin",
                f"{margin:.2f}%",
                delta="Healthy" if margin > 10 else "Monitor"
            )

        st.markdown("---")

        # FINANCIAL HEALTH ALERT
        if net_result >= 0:
            st.markdown(f"""
                <div class="alert-success">
                    ✅ <strong>SURPLUS POSITION:</strong> The college is projected to operate with a surplus of ${net_result:,.0f}.
                </div>
            """, unsafe_allow_html=True)
        elif net_result > -100000:
            st.markdown(f"""
                <div class="alert-warning">
                    ⚠️ <strong>MINOR DEFICIT:</strong> Projected deficit of ${abs(net_result):,.0f}. Consider optimization.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="alert-danger">
                    🚨 <strong>SIGNIFICANT DEFICIT:</strong> Projected deficit of ${abs(net_result):,.0f}. Immediate action required.
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # VISUAL BREAKDOWN - DARK BACKGROUNDS
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3 style='color: #e0e0e0;'>💰 Revenue vs Expenses</h3>", unsafe_allow_html=True)

            fig_comparison = go.Figure()
            fig_comparison.add_trace(go.Bar(
                name='Revenue',
                x=['Financial Overview'],
                y=[total_revenue],
                marker_color='#28a745',
                text=[f'${total_revenue:,.0f}'],
                textposition='outside',
                textfont=dict(color='#e0e0e0', size=14, family='Inter')
            ))
            fig_comparison.add_trace(go.Bar(
                name='Expenses',
                x=['Financial Overview'],
                y=[total_cost],
                marker_color='#dc3545',
                text=[f'${total_cost:,.0f}'],
                textposition='outside',
                textfont=dict(color='#e0e0e0', size=14, family='Inter')
            ))

            fig_comparison.update_layout(
                barmode='group',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(44, 44, 44, 1)',
                font=dict(size=12, color='#e0e0e0', family='Inter'),
                margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(font=dict(color='#e0e0e0'))
            )

            st.plotly_chart(fig_comparison, use_container_width=True)

        with col2:
            st.markdown("<h3 style='color: #e0e0e0;'>📊 Expense Distribution</h3>", unsafe_allow_html=True)

            expense_data = pd.DataFrame({
                'Category': ['Faculty (FT)', 'Faculty (Adj)', 'Staff', 'Ambassadors',
                             'Graders', 'Tutors', 'Operations'],
                'Amount': [faculty_cost, adjunct_cost, staff_cost, ambassador_cost,
                           grader_cost, tutor_cost, operating_cost]
            })

            fig_pie = px.pie(
                expense_data,
                values='Amount',
                names='Category',
                color_discrete_sequence=px.colors.sequential.Oranges_r,
                hole=0.4
            )

            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=11,
                textfont_color='white'
            )

            fig_pie.update_layout(
                height=400,
                showlegend=False,
                paper_bgcolor='rgba(44, 44, 44, 1)',
                margin=dict(t=20, b=20, l=20, r=20),
                font=dict(family='Inter', color='#e0e0e0')
            )

            st.plotly_chart(fig_pie, use_container_width=True)

        # QUICK STATS
        st.markdown("---")
        st.markdown("<h3 style='color: #e0e0e0;'>📋 Quick Statistics</h3>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            cost_per_student = total_cost / students if students > 0 else 0
            st.metric("Cost per Student", f"${cost_per_student:,.2f}")

        with col2:
            revenue_per_student = total_revenue / students if students > 0 else 0
            st.metric("Revenue per Student", f"${revenue_per_student:,.2f}")

        with col3:
            student_staff_ratio = students / total_personnel if total_personnel > 0 else 0
            st.metric("Student:Staff Ratio", f"{student_staff_ratio:.1f}:1")

        with col4:
            st.metric("Total Personnel", f"{total_personnel:,}")

    with tab2:
        st.markdown("<h2 style='color: #e0e0e0;'>👥 Comprehensive Staffing Analysis</h2>", unsafe_allow_html=True)

        # STAFFING OVERVIEW
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Workforce", f"{total_personnel:,}",
                      delta=f"{(total_personnel / students * 100):.1f}% of students")
        with col2:
            st.metric("Faculty Members", f"{full_time_faculty + adjunct_faculty:,}",
                      delta=f"{full_time_faculty} FT + {adjunct_faculty} Adj")
        with col3:
            st.metric("Support Staff", f"{staff_members + ambassadors + graders + tutors:,}",
                      delta="Non-faculty personnel")

        st.markdown("---")

        # DETAILED STAFFING BREAKDOWN
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h4 style='color: #FF8200;'>📊 Staffing Requirements by Role</h4>", unsafe_allow_html=True)

            staffing_df = pd.DataFrame({
                'Position': ['Full-Time Faculty', 'Adjunct Faculty', 'Staff Members',
                             'Student Ambassadors', 'Graders', 'Tutors'],
                'Count': [full_time_faculty, adjunct_faculty, staff_members,
                          ambassadors, graders, tutors],
                'Ratio': [f'1:{faculty_ratio}', f'1:{adjunct_ratio}', f'1:{staff_ratio}',
                          f'1:{ambassador_ratio}', f'1:{grader_ratio}', f'1:{tutor_ratio}'],
                '% of Total': [
                    f'{(full_time_faculty / total_personnel * 100):.1f}%' if total_personnel > 0 else '0%',
                    f'{(adjunct_faculty / total_personnel * 100):.1f}%' if total_personnel > 0 else '0%',
                    f'{(staff_members / total_personnel * 100):.1f}%' if total_personnel > 0 else '0%',
                    f'{(ambassadors / total_personnel * 100):.1f}%' if total_personnel > 0 else '0%',
                    f'{(graders / total_personnel * 100):.1f}%' if total_personnel > 0 else '0%',
                    f'{(tutors / total_personnel * 100):.1f}%' if total_personnel > 0 else '0%'
                ]
            })

            st.dataframe(staffing_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("<h4 style='color: #FF8200;'>💰 Compensation by Role</h4>", unsafe_allow_html=True)

            comp_df = pd.DataFrame({
                'Position': ['Full-Time Faculty', 'Adjunct Faculty', 'Staff Members',
                             'Student Ambassadors', 'Graders', 'Tutors'],
                'Total Annual Cost': [
                    f'${faculty_cost:,.0f}',
                    f'${adjunct_cost:,.0f}',
                    f'${staff_cost:,.0f}',
                    f'${ambassador_cost:,.0f}',
                    f'${grader_cost:,.0f}',
                    f'${tutor_cost:,.0f}'
                ],
                'Avg Salary': [
                    f'${faculty_salary:,.0f}',
                    f'${adjunct_salary:,.0f}',
                    f'${staff_salary:,.0f}',
                    f'${ambassador_pay:,.0f}',
                    f'${grader_pay:,.0f}',
                    f'${tutor_pay:,.0f}'
                ],
                '% of Personnel Budget': [
                    f'{(faculty_cost / total_personnel_cost * 100):.1f}%' if total_personnel_cost > 0 else '0%',
                    f'{(adjunct_cost / total_personnel_cost * 100):.1f}%' if total_personnel_cost > 0 else '0%',
                    f'{(staff_cost / total_personnel_cost * 100):.1f}%' if total_personnel_cost > 0 else '0%',
                    f'{(ambassador_cost / total_personnel_cost * 100):.1f}%' if total_personnel_cost > 0 else '0%',
                    f'{(grader_cost / total_personnel_cost * 100):.1f}%' if total_personnel_cost > 0 else '0%',
                    f'{(tutor_cost / total_personnel_cost * 100):.1f}%' if total_personnel_cost > 0 else '0%'
                ]
            })

            st.dataframe(comp_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # STAFFING VISUALIZATIONS - DARK BACKGROUNDS
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h4 style='color: #FF8200;'>📊 Headcount Distribution</h4>", unsafe_allow_html=True)

            fig_staffing = px.bar(
                staffing_df,
                x='Position',
                y='Count',
                color='Count',
                color_continuous_scale='Oranges',
                text='Count'
            )

            fig_staffing.update_traces(
                textposition='outside',
                textfont=dict(color='#e0e0e0', size=12)
            )
            fig_staffing.update_layout(
                height=400,
                showlegend=False,
                xaxis_title='',
                yaxis_title='Number of Personnel',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(44, 44, 44, 1)',
                font=dict(family='Inter', color='#e0e0e0')
            )

            st.plotly_chart(fig_staffing, use_container_width=True)

        with col2:
            st.markdown("<h4 style='color: #FF8200;'>💵 Cost Distribution</h4>", unsafe_allow_html=True)

            cost_df = pd.DataFrame({
                'Position': ['Full-Time Faculty', 'Adjunct Faculty', 'Staff Members',
                             'Student Ambassadors', 'Graders', 'Tutors'],
                'Total Cost': [faculty_cost, adjunct_cost, staff_cost,
                               ambassador_cost, grader_cost, tutor_cost]
            })

            fig_cost = px.bar(
                cost_df,
                x='Position',
                y='Total Cost',
                color='Total Cost',
                color_continuous_scale='Reds',
                text='Total Cost'
            )

            fig_cost.update_traces(
                texttemplate='$%{text:,.0f}',
                textposition='outside',
                textfont=dict(color='#e0e0e0', size=12)
            )

            fig_cost.update_layout(
                height=400,
                showlegend=False,
                xaxis_title='',
                yaxis_title='Total Annual Cost',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(44, 44, 44, 1)',
                font=dict(family='Inter', color='#e0e0e0')
            )

            st.plotly_chart(fig_cost, use_container_width=True)

        st.markdown("---")

        # WORKFORCE COMPOSITION
        st.markdown("<h4 style='color: #FF8200;'>🎯 Workforce Composition Analysis</h4>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            faculty_pct = ((full_time_faculty + adjunct_faculty) / total_personnel * 100) if total_personnel > 0 else 0
            st.metric("Faculty Composition", f"{faculty_pct:.1f}%",
                      delta=f"{full_time_faculty + adjunct_faculty} total")

        with col2:
            ft_ratio = (full_time_faculty / (full_time_faculty + adjunct_faculty) * 100) if (
                                                                                                        full_time_faculty + adjunct_faculty) > 0 else 0
            st.metric("Full-Time Ratio", f"{ft_ratio:.1f}%", delta="Of all faculty")

        with col3:
            support_pct = ((
                                       staff_members + ambassadors + graders + tutors) / total_personnel * 100) if total_personnel > 0 else 0
            st.metric("Support Staff %", f"{support_pct:.1f}%",
                      delta=f"{staff_members + ambassadors + graders + tutors} total")

        with col4:
            avg_compensation = total_personnel_cost / total_personnel if total_personnel > 0 else 0
            st.metric("Avg Compensation", f"${avg_compensation:,.0f}", delta="Per person")

    with tab3:
        st.markdown("<h2 style='color: #e0e0e0;'>💰 Detailed Financial Analysis</h2>", unsafe_allow_html=True)

        # REVENUE BREAKDOWN
        st.markdown("<h4 style='color: #FF8200;'>📈 Revenue Sources</h4>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Tuition Revenue", f"${students * tuition_per_student:,.0f}",
                      delta=f"{students:,} students")
        with col2:
            st.metric("Other Revenue", f"${other_revenue:,.0f}",
                      delta=f"{(other_revenue / total_revenue * 100):.1f}% of total" if total_revenue > 0 else "0%")
        with col3:
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        with col4:
            rev_per_student = total_revenue / students if students > 0 else 0
            st.metric("Revenue/Student", f"${rev_per_student:,.0f}")

        st.markdown("---")

        # EXPENSE BREAKDOWN
        st.markdown("<h4 style='color: #FF8200;'>💸 Expense Categories</h4>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Personnel Costs**")
            st.metric("Full-Time Faculty", f"${faculty_cost:,.0f}",
                      delta=f"{full_time_faculty} positions")
            st.metric("Adjunct Faculty", f"${adjunct_cost:,.0f}",
                      delta=f"{adjunct_faculty} positions")
            st.metric("Staff Members", f"${staff_cost:,.0f}",
                      delta=f"{staff_members} positions")
            st.metric("Student Workers", f"${ambassador_cost + grader_cost + tutor_cost:,.0f}",
                      delta=f"{ambassadors + graders + tutors} positions")

        with col2:
            st.markdown("**Operational Analysis**")
            st.metric("Operating Supplies", f"${operating_cost:,.0f}",
                      delta=f"${operating_per_student:,} per student")
            st.metric("Total Personnel Cost", f"${total_personnel_cost:,.0f}",
                      delta=f"{(total_personnel_cost / total_cost * 100):.1f}% of budget")
            st.metric("Total Expenses", f"${total_cost:,.0f}")

            contingency_amount = total_cost * (contingency_fund / 100)
            st.metric("Contingency Reserve", f"${contingency_amount:,.0f}",
                      delta=f"{contingency_fund}% of expenses")

        st.markdown("---")

        # FINANCIAL RATIOS
        st.markdown("<h4 style='color: #FF8200;'>📊 Key Financial Ratios</h4>", unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            expense_ratio = (total_cost / total_revenue * 100) if total_revenue > 0 else 0
            st.metric("Expense Ratio", f"{expense_ratio:.1f}%", delta="Of revenue")

        with col2:
            personnel_ratio = (total_personnel_cost / total_cost * 100) if total_cost > 0 else 0
            st.metric("Personnel %", f"{personnel_ratio:.1f}%", delta="Of expenses")

        with col3:
            operating_ratio = (operating_cost / total_cost * 100) if total_cost > 0 else 0
            st.metric("Operating %", f"{operating_ratio:.1f}%", delta="Of expenses")

        with col4:
            cost_per_student = total_cost / students if students > 0 else 0
            st.metric("Cost/Student", f"${cost_per_student:,.0f}")

        with col5:
            margin = (net_result / total_revenue * 100) if total_revenue > 0 else 0
            st.metric("Margin", f"{margin:.2f}%")

        st.markdown("---")

        # DETAILED FINANCIAL STATEMENT
        if show_detailed_breakdown:
            st.markdown("<h4 style='color: #FF8200;'>📋 Complete Financial Statement</h4>", unsafe_allow_html=True)

            financial_data = {
                'Line Item': [
                    '═══ REVENUE ═══',
                    'Tuition Revenue',
                    'Other Revenue Sources',
                    'Total Revenue',
                    '',
                    '═══ EXPENSES ═══',
                    '--- Personnel ---',
                    'Full-Time Faculty Salaries',
                    'Adjunct Faculty Salaries',
                    'Staff Salaries',
                    'Student Ambassador Pay',
                    'Grader Compensation',
                    'Tutor Compensation',
                    'Total Personnel Cost',
                    '',
                    '--- Operations ---',
                    'Operating Supplies',
                    'Total Operating Cost',
                    '',
                    'TOTAL EXPENSES',
                    '',
                    '═══ SUMMARY ═══',
                    'Net Position',
                    'Contingency Fund',
                    'Effective Net Position'
                ],
                'Amount': [
                    '',
                    f'${students * tuition_per_student:,.0f}',
                    f'${other_revenue:,.0f}',
                    f'${total_revenue:,.0f}',
                    '',
                    '',
                    '',
                    f'${faculty_cost:,.0f}',
                    f'${adjunct_cost:,.0f}',
                    f'${staff_cost:,.0f}',
                    f'${ambassador_cost:,.0f}',
                    f'${grader_cost:,.0f}',
                    f'${tutor_cost:,.0f}',
                    f'${total_personnel_cost:,.0f}',
                    '',
                    '',
                    f'${operating_cost:,.0f}',
                    f'${operating_cost:,.0f}',
                    '',
                    f'${total_cost:,.0f}',
                    '',
                    '',
                    f'${net_result:,.0f}',
                    f'${contingency_amount:,.0f}',
                    f'${net_result - contingency_amount:,.0f}'
                ],
                'Details': [
                    '',
                    f'{students:,} students × ${tuition_per_student:,}/student',
                    'Grants, donations, auxiliary services',
                    f'{(total_revenue):,.0f}',
                    '',
                    '',
                    '',
                    f'{full_time_faculty} positions × ${faculty_salary:,}/year',
                    f'{adjunct_faculty} positions × ${adjunct_salary:,}/year',
                    f'{staff_members} positions × ${staff_salary:,}/year',
                    f'{ambassadors} positions × ${ambassador_pay:,}/year',
                    f'{graders} positions × ${grader_pay:,}/year',
                    f'{tutors} positions × ${tutor_pay:,}/year',
                    f'{total_personnel} total positions',
                    '',
                    '',
                    f'{students:,} students × ${operating_per_student}/student',
                    'Books, supplies, technology',
                    '',
                    f'{(total_cost / total_revenue * 100):.1f}% of revenue',
                    '',
                    '',
                    'Surplus' if net_result >= 0 else 'Deficit',
                    f'{contingency_fund}% reserve',
                    'After contingency'
                ]
            }

            fin_df = pd.DataFrame(financial_data)
            st.dataframe(fin_df, use_container_width=True, hide_index=True, height=800)

    with tab4:
        st.markdown("<h2 style='color: #e0e0e0;'>📈 Advanced Analytics & Projections</h2>", unsafe_allow_html=True)

        # ENROLLMENT SCENARIOS
        st.markdown("<h4 style='color: #FF8200;'>🔄 Enrollment Impact Analysis</h4>", unsafe_allow_html=True)

        scenarios = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]
        scenario_labels = ['-30%', '-20%', '-10%', 'Current', '+10%', '+20%', '+30%']
        scenario_students = [int(students * s) for s in scenarios]
        scenario_revenues = [s * tuition_per_student + other_revenue for s in scenario_students]

        scenario_costs = []
        scenario_personnel = []
        for s_students in scenario_students:
            s_faculty = max(1, int(s_students / faculty_ratio)) * faculty_salary
            s_adjunct = max(1, int(s_students / adjunct_ratio)) * adjunct_salary
            s_staff = max(1, int(s_students / staff_ratio)) * staff_salary
            s_support = (int(s_students / ambassador_ratio) * ambassador_pay +
                         int(s_students / grader_ratio) * grader_pay +
                         int(s_students / tutor_ratio) * tutor_pay)
            s_ops = s_students * operating_per_student
            scenario_costs.append(s_faculty + s_adjunct + s_staff + s_support + s_ops)

            s_personnel = (max(1, int(s_students / faculty_ratio)) +
                           max(1, int(s_students / adjunct_ratio)) +
                           max(1, int(s_students / staff_ratio)) +
                           int(s_students / ambassador_ratio) +
                           int(s_students / grader_ratio) +
                           int(s_students / tutor_ratio))
            scenario_personnel.append(s_personnel)

        scenario_net = [r - c for r, c in zip(scenario_revenues, scenario_costs)]

        # SCENARIO CHART - DARK BACKGROUND
        fig_scenarios = go.Figure()

        fig_scenarios.add_trace(go.Scatter(
            x=scenario_labels,
            y=scenario_revenues,
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#28a745', width=3),
            marker=dict(size=10),
            text=[f'${r:,.0f}' for r in scenario_revenues],
            textposition='top center',
            textfont=dict(color='#e0e0e0')
        ))

        fig_scenarios.add_trace(go.Scatter(
            x=scenario_labels,
            y=scenario_costs,
            mode='lines+markers',
            name='Expenses',
            line=dict(color='#dc3545', width=3),
            marker=dict(size=10),
            text=[f'${c:,.0f}' for c in scenario_costs],
            textposition='bottom center',
            textfont=dict(color='#e0e0e0')
        ))

        fig_scenarios.add_trace(go.Scatter(
            x=scenario_labels,
            y=scenario_net,
            mode='lines+markers',
            name='Net Position',
            line=dict(color='#FF8200', width=3, dash='dash'),
            marker=dict(size=10),
            text=[f'${n:,.0f}' for n in scenario_net],
            textposition='middle right',
            textfont=dict(color='#e0e0e0')
        ))

        fig_scenarios.update_layout(
            title='Financial Impact of Enrollment Changes',
            xaxis_title='Enrollment Scenario',
            yaxis_title='Amount ($)',
            height=500,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(44, 44, 44, 1)',
            font=dict(family='Inter', color='#e0e0e0'),
            legend=dict(font=dict(color='#e0e0e0'))
        )

        st.plotly_chart(fig_scenarios, use_container_width=True)

        # SCENARIO COMPARISON TABLE
        st.markdown("<h4 style='color: #FF8200;'>📊 Scenario Comparison Matrix</h4>", unsafe_allow_html=True)

        scenario_df = pd.DataFrame({
            'Scenario': scenario_labels,
            'Students': [f'{s:,}' for s in scenario_students],
            'Personnel': scenario_personnel,
            'Revenue': [f'${r:,.0f}' for r in scenario_revenues],
            'Expenses': [f'${c:,.0f}' for c in scenario_costs],
            'Net Position': [f'${n:,.0f}' for n in scenario_net],
            'Margin %': [f'{(n / r * 100):.2f}%' if r > 0 else '0%' for n, r in zip(scenario_net, scenario_revenues)]
        })

        st.dataframe(scenario_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # BREAK-EVEN ANALYSIS
        st.markdown("<h4 style='color: #FF8200;'>⚖️ Break-Even Analysis</h4>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            fixed_costs = total_personnel_cost
            variable_cost_per_student = operating_per_student
            contribution_per_student = tuition_per_student - variable_cost_per_student

            if contribution_per_student > 0:
                breakeven_students = int(fixed_costs / contribution_per_student)
                st.metric("Break-Even Enrollment", f"{breakeven_students:,} students")
                st.metric("Current vs Break-Even", f"{((students / breakeven_students - 1) * 100):.1f}%",
                          delta="Above BE" if students > breakeven_students else "Below BE")
            else:
                st.warning("⚠️ Negative contribution margin")

        with col2:
            if contribution_per_student > 0:
                margin_of_safety = students - breakeven_students
                margin_of_safety_pct = (margin_of_safety / students * 100) if students > 0 else 0

                st.metric("Margin of Safety", f"{margin_of_safety:,} students")
                st.metric("Safety %", f"{margin_of_safety_pct:.1f}%")
                st.metric("Contribution Margin", f"${contribution_per_student:,.0f}",
                          delta="Per student")

        with col3:
            if contribution_per_student > 0:
                target_profit = 1000000
                target_students = int((fixed_costs + target_profit) / contribution_per_student)
                st.metric("For $1M Surplus", f"{target_students:,} students",
                          delta=f"{target_students - students:,} more needed")

                revenue_needed = target_students * tuition_per_student
                st.metric("Revenue Needed", f"${revenue_needed:,.0f}")

        st.markdown("---")

        # SENSITIVITY ANALYSIS
        st.markdown("<h4 style='color: #FF8200;'>🎯 Sensitivity Analysis</h4>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Tuition Impact**")
            tuition_variations = [0.9, 0.95, 1.0, 1.05, 1.1]
            tuition_labels = ['-10%', '-5%', 'Current', '+5%', '+10%']
            tuition_net = [(students * tuition_per_student * t + other_revenue) - total_cost for t in
                           tuition_variations]

            fig_tuition = go.Figure(data=[
                go.Bar(
                    x=tuition_labels,
                    y=tuition_net,
                    marker_color=['#dc3545' if n < 0 else '#28a745' for n in tuition_net],
                    text=[f'${n:,.0f}' for n in tuition_net],
                    textposition='outside',
                    textfont=dict(color='#e0e0e0')
                )
            ])

            fig_tuition.update_layout(
                title='Impact of Tuition Changes on Net Position',
                xaxis_title='Tuition Adjustment',
                yaxis_title='Net Position ($)',
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(44, 44, 44, 1)',
                font=dict(family='Inter', color='#e0e0e0')
            )

            st.plotly_chart(fig_tuition, use_container_width=True)

        with col2:
            st.markdown("**Cost Reduction Impact**")
            cost_reductions = [0, 5, 10, 15, 20]
            cost_labels = ['0%', '5%', '10%', '15%', '20%']
            cost_net = [total_revenue - (total_cost * (1 - r / 100)) for r in cost_reductions]

            fig_cost_reduction = go.Figure(data=[
                go.Bar(
                    x=cost_labels,
                    y=cost_net,
                    marker_color='#FF8200',
                    text=[f'${n:,.0f}' for n in cost_net],
                    textposition='outside',
                    textfont=dict(color='#e0e0e0')
                )
            ])

            fig_cost_reduction.update_layout(
                title='Impact of Cost Reduction on Net Position',
                xaxis_title='Cost Reduction',
                yaxis_title='Net Position ($)',
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(44, 44, 44, 1)',
                font=dict(family='Inter', color='#e0e0e0')
            )

            st.plotly_chart(fig_cost_reduction, use_container_width=True)

        st.markdown("---")

        # MULTI-YEAR PROJECTIONS
        st.markdown("<h4 style='color: #FF8200;'>📅 5-Year Financial Projections</h4>", unsafe_allow_html=True)

        years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
        growth_rate = 0.03  # 3% annual growth

        projected_students = [int(students * ((1 + growth_rate) ** i)) for i in range(5)]
        projected_revenues = [s * tuition_per_student * ((1 + inflation_rate / 100) ** i) + other_revenue for i, s in
                              enumerate(projected_students)]
        projected_costs = []

        for i, s_students in enumerate(projected_students):
            inflation_factor = (1 + inflation_rate / 100) ** i
            s_faculty = max(1, int(s_students / faculty_ratio)) * faculty_salary * inflation_factor
            s_adjunct = max(1, int(s_students / adjunct_ratio)) * adjunct_salary * inflation_factor
            s_staff = max(1, int(s_students / staff_ratio)) * staff_salary * inflation_factor
            s_support = ((int(s_students / ambassador_ratio) * ambassador_pay +
                          int(s_students / grader_ratio) * grader_pay +
                          int(s_students / tutor_ratio) * tutor_pay) * inflation_factor)
            s_ops = s_students * operating_per_student * inflation_factor
            projected_costs.append(s_faculty + s_adjunct + s_staff + s_support + s_ops)

        projected_net = [r - c for r, c in zip(projected_revenues, projected_costs)]

        fig_projection = go.Figure()

        fig_projection.add_trace(go.Scatter(
            x=years,
            y=projected_revenues,
            mode='lines+markers',
            name='Projected Revenue',
            line=dict(color='#28a745', width=3),
            marker=dict(size=12),
            fill='tonexty'
        ))

        fig_projection.add_trace(go.Scatter(
            x=years,
            y=projected_costs,
            mode='lines+markers',
            name='Projected Expenses',
            line=dict(color='#dc3545', width=3),
            marker=dict(size=12),
            fill='tozeroy'
        ))

        fig_projection.update_layout(
            title=f'5-Year Financial Forecast ({growth_rate * 100:.0f}% Growth, {inflation_rate:.1f}% Inflation)',
            xaxis_title='Year',
            yaxis_title='Amount ($)',
            height=450,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(44, 44, 44, 1)',
            font=dict(family='Inter', color='#e0e0e0'),
            legend=dict(font=dict(color='#e0e0e0'))
        )

        st.plotly_chart(fig_projection, use_container_width=True)

        # 5-YEAR SUMMARY TABLE
        projection_df = pd.DataFrame({
            'Year': years,
            'Students': [f'{s:,}' for s in projected_students],
            'Revenue': [f'${r:,.0f}' for r in projected_revenues],
            'Expenses': [f'${c:,.0f}' for c in projected_costs],
            'Net Position': [f'${n:,.0f}' for n in projected_net],
            'Margin %': [f'{(n / r * 100):.2f}%' if r > 0 else '0%' for n, r in zip(projected_net, projected_revenues)]
        })

        st.dataframe(projection_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # RISK ANALYSIS
        st.markdown("<h4 style='color: #FF8200;'>⚠️ Risk Assessment Dashboard</h4>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            enrollment_risk = "LOW" if students > breakeven_students * 1.2 else (
                "MEDIUM" if students > breakeven_students else "HIGH")
            risk_color = "#28a745" if enrollment_risk == "LOW" else (
                "#ffc107" if enrollment_risk == "MEDIUM" else "#dc3545")
            st.markdown(f"<h4 style='color: {risk_color};'>Enrollment Risk: {enrollment_risk}</h4>",
                        unsafe_allow_html=True)
            st.metric("Buffer",
                      f"{((students / breakeven_students - 1) * 100):.1f}%" if contribution_per_student > 0 else "N/A")

        with col2:
            margin_risk = "LOW" if margin > 15 else ("MEDIUM" if margin > 5 else "HIGH")
            risk_color = "#28a745" if margin_risk == "LOW" else ("#ffc107" if margin_risk == "MEDIUM" else "#dc3545")
            st.markdown(f"<h4 style='color: {risk_color};'>Margin Risk: {margin_risk}</h4>", unsafe_allow_html=True)
            st.metric("Current Margin", f"{margin:.2f}%")

        with col3:
            dependency_risk = "HIGH" if (tuition_per_student * students / total_revenue) > 0.9 else (
                "MEDIUM" if (tuition_per_student * students / total_revenue) > 0.7 else "LOW")
            risk_color = "#dc3545" if dependency_risk == "HIGH" else (
                "#ffc107" if dependency_risk == "MEDIUM" else "#28a745")
            st.markdown(f"<h4 style='color: {risk_color};'>Revenue Dependency: {dependency_risk}</h4>",
                        unsafe_allow_html=True)
            st.metric("Tuition %", f"{(tuition_per_student * students / total_revenue * 100):.1f}%")

        with col4:
            personnel_risk = "HIGH" if personnel_ratio > 80 else ("MEDIUM" if personnel_ratio > 70 else "LOW")
            risk_color = "#dc3545" if personnel_risk == "HIGH" else (
                "#ffc107" if personnel_risk == "MEDIUM" else "#28a745")
            st.markdown(f"<h4 style='color: {risk_color};'>Personnel Cost Risk: {personnel_risk}</h4>",
                        unsafe_allow_html=True)
            st.metric("Personnel %", f"{personnel_ratio:.1f}%")

        st.markdown("---")

        # EXPORT OPTIONS
        st.markdown("<h4 style='color: #FF8200;'>📥 Export & Reporting</h4>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📊 Export to Excel", use_container_width=True):
                st.info("📊 Excel export - Coming soon!")

        with col2:
            if st.button("📄 Generate PDF", use_container_width=True):
                st.info("📄 PDF export - Coming soon!")

        with col3:
            if st.button("📧 Email Report", use_container_width=True):
                st.info("📧 Email feature - Coming soon!")

        with col4:
            if st.button("💾 Save Analysis", use_container_width=True):
                st.success("✅ Analysis saved to scenarios!")

    # FOOTER
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #b0b0b0; padding: 2rem 0;'>
            <p style='font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; color: #FF8200;'>
                🍊 University of Tennessee, Knoxville
            </p>
            <p style='font-size: 0.875rem; margin-bottom: 0.5rem; color: #b0b0b0;'>
                College of Emerging & Collaborative Studies | Financial Analytics Platform
            </p>
            <p style='font-size: 0.75rem; color: #808080;'>
                v2.4.0 COMPLETE NUCLEAR EDITION | © 2025
            </p>
        </div>
    """, unsafe_allow_html=True)


# APPLICATION ENTRY POINT
if not st.session_state.logged_in:
    login_page()
else:
    main_dashboard()