import streamlit as st
from home import show_home
from premium import show_premium
from about import show_about

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Premium", "About"])

if page == "Home":
    show_home()
elif page == "Premium":
    show_premium()
elif page == "About":
    show_about()


