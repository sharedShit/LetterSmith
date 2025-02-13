import io
import streamlit as st
import time
from utils import generate_cover_letter_new
import PyPDF2

st.set_page_config(page_title="AI Cover Letter Generator", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state variables
if "current_page" not in st.session_state:
    st.session_state.current_page = "upload"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_text" not in st.session_state:
    st.session_state.job_text = ""
if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "ai_processing" not in st.session_state:
    st.session_state.ai_processing = False
if "ai_regenerating" not in st.session_state:
    st.session_state.ai_regenerating = False

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file using PyPDF2."""
    try:
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
        extracted_text = ""

        # Loop through all pages and extract text
        for page in pdf_reader.pages:
            extracted_text += page.extract_text() + "\n"

        if not extracted_text.strip():
            st.warning(f"⚠️ No extractable text found in {uploaded_file.name}. It may be a scanned or image-based PDF.")
            return ""

        return extracted_text.strip()
    
    except Exception as e:
        return f"❌ Error extracting text: {str(e)}"



# Function to simulate AI-based editing
def edit_with_ai(user_instruction, current_text):
    time.sleep(5)  # Simulate AI processing time
    return f"✍️ AI Edit: {user_instruction} \n\n{current_text}"

### ✅ UPLOAD PAGE
if st.session_state.current_page == "upload":
    st.title("📄 Upload Your Resume & Job Description")
    
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
    
    if st.button("Process Documents"):
        if resume_file and job_file:
            with st.spinner("🔄 Extracting text from PDFs... Please wait."):
                resume_text = extract_text_from_pdf(resume_file)
                job_text = extract_text_from_pdf(job_file)
                
                
            if not resume_text.strip() or not job_text.strip() :
                st.error("❌ The PDF has no extractable text! Please upload a text-based PDF.")
            else :    

                with st.spinner("🤖 Generating AI cover letter... Please wait."):
                    generated_text = generate_cover_letter_new( job_text,resume_text)

                # Store results & move to edit page
                st.session_state.resume_text = resume_text
                st.session_state.job_text = job_text
                st.session_state.generated_text = generated_text
                st.session_state.current_page = "edit"
                st.rerun()
        else:
            st.error("❌ Please upload both resume and job description.")

### ✅ EDIT PAGE (After Cover Letter Generation)
elif st.session_state.current_page == "edit":
    st.title("✍️ Edit Your AI-Generated Cover Letter")

    # Copy Button
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.subheader("Your AI-Generated Cover Letter")
    with col2:
        c1,c2 = st.columns([0.2,0.1])
        with c1:
            if st.button("📋", help="Copy to clipboard"):
                st.session_state.copied_text = st.session_state.generated_text
                st.toast("Text copied successfully!", icon="✅")
        with c2 :        
            if st.button("Regenerate Cover Letter", help="Regenerate Cover Letter"):
                st.session_state.ai_regenerating = True
                st.rerun()

    # Show AI processing message in text area
    text_area_content = "🤖 AI is refining your cover letter... Please wait." if st.session_state.ai_processing else st.session_state.generated_text
    text_area_content = "🤖 AI is regenerating your cover letter... Please wait." if st.session_state.ai_regenerating else st.session_state.generated_text
    edited_text = st.text_area("Modify the cover letter as needed:", text_area_content, height=300)

    # Input + Button in a Single Row
    # col1, col2 = st.columns([0.8, 0.2])
    # with col1:
    #     user_instruction = st.text_input("Need AI Assistance? Enter Instructions Below:")
    # with col2:
    #     if st.button("✏️ Edit with AI"):
    #         st.session_state.ai_processing = True
    #         st.rerun()

    # Process AI Edit
    # if st.session_state.ai_processing:
    #     with st.spinner("🤖 AI is refining your cover letter... Please wait."):
    #         new_text = edit_with_ai(user_instruction, edited_text)
    #         st.session_state.generated_text = new_text  # Update text
    #         st.session_state.ai_processing = False  # Reset flag
    #     st.rerun()  # Refresh UI


    if st.session_state.ai_regenerating:
        with st.spinner("🤖 AI is regenerating your cover letter... Please wait."):
            generated_text = generate_cover_letter_new( st.session_state.job_text,st.session_state.resume_text)
            print("working",st.session_state.resume_text)
            st.session_state.generated_text = generated_text
            st.session_state.ai_regenerating = False  # Reset flag
            
        st.rerun()  # Refresh UI