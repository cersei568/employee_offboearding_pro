import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Employee Offboarding Pro",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Green & Gold Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F0FDF4 0%, #FFFBEB 100%);
    }
    
    /* Headers */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10B981 0%, #D97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .subheader {
        text-align: center;
        color: #6B7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    h2, h3 {
        color: #065F46 !important;
        font-weight: 700 !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1);
        border: 2px solid #D1FAE5;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #10B981 0%, #D97706 100%);
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 30px rgba(16, 185, 129, 0.2);
        transform: translateY(-4px);
        border-color: #10B981;
    }
    
    /* Status Badges */
    .status-complete {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .status-pending {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
    }
    
    .status-overdue {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }
    
    .status-active {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
    }
    
    /* Checklist Items */
    .checklist-item {
        background: white;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 12px;
        border-left: 4px solid #10B981;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    
    .checklist-item:hover {
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.15);
        transform: translateX(4px);
    }
    
    .checklist-item-completed {
        background: #F0FDF4;
        border-left-color: #34D399;
        opacity: 0.7;
    }
    
    .checklist-item-overdue {
        background: #FEF2F2;
        border-left-color: #EF4444;
    }
    
    /* Cards */
    .info-card {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-radius: 16px;
        padding: 1.8rem;
        border-left: 5px solid #10B981;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
        margin: 1rem 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-radius: 16px;
        padding: 1.8rem;
        border-left: 5px solid #F59E0B;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.1);
        margin: 1rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-radius: 16px;
        padding: 1.8rem;
        border-left: 5px solid #10B981;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
        margin: 1rem 0;
    }
    
    .employee-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 2px solid #D1FAE5;
        margin: 1.5rem 0;
        transition: all 0.3s;
    }
    
    .employee-card:hover {
        box-shadow: 0 8px 30px rgba(16, 185, 129, 0.15);
        border-color: #10B981;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 6px 24px rgba(16, 185, 129, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Secondary button style */
    .stButton button[kind="secondary"] {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3) !important;
    }
    
    .stButton button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #D97706 0%, #B45309 100%) !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #065F46 0%, #78350F 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #F0FDF4 !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255, 255, 255, 0.1);
        padding: 12px 16px;
        border-radius: 8px;
        margin: 4px 0;
        transition: all 0.2s;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(4px);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #10B981 0%, #D97706 100%);
        border-radius: 10px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10B981 0%, #D97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stMetricLabel"] {
        color: #065F46 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 2px solid #D1FAE5;
    }
    
    /* Forms */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, 
    .stNumberInput input, .stDateInput input, .stTimeInput input {
        border: 2px solid #D1FAE5 !important;
        border-radius: 10px !important;
        padding: 14px !important;
        font-size: 15px !important;
        transition: all 0.2s !important;
        background: white !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: white;
        padding: 12px;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #6B7280;
        font-weight: 700;
        padding: 14px 28px;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 13px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #F0FDF4;
        color: #10B981;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 12px !important;
        border-left: 4px solid #10B981 !important;
        font-weight: 700 !important;
        padding: 18px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
        transition: all 0.2s !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F0FDF4 !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.15) !important;
    }
    
    /* Priority Indicators */
    .priority-critical {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 8px 18px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }
    
    .priority-high {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 8px 18px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
    }
    
    .priority-normal {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 8px 18px;
        border-radius: 24px;
        font-weight: 700;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    /* Category Tags */
    .category-tag {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        color: #065F46;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        border: 1px solid #A7F3D0;
        display: inline-block;
        margin: 4px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F3F4F6;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #10B981 0%, #D97706 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #059669 0%, #B45309 100%);
    }
    
    /* Divider */
    hr {
        border-color: #D1FAE5 !important;
        opacity: 0.5;
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 4px solid #10B981;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-left: 4px solid #10B981;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 4px solid #F59E0B;
    }
    
    .stError {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border-left: 4px solid #EF4444;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Role-based exit checklists
ROLE_CHECKLISTS = {
    "Software Engineer": [
        {"task": "Return laptop and accessories", "category": "Asset Return", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke GitHub/GitLab access", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke AWS/Cloud access", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer code ownership and repositories", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Manager", "priority": "High"},
        {"task": "Document ongoing projects and architecture", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "High"},
        {"task": "Return security badge and building access", "category": "Asset Return", "days_before": 0, "responsible": "Security", "priority": "Critical"},
        {"task": "Revoke Slack/Teams access", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke VPN access", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Conduct knowledge transfer session", "category": "Knowledge Transfer", "days_before": 3, "responsible": "Manager", "priority": "High"},
        {"task": "Archive code documentation", "category": "Administrative", "days_before": 2, "responsible": "Employee", "priority": "Normal"},
        {"task": "Transfer development environment configs", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "Normal"},
    ],
    "Sales Representative": [
        {"task": "Return company phone and accessories", "category": "Asset Return", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Return laptop and equipment", "category": "Asset Return", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke CRM access (Salesforce/HubSpot)", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer all client accounts and contacts", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Manager", "priority": "Critical"},
        {"task": "Return company credit card", "category": "Asset Return", "days_before": 0, "responsible": "Finance", "priority": "Critical"},
        {"task": "Submit final expense report", "category": "Administrative", "days_before": 2, "responsible": "Employee", "priority": "High"},
        {"task": "Conduct client handover meetings", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "High"},
        {"task": "Revoke email access", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer pending deals and pipeline", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Manager", "priority": "Critical"},
        {"task": "Document sales processes and best practices", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "Normal"},
    ],
    "HR Manager": [
        {"task": "Return laptop and company phone", "category": "Asset Return", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer all employee files and records", "category": "Knowledge Transfer", "days_before": 7, "responsible": "HR", "priority": "Critical"},
        {"task": "Revoke HRIS access (Workday/BambooHR)", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke payroll system access", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Document ongoing HR cases and investigations", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "High"},
        {"task": "Return office keys and access cards", "category": "Asset Return", "days_before": 0, "responsible": "Security", "priority": "Critical"},
        {"task": "Transfer active recruitment pipeline", "category": "Knowledge Transfer", "days_before": 7, "responsible": "HR", "priority": "High"},
        {"task": "Conduct comprehensive knowledge transfer", "category": "Knowledge Transfer", "days_before": 3, "responsible": "Manager", "priority": "High"},
        {"task": "Transfer vendor and consultant relationships", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "Normal"},
        {"task": "Archive sensitive HR documents", "category": "Administrative", "days_before": 2, "responsible": "Employee", "priority": "High"},
    ],
    "Finance Manager": [
        {"task": "Return laptop and equipment", "category": "Asset Return", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke accounting software access (QuickBooks/SAP)", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke banking system access", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer pending approvals and workflows", "category": "Knowledge Transfer", "days_before": 3, "responsible": "Manager", "priority": "Critical"},
        {"task": "Document all financial processes", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Employee", "priority": "High"},
        {"task": "Return company credit card", "category": "Asset Return", "days_before": 0, "responsible": "Finance", "priority": "Critical"},
        {"task": "Handover vendor relationships and contracts", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "High"},
        {"task": "Archive financial documents properly", "category": "Administrative", "days_before": 2, "responsible": "Employee", "priority": "High"},
        {"task": "Transfer budgeting and forecasting models", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Employee", "priority": "High"},
        {"task": "Complete final financial reconciliations", "category": "Administrative", "days_before": 3, "responsible": "Employee", "priority": "High"},
    ],
    "Marketing Specialist": [
        {"task": "Return laptop and camera equipment", "category": "Asset Return", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke social media account access", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Revoke marketing automation tools", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer campaign ownership and schedules", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Manager", "priority": "High"},
        {"task": "Document brand guidelines and standards", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "Normal"},
        {"task": "Transfer content calendar and workflows", "category": "Knowledge Transfer", "days_before": 3, "responsible": "Employee", "priority": "High"},
        {"task": "Revoke design tool access (Adobe/Canva)", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer creative asset libraries", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "Normal"},
        {"task": "Document marketing processes and workflows", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "Normal"},
    ],
    "Product Manager": [
        {"task": "Return laptop and equipment", "category": "Asset Return", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer product roadmap and backlog", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Manager", "priority": "Critical"},
        {"task": "Document product strategy and vision", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Employee", "priority": "High"},
        {"task": "Transfer stakeholder relationships", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "High"},
        {"task": "Handover customer research and insights", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Employee", "priority": "Normal"},
        {"task": "Revoke product management tools", "category": "Access Revocation", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer analytics and metrics dashboards", "category": "Knowledge Transfer", "days_before": 3, "responsible": "Employee", "priority": "Normal"},
    ],
    "Operations Manager": [
        {"task": "Return laptop and equipment", "category": "Asset Return", "days_before": 0, "responsible": "IT", "priority": "Critical"},
        {"task": "Transfer operational processes and SOPs", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Manager", "priority": "Critical"},
        {"task": "Document vendor and supplier relationships", "category": "Knowledge Transfer", "days_before": 7, "responsible": "Employee", "priority": "High"},
        {"task": "Transfer project management tools access", "category": "Knowledge Transfer", "days_before": 3, "responsible": "IT", "priority": "High"},
        {"task": "Handover team management responsibilities", "category": "Knowledge Transfer", "days_before": 5, "responsible": "Manager", "priority": "Critical"},
        {"task": "Archive operational reports and metrics", "category": "Administrative", "days_before": 2, "responsible": "Employee", "priority": "Normal"},
    ],
}

# Enhanced systems list
SYSTEMS = {
    "Core Systems": ["Email (Office 365/Gmail)", "Slack/Teams", "VPN", "Building Access"],
    "Development": ["GitHub/GitLab", "AWS/Azure/GCP", "Jenkins/CI-CD", "Docker/Kubernetes"],
    "Business Applications": ["CRM (Salesforce)", "HRIS", "Payroll System", "ERP"],
    "Productivity Tools": ["Project Management (Jira/Asana)", "Document Management", "Google Workspace/Office 365"],
    "Communication": ["Phone System", "Video Conferencing", "Internal Chat"],
    "Finance": ["Accounting Software", "Banking Systems", "Expense Management"],
    "Marketing": ["Social Media Accounts", "Marketing Automation", "Design Tools", "Analytics Platforms"]
}

# Initialize session state with sample data
if 'offboarding_cases' not in st.session_state:
    st.session_state.offboarding_cases = [
        {
            'id': 1,
            'employee_name': 'John Smith',
            'employee_id': 'EMP001',
            'role': 'Software Engineer',
            'department': 'Engineering',
            'last_day': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
            'reason': 'Resignation',
            'manager_name': 'Sarah Johnson',
            'email': 'john.smith@company.com',
            'assets': ['Laptop', 'Phone', 'Security Badge'],
            'systems': ['Email (Office 365/Gmail)', 'GitHub/GitLab', 'Slack/Teams'],
            'checklist': [],
            'status': 'Active',
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completion_percentage': 35,
            'access_status': {}
        }
    ]

if 'exit_interviews' not in st.session_state:
    st.session_state.exit_interviews = []

if 'skill_assessments' not in st.session_state:
    st.session_state.skill_assessments = []

# Helper functions
def calculate_days_remaining(last_day):
    """Calculate days until last working day"""
    last_date = datetime.strptime(last_day, '%Y-%m-%d').date()
    today = datetime.now().date()
    return (last_date - today).days

def get_task_priority_class(task):
    """Get CSS class for task priority"""
    priority_map = {
        'Critical': 'priority-critical',
        'High': 'priority-high',
        'Normal': 'priority-normal'
    }
    return priority_map.get(task.get('priority', 'Normal'), 'priority-normal')

def generate_completion_report(case):
    """Generate detailed completion report"""
    total_tasks = len(case['checklist'])
    completed_tasks = sum(1 for t in case['checklist'] if t['status'] == 'Completed')
    overdue_tasks = sum(1 for t in case['checklist'] if t['status'] == 'Pending' and 
                       datetime.strptime(t['due_date'], '%Y-%m-%d').date() < datetime.now().date())
    
    return {
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': total_tasks - completed_tasks,
        'overdue': overdue_tasks
    }

# Header
st.markdown("<h1 class='main-header'>Employee Offboarding Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Streamlined Employee Transition Management System</p>", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    page = st.radio("", [
        "📊 Dashboard",
        "➕ New Offboarding",
        "📋 Active Cases",
        "💼 Asset Tracking",
        "🔒 Access Management",
        "💬 Exit Interviews",
        "💰 Final Compensation",
        "📈 Analytics & Insights",
        "⚙️ Settings"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 📌 Quick Stats")
    total_cases = len(st.session_state.offboarding_cases)
    active_cases = len([c for c in st.session_state.offboarding_cases if c['status'] == 'Active'])
    st.metric("Total Cases", total_cases)
    st.metric("Active", active_cases)
    
    st.markdown("---")
    st.markdown("### 🔔 Alerts")
    urgent_tasks = 0
    for case in st.session_state.offboarding_cases:
        if case['status'] == 'Active':
            days = calculate_days_remaining(case['last_day'])
            if days <= 3:
                urgent_tasks += 1
    
    if urgent_tasks > 0:
        st.warning(f"⚠️ {urgent_tasks} case(s) require immediate attention")
    else:
        st.success("✅ All cases on track")

# ========== DASHBOARD ==========
if page == "📊 Dashboard":
    st.header("📊 Offboarding Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_cases = len(st.session_state.offboarding_cases)
    active_cases = len([c for c in st.session_state.offboarding_cases if c['status'] == 'Active'])
    completed_cases = len([c for c in st.session_state.offboarding_cases if c['status'] == 'Completed'])
    avg_completion = sum(c['completion_percentage'] for c in st.session_state.offboarding_cases) / total_cases if total_cases > 0 else 0
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Cases", total_cases, delta=None)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Active Cases", active_cases, delta=None)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Completed", completed_cases, delta=None)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Avg Completion", f"{avg_completion:.0f}%", delta=None)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.offboarding_cases:
        # Urgent cases alert
        urgent_cases = [c for c in st.session_state.offboarding_cases 
                       if c['status'] == 'Active' and calculate_days_remaining(c['last_day']) <= 3]
        
        if urgent_cases:
            st.markdown("### ⚠️ Urgent Attention Required")
            for case in urgent_cases:
                days = calculate_days_remaining(case['last_day'])
                st.markdown(f"""
                <div class='warning-card'>
                    <h4 style='margin:0 0 8px 0;'>{case['employee_name']} - {case['role']}</h4>
                    <p style='margin:0;'><strong>Last Day:</strong> {case['last_day']} ({days} days remaining)</p>
                    <p style='margin:0;'><strong>Completion:</strong> {case['completion_percentage']}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Recent cases overview
        st.markdown("### 📋 Recent Offboarding Cases")
        df = pd.DataFrame(st.session_state.offboarding_cases)
        
        display_df = df[['employee_name', 'role', 'department', 'last_day', 'status', 'completion_percentage']].copy()
        display_df.columns = ['Employee', 'Role', 'Department', 'Last Day', 'Status', 'Completion %']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            status_counts = df['status'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=0.5,
                marker=dict(colors=['#10B981', '#F59E0B', '#EF4444']),
                textinfo='label+percent'
            )])
            fig.update_layout(
                title="Cases by Status",
                height=350,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            role_counts = df['role'].value_counts().head(10)
            fig = go.Figure(data=[go.Bar(
                x=role_counts.values,
                y=role_counts.index,
                orientation='h',
                marker=dict(
                    color=role_counts.values,
                    colorscale=[[0, '#10B981'], [1, '#D97706']],
                    showscale=False
                )
            )])
            fig.update_layout(
                title="Cases by Role",
                height=350,
                xaxis_title="Count",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("""
        <div class='info-card'>
            <h3 style='margin:0 0 12px 0;'>👋 Welcome to Offboarding Pro</h3>
            <p style='margin:0;'>No offboarding cases yet. Click on <strong>"➕ New Offboarding"</strong> to create your first case.</p>
        </div>
        """, unsafe_allow_html=True)

# ========== NEW OFFBOARDING ==========
elif page == "➕ New Offboarding":
    st.header("➕ Create New Offboarding Case")
    
    st.markdown("""
    <div class='info-card'>
        <p style='margin:0;'><strong>Automated Workflow:</strong> This system will automatically generate a role-specific checklist, 
        schedule tasks, and notify relevant stakeholders.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("new_offboarding_form"):
        st.markdown("### 👤 Employee Information")
        col1, col2 = st.columns(2)
        
        with col1:
            employee_name = st.text_input("Employee Name*", placeholder="John Doe")
            employee_id = st.text_input("Employee ID*", placeholder="EMP12345")
            role = st.selectbox("Role*", [""] + list(ROLE_CHECKLISTS.keys()))
            department = st.text_input("Department*", placeholder="Engineering")
        
        with col2:
            last_day = st.date_input("Last Working Day*", min_value=datetime.now().date())
            reason = st.selectbox("Reason for Leaving", 
                                 ["Resignation", "Retirement", "Termination", "Contract End", "Mutual Agreement", "Other"])
            manager_name = st.text_input("Manager Name", placeholder="Jane Smith")
            email = st.text_input("Employee Email", placeholder="john.doe@company.com")
        
        st.markdown("---")
        st.markdown("### 💼 Assets & Access")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Assets to Return**")
            assets = st.multiselect("Select Assets", 
                                   ["Laptop", "Phone", "Security Badge", "Keys", "Credit Card", 
                                    "Headphones", "Monitor", "Keyboard", "Mouse", "Tablet", 
                                    "Other Equipment"])
        
        with col2:
            st.markdown("**System Access**")
            systems_list = []
            for category, sys_list in SYSTEMS.items():
                systems_list.extend(sys_list)
            systems = st.multiselect("Select Systems", systems_list)
        
        st.markdown("---")
        st.markdown("### 📝 Additional Information")
        
        col1, col2 = st.columns(2)
        with col1:
            knowledge_transfer_required = st.checkbox("Knowledge Transfer Required", value=True)
            exit_interview_required = st.checkbox("Exit Interview Required", value=True)
        with col2:
            replacement_hired = st.selectbox("Replacement Status", 
                                           ["Not Started", "In Progress", "Hired", "Not Applicable"])
        
        notes = st.text_area("Additional Notes", placeholder="Any special considerations or instructions...")
        
        st.markdown("---")
        submit = st.form_submit_button("🚀 Create Offboarding Case", type="primary", use_container_width=True)
        
        if submit:
            if employee_name and employee_id and role and department and role in ROLE_CHECKLISTS:
                # Generate checklist based on role
                checklist = []
                for item in ROLE_CHECKLISTS[role]:
                    due_date = last_day - timedelta(days=item['days_before'])
                    checklist.append({
                        'task': item['task'],
                        'category': item['category'],
                        'due_date': due_date.strftime('%Y-%m-%d'),
                        'status': 'Pending',
                        'completed_date': None,
                        'responsible': item.get('responsible', 'Manager'),
                        'priority': item.get('priority', 'Normal')
                    })
                
                # Create offboarding case
                case = {
                    'id': len(st.session_state.offboarding_cases) + 1,
                    'employee_name': employee_name,
                    'employee_id': employee_id,
                    'role': role,
                    'department': department,
                    'last_day': last_day.strftime('%Y-%m-%d'),
                    'reason': reason,
                    'manager_name': manager_name,
                    'email': email,
                    'assets': assets,
                    'systems': systems,
                    'checklist': checklist,
                    'status': 'Active',
                    'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'completion_percentage': 0,
                    'access_status': {system: 'Active' for system in systems},
                    'knowledge_transfer': knowledge_transfer_required,
                    'exit_interview': exit_interview_required,
                    'replacement_status': replacement_hired,
                    'notes': notes
                }
                
                st.session_state.offboarding_cases.append(case)
                
                st.markdown(f"""
                <div class='success-card'>
                    <h3 style='margin:0 0 12px 0;'>✅ Offboarding Case Created Successfully!</h3>
                    <p style='margin:0;'><strong>Case ID:</strong> #{case['id']}</p>
                    <p style='margin:0;'><strong>Employee:</strong> {employee_name}</p>
                    <p style='margin:0;'><strong>Tasks Generated:</strong> {len(checklist)}</p>
                    <p style='margin:8px 0 0 0;'>📧 Notifications sent to manager and stakeholders.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
            else:
                st.error("❌ Please fill in all required fields marked with *")

# ========== ACTIVE CASES ==========
elif page == "📋 Active Cases":
    st.header("📋 Active Offboarding Cases")
    
    active_cases = [c for c in st.session_state.offboarding_cases if c['status'] == 'Active']
    
    if active_cases:
        # Case selector
        case_options = [f"#{c['id']} - {c['employee_name']} ({c['role']})" for c in active_cases]
        selected_case_name = st.selectbox("Select Case to Manage", case_options)
        
        if selected_case_name:
            case_index = case_options.index(selected_case_name)
            case = active_cases[case_index]
            
            # Employee card
            days_remaining = calculate_days_remaining(case['last_day'])
            urgency_class = 'status-overdue' if days_remaining < 0 else 'status-pending' if days_remaining <= 3 else 'status-active'
            
            st.markdown(f"""
            <div class='employee-card'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <div style='flex: 1;'>
                        <h2 style='margin: 0 0 12px 0;'>{case['employee_name']}</h2>
                        <p style='margin: 0; color: #6B7280; font-size: 16px;'><strong>Role:</strong> {case['role']} | <strong>Department:</strong> {case['department']}</p>
                        <p style='margin: 8px 0 0 0; color: #6B7280;'><strong>Employee ID:</strong> {case['employee_id']} | <strong>Manager:</strong> {case.get('manager_name', 'N/A')}</p>
                        <p style='margin: 8px 0 0 0; color: #6B7280;'><strong>Reason:</strong> {case['reason']}</p>
                    </div>
                    <div style='text-align: right;'>
                        <div style='font-size: 48px; font-weight: 800; background: linear-gradient(135deg, #10B981 0%, #D97706 100%); 
                                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                            {case['completion_percentage']}%
                        </div>
                        <div style='color: #6B7280; font-weight: 600; margin-bottom: 12px;'>COMPLETION</div>
                        <span class='{urgency_class}'>{days_remaining} DAYS</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bars
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks", len(case['checklist']))
            with col2:
                completed = sum(1 for t in case['checklist'] if t['status'] == 'Completed')
                st.metric("Completed", completed)
            with col3:
                pending = len(case['checklist']) - completed
                st.metric("Pending", pending)
            
            st.progress(case['completion_percentage'] / 100)
            
            st.markdown("---")
            
            # Task Management
            st.markdown("### 📝 Exit Checklist")
            
            # Group tasks by category
            categories = {}
            for task in case['checklist']:
                cat = task['category']
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(task)
            
            for category, tasks in categories.items():
                completed_in_cat = sum(1 for t in tasks if t['status'] == 'Completed')
                
                with st.expander(f"📁 {category} ({completed_in_cat}/{len(tasks)} completed)", expanded=True):
                    for i, task in enumerate(tasks):
                        task_key = f"task_{case['id']}_{category}_{i}"
                        
                        col1, col2, col3, col4, col5 = st.columns([0.4, 3, 1, 1.5, 1])
                        
                        with col1:
                            checked = st.checkbox("", value=task['status'] == 'Completed', 
                                                key=task_key, label_visibility="collapsed")
                            
                            if checked and task['status'] != 'Completed':
                                task['status'] = 'Completed'
                                task['completed_date'] = datetime.now().strftime('%Y-%m-%d')
                                total = len(case['checklist'])
                                completed = sum(1 for t in case['checklist'] if t['status'] == 'Completed')
                                case['completion_percentage'] = int((completed / total) * 100)
                                st.rerun()
                            elif not checked and task['status'] == 'Completed':
                                task['status'] = 'Pending'
                                task['completed_date'] = None
                                total = len(case['checklist'])
                                completed = sum(1 for t in case['checklist'] if t['status'] == 'Completed')
                                case['completion_percentage'] = int((completed / total) * 100)
                                st.rerun()
                        
                        with col2:
                            task_text = f"~~{task['task']}~~" if task['status'] == 'Completed' else task['task']
                            st.markdown(f"{task_text}")
                            st.caption(f"👤 Responsible: {task.get('responsible', 'N/A')}")
                        
                        with col3:
                            priority_class = get_task_priority_class(task)
                            st.markdown(f"<span class='{priority_class}'>{task.get('priority', 'Normal')}</span>", 
                                      unsafe_allow_html=True)
                        
                        with col4:
                            due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                            days_until = (due_date - datetime.now().date()).days
                            
                            if task['status'] == 'Completed':
                                st.markdown("<span class='status-complete'>✓ COMPLETED</span>", unsafe_allow_html=True)
                            elif days_until < 0:
                                st.markdown(f"<span class='status-overdue'>⚠ OVERDUE {abs(days_until)}d</span>", 
                                          unsafe_allow_html=True)
                            elif days_until == 0:
                                st.markdown("<span class='status-pending'>⏰ DUE TODAY</span>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<span class='status-pending'>📅 {days_until} DAYS</span>", 
                                          unsafe_allow_html=True)
                        
                        with col5:
                            st.caption(f"📅 {task['due_date']}")
            
            st.markdown("---")
            
            # Quick Actions
            st.markdown("### ⚡ Quick Actions")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("✅ Mark Complete", use_container_width=True, type="primary"):
                    case['status'] = 'Completed'
                    case['completion_percentage'] = 100
                    for task in case['checklist']:
                        if task['status'] != 'Completed':
                            task['status'] = 'Completed'
                            task['completed_date'] = datetime.now().strftime('%Y-%m-%d')
                    st.success("Case marked as completed!")
                    st.rerun()
            
            with col2:
                if st.button("📄 Export Report", use_container_width=True):
                    df = pd.DataFrame(case['checklist'])
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "⬇ Download CSV",
                        csv,
                        f"offboarding_report_{case['employee_name'].replace(' ', '_')}.csv",
                        "text/csv",
                        use_container_width=True
                    )
            
            with col3:
                if st.button("📧 Send Reminder", use_container_width=True):
                    st.info("📧 Reminder sent to all stakeholders!")
            
            with col4:
                if st.button("🔄 Refresh Status", use_container_width=True):
                    st.rerun()
    else:
        st.markdown("""
        <div class='info-card'>
            <h3 style='margin:0 0 12px 0;'>📋 No Active Cases</h3>
            <p style='margin:0;'>All offboarding cases are completed. Create a new case to get started.</p>
        </div>
        """, unsafe_allow_html=True)

# ========== ASSET TRACKING ==========
elif page == "💼 Asset Tracking":
    st.header("💼 Asset Return Management")
    
    if st.session_state.offboarding_cases:
        # Collect all assets from active cases
        all_assets = []
        for case in st.session_state.offboarding_cases:
            if case['status'] == 'Active' and case['assets']:
                for asset in case['assets']:
                    days_remaining = calculate_days_remaining(case['last_day'])
                    status = "⚠️ Urgent" if days_remaining <= 3 else "📅 Pending"
                    
                    all_assets.append({
                        'Case ID': f"#{case['id']}",
                        'Employee': case['employee_name'],
                        'Asset': asset,
                        'Last Day': case['last_day'],
                        'Days Remaining': days_remaining,
                        'Status': status,
                        'Department': case['department']
                    })
        
        if all_assets:
            df = pd.DataFrame(all_assets)
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_employee = st.multiselect("Filter by Employee", df['Employee'].unique())
            with col2:
                filter_asset = st.multiselect("Filter by Asset Type", df['Asset'].unique())
            with col3:
                filter_dept = st.multiselect("Filter by Department", df['Department'].unique())
            
            # Apply filters
            filtered_df = df.copy()
            if filter_employee:
                filtered_df = filtered_df[filtered_df['Employee'].isin(filter_employee)]
            if filter_asset:
                filtered_df = filtered_df[filtered_df['Asset'].isin(filter_asset)]
            if filter_dept:
                filtered_df = filtered_df[filtered_df['Department'].isin(filter_dept)]
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Assets", len(filtered_df))
            with col2:
                urgent = len(filtered_df[filtered_df['Status'] == "⚠️ Urgent"])
                st.metric("Urgent Returns", urgent)
            with col3:
                st.metric("Unique Employees", filtered_df['Employee'].nunique())
            with col4:
                st.metric("Asset Types", filtered_df['Asset'].nunique())
            
            st.markdown("---")
            
            # Asset table
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                asset_counts = df['Asset'].value_counts()
                fig = go.Figure(data=[go.Bar(
                    x=asset_counts.values,
                    y=asset_counts.index,
                    orientation='h',
                    marker=dict(
                        color=asset_counts.values,
                        colorscale=[[0, '#10B981'], [1, '#D97706']],
                        showscale=False
                    )
                )])
                fig.update_layout(
                    title="Assets by Type",
                    height=400,
                    xaxis_title="Count"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                dept_counts = df['Department'].value_counts()
                fig = go.Figure(data=[go.Pie(
                    labels=dept_counts.index,
                    values=dept_counts.values,
                    hole=0.4,
                    marker=dict(colors=['#10B981', '#D97706', '#3B82F6', '#EF4444'])
                )])
                fig.update_layout(
                    title="Assets by Department",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Export
            st.markdown("---")
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                "📥 Export Asset List",
                csv,
                "asset_tracking_report.csv",
                "text/csv",
                use_container_width=False
            )
        else:
            st.info("✅ No pending asset returns for active cases.")
    else:
        st.info("No offboarding cases with assets to track.")

# ========== ACCESS MANAGEMENT ==========
elif page == "🔒 Access Management":
    st.header("🔒 System Access Revocation")
    
    st.markdown("""
    <div class='warning-card'>
        <h4 style='margin:0 0 8px 0;'>⚠️ Security Notice</h4>
        <p style='margin:0;'>Ensure all system access is revoked on or before the employee's last working day to maintain security compliance.</p>
    </div>
    """, unsafe_allow_html=True)
    
    active_cases = [c for c in st.session_state.offboarding_cases if c['status'] == 'Active']
    
    if active_cases:
        for case in active_cases:
            days_remaining = calculate_days_remaining(case['last_day'])
            urgency = "🔴 CRITICAL" if days_remaining <= 0 else "🟡 URGENT" if days_remaining <= 3 else "🟢 ON TRACK"
            
            with st.expander(f"👤 {case['employee_name']} - {case['role']} | {urgency}", expanded=days_remaining <= 3):
                st.caption(f"Last Day: {case['last_day']} ({days_remaining} days)")
                
                if 'access_status' not in case:
                    case['access_status'] = {system: 'Active' for system in case['systems']}
                
                # Group systems by category
                systems_by_category = {}
                for system in case['systems']:
                    found_category = "Other"
                    for category, sys_list in SYSTEMS.items():
                        if system in sys_list:
                            found_category = category
                            break
                    if found_category not in systems_by_category:
                        systems_by_category[found_category] = []
                    systems_by_category[found_category].append(system)
                
                # Display by category
                for category, systems in systems_by_category.items():
                    st.markdown(f"**{category}**")
                    
                    for system in systems:
                        cols = st.columns([4, 2, 1.5])
                        with cols[0]:
                            st.write(f"🔐 {system}")
                        with cols[1]:
                            current_status = case['access_status'].get(system, 'Active')
                            if current_status == 'Revoked':
                                st.markdown("<span class='status-complete'>✅ REVOKED</span>", unsafe_allow_html=True)
                            else:
                                st.markdown("<span class='status-pending'>⚠️ ACTIVE</span>", unsafe_allow_html=True)
                        with cols[2]:
                            if current_status != 'Revoked':
                                if st.button("Revoke", key=f"revoke_{case['id']}_{system}", use_container_width=True):
                                    case['access_status'][system] = 'Revoked'
                                    st.success(f"✅ Revoked: {system}")
                                    st.rerun()
                
                # Progress summary
                st.markdown("---")
                total_systems = len(case['systems'])
                revoked_systems = sum(1 for s in case['systems'] if case['access_status'].get(s) == 'Revoked')
                progress = (revoked_systems / total_systems * 100) if total_systems > 0 else 0
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(progress / 100)
                with col2:
                    st.metric("Progress", f"{revoked_systems}/{total_systems}")
                
                if revoked_systems == total_systems:
                    st.markdown("""
                    <div class='success-card'>
                        <p style='margin:0;'>✅ All system access has been revoked for this employee.</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No active cases requiring access revocation.")

# ========== EXIT INTERVIEWS ==========
elif page == "💬 Exit Interviews":
    st.header("💬 Exit Interview Management")
    
    tab1, tab2, tab3 = st.tabs(["📅 Schedule", "📝 Conduct Interview", "📊 Analysis"])
    
    with tab1:
        st.subheader("Schedule Exit Interview")
        
        active_cases = [c for c in st.session_state.offboarding_cases if c['status'] == 'Active']
        
        if active_cases:
            with st.form("schedule_interview"):
                col1, col2 = st.columns(2)
                
                with col1:
                    employee = st.selectbox("Select Employee", 
                                           [f"{c['employee_name']} ({c['role']})" for c in active_cases])
                    interview_date = st.date_input("Interview Date")
                    interview_time = st.time_input("Interview Time")
                
                with col2:
                    interviewer = st.text_input("Interviewer Name")
                    location = st.selectbox("Location", ["In-Person", "Video Call", "Phone"])
                    send_reminder = st.checkbox("Send calendar invite", value=True)
                
                notes = st.text_area("Preparation Notes")
                
                if st.form_submit_button("📅 Schedule Interview", type="primary", use_container_width=True):
                    st.markdown(f"""
                    <div class='success-card'>
                        <h4 style='margin:0 0 8px 0;'>✅ Exit Interview Scheduled</h4>
                        <p style='margin:0;'><strong>Employee:</strong> {employee}</p>
                        <p style='margin:0;'><strong>Date:</strong> {interview_date} at {interview_time}</p>
                        <p style='margin:0;'><strong>Location:</strong> {location}</p>
                        {f'<p style="margin:0;">📧 Calendar invite sent</p>' if send_reminder else ''}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No active employees to schedule interviews for.")
    
    with tab2:
        st.subheader("Conduct Exit Interview")
        
        with st.form("exit_interview_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                employee_name = st.text_input("Employee Name*")
                role = st.text_input("Role*")
                department = st.text_input("Department*")
            
            with col2:
                interview_date = st.date_input("Interview Date")
                interviewer_name = st.text_input("Interviewer")
                tenure_years = st.number_input("Years at Company", min_value=0.0, step=0.5)
            
            st.markdown("---")
            st.markdown("### 📋 Interview Questions")
            
            q1 = st.radio("1. Overall, how satisfied were you with your employment?",
                         ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"])
            
            q2 = st.text_area("2. What were your primary reasons for leaving?", height=100)
            
            q3 = st.radio("3. Would you recommend our company as a place to work?",
                         ["Definitely", "Probably", "Not Sure", "Probably Not", "Definitely Not"])
            
            q4 = st.text_area("4. What did you like most about working here?", height=100)
            
            q5 = st.text_area("5. What could we improve?", height=100)
            
            q6 = st.radio("6. How would you rate your relationship with your manager?",
                         ["Excellent", "Good", "Fair", "Poor"])
            
            q7 = st.radio("7. Were you satisfied with career growth opportunities?",
                         ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"])
            
            q8 = st.radio("8. How would you rate work-life balance?",
                         ["Excellent", "Good", "Fair", "Poor"])
            
            q9 = st.text_area("9. Any additional comments or suggestions?", height=100)
            
            submit = st.form_submit_button("💾 Submit Interview", type="primary", use_container_width=True)
            
            if submit and employee_name and role:
                interview_data = {
                    'employee_name': employee_name,
                    'role': role,
                    'department': department,
                    'date': interview_date.strftime('%Y-%m-%d'),
                    'interviewer': interviewer_name,
                    'tenure_years': tenure_years,
                    'satisfaction': q1,
                    'reasons': q2,
                    'recommend': q3,
                    'liked_most': q4,
                    'improvements': q5,
                    'manager_relationship': q6,
                    'career_growth': q7,
                    'work_life_balance': q8,
                    'additional_comments': q9
                }
                st.session_state.exit_interviews.append(interview_data)
                
                st.markdown("""
                <div class='success-card'>
                    <h4 style='margin:0 0 8px 0;'>✅ Exit Interview Submitted Successfully!</h4>
                    <p style='margin:0;'>Data has been recorded and will be included in analytics.</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Exit Interview Analytics")
        
        if st.session_state.exit_interviews:
            df = pd.DataFrame(st.session_state.exit_interviews)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Interviews", len(df))
            
            with col2:
                if 'satisfaction' in df.columns:
                    satisfied = len(df[df['satisfaction'].isin(['Very Satisfied', 'Satisfied'])])
                    satisfaction_rate = (satisfied / len(df) * 100) if len(df) > 0 else 0
                    st.metric("Satisfaction Rate", f"{satisfaction_rate:.0f}%")
            
            with col3:
                if 'recommend' in df.columns:
                    recommend_yes = len(df[df['recommend'].isin(['Definitely', 'Probably'])])
                    recommend_rate = (recommend_yes / len(df) * 100) if len(df) > 0 else 0
                    st.metric("Would Recommend", f"{recommend_rate:.0f}%")
            
            with col4:
                if 'tenure_years' in df.columns:
                    avg_tenure = df['tenure_years'].mean()
                    st.metric("Avg Tenure", f"{avg_tenure:.1f} years")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                if 'satisfaction' in df.columns:
                    satisfaction_counts = df['satisfaction'].value_counts()
                    fig = go.Figure(data=[go.Pie(
                        labels=satisfaction_counts.index,
                        values=satisfaction_counts.values,
                        hole=0.4,
                        marker=dict(colors=['#10B981', '#34D399', '#FCD34D', '#F59E0B', '#EF4444'])
                    )])
                    fig.update_layout(title="Overall Satisfaction", height=350)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'recommend' in df.columns:
                    recommend_counts = df['recommend'].value_counts()
                    fig = go.Figure(data=[go.Bar(
                        x=recommend_counts.index,
                        y=recommend_counts.values,
                        marker_color=['#10B981', '#34D399', '#FCD34D', '#F59E0B', '#EF4444']
                    )])
                    fig.update_layout(title="Would Recommend Company", height=350, xaxis_title="", yaxis_title="Count")
                    st.plotly_chart(fig, use_container_width=True)
            
            # Additional metrics
            col1, col2 = st.columns(2)
            
            with col1:
                if 'manager_relationship' in df.columns:
                    manager_counts = df['manager_relationship'].value_counts()
                    fig = go.Figure(data=[go.Bar(
                        y=manager_counts.index,
                        x=manager_counts.values,
                        orientation='h',
                        marker_color='#10B981'
                    )])
                    fig.update_layout(title="Manager Relationship Rating", height=300)
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'work_life_balance' in df.columns:
                    wlb_counts = df['work_life_balance'].value_counts()
                    fig = go.Figure(data=[go.Bar(
                        y=wlb_counts.index,
                        x=wlb_counts.values,
                        orientation='h',
                        marker_color='#D97706'
                    )])
                    fig.update_layout(title="Work-Life Balance Rating", height=300)
                    st.plotly_chart(fig, use_container_width=True)
            
            # Key Insights
            st.markdown("---")
            st.subheader("💡 Key Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Common Reasons for Leaving:**")
                if 'reasons' in df.columns:
                    reasons = df['reasons'].tolist()
                    for i, reason in enumerate(reasons[-5:], 1):
                        if reason:
                            st.write(f"{i}. {reason[:100]}...")
            
            with col2:
                st.markdown("**Top Improvement Suggestions:**")
                if 'improvements' in df.columns:
                    improvements = df['improvements'].tolist()
                    for i, improvement in enumerate(improvements[-5:], 1):
                        if improvement:
                            st.write(f"{i}. {improvement[:100]}...")
            
            # Export
            st.markdown("---")
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Export Interview Data",
                csv,
                "exit_interviews_report.csv",
                "text/csv"
            )
        else:
            st.markdown("""
            <div class='info-card'>
                <p style='margin:0;'>No exit interviews conducted yet. Use the "Conduct Interview" tab to record interviews.</p>
            </div>
            """, unsafe_allow_html=True)

# ========== FINAL COMPENSATION ==========
elif page == "💰 Final Compensation":
    st.header("💰 Final Paycheck Calculator")
    
    st.markdown("""
    <div class='info-card'>
        <p style='margin:0;'><strong>Note:</strong> This calculator provides estimates. Please consult with Finance/Payroll for official calculations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("paycheck_calculator"):
        st.markdown("### 👤 Employee Information")
        col1, col2 = st.columns(2)
        
        with col1:
            employee_name = st.text_input("Employee Name*")
            employee_id = st.text_input("Employee ID")
            annual_salary = st.number_input("Annual Salary ($)*", min_value=0.0, step=1000.0, format="%.2f")
        
        with col2:
            pay_frequency = st.selectbox("Pay Frequency", ["Weekly", "Bi-Weekly", "Semi-Monthly", "Monthly"])
            last_pay_date = st.date_input("Last Pay Date")
            last_working_day = st.date_input("Last Working Day")
        
        st.markdown("---")
        st.markdown("### 💵 Additional Compensation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            unused_pto = st.number_input("Unused PTO Days", min_value=0.0, step=0.5, format="%.1f")
            bonus_amount = st.number_input("Bonus/Commission ($)", min_value=0.0, step=100.0, format="%.2f")
            expenses = st.number_input("Unreimbursed Expenses ($)", min_value=0.0, step=50.0, format="%.2f")
        
        with col2:
            severance_weeks = st.number_input("Severance (weeks)", min_value=0.0, step=1.0, format="%.0f")
            stock_options = st.number_input("Vested Stock Value ($)", min_value=0.0, step=100.0, format="%.2f")
            other_compensation = st.number_input("Other Compensation ($)", min_value=0.0, step=50.0, format="%.2f")
        
        st.markdown("---")
        st.markdown("### ➖ Deductions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            outstanding_loans = st.number_input("Outstanding Loans ($)", min_value=0.0, step=50.0, format="%.2f")
            equipment_charges = st.number_input("Equipment/Asset Charges ($)", min_value=0.0, step=50.0, format="%.2f")
        
        with col2:
            other_deductions = st.number_input("Other Deductions ($)", min_value=0.0, step=50.0, format="%.2f")
        
        st.markdown("---")
        calculate = st.form_submit_button("🧮 Calculate Final Paycheck", type="primary", use_container_width=True)
        
        if calculate and employee_name and annual_salary > 0:
            # Calculate working days
            working_days = (last_working_day - last_pay_date).days + 1
            
            # Calculate daily rate
            daily_rate = annual_salary / 365
            
            # Calculate components
            regular_pay = daily_rate * working_days
            pto_payout = daily_rate * unused_pto
            severance_pay = (annual_salary / 52) * severance_weeks
            
            total_earnings = regular_pay + pto_payout + bonus_amount + expenses + severance_pay + stock_options + other_compensation
            total_deductions = outstanding_loans + equipment_charges + other_deductions
            
            # Estimated taxes (simplified - 25% federal + 7% state)
            estimated_tax_rate = 0.32
            estimated_taxes = total_earnings * estimated_tax_rate
            
            net_pay = total_earnings - total_deductions - estimated_taxes
            
            st.markdown("""
            <div class='success-card'>
                <h3 style='margin:0 0 12px 0;'>✅ Final Paycheck Calculated</h3>
                <p style='margin:0;'>Review the breakdown below and download the summary.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display breakdown
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 💵 Earnings")
                st.write(f"**Regular Pay** ({working_days} days)")
                st.write(f"${regular_pay:,.2f}")
                st.write("")
                st.write(f"**Unused PTO** ({unused_pto} days)")
                st.write(f"${pto_payout:,.2f}")
                st.write("")
                st.write(f"**Severance** ({severance_weeks} weeks)")
                st.write(f"${severance_pay:,.2f}")
                st.write("")
                st.write("**Bonus/Commission**")
                st.write(f"${bonus_amount:,.2f}")
                st.write("")
                st.write("**Expenses**")
                st.write(f"${expenses:,.2f}")
                st.write("")
                st.write("**Stock Options**")
                st.write(f"${stock_options:,.2f}")
                st.write("")
                st.write("**Other**")
                st.write(f"${other_compensation:,.2f}")
                st.markdown("---")
                st.markdown(f"### Total Gross: ${total_earnings:,.2f}")
            
            with col2:
                st.markdown("### ➖ Deductions")
                st.write("**Outstanding Loans**")
                st.write(f"${outstanding_loans:,.2f}")
                st.write("")
                st.write("**Equipment Charges**")
                st.write(f"${equipment_charges:,.2f}")
                st.write("")
                st.write("**Other Deductions**")
                st.write(f"${other_deductions:,.2f}")
                st.write("")
                st.write("**Estimated Taxes** (32%)")
                st.write(f"${estimated_taxes:,.2f}")
                st.markdown("---")
                st.markdown(f"### Total Deductions: ${total_deductions + estimated_taxes:,.2f}")
            
            with col3:
                st.markdown("### 💰 Final Net Pay")
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #10B981 0%, #D97706 100%); 
                            padding: 2rem; border-radius: 16px; text-align: center; margin-top: 20px;'>
                    <div style='font-size: 3rem; font-weight: 800; color: white;'>
                        ${net_pay:,.2f}
                    </div>
                    <div style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 8px;'>
                        Net Amount
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("")
                st.info("⚠️ Tax estimate only. Actual taxes may vary based on tax bracket, deductions, and local regulations.")
            
            # Download summary
            st.markdown("---")
            summary_data = {
                'Component': ['Regular Pay', 'Unused PTO', 'Severance', 'Bonus/Commission', 'Expenses', 
                            'Stock Options', 'Other', 'Gross Pay', 'Loans', 'Equipment', 'Other Deductions', 
                            'Estimated Taxes', 'Total Deductions', 'Net Pay'],
                'Amount': [f"${regular_pay:,.2f}", f"${pto_payout:,.2f}", f"${severance_pay:,.2f}", 
                          f"${bonus_amount:,.2f}", f"${expenses:,.2f}", f"${stock_options:,.2f}",
                          f"${other_compensation:,.2f}", f"${total_earnings:,.2f}",
                          f"-${outstanding_loans:,.2f}", f"-${equipment_charges:,.2f}", 
                          f"-${other_deductions:,.2f}", f"-${estimated_taxes:,.2f}",
                          f"-${total_deductions + estimated_taxes:,.2f}", f"${net_pay:,.2f}"]
            }
            df = pd.DataFrame(summary_data)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "📄 Download Payment Summary",
                csv,
                f"final_paycheck_{employee_name.replace(' ', '_')}.csv",
                "text/csv",
                use_container_width=False
            )

# ========== ANALYTICS ==========
elif page == "📈 Analytics & Insights":
    st.header("📈 Offboarding Analytics & Insights")
    
    if st.session_state.offboarding_cases:
        df = pd.DataFrame(st.session_state.offboarding_cases)
        
        # Key Performance Indicators
        st.subheader("📊 Key Performance Indicators")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Cases", len(df))
        
        with col2:
            avg_completion = df['completion_percentage'].mean()
            st.metric("Avg Completion", f"{avg_completion:.1f}%")
        
        with col3:
            completed = len(df[df['status'] == 'Completed'])
            st.metric("Completed", completed)
        
        with col4:
            active = len(df[df['status'] == 'Active'])
            st.metric("Active", active)
        
        with col5:
            completion_rate = (completed / len(df) * 100) if len(df) > 0 else 0
            st.metric("Success Rate", f"{completion_rate:.0f}%")
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            if 'department' in df.columns:
                dept_counts = df['department'].value_counts()
                fig = go.Figure(data=[go.Bar(
                    x=dept_counts.values,
                    y=dept_counts.index,
                    orientation='h',
                    marker=dict(
                        color=dept_counts.values,
                        colorscale=[[0, '#10B981'], [1, '#D97706']],
                        showscale=False
                    )
                )])
                fig.update_layout(
                    title="Offboarding Cases by Department",
                    height=400,
                    xaxis_title="Number of Cases"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'reason' in df.columns:
                reason_counts = df['reason'].value_counts()
                fig = go.Figure(data=[go.Pie(
                    labels=reason_counts.index,
                    values=reason_counts.values,
                    hole=0.4,
                    marker=dict(colors=['#10B981', '#D97706', '#3B82F6', '#EF4444', '#8B5CF6'])
                )])
                fig.update_layout(
                    title="Reasons for Leaving",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Role analysis
        col1, col2 = st.columns(2)
        
        with col1:
            role_counts = df['role'].value_counts().head(10)
            fig = go.Figure(data=[go.Bar(
                x=role_counts.index,
                y=role_counts.values,
                marker_color='#10B981'
            )])
            fig.update_layout(
                title="Top 10 Roles",
                height=400,
                xaxis_title="Role",
                yaxis_title="Count"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Completion rate by role
            if len(df) > 0:
                role_completion = df.groupby('role')['completion_percentage'].mean().sort_values(ascending=False).head(10)
                fig = go.Figure(data=[go.Bar(
                    y=role_completion.index,
                    x=role_completion.values,
                    orientation='h',
                    marker_color='#D97706'
                )])
                fig.update_layout(
                    title="Avg Completion by Role",
                    height=400,
                    xaxis_title="Completion %"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Exit interview correlation
        if st.session_state.exit_interviews:
            st.markdown("---")
            st.subheader("💬 Exit Interview Correlation")
            
            interview_df = pd.DataFrame(st.session_state.exit_interviews)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                satisfaction_map = {'Very Satisfied': 5, 'Satisfied': 4, 'Neutral': 3, 'Dissatisfied': 2, 'Very Dissatisfied': 1}
                if 'satisfaction' in interview_df.columns:
                    avg_satisfaction = interview_df['satisfaction'].map(satisfaction_map).mean()
                    st.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}/5.0")
            
            with col2:
                if 'recommend' in interview_df.columns:
                    recommend_yes = len(interview_df[interview_df['recommend'].isin(['Definitely', 'Probably'])])
                    recommend_rate = (recommend_yes / len(interview_df) * 100) if len(interview_df) > 0 else 0
                    st.metric("Recommendation Rate", f"{recommend_rate:.0f}%")
            
            with col3:
                if 'tenure_years' in interview_df.columns:
                    avg_tenure = interview_df['tenure_years'].mean()
                    st.metric("Avg Tenure", f"{avg_tenure:.1f} years")
        
        # Data table
        st.markdown("---")
        st.subheader("📋 Detailed Data")
        
        display_columns = ['employee_name', 'role', 'department', 'last_day', 'reason', 'status', 'completion_percentage', 'created_date']
        available_columns = [col for col in display_columns if col in df.columns]
        
        st.dataframe(df[available_columns], use_container_width=True, hide_index=True)
        
        # Export
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Export Full Dataset",
            csv,
            f"offboarding_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    else:
        st.info("No data available. Create offboarding cases to see analytics.")

# ========== SETTINGS ==========
elif page == "⚙️ Settings":
    st.header("⚙️ System Settings")
    
    tab1, tab2, tab3 = st.tabs(["🔧 General", "📧 Notifications", "📊 Reports"])
    
    with tab1:
        st.subheader("General Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Default Settings**")
            default_notice_period = st.number_input("Default Notice Period (days)", min_value=0, value=14)
            auto_generate_tasks = st.checkbox("Auto-generate role-based tasks", value=True)
            require_exit_interview = st.checkbox("Require exit interview", value=True)
        
        with col2:
            st.markdown("**System Preferences**")
            date_format = st.selectbox("Date Format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"])
            timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "CST", "MST"])
        
        if st.button("💾 Save Settings", type="primary"):
            st.success("✅ Settings saved successfully!")
    
    with tab2:
        st.subheader("Notification Settings")
        
        st.markdown("**Email Notifications**")
        notify_manager = st.checkbox("Notify manager on case creation", value=True)
        notify_hr = st.checkbox("Notify HR on case creation", value=True)
        notify_it = st.checkbox("Notify IT for access revocation", value=True)
        
        st.markdown("**Reminder Settings**")
        remind_before_days = st.number_input("Send reminders (days before due)", min_value=1, value=3)
        reminder_frequency = st.selectbox("Reminder Frequency", ["Daily", "Every 2 days", "Weekly"])
        
        if st.button("💾 Save Notification Settings", type="primary"):
            st.success("✅ Notification settings saved!")
    
    with tab3:
        st.subheader("Report Settings")
        
        st.markdown("**Automated Reports**")
        weekly_summary = st.checkbox("Weekly summary report", value=True)
        monthly_analytics = st.checkbox("Monthly analytics report", value=True)
        
        st.markdown("**Report Recipients**")
        report_emails = st.text_area("Email addresses (one per line)", 
                                     placeholder="hr@company.com\nmanager@company.com")
        
        if st.button("💾 Save Report Settings", type="primary"):
            st.success("✅ Report settings saved!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 30px 20px; background: white; 
            border-radius: 16px; margin-top: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
    <div style='font-size: 24px; font-weight: 800; 
                background: linear-gradient(135deg, #10B981 0%, #D97706 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                margin-bottom: 12px;'>
        Employee Offboarding Pro
    </div>
    <div style='color: #6B7280; font-size: 14px; margin-bottom: 16px;'>
        Streamlined employee transition management with automated workflows
    </div>
    <div style='color: #9CA3AF; font-size: 12px;'>
        © 2025 Offboarding Pro • Privacy Policy • Terms of Service • Support
    </div>
</div>
""", unsafe_allow_html=True)