"""
AI-Powered Smart Resume Parser
==============================
Advanced resume parsing system using NLP, spaCy, and machine learning
Author: Awais Syed
Email: awaissyed1212@gmail.com
Technologies: Python, spaCy, PyMuPDF, python-docx, Streamlit, AI/ML
"""

import streamlit as st
import pymupdf  # PyMuPDF for PDF extraction
import docx
import re
import json
import pandas as pd
from datetime import datetime
import spacy
from collections import Counter
import os
import io  # ✅ Added for Excel export fix


# Load spaCy model for NLP
@st.cache_resource
def load_spacy_model():
    """Load spaCy English model for NER and text processing"""
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        st.error("Please install spaCy model: python -m spacy download en_core_web_sm")
        nlp = None
    return nlp


class ResumeParser:
    """Advanced AI-powered resume parser with NLP capabilities"""

    def __init__(self):
        self.nlp = load_spacy_model()

        # Common skills keywords
        self.technical_skills = {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'swift',
            'kotlin', 'go', 'rust', 'scala', 'sql', 'mongodb', 'postgresql', 'mysql', 'oracle',
            'react', 'angular', 'vue', 'nodejs', 'django', 'flask', 'spring', 'fastapi',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'docker',
            'kubernetes', 'aws', 'azure', 'gcp', 'git', 'jenkins', 'machine learning',
            'deep learning', 'nlp', 'data science', 'artificial intelligence'
        }

        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'[+]*[\d\s().-]{7,}')

    # --- Text Extraction ---
    def extract_text_from_pdf(self, pdf_file):
        try:
            doc = pymupdf.open(stream=pdf_file.read(), filetype="pdf")
            text = "".join([page.get_text() for page in doc])
            doc.close()
            return text
        except Exception as e:
            st.error(f"Error extracting PDF: {e}")
            return ""

    def extract_text_from_docx(self, docx_file):
        try:
            doc = docx.Document(docx_file)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")
            return ""

    # --- Core Extraction Methods ---
    def extract_name(self, text):
        if not self.nlp:
            return "Name Not Found"
        doc = self.nlp(text[:500])
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        return names[0] if names else "Name Not Found"

    def extract_email(self, text):
        emails = self.email_pattern.findall(text)
        return emails[0] if emails else "Email Not Found"

    def extract_phone(self, text):
        phones = self.phone_pattern.findall(text)
        return phones[0] if phones else "Phone Not Found"

    def extract_skills(self, text):
        text_lower = text.lower()
        found = [s.capitalize() for s in self.technical_skills if s in text_lower]
        return list(set(found))[:20] if found else ["No skills found"]

    def extract_education(self, text):
        degrees = re.findall(r'(?i)(bachelor|master|phd|mba|b\.tech|m\.tech|b\.sc|m\.sc|degree)', text)
        return list(set(degrees)) if degrees else ["Education details not found"]

    def extract_experience(self, text):
        exp_section = re.findall(r'(?i)(experience|employment history|work experience)(.*?)(education|skills|projects|$)', text, re.S)
        if exp_section:
            exp_text = exp_section[0][1][:800]
            entries = [line.strip() for line in exp_text.split("\n") if len(line.strip()) > 30]
            return entries[:3]
        return ["Work experience not specified"]

    def calculate_experience_years(self, text):
        year_ranges = re.findall(r'(20\d{2})\s*[-–]\s*(20\d{2}|present|current)', text.lower())
        total_years = 0
        for start, end in year_ranges:
            start = int(start)
            end = datetime.now().year if "present" in end or "current" in end else int(end)
            total_years += max(0, end - start)
        return total_years if total_years else "Not Specified"

    # --- Parse Resume ---
    def parse_resume(self, file, filename):
        if filename.endswith('.pdf'):
            text = self.extract_text_from_pdf(file)
        elif filename.endswith('.docx'):
            text = self.extract_text_from_docx(file)
        else:
            st.error("Unsupported file format")
            return None

        if not text:
            st.error("Could not extract text")
            return None

        return {
            "Filename": filename,
            "Name": self.extract_name(text),
            "Email": self.extract_email(text),
            "Phone": self.extract_phone(text),
            "Skills": self.extract_skills(text),
            "Education": self.extract_education(text),
            "Experience": self.extract_experience(text),
            "Total Experience (Years)": self.calculate_experience_years(text),
            "Parsed Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


# --- Streamlit App ---
def main():
    st.set_page_config(page_title="AI Resume Parser", layout="wide")

    st.title("🤖 AI-Powered Smart Resume Parser")
    st.subheader("Extract key information from resumes using AI & NLP")
    st.markdown("---")

    parser = ResumeParser()
    if not parser.nlp:
        return

    uploaded_files = st.file_uploader(
        "📤 Upload Resume Files (PDF or DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("🚀 Parse Resumes"):
        all_data = []
        prog = st.progress(0)
        for i, file in enumerate(uploaded_files):
            data = parser.parse_resume(file, file.name)
            if data: all_data.append(data)
            prog.progress((i + 1) / len(uploaded_files))

        if all_data:
            st.success(f"✅ Parsed {len(all_data)} resumes successfully!")

            df = pd.DataFrame(all_data)
            st.subheader("📊 Parsed Resume Data")
            st.dataframe(df)

            st.markdown("---")
            st.subheader("💾 Export Options")

            # CSV Export
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="parsed_resumes.csv",
                mime="text/csv"
            )

            # JSON Export
            json_str = json.dumps(all_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name="parsed_resumes.json",
                mime="application/json"
            )

            # ✅ FIXED Excel Export
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            excel_buffer.seek(0)

            st.download_button(
                label="📥 Download Excel",
                data=excel_buffer,
                file_name="parsed_resumes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.markdown("---")
            st.subheader("📈 Statistics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Resumes Parsed", len(all_data))
            avg_skills = sum(len(d["Skills"]) for d in all_data) / len(all_data)
            col2.metric("Avg Skills", f"{avg_skills:.1f}")
            col3.metric("Emails Found", sum('Email Not Found' not in d["Email"] for d in all_data))


if __name__ == "__main__":
    main()
