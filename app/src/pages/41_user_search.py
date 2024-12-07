import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

def fetch_user_data(UserID):
    """
    Fetch user data from the Flask API.
    Returns a Pandas DataFrame if successful, otherwise None.
    """
    try:
        response = requests.get("http://api:4000/aa/users/view/" + str(UserID))
        response.raise_for_status() 
        users = response.json() 
        user_data = pd.DataFrame(users, columns=["UserID", 'Name', "Occupation", "Location,", "Age", "Bio", 'Industry', 'NUCollege'])
        return user_data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch  data from the API: {e}")
        return None

def fetch_user_data_industry(industry):
    """
    Fetch user data from the Flask API.
    Returns a Pandas DataFrame if successful, otherwise None.
    """
    try:
        response = requests.get("http://api:4000/aa/users/by-industry", json={'industry':industry})
        response.raise_for_status() 
        users = response.json() 
        user_data = pd.DataFrame(users, columns=["UserID", "Name", "Bio", "IndustryName", "NUCollege"])
        return user_data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch  data from the API: {e}") 
        return None

def fetch_user_data_skills(soft_skills, tech_skills):
    """
    Fetch user data from the Flask API.
    Returns a Pandas DataFrame if successful, otherwise None.
    """
    try:
        skills_data = {'soft_skills' : soft_skills, 'tech_skills' : tech_skills}
        response = requests.get("http://api:4000/aa/users/by-skills", json=skills_data)
        response.raise_for_status() 
        users = response.json() 
        user_data = pd.DataFrame(users, columns=["UserID", "Name", "Bio", "Occupation", "CompanyName", 'SoftSkills', 'TechnicalSkills'])
        return user_data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch  data from the API: {e}")
        return None
    
def fetch_user_data_by_year(year):
    """
    Fetch user data by year from the Flask API.
    Returns a Pandas DataFrame if successful, otherwise None.
    """
    try:
        response = requests.get("http://api:4000/aaa/student/by-year", json={'year': year})
        response.raise_for_status() 
        users = response.json()
        user_data = pd.DataFrame(users, columns=["UserID", "Name", "Bio", "IndustryName", "NUCollege"])
        return user_data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data from the API: {e}")
        return None


def main():
    """
    Main function to render the Streamlit app.
    """
    st.title('Users')

    st.write('Search by users')
    with st.form("search_user_form"):
    
        UserID = int(st.number_input("UserID", step=1))
    
        # Add the submit button (which every form needs)
        submit_button = st.form_submit_button("Search for User")
        
        # Validate all fields are filled when form is submitted
        if submit_button:
            if not UserID:
                st.error("Please enter a UserID")
            else:
                # Fetch user data from the API
                user_data = fetch_user_data(UserID)
            
                # show user data
                if user_data is not None and not user_data.empty:
                    st.success("Successfully fetched data from the API.")
                    st.dataframe(user_data)
                else:
                    st.warning("No user data available.")

    st.write('Search by Industry')
    with st.form('search_user_industry_form'):
        industry = st.text_area('Industry')

        # Add the submit button (which every form needs)
        submit_button = st.form_submit_button("Search for User")

        if submit_button:
            if not industry:
                st.error("Please enter an Industry")
            else:
                st.write(f"searching for users in industry: '{industry}'")
                user_data = fetch_user_data_industry(industry)
                # show user data
                if user_data is not None and not user_data.empty:
                    st.success("Successfully fetched data from the API.")
                    st.dataframe(user_data)
                else:
                    st.warning("No user data available.")
    
    st.write('Search by Skills (Employers)')
    with st.form('search_user_skills_form'):

        soft_skills = st.text_area('Soft Skills')
        tech_skills = st.text_area('Technical Skills')

        # Add the submit button (which every form needs)
        submit_button = st.form_submit_button("Search for User")

        if submit_button:
            if not soft_skills or not tech_skills:
                st.error("Please enter skills")

            else:
                user_data = fetch_user_data_skills(soft_skills, tech_skills)
                # show user data
                if user_data is not None and not user_data.empty:
                    st.success("Successfully fetched data from the API.")
                    st.dataframe(user_data)
                else:
                    st.warning("No user data available.")

    with st.form('view_user_search_form'):
        UserID_toview = st.number_input('UserID', min_value = 0, step=1)
        
        submit_button = st.form_submit_button("Search for User")
        if submit_button:
            try:
                response = requests.get("http://api:4000/aa/users/view/" + str(UserID))
                response.raise_for_status() 
                st.session_state['profile_view_UserID'] = UserID_toview
                st.switch_page('pages/42_view_profile.py')
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch user data from the API: {e}")
    
    st.write('If you want to find an older student to talk to: Search by Student Year')
    with st.form('search_user_year_form'):
        year = st.text_input('Enter Year to Search for Students:')

        # Add the submit button (which every form needs)
        submit_button = st.form_submit_button("Search for Users")

        if submit_button:
            if not year:
                st.error("Please enter a Year")
            else:
                st.write(f"Searching for users in year: '{year}'")
                user_data = fetch_user_data_by_year(year)
                
                # Show user data
                if user_data is not None and not user_data.empty:
                    st.success("Successfully fetched data from the API.")
                    st.dataframe(user_data)
                else:
                    st.warning("No user data available for the specified year.") 

    
            



main()
