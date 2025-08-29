import streamlit as st
import home
import premium
import about

# App Title + Logo
st.set_page_config(page_title="PersonaX", page_icon="✨")

st.sidebar.title("PersonaX Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Premium", "About Me"])

if page == "Home":
    home.show_home()
elif page == "Premium":
    premium.show_premium()
elif page == "About Me":
    about.show_about()
