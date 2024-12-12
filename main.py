import streamlit as st
from streamlit_option_menu import option_menu
from google_sheets import connect_to_sheet
import pandas as pd

# Set the page configuration as the first Streamlit command
st.set_page_config(
    page_title="GoMechanic Dashboard",
    page_icon="🚗",
    layout="wide",
)

# Load Google Sheets data
json_keyfile = "hybrid-creek-431418-h8-e329e9e00ef5.json"
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1nN11gQ_F38CdjC7Wd0X0tj8ZRY6qgU-cGB9PZ24twc0/edit?gid=0#gid=0"
sheet_name = "test sheet"

# Fetch data from Google Sheets
try:
    data = connect_to_sheet(json_keyfile, spreadsheet_url, sheet_name)
except Exception as e:
    st.error(f"Error loading data from Google Sheets: {e}")
    data = pd.DataFrame()  # Fallback empty dataframe

# Session State for login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "source_name" not in st.session_state:
    st.session_state["source_name"] = ""

# Login Page
if not st.session_state["logged_in"]:
    st.title("🔒 Login")
    source_name = st.text_input("Enter Source Name:")
    password = st.text_input("Enter Password:", type="password")
    login_button = st.button("Login")

    if login_button:
        if ((data["Source Name"] == source_name) & (data["Password"] == password)).any():
            st.session_state["logged_in"] = True
            st.session_state["source_name"] = source_name
            st.success("Login Successful! Redirecting...")
            st.rerun()  # Refresh the app state
        else:
            st.error("Incorrect Source Name or Password. Please try again.")
else:
    with st.sidebar:
        # Styled title for the sidebar
        styled_title = '''<h1><span style="color:red; font-size: 50px; font-weight: bold;">Go</span><span style="font-size: 40px;">Mechanic</span> 🚗</h1>'''
        st.markdown(styled_title, unsafe_allow_html=True)

        app = option_menu(
            menu_title="GoMechanic",  # Default title
            options=["Home", "Dashboard", "Analytics", "Show Data", "Logout"],
            icons=["house-fill", "person-circle", "trophy-fill", "chat-fill", "sign-out"],
            menu_icon="chat-text-fill",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "black"},
                "icon": {"color": "white", "font-size": "23px"},
                "nav-link": {
                    "color": "white",
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "blue",
                },
                "nav-link-selected": {"background-color": "#02ab21"},
            },
        )

    # Define menu pages
    if app == "Home":
        st.title("🏠 Home")
        st.header("Welcome to GoMechanic! Navigate through the menu to explore.")

    elif app == "Dashboard":
        import dashboard  # Import your dashboard logic
        dashboard.show(st.session_state["source_name"], data)

    elif app == "Analytics":
        import analytics  # Import your analysis logic
        analytics.show(st.session_state["source_name"], data)

    elif app == "Show Data":
        import show_data  # Import your show_data logic
        show_data.show(st.session_state["source_name"], data)

    elif app == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["source_name"] = ""
        st.rerun()
