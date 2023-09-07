import streamlit as st
from PIL import Image

#Trick to not init function multitime
if "censor" not in st.session_state:
    print("INIT MODEL")
    from src.censor import Censor
    st.session_state.censor = Censor()
    print("DONE INIT MODEL")

st.set_page_config(page_title="Social Media Censorship", layout="wide", page_icon = "./storage/linhai.jpeg")
hide_menu_style = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html= True)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        margin-left: -400px;
    }
     
    """,
    unsafe_allow_html=True,
)

st.markdown("<h2 style='text-align: center; color: grey;'>Input: Image </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Output: Is the image safe or not?</h2>", unsafe_allow_html=True)
left_col, right_col = st.columns(2)

#LEFT COLUMN
upload_image = left_col.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "webp", ])

if left_col.button("Submit"):
    image, texts, boxes = st.session_state.censor.detect(upload_image, is_local=True)
    left_col.write("**RESULTS:** ")
    if texts:
        color = "red"
        rs = "NOT SAFE"
    else:
        color = "green"
        rs = "SAFE"
    left_col.markdown(f"<h3 style='text-align: left; color: {color};'>{rs} </h3>", unsafe_allow_html=True)
    
    #RIGHT COLUMN
    visualize_image = st.session_state.censor.visualize(image, texts, boxes)
    right_col.write("**ORIGIN IMAGE:** ")
    right_col.image(image)
    right_col.write("**DETECTED IMAGE:** ")
    right_col.image(visualize_image)