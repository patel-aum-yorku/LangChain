import Langchain_helper
import streamlit as st

st.title("Restaurant Name Generator!")

st.sidebar.title("Options")
cuisine =st.sidebar.selectbox("Pick a cuisine", ("Arabic","Indian","Italian", "Chinese", "Mexican"))




if cuisine:
    response =  Langchain_helper.generate_restaurant_name_and_items(cuisine)
    st.header(response['restuarant_name'].strip())
    st.subheader("Menu Items")
    menu_items = response['menu_items'].strip().split(",")
    for item in menu_items:
        st.write(f"- {item}")