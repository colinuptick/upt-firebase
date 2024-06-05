import pymongo
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient
import streamlit as st
import re
import pandas as pd

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
user = None
logged_in = False

for database in user_databases:
    values = database.replace(" ", "_")
    companies[database] = values

# Select company (database)
company = st.selectbox(
    "Select your company:", 
    list(companies.keys()), 
    index=None,
)   

db = None
user_list = None

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
            id1 = new_users.insert_one({}).inserted_id
            id2 = new_teams.insert_one({}).inserted_id
            id3 = new_tickets.insert_one({}).inserted_id
            id4 = new_representatives.insert_one({}).inserted_id
            id5 = new_identities.insert_one({}).inserted_id
            
            new_users.delete_one({'_id': id1})
            new_teams.delete_one({'_id': id2})
            new_tickets.delete_one({'_id': id3})
            new_representatives.delete_one({'_id': id4})
            new_identities.delete_one({'_id': id5})
            
        else:
            st.error('No special characters or symbols allowed.')

if company:
    
    db = cluster[companies[company]]
    user_list = db['users']
    
    st.session_state.db = db
    st.session_state.user_list = user_list
    
    # Login
    with st.form("login_form"):
        st.write("Login or Create New Account")
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        
        login_submitted = st.form_submit_button("Login")
        
        if login_submitted:
            temp_user = user_list.find_one({'username': username})
            if temp_user:
                if temp_user['password'] == password:
                    logged_in = True
                    user = temp_user
                    st.success('Logged in successfully!')
                    
                    # Update session state with new variables
                    st.session_state.logged_in = logged_in
                    st.session_state.user = user
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
                           
    # Opens other tabs after login            
    if st.session_state.logged_in:
        tab1, tab2 = st.tabs(['Data View', 'Admin Console'])
        
        # Data viewer tab
        with tab1:
            
            tickets = db['tickets']
            role = st.session_state.user['role']
            
            visible_tickets = list(tickets.find({"tag": role}))
            if role == 'admin':
                visible_tickets = list(tickets.find())
            
            print(visible_tickets)
            df = pd.DataFrame(visible_tickets)
            # df = df.drop(columns=['_id'])
            
            st.dataframe(df)
        
        with tab2:
            if st.session_state.user['role'] == 'admin':
            
                st.subheader('Admin Console')
                
                # Lists users for the admin to
                users = list(st.session_state.user_list.find())
                usernames = [user['username'] for user in users]
                selected_username = st.selectbox('Select a user', usernames, index=None)
                selected_user = next((user for user in users if user['username'] == selected_username), None)            
                
                if selected_username:
                    new_role = st.text_input(f"Enter new role for {selected_username}")
                    if st.button('Change Role'):
                        
                        user_list.find_one_and_update({'username': selected_username}, {'$set': {'role': new_role}})
                        
                        st.success('Role updated!')                 
                
            else:
                st.error("You do not have permission to access the admin panel.")