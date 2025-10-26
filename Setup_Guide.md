# AI-Powered Smart Resume Parser - Setup & Usage Guide

## 📋 Quick Setup Instructions

### Step 1: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_sm
```

### Step 2: Run the Application
```bash
# Start the Streamlit app
streamlit run resume_parser_app.py
```

### Step 3: Access the Application
- The app will automatically open in your default browser
- If not, navigate to: `http://localhost:8501`

## 💻 How to Execute in VS Code

### Complete Execution Steps:

1. **Open VS Code Terminal:**
   - Press `Ctrl + `` (backtick) or Terminal → New Terminal

2. **Navigate to project directory:**
   ```bash
   cd path/to/AI-Powered-Smart-Resume-Parser
   ```

3. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv

   # Activate:
   # Windows:
   venv\Scripts\activate

   # macOS/Linux:
   source venv/bin/activate
   ```

4. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt

   # IMPORTANT: Download spaCy model
   python -m spacy download en_core_web_sm
   ```

5. **Run the application:**
   ```bash
   streamlit run resume_parser_app.py
   ```

6. **Use the application:**
   - Browser will open automatically at http://localhost:8501
   - Upload resume files (PDF or DOCX)
   - Click "Parse Resumes" button
   - View results and export data

7. **For testing with sample resumes:**
   - Use the provided sample resume files in `sample_resumes/` folder
   - Or create your own PDF/DOCX resumes

## 🎯 Usage Tips

### For Best Results:
- Use clear, well-formatted resumes
- Supported formats: PDF and DOCX
- Multiple files can be uploaded at once
- Results are displayed immediately after parsing

### Export Options:
- **CSV**: For spreadsheet analysis
- **JSON**: For programmatic use
- **Excel**: For formatted reports

## 🔧 Troubleshooting

### Common Issues:

**Issue: spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**Issue: Streamlit not opening**
```bash
# Manually open browser and go to:
http://localhost:8501
```

**Issue: PDF extraction error**
- Ensure PyMuPDF is installed correctly
- Check if PDF is not password-protected

**Issue: Import errors**
- Reinstall all requirements:
```bash
pip install --upgrade -r requirements.txt
```

## 📊 Expected Output

After parsing, you will get:
- ✅ Candidate name
- ✅ Email address
- ✅ Phone number
- ✅ List of technical skills
- ✅ Education details
- ✅ Work experience
- ✅ Total years of experience
- ✅ Structured data in table format

## 🚀 Advanced Features

### Batch Processing:
Upload multiple resumes at once for bulk parsing

### Data Export:
Export results in multiple formats for further analysis

### Statistics:
View aggregate statistics across all parsed resumes

### Real-time Processing:
See results as each resume is parsed
