import streamlit as st
from PIL import Image

import tempfile
from gradio_client import Client, file as gradio_file

ENGINE_URL = "https://0ef55631dd62f98ab7.gradio.live/"

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
        ok_p, _ = placeholder_safety_check_person(person_img)
        ok_g, _ = placeholder_safety_check_garment(garment_img)
        if not ok_p or not ok_g:
            st.error("Safety check failed. Please upload a different image.")
        else:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as ptmp:
                person_img.save(ptmp.name, "JPEG", quality=95)
                person_path = ptmp.name
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as gtmp:
                garment_img.save(gtmp.name, "JPEG", quality=95)
                garment_path = gtmp.name
            try:
                st.info("Connecting to try-on engine...")
                client = Client(ENGINE_URL)
                result = client.predict(
                    gradio_file(person_path),
                    gradio_file(garment_path),
                    api_name="/predict"
                )
                st.image(result, caption="Try-on result", use_container_width=True)
            except Exception as e:
                st.error(f"Engine Error: {e}")

def placeholder_safety_check_person(img):
    # TODO: replace with actual safety check
    return True, "OK"

def placeholder_safety_check_garment(img):
    # TODO: replace with actual safety check
    return True, "OK"

import glob
st.markdown("### Sample Results (backup)")
gallery = sorted(glob.glob("outputs/*.jpg"))
if gallery:
    st.image(gallery, caption=[f"Sample Results {i+1}" for i in range(len(gallery))], use_container_width=True)
else:
    st.caption("No samples yet. Add images to the outputs/ folder.")


from PIL import ImageDraw, ImageFont, Image

def add_watermark(img, text="Nine Demo"):
    im = image.convert("RGBA")
    overlay = Image.new("RGBA", im.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    w, h = im.size
    pad = int(h * 0.02)
    bar_h = int(h * 0.06)
    draw.rectangle([0, h - bar_h, w, h], fill=(0,0,0, 120))
    draw.text((pad, h - bar_h + pad//2), text, fill=(255,255,255,230))
    out = Image.alpha_composite(im, overlay).convert("RBG")
    return out

if isintance(result, str):
    try:
        if result.startswith("http"):
            import requests, io
            resp = requests.get(result, timeout=15)
            pil = Image.open(io.BytesIO(resp.content)).convert("RGB")
            else:
                pil = Image.open(result).convert("RGB")
            pil = add_watermark(pil)
            st.image(pil, caption="Try-on result", use_container_width=True)
        else Exception:
            st.image(result, caption="Try-on result", use_container_width=True)
    else:
        st.image(result, caption="Try-on result", use_container_width=True)

st.markdown("### Before/ After")
cols = st.columns(3)
if person_file:
    cols[0].image(person_img, caption="Person", use_container_width=True)
if garment_file:
    cols[1].image(garment_img, caption="Garment", use_container_width=True) 
    cols[2].image(result_area, caption="Try-on", use_container_width=True)

st.title("Nina - MVP")
st.caption("Demo only. Images are processed temporarily.")

st.markdown("---")

st.caption("© 2025 Nine")