
import json
import streamlit as st

from report import generate_report
from app_monitor import monitor_apps
from brand_profile import show_brand_profile, load_brands
from social_monitor import monitor_social_profiles
if "profiles_reviewed" not in st.session_state:
    st.session_state.profiles_reviewed = 0
if "apps_reviewed" not in st.session_state:
    st.session_state.apps_reviewed = 0
if "app_scan_results" not in st.session_state:
    st.session_state.app_scan_results = []

if "social_scan_results" not in st.session_state:
    st.session_state.social_scan_results = []
st.set_page_config(
    page_title="ThreatLens AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ ThreatLens AI")
st.subheader("Digital Risk Protection Platform")

st.write(
    "Monitor possible fake social media profiles "
    "and suspicious mobile apps."
)

st.info(
    "Prototype mode: This dashboard uses sample data "
    "until approved data sources are connected."
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a module",
    [
        "Dashboard",
        "Brand Profile",
        "Social Media Monitoring",
        "App Store Monitoring",
        "Risk Reports"
    ]
)



if page == "Dashboard":
    st.header("Security Dashboard")

    brands = load_brands()

    col1, col2, col3 = st.columns(3)

    col1.metric("Brands Registered", len(brands))
    col2.metric("Profiles Reviewed", st.session_state.profiles_reviewed)
    col3.metric("Apps Reviewed", st.session_state.apps_reviewed)

    st.write("### Welcome to ThreatLens AI")
    st.write(
        "Register a brand and review possible "
        "look-alike profiles and apps."
    )

    st.info(
        "Monitoring results will appear here after "
        "you scan sample social profiles and app listings."
    )

    st.write("### Project Modules")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Social Media Monitoring")
        st.write("Detect potential fake or look-alike accounts.")

    with col2:
        st.subheader("App Store Monitoring")
        st.write("Identify apps with similar names or publishers.")



elif page == "Brand Profile":
    show_brand_profile()



elif page == "Social Media Monitoring":
    st.header("Social Media Monitoring")
    st.caption(
        "Demo data only. No live accounts are being scanned."
    )

    brands = load_brands()

    if not brands:
        st.info("Please register a brand in Brand Profile first.")
    else:
        brand_profile = st.selectbox(
            "Choose a registered brand",
            brands,
            format_func=lambda brand: brand["brand_name"]
        )

        brand_name = brand_profile["brand_name"]
        brand_key = "".join(
            character.lower()
            for character in brand_name
            if character.isalnum()
        )

        sample_profiles = [
            {
                "name": brand_name,
                "username": "@" + brand_key + "official1",
                "platform": "Instagram",
                "url": "https://example.com/" + brand_key + "official1"
            },
            {
                "name": brand_name + " Customer Support",
                "username": "@" + brand_key + "_help",
                "platform": "Instagram",
                "url": "https://example.com/" + brand_key + "_help"
            },
            {
                "name": "Random Store",
                "username": "@randomstore",
                "platform": "Instagram",
                "url": "https://example.com/random"
            }
        ]
        

       
        if st.button("Scan Sample Profiles"):
            st.session_state.profiles_reviewed += len(sample_profiles)

            findings = monitor_social_profiles(
                brand_profile, sample_profiles
            )
            st.session_state.social_scan_results = findings

            st.subheader("Monitoring Results")
            st.write("Sample profiles reviewed:", len(sample_profiles))

            if findings:
                for profile in findings:
                    st.write("---")
                    st.write("**Name:**", profile["name"])
                    st.write("**Username:**", profile["username"])

                    st.write(
                        "**Name similarity:**",
                        str(profile.get("name_similarity", 0)) + "%"
                    )

                    st.write(
                        "**Username similarity:**",
                        str(profile.get("username_similarity", 0)) + "%"
                    )
                    st.write(
                        "**Risk score:**",
                        str(profile["risk_score"]) + "/100"
                    )
                    st.write("**Risk level:**", profile["risk_level"])
                    st.write(
                        "**Reasons:**",
                        ", ".join(profile["reasons"])
                    )

                    if profile["risk_level"] == "High":
                        st.error("High-risk indicators detected. Review this profile.")
                    elif profile["risk_level"] == "Medium":
                        st.warning("Potential risk detected. Further review is recommended.")
                    else:
                        st.success("Low risk based on current rules.")
            else:
                st.info("No findings returned.")





elif page == "App Store Monitoring":
    st.header("App Store Monitoring")

    brands = load_brands()

    if not brands:
        st.info("Register a brand profile first.")
    else:
        brand_profile = st.selectbox(
            "Choose a registered brand",
            brands,
            format_func=lambda brand: brand["brand_name"]
        )

        official_app = brand_profile.get("official_app", {})

        app_listings = [
            {
                "name": official_app.get("name", ""),
                "developer": "Unknown Developer",
                "description": "Shop products online, compare prices, explore new arrivals, and track orders.",
                "store": "Sample data",
                "url": ""
            },
            {
                "name": brand_profile["brand_name"] + " Customer Support",
                "developer": "Unknown Developer",
                "description": "Get help with your account and shopping orders.",
                "store": "Sample data",
                "url": ""
            }
        ]

        if st.button("Scan Sample Apps"):
            st.session_state.apps_reviewed += len(app_listings)

            findings = monitor_apps(brand_profile, app_listings)

            existing = st.session_state.app_scan_results

            for item in findings:
                item = dict(item)
                item["brand_checked"] = brand_profile["brand_name"]

                existing = [
                    old for old in existing
                    if not (
                        old.get("brand_checked") == item["brand_checked"]
                        and old.get("name") == item.get("name")
                    )
                ]

                existing.append(item)

            st.session_state.app_scan_results = existing

            if findings:
                st.write("### Potentially suspicious apps")

                for app in findings:
                    st.warning(
                        f"**{app.get('name', 'Unknown app')}** — "
                        f"risk score: {app.get('risk_score', 0)}/100"
                    )
                    st.write(
                        "Risk level: " + app.get("risk_level", "Unknown")
                    )
                    st.write(
                        "Reasons: " + ", ".join(app.get("reasons", []))
                    )
            else:
                st.success(
                    "No suspicious apps found in the current sample listings."
                )



elif page == "Risk Reports":
    st.header("Risk Reports")
    st.write("Generate a report from the latest scan results.")

    if "app_scan_results" not in st.session_state:
        st.session_state.app_scan_results = []

    if "social_scan_results" not in st.session_state:
        st.session_state.social_scan_results = []

    app_results = st.session_state.app_scan_results
    social_results = st.session_state.social_scan_results

    all_results = []

    for item in app_results:
        result = dict(item)
        result["scan_type"] = "Mobile App"
        all_results.append(result)

    for item in social_results:
        result = dict(item)
        result["scan_type"] = "Social Profile"
        all_results.append(result)

    if not all_results:
        st.info(
            "No scan results available yet. "
            "Run a scan in Social Media Monitoring or "
            "App Store Monitoring first."
        )
    else:
        flagged_count = sum(
            1 for item in all_results
            if item.get("risk_level") in ("Medium", "High")
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Items Scanned", len(all_results))
        col2.metric("Items Flagged", flagged_count)
        col3.metric(
            "Low Risk",
            sum(
                1 for item in all_results
                if item.get("risk_level") == "Low"
            )
        )

        st.subheader("Scan Results")
        st.dataframe(all_results, use_container_width=True)

        if st.button("Generate Report"):
            report_data = generate_report(all_results)

            st.success("Report generated successfully!")
            st.json(report_data)

            report_json = json.dumps(
                report_data,
                indent=4,
                ensure_ascii=False
            )

            st.download_button(
                label="Download JSON Report",
                data=report_json,
                file_name="threatlens_risk_report.json",
                mime="application/json"
            )
