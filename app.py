import streamlit as st
from PIL import Image

st.set_page_config(page_title="NINE (MVP Demo)", page_icon=":eyes:", layout="centered")

st.title("NINE (MVP Demo)")
st.caption("Upload your own photo and a clohting image. This is a private demo preview.")

with st.expander("Consent & Terms (Required)"):
    st.write("""
    **By uploading, you confirm:**
    - You own the rights to the photo(s) or have permission from the person depicted.
    - You consent to processing the images for a virtual try-on demo.
    - You will not upload images of minors, celebrities, unsafe content, or copyrighted material.

    *(In the full-MVP, images auto-delete within 24 hours and pass safety checks)*
    """)

consent = st.checkbox ("I agree to the terms above and consent to processing", value=False)

col1, col2 = st.columns(2, gap="large")

with col1:
    person_file = st.file_uploader("Upload Person's image (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if person_file:
        person_img = Image.open(person_file).convert("RGB")
        st.image(person_img, caption="Person's image preview", use_container_width=True)

with col2:
    garment_file = st.file_uploader("Upload Garment Image (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if garment_file:
        garment_img = Image.open(garment_file).convert("RGB")
        st.image(garment_img, caption="Garment image preview", use_container_width=True)

st.markdown("---")

generate = st.button("Generate Try-On")

result_area = st.empty()

if generate:
    if not consent:
        st.error("Please check the consent box before continuing.")
    elif not person_file or not garment_file:
        st.error("Please upload both person's image and garment image.")
    else:
        st.info("This is a placeholder. The AI engine will be connected soon.")
        result_area.image(person_img, caption="(Placeholder) Try-On image will appear here", use_container_width=True)


def placeholder_safety_check_person(img):
    # TODO: replace with actual safety check
    return True, "OK"

def placeholder_safety_check_garment(img):
    # TODO: replace with actual safety check
    return True, "OK"


if generate:
    if not consent:
        st.error("Please check the consent box before continuing.")
    elif not person_file or not garment_file:
        st.error("Please upload both person's image and garment image.")
    else:
        ok_p, _ = placeholder_safety_check_person(person_img)
        ok_g, _ = placeholder_safety_check_garment(garment_img)
        if not ok_p or not ok_g:
            st.error("Safety check failed. Please upload a different image.")
        else:
            st.info("PlceholderL try-on engine will be connected soon.")
            st.image(person_img, caption="(Placeholder) Result will appear here", use_container_width=True)






st.markdown("---")

st.caption("© 2025 Nine")