import streamlit as st

st.set_page_config(
    page_title="Hello",
    #page_icon="👋",
)

st.markdown(
    """
    <style>
    .centerized-text {
        text-align: center;
    }
    .centerized-text .text {
        font-size: 30px;
    }
    .centerized-text.large {
        font-size: 50px;
    }
    .centerized-text.title {
        font-size: 60px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<p class='centerized-text title'>COMP90024 Assignment 2</p>", unsafe_allow_html=True)

#st.sidebar.success("Select a demo above.")

st.markdown("<p class='centerized-text large'>Group 83 Members</p>", unsafe_allow_html=True)
st.markdown(
    """
    <p class='centerized-text'>
    <span class='text'>Seth Ng - 1067992</span> <br>
    <span class='text'>Li Sean Wong - 1074679</span> <br>
    <span class='text'>Jason Mack - 993060</span> <br>
    <span class='text'>Chayanit Jaroonsophonsak - 1025399</span> <br>
    <span class='text'>Lu Chen - 1238973</span> <br>
    </p>
    """
    ,unsafe_allow_html=True
)