# ATS-Optimized Resume Builder

A password-protected web application to create ATS (Applicant Tracking System) optimized resumes.

## Features

* 🔒 Password protected access
* 📝 Easy-to-use form interface
* 📄 ATS-optimized resume format
* 💾 Save and preview functionality
* 📥 Download resume as HTML
* 🎨 Clean, professional design

## Installation & Local Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ats-resume-builder.git
cd ats-resume-builder
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

## Changing the Password

The default password is `your_secure_password`. To change it:

1. Open `app.py`
2. Find line 10: `"your_secure_password"`
3. Replace it with your desired password
4. Save the file

## Deployment on Streamlit Cloud

### Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Initialize git in your project folder:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file (app.py)
5. Click "Deploy"

### Step 3: Configure Secrets (Optional - for better security)

Instead of hardcoding the password, you can use Streamlit secrets:

1. In your Streamlit Cloud dashboard, go to your app settings
2. Click on "Secrets"
3. Add:

```toml
password = "your_secure_password"
```

4. Update `app.py` line 10 to:

```python
hashlib.sha256("your_secure_password".encode()).hexdigest()
```

Replace with:

```python
hashlib.sha256(st.secrets["password"].encode()).hexdigest()
```

## Project Structure

```
ats-resume-builder/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Usage

1. Enter the password to access the application
2. Fill in your personal information, work experience, education, skills, projects, and certifications
3. Click "Save Information"
4. Navigate to the "Preview & Download" tab
5. Review your resume and download it as HTML

## ATS Optimization Features

* Clean, simple formatting without complex layouts
* Standard section headings
* No tables, columns, or graphics that confuse ATS
* Professional font (Arial/Helvetica)
* Clear hierarchy with proper heading tags
* Keyword-friendly structure

## Tips for Best Results

1. Use action verbs in your work experience (e.g., "Developed", "Managed", "Led")
2. Include relevant keywords from the job description
3. Quantify achievements with numbers and percentages
4. Keep formatting simple and consistent
5. Use standard section names

## Converting HTML to PDF

To convert your resume to PDF:

1. Open the downloaded HTML file in a web browser
2. Press `Ctrl+P` (Windows) or `Cmd+P` (Mac)
3. Select "Save as PDF" as the destination
4. Adjust margins if needed
5. Save the PDF

## Support

For issues or questions, please open an issue on the GitHub repository.

## License

MIT License - feel free to modify and use for your needs.
