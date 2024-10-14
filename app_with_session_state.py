import streamlit as st
import threading
import time  # For simulating long-running tasks
from users import user_data  # Assuming user_data is a dictionary of usernames and passwords
from send_email import send_email  # Import the email sending function
from dotenv import load_dotenv
from utils_consts import to_addresses, subject, body, today_date
from utils_funcs import *
from users import *

load_dotenv()  # Load environment variables from the .env file


# Function to check user credentials
def check_credentials(username, password):
    return username in user_data and user_data[username][0] == password

# Streamlit app
def main():
    # Page 1: User Authentication
    st.title("User Authentication")

    # Store username and password in session state to retain after login
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    
    if "password" not in st.session_state:
        st.session_state["password"] = ""

    # Input fields for authentication
    st.session_state["username"] = st.text_input("Username", value=st.session_state["username"])
    st.session_state["password"] = st.text_input("Password", type="password", value=st.session_state["password"])

    if st.button("Login"):
        if check_credentials(st.session_state["username"], st.session_state["password"]):
            st.success("Login successful!")
            # Redirect to new page
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid username or password.")

    # Only show input page if authenticated
    if st.session_state.get("authenticated"):
        show_input_page()

def show_input_page():
    # Page 2: Input form for email, keywords, and dropdown menu
    st.title("Search Input Page")

    # Store input values in session state to avoid page reset
    if "email" not in st.session_state:
        st.session_state["email"] = ""
    
    if "keywords" not in st.session_state:
        st.session_state["keywords"] = ""
    
    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = ""

    if "task_complete" not in st.session_state:
        st.session_state["task_complete"] = False

    # Input fields
    st.session_state["email"] = st.text_input("Enter your email (e.g., abc.def@devoteam.com)", value=st.session_state["email"])

    st.write(st.session_state)

    # If the email is not yet stored in session state, prompt for it again or further input will be disabled
    if not st.session_state["email"]:
        st.warning("Please enter your email to proceed.")
        return

    # If email is entered, display the remaining input fields
    st.session_state["keywords"] = st.text_input("Enter keywords for search", value=st.session_state["keywords"])
    
    # Dropdown menu with choices
    dropdown_options = ["التجارة", "المقاولات", "التشغيل والصيانة والنظافة للمنشآت",
                        "العقارات والأراضي", "الصناعة والتعدين والتدوير", "الغاز والمياه والطاقة",
                        "المناجم والبترول والمحاجر", "الإعلام والنشر والتوزيع", "الاتصالات وتقنية المعلومات",
                        "الزراعة والصيد", "الرعاية الصحية والنقاهة", "التعليم والتدريب",
                        "التوظيف والاستقدام", "الأمن والسلامة", "النقل والبريد والتخزين",
                        "المهن الاستشارية", "السياحة والمطاعم والفنادق وتنظيم المعارض",
                        "المالية والتمويل والتأمين", "الخدمات الأخرى"]  # Replace with your actual choices
    st.session_state["selected_option"] = st.selectbox("النشاط الاساسي", dropdown_options, index=dropdown_options.index(st.session_state["selected_option"]) if st.session_state["selected_option"] else 0)

    if st.button("Submit"):
        # Reset task state
        st.session_state["task_complete"] = False
        thread = threading.Thread(target=process_request)
        thread.start()

        # Display the spinner and wait for the task to complete
        with st.spinner('Processing...'):
            while thread.is_alive():
                time.sleep(0.1)

        # Once the task is complete, show success message
        if st.session_state["task_complete"]:
            st.success(f"Email successfully sent to {st.session_state['email']}!")
        else:
            st.error("There was an error processing your request.")

def process_request():
    # Simulate a long-running process
    try:
        
        time.sleep(5)  # Simulate time-consuming task

        # Send email after processing
        to_addresses = [st.session_state["email"]]
        subject = f"Search Results for {st.session_state['keywords']}"
        body = f"Keywords: {st.session_state['keywords']}\nSelected Option: {st.session_state['selected_option']}\nPlease find the attached results."

        # Split keywords into a list based on commas or spaces
        keywords = [keyword.strip() for keyword in st.session_state["keywords"].split(',') if keyword.strip()]
        main_activity = st.session_state["selected_option"]

        get_terms_files(keywords, str(main_activity))
        agg_files()

        send_email(to_addresses, subject, body)
        st.session_state["task_complete"] = True

    except Exception as e:
        st.error(f"Failed to send the email: {str(e)}")
        st.session_state["task_complete"] = False

if __name__ == "__main__":
    main()
