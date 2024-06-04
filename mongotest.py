import pymongo
from pymongo.mongo_client import MongoClient
import streamlit as st

st.title("MongoDB Test")
st.write('Welcome to the ticket CRM database.')

# Create a new client and connect to the server
cluster = MongoClient("mongodb+srv://colin:Momy1234@cluster0.1zmkjho.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# List of companies and corresponding names
companies = {
    "Company A": "company_a",
    "Company B": "company_b",
}

# Select company (database)
company = st.selectbox(
    "Select your company:", 
    list(companies.keys()), 
    index=None,
    placeholder="Choose a company"
)

if company:
    
    db = cluster[companies[company]]
    user_list = db['users']
    logged_in = False
    
    # Login
    with st.form("login_form"):
        st.write("Login or Create New Account")
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        
        login_submitted = st.form_submit_button("Login")
        
        if login_submitted:
            user = user_list.find_one({'username': username})
            if user:
                if user['password'] == password:
                    logged_in = True
                    st.success('Logged in successfully!')
                else:
                    st.error('Incorrect password.')
            else:
                st.error('User not found.')

    
    # Create new user popover
    with st.popover("Create New User"):
        st.write("Enter information:")
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        email = st.text_input('Email')
        role = ''
        
        # Checks if it's the first account, then makes it the admin
        if user_list.count_documents({}) == 0:
            role = 'admin'
        
        new_user = {
            'username': username,
            'password': password,
            'email': email,
            'role': role, 
        }
        
        if st.button("Enter"):
            if user_list.find_one({"username": username}) is None:
                user_list.insert_one(new_user)
                st.success(f"User {new_user['username']} created! Proceed to login.")
            else: 
                st.error('Username taken. Try again')