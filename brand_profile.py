import uuid
import streamlit as st
import json
import os

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "sample_data.json"
)


def load_brands():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        return data.get("brands", [])
    except (json.JSONDecodeError, OSError):
        return []


def save_brands(brands):
    with open(DATA_FILE, "w") as file:
        json.dump({"brands": brands}, file, indent=4)


def show_brand_profile():
    st.header("Brand Profile")
    st.write("Register and manage official brand assets.")

    brands = load_brands()

    if brands:
        st.subheader("Registered Brands")
        for brand in brands:
            st.write("### " + brand["brand_name"])

            logo_filename = brand.get("logo_filename", "")

            if logo_filename:
                logo_path = os.path.join(
                    os.path.dirname(__file__),
                    "data",
                    "logos",
                    logo_filename
                )

                if os.path.isfile(logo_path):
                    st.write("Logo path:", logo_path)
                    st.write("File exists:", os.path.isfile(logo_path))
                    st.image(logo_path, width=150)
                elif brand.get("logo_url"):
                    st.image(brand["logo_url"], width=150)

            elif brand.get("logo_url"):
                st.image(brand["logo_url"], width=150)

            st.json(brand)

            st.subheader("Register a New Brand")

    with st.form("brand_profile_form"):
        brand_name = st.text_input("Brand / Company Name")
        website = st.text_input("Official Website")
        logo_url = st.text_input("Logo URL (optional)")
        logo_file = st.file_uploader(
    "Upload Official Logo (optional)",
    type=["png", "jpg", "jpeg"]
)

        st.subheader("Official Social Media Accounts")
        instagram = st.text_input("Instagram Username or URL")
        facebook = st.text_input("Facebook Page URL")
        linkedin = st.text_input("LinkedIn Page URL")
        other_social = st.text_input("Other Official Account URLs")

        st.subheader("Official Mobile App")
        app_name = st.text_input("Official App Name")
        developer = st.text_input("Official App Developer / Publisher")
        app_description = st.text_area("Official App Description")
        submitted = st.form_submit_button("Register Brand")

        if submitted:
            if not brand_name.strip():
                st.error("Please enter a brand name.")
            else:
                logo_filename = ""

                if logo_file:
                    logo_folder = os.path.join(
                        os.path.dirname(__file__),
                        "data",
                        "logos"
                    )
                    os.makedirs(logo_folder, exist_ok=True)

                    logo_filename = str(uuid.uuid4()) + "_" + logo_file.name
                    logo_path = os.path.join(logo_folder, logo_filename)

                    with open(logo_path, "wb") as file:
                        file.write(logo_file.getbuffer())
                new_brand = {
                    "brand_name": brand_name.strip(),
                    "website": website.strip(),
                    "logo_url": logo_url.strip(),
                    "logo_filename": logo_filename,
                    "social_accounts": {
                        "instagram": instagram.strip(),
                        "facebook": facebook.strip(),
                        "linkedin": linkedin.strip(),
                        "other": other_social.strip()
                    },
                    "official_app": {
                        "name": app_name.strip(),
                        "developer": developer.strip(),
                        "description": app_description.strip()
                    }
                }

                brands.append(new_brand)
                save_brands(brands)

                st.success(
                    "Brand profile saved permanently!"
                )
                st.json(new_brand)
