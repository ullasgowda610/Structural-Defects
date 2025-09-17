import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt
from io import BytesIO

# --- Config ---
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

st.set_page_config(
    page_title="Structural Defect Identifier 🏗",
    page_icon="🛠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Background + Styling ---
page_bg = """
<style>
/* Background with gradient overlay */
.stApp {
    background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                url("https://images.unsplash.com/photo-1581092795360-6c12f39ecdc4?auto=format&fit=crop&w=1400&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Main title styling */
h1 {
    color: #1E3D59;
    font-weight: bold;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(240, 248, 255, 0.9);
    border-right: 2px solid #ccc;
}

/* Report box styling */
.report-box {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
    font-size: 16px;
    line-height: 1.6;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("📂 Upload Section")
uploaded_image = st.sidebar.file_uploader("Upload a structure image", type=["jpeg", "jpg", "png"])
if uploaded_image:
    st.sidebar.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

# --- Main Header ---
st.markdown(
    """
    <div style="text-align:center; padding:15px;">
        <h1>🏗 AI-Assisted Structural Defect Identifier</h1>
        <p style="font-size:18px; color:#444;">
            Upload an image of a structure and generate a professional defect report instantly.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Instructions ---
with st.expander("📘 How to use this app"):
    st.markdown(
        """
        1. *Upload an image* of the structure from the sidebar  
        2. Fill in the *report details* (title, prepared by, prepared for)  
        3. Click *Generate Report*  
        4. Review your report and *download it*  
        """
    )

# --- Report Inputs ---
rep_title = st.text_input("📑 Report Title", "")
prep_by = st.text_input("👷 Report Prepared by", "")
prep_for = st.text_input("🏢 Report Prepared for", "")

# --- Prompt Builder ---
prompt = f"""
Assume you are a structural engineer. The user has provided an image of a structure. 
You need to identify the structural defects in the image and generate a report.

The report must contain:
- Title: {rep_title}
- Prepared by: {prep_by}
- Prepared for: {prep_for}
- Date: {dt.datetime.now().date()}

Instructions:
* Identify and classify each defect (crack, spalling, corrosion, honeycombing, etc.)
* Provide a description and potential impact of each defect
* Rate severity (Low / Medium / High)
* Estimate time before permanent damage
* Suggest short-term and long-term solutions with estimated *costs (₹)* and time
* Provide preventive measures
* Use bullet points and tables where possible
* Keep report ≤ 3 pages
"""

# --- Report Generation ---
if st.button("🚀 Generate Report"):
    if uploaded_image is None:
        st.error("⚠ Please upload an image first.")
    else:
        with st.spinner("⏳ Analyzing image and preparing report..."):
            response = model.generate_content([prompt, Image.open(uploaded_image)])
            report_text = response.text

        st.success("✅ Report generated successfully!")
        st.balloons()

        # Show report inside styled box
        st.markdown("### 📄 Generated Report")
        st.markdown(f"<div class='report-box'>{report_text}</div>", unsafe_allow_html=True)

        # --- Download Option ---
        buffer = BytesIO()
        buffer.write(report_text.encode("utf-8"))
        buffer.seek(0)

        st.download_button(
            label="💾 Download PDF Report",
            data=buffer,
            file_name=f"Structural_Report_{dt.datetime.now().date()}.pdf",
            mime="application/pdf"
        )