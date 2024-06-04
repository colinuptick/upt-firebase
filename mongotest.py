import pymongo
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient
import streamlit as st
import re


st.title("MongoDB Test")
st.write('Welcome to the ticket CRM database.')

# Create a new client and connect to the server
cluster = MongoClient("mongodb+srv://colin:Momy1234@cluster0.1zmkjho.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Get a list of all databases
all_databases = cluster.list_database_names()
system_databases = {'admin', 'local', 'config'}
user_databases = [db for db in all_databases if db not in system_databases]

# List of companies with proper names
companies = {}

for database in user_databases:
    values = database.replace(" ", "_")
    companies[database] = values

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
        
        # Checks for unique username
        if st.button("Enter"):
            if user_list.find_one({"username": username}) is None:
                user_list.insert_one(new_user)
                st.success(f"User {new_user['username']} created! Proceed to login.")
            else: 
                st.error('Username taken. Try again')
                
with st.popover("Create New Company"):
    
    company_name = st.text_input("New Company Name")
    
    # Check if the name has any special characters
    pattern = re.compile(r'^[A-Za-z\s]+$')
    if st.button("Create"):
    
        if pattern.match(company_name):
            new_company_name = company_name.replace(" ", "_")
            new_company = cluster[new_company_name]
            # get_database(new_company_name)
            
            new_teams = new_company['teams']
            new_identities = new_company['identities']
            new_tickets = new_company['tickets']
            new_representatives = new_company['representatives']
            new_users = new_company['users']
            
            st.success('Company created! Now create a new user')
            new_users.insert_one({
                'username': 'h',
                'password': 'h',
                'email': 'h',
                'role': '',
            })
            
            indexes = new_users.index_information()
            for index in indexes:
                new_users.drop_index(index)
        else:
            st.error('No special characters or symbols allowed.')