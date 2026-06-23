import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

# ==========================================
# HELPER FUNCTION (The Engine)
# ==========================================
def process_images(files, sizes_dict, output_format, crop_method, compression_level):
    zip_buffer = io.BytesIO()
    
    # Map the UI toggle to actual quality percentages
    quality_map = {
        "High": 95,
        "Medium": 80,
        "Low": 60
    }
    q_val = quality_map[compression_level]
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for uploaded_file in files:
            img = Image.open(uploaded_file)
            original_name = uploaded_file.name.rsplit('.', 1)[0]
            
            # Format conversions (handles transparency cleanly)
            if output_format.upper() in ('JPG', 'JPEG', 'GIF'):
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert("RGBA") # Standardizes to alpha channel
                    background = Image.new('RGB', img.size, (255, 255, 255)) # Fills transparent with white
                    background.paste(img, mask=img.split()[3]) 
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
            elif output_format.upper() == 'PNG':
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

            # Process each requested size
            for label, size in sizes_dict.items():
                if crop_method == "Crop from Center":
                    resized_img = ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                elif crop_method == "Crop from Top":
                    resized_img = ImageOps.fit(img, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.0))
                elif crop_method == "Fit (No Crop, Add Padding)":
                    pad_color = (255, 255, 255, 0) if output_format.upper() == 'PNG' else (255, 255, 255)
                    resized_img = ImageOps.pad(img, size, method=Image.Resampling.LANCZOS, color=pad_color)
                
                img_buffer = io.BytesIO()
                save_format = "JPEG" if output_format.upper() in ("JPG", "JPEG") else output_format.upper()
                
                # Apply ImageOptim-style compression
                if save_format == "JPEG":
                    resized_img.save(img_buffer, format=save_format, quality=q_val, optimize=True)
                elif save_format == "PNG":
                    resized_img.save(img_buffer, format=save_format, optimize=True)
                else:
                    resized_img.save(img_buffer, format=save_format, optimize=True)
                
                # File Naming Convention: size_originalname.ext
                ext = output_format.lower()
                new_filename = f"{label}_{original_name}.{ext}"
                zip_file.writestr(new_filename, img_buffer.getvalue())
                
    return zip_buffer.getvalue()

# ==========================================
# UI LAYOUT (Tabs at the Absolute Top)
# ==========================================
st.set_page_config(page_title="Agency Image Optimizer", page_icon="🖼️", layout="wide")

st.title("🚀 Agency Media Optimizer")
st.write("Select a client tab below, adjust your individual settings, drop your images, and click generate.")

# The 6 specific tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎨 create digital", 
    "🎖️ RSL NSW", 
    "🤝 AHRI", 
    "⚕️ PSA", 
    "💳 Adyen", 
    "🖥️ Online Digital Banners"
])

# ==========================================
# 1. create digital TAB
# ==========================================
with tab1:
    st.subheader("create digital")
    
    # Settings row cleanly boxed inside the tab
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        cd_format = st.radio("Output Format:", ["PNG", "JPG", "GIF"], index=0, horizontal=True, key="fmt_cd")
    with col_set2:
        cd_crop = st.radio("Crop Style:", ["Crop from Center", "Crop from Top", "Fit (No Crop, Add Padding)"], horizontal=True, key="crop_cd")
    with col_set3:
        cd_comp = st.select_slider("Web Compression:", options=["Low", "Medium", "High"], value="High", key="comp_cd")
    
    st.divider()
    
    cd_sizes = {"1540x1080": (1540, 1080), "628x320": (628, 320), "240x165": (240, 165), "500x500": (500, 500)}
    cols1 = st.columns(4)
    cd_selected = {}
    for i, (label, size) in enumerate(cd_sizes.items()):
        with cols1[i % 4]:
            if st.checkbox(label, value=True, key=f"cd_{label}"):
                cd_selected[label] = size
                
    files_cd = st.file_uploader("Upload assets", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="cd_upload")
    
    if files_cd and cd_selected:
        if st.button("Generate 'create digital' Kit", key="btn_cd"):
            zip_data = process_images(files_cd, cd_selected, cd_format, cd_crop, cd_comp)
            st.download_button(f"📥 Download {cd_format} Kit", data=zip_data, file_name="create_digital_Kit.zip", mime="application/zip")

# ==========================================
# 2. RSL NSW TAB
# ==========================================
with tab2:
    st.subheader("RSL NSW")
    
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        rsl_format = st.radio("Output Format:", ["PNG", "JPG", "GIF"], index=1, horizontal=True, key="fmt_rsl")
    with col_set2:
        rsl_crop = st.radio("Crop Style:", ["Crop from Center", "Crop from Top", "Fit (No Crop, Add Padding)"], horizontal=True, key="crop_rsl")
    with col_set3:
        rsl_comp = st.select_slider("Web Compression:", options=["Low", "Medium", "High"], value="High", key="comp_rsl")
    
    st.divider()

    rsl_sizes = {"766x459": (766, 459), "591x394": (591, 394), "1080x1080": (1080, 1080)}
    cols2 = st.columns(3)
    rsl_selected = {}
    for i, (label, size) in enumerate(rsl_sizes.items()):
        with cols2[i % 3]:
            if st.checkbox(label, value=True, key=f"rsl_{label}"):
                rsl_selected[label] = size
                
    files_rsl = st.file_uploader("Upload assets", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="rsl_upload")
    
    if files_rsl and rsl_selected:
        if st.button("Generate 'RSL NSW' Kit", key="btn_rsl"):
            zip_data = process_images(files_rsl, rsl_selected, rsl_format, rsl_crop, rsl_comp)
            st.download_button(f"📥 Download {rsl_format} Kit", data=zip_data, file_name="RSL_NSW_Kit.zip", mime="application/zip")

# ==========================================
# 3. AHRI TAB
# ==========================================
with tab3:
    st.subheader("AHRI")
    
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        ahri_format = st.radio("Output Format:", ["PNG", "JPG", "GIF"], index=1, horizontal=True, key="fmt_ahri")
    with col_set2:
        ahri_crop = st.radio("Crop Style:", ["Crop from Center", "Crop from Top", "Fit (No Crop, Add Padding)"], horizontal=True, key="crop_ahri")
    with col_set3:
        ahri_comp = st.select_slider("Web Compression:", options=["Low", "Medium", "High"], value="High", key="comp_ahri")
    
    st.divider()

    ahri_sizes = {"1400x800": (1400, 800), "600x265": (600, 265), "300x150": (300, 150)}
    cols3 = st.columns(3)
    ahri_selected = {}
    for i, (label, size) in enumerate(ahri_sizes.items()):
        with cols3[i % 3]:
            if st.checkbox(label, value=True, key=f"ahri_{label}"):
                ahri_selected[label] = size
                
    files_ahri = st.file_uploader("Upload assets", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="ahri_upload")
    
    if files_ahri and ahri_selected:
        if st.button("Generate 'AHRI' Kit", key="btn_ahri"):
            zip_data = process_images(files_ahri, ahri_selected, ahri_format, ahri_crop, ahri_comp)
            st.download_button(f"📥 Download {ahri_format} Kit", data=zip_data, file_name="AHRI_Kit.zip", mime="application/zip")

# ==========================================
# 4. PSA TAB
# ==========================================
with tab4:
    st.subheader("PSA")
    
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        psa_format = st.radio("Output Format:", ["PNG", "JPG", "GIF"], index=1, horizontal=True, key="fmt_psa")
    with col_set2:
        psa_crop = st.radio("Crop Style:", ["Crop from Center", "Crop from Top", "Fit (No Crop, Add Padding)"], horizontal=True, key="crop_psa")
    with col_set3:
        psa_comp = st.select_slider("Web Compression:", options=["Low", "Medium", "High"], value="High", key="comp_psa")
    
    st.divider()

    psa_sizes = {"1280x780": (1280, 780), "560x300": (560, 300), "300x250": (300, 250), "560x150": (560, 150)}
    cols4 = st.columns(4)
    psa_selected = {}
    for i, (label, size) in enumerate(psa_sizes.items()):
        with cols4[i % 4]:
            if st.checkbox(label, value=True, key=f"psa_{label}"):
                psa_selected[label] = size
                
    files_psa = st.file_uploader("Upload assets", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="psa_upload")
    
    if files_psa and psa_selected:
        if st.button("Generate 'PSA' Kit", key="btn_psa"):
            zip_data = process_images(files_psa, psa_selected, psa_format, psa_crop, psa_comp)
            st.download_button(f"📥 Download {psa_format} Kit", data=zip_data, file_name="PSA_Kit.zip", mime="application/zip")

# ==========================================
# 5. Adyen TAB
# ==========================================
with tab5:
    st.subheader("Adyen")
    
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        adyen_format = st.radio("Output Format:", ["PNG", "JPG", "GIF"], index=0, horizontal=True, key="fmt_adyen")
    with col_set2:
        adyen_crop = st.radio("Crop Style:", ["Crop from Center", "Crop from Top", "Fit (No Crop, Add Padding)"], horizontal=True, key="crop_adyen")
    with col_set3:
        adyen_comp = st.select_slider("Web Compression:", options=["Low", "Medium", "High"], value="High", key="comp_adyen")
    
    st.divider()

    adyen_sizes = {
        "300x250": (300, 250), "728x90": (728, 90), "300x600": (300, 600), 
        "160x600": (160, 600), "970x250": (970, 250), "336x280": (336, 280), "320x50": (320, 50)
    }
    cols5 = st.columns(4)
    adyen_selected = {}
    for i, (label, size) in enumerate(adyen_sizes.items()):
        with cols5[i % 4]:
            if st.checkbox(label, value=True, key=f"adyen_{label}"):
                adyen_selected[label] = size
                
    files_adyen = st.file_uploader("Upload assets", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="adyen_upload")
    
    if files_adyen and adyen_selected:
        if st.button("Generate 'Adyen' Kit", key="btn_adyen"):
            zip_data = process_images(files_adyen, adyen_selected, adyen_format, adyen_crop, adyen_comp)
            st.download_button(f"📥 Download {adyen_format} Kit", data=zip_data, file_name="Adyen_Kit.zip", mime="application/zip")

# ==========================================
# 6. Online Digital Banners (Internal Tool)
# ==========================================
with tab6:
    st.subheader("Internal: Online Digital Banners")
    
    col_set1, col_set2, col_set3 = st.columns(3)
    with col_set1:
        ban_format = st.radio("Output Format:", ["PNG", "JPG", "GIF"], index=0, horizontal=True, key="fmt_ban")
    with col_set2:
        ban_crop = st.radio("Crop Style:", ["Crop from Center", "Crop from Top", "Fit (No Crop, Add Padding)"], horizontal=True, key="crop_ban")
    with col_set3:
        ban_comp = st.select_slider("Web Compression:", options=["Low", "Medium", "High"], value="High", key="comp_ban")
    
    st.divider()

    banner_sizes = {
        "320x50": (320, 50), "336x280": (336, 280), "728x90": (728, 90), 
        "970x250": (970, 250), "300x600": (300, 600), "300x250": (300, 250), "160x600": (160, 600)
    }
    cols6 = st.columns(4)
    banner_selected = {}
    for i, (label, size) in enumerate(banner_sizes.items()):
        with cols6[i % 4]:
            if st.checkbox(label, value=True, key=f"ban_{label}"):
                banner_selected[label] = size
                
    files_banner = st.file_uploader("Upload assets", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="banner_upload")
    
    if files_banner and banner_selected:
        if st.button("Generate Banner Kit", key="btn_banner"):
            zip_data = process_images(files_banner, banner_selected, ban_format, ban_crop, ban_comp)
            st.download_button(f"📥 Download {ban_format} Kit", data=zip_data, file_name="Digital_Banners_Kit.zip", mime="application/zip")