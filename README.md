# 📄 ATS Resume Builder - Smart Resume Creator

Create professional, ATS-optimized resumes with AI-powered features and get instant job matching scores!

## 🌟 Key Features

* 🔒 **Secure & Private** - Password protected
* 🤖 **Auto-Generate Summary** - Upload your old CV and let AI create a professional summary
* 📸 **Add Your Photo** - Optional profile picture
* 🎯 **Smart ATS Scoring** - See how well you match job descriptions (weighted algorithm)
* 📊 **Detailed Analysis** - Get specific recommendations to improve
* 📥 **Download Ready** - Professional HTML resume

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Download Files

Download these 3 files to a folder on your computer:

* `app.py`
* `requirements.txt`
* `README.md` (this file)

### Step 2: Open Terminal

Open Command Prompt (Windows) or Terminal (Mac/Linux) in your folder

### Step 3: Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Install everything
pip install -r requirements.txt
```

### Step 4: Set Password

Create folder `.streamlit` and file `secrets.toml` inside it:

**File: `.streamlit/secrets.toml`**

```toml
password = "mypassword123"
```

### Step 5: Run!

```bash
streamlit run app.py
```

Browser opens automatically at `http://localhost:8501` 🎉

---

## 💻 How to Use

### Tab 1: Fill Information

#### 1️⃣ Upload Your CV (Optional)

* Click "Upload CV"
* Select PDF, DOCX, or TXT file
* Click "Auto-Generate Summary from CV"
* Edit the generated summary as needed

#### 2️⃣ Add Your Details

* **Personal Info** : Name, email, phone, location
* **Photo** : Upload your professional headshot (optional)
* **Links** : LinkedIn, GitHub, Portfolio
* **Work Experience** : Add all your jobs
* **Education** : Add your degrees
* **Skills** : List technical skills (comma-separated)

#### 3️⃣ Fixed Entries (Already Included)

* ✅ AI/ML Project automatically added
* ✅ Professional Certificate in AI automatically added
* You can add more certifications if needed

#### 4️⃣ Save

Click "💾 Save Information"

### Tab 2: ATS Analysis 🎯

#### What You'll Get:

1. **Overall Score** (0-100%)
   * 85-100%: 🏆 Top Tier
   * 70-84%: ✅ Strong
   * 60-69%: ⚠️ Average
   * Below 60%: ❌ Needs Work
2. **Score Breakdown**
   * Keywords Match (40 points)
   * Technical Skills (25 points)
   * Key Phrases (20 points)
   * Action Verbs (10 points)
   * Format (5 points)
3. **What It Shows**
   * Matched keywords & skills
   * Missing important terms
   * Specific improvements needed
   * Industry benchmark comparison

#### How to Use:

1. Copy entire job description from job posting
2. Paste it in the text box
3. Click "📊 Calculate ATS Score"
4. Review your results
5. Follow recommendations
6. Update your resume
7. Check score again!

### Tab 3: Preview & Download 👁️

* See your final resume
* Download as HTML
* Convert to PDF using browser (Ctrl+P → Save as PDF)

---

## 📊 Understanding Your ATS Score

### Score Components:

**Keywords (40 points)**

* Matches important words from job description
* More matches = higher score

**Technical Skills (25 points)**

* Identifies tech skills: Python, AWS, React, etc.
* Important for tech jobs

**Key Phrases (20 points)**

* Matches 2-word phrases like "machine learning"
* Shows deeper relevance

**Action Verbs (10 points)**

* Finds strong words: Developed, Led, Managed
* Shows achievements

**Format (5 points)**

* Our template is always ATS-friendly ✅

### Quality Checks:

* ✅ Contact info complete
* ✅ Numbers & metrics used
* ✅ Action verbs present
* ✅ Technical skills listed

---

## 🎯 Tips for Best Results

### Do's ✅

* **Use keywords from job description** - Copy exact terms
* **Add numbers** - "Increased sales by 25%"
* **Start with action verbs** - "Developed", "Led", "Created"
* **Match exact phrases** - If job says "machine learning", use that
* **List all relevant skills** - Don't be modest!

### Don'ts ❌

* Don't use creative section names
* Don't add tables or graphics
* Don't stuff keywords unnaturally
* Don't lie about skills
* Don't use fancy fonts

### ATS Optimization Checklist:

* [ ] Keywords from job description included
* [ ] Technical skills listed
* [ ] Quantifiable achievements (numbers)
* [ ] Action verbs in experience
* [ ] Standard section headings
* [ ] Simple, clean format
* [ ] Contact info complete

---

## 🌐 Deploy Online (Streamlit Cloud)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "ATS Resume Builder"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### Step 2: Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Click "Deploy"

### Step 3: Add Password

1. Go to app Settings → Secrets
2. Add:

```toml
password = "your_secure_password"
```

3. Save

Done! Share the URL with anyone 🎉

---

## 🔧 Troubleshooting

### "streamlit not found"

```bash
venv\Scripts\activate
pip install streamlit
```

### "Module not found: PyPDF2"

```bash
pip install -r requirements.txt
```

### "Secrets not found"

* Create `.streamlit` folder
* Create `secrets.toml` file inside
* Add: `password = "yourpassword"`

### Password not working

* Check spelling in `secrets.toml`
* No extra spaces
* Password is case-sensitive
* Restart app after changes

### CV upload fails

* File must be PDF, DOCX, or TXT
* Try a different file
* Check file isn't corrupted

### Photo not showing

* Use JPG, JPEG, or PNG
* Keep file size under 5MB
* Try a different image

---

## 📁 What You Need

### Required Files:

```
your-folder/
├── .streamlit/
│   └── secrets.toml       (password here)
├── app.py                 (main code)
└── requirements.txt       (dependencies)
```

### Dependencies (auto-installed):

* streamlit - Web framework
* PyPDF2 - Read PDFs
* python-docx - Read Word files
* Pillow - Handle images

---

## 💡 Pro Tips

### Get Higher ATS Scores:

1. **Copy-paste keywords** from job description
2. **Use exact job title** if you have similar experience
3. **Mirror the language** used in posting
4. **Add all relevant skills** - even if you only used them once
5. **Quantify everything** - Turn "improved process" into "improved process by 30%"

### For Different Jobs:

* Create different versions of your resume
* Customize keywords for each application
* Test each version with job description
* Aim for 75%+ match

### Converting to PDF:

1. Download HTML resume
2. Open in Chrome/Firefox
3. Press Ctrl+P (Cmd+P on Mac)
4. Select "Save as PDF"
5. Set margins to "Minimum"
6. Uncheck "Headers and footers"
7. Save as: FirstName_LastName_Resume.pdf

---

## 🆕 What's New in Version 2.0

### Upgraded ATS Scoring ⭐

* **Weighted algorithm** (not just word counting)
* **Technical skills recognition** (35+ skills)
* **Phrase matching** (understands context)
* **Action verb detection** (finds strong words)
* **Quality checks** (metrics, contact info)
* **Detailed breakdown** (see exactly where you stand)
* **Smart recommendations** (specific improvements)
* **Industry benchmarks** (compare to others)

### Other Features:

* CV upload & auto-summary
* Profile photo support
* Fixed project & certification entries
* Centered header design
* Better formatting

---

## 📞 Need Help?

### Common Questions:

**Q: Is my data private?**
A: Yes! Everything runs on your computer locally, or on your own Streamlit deployment.

**Q: Can I use this for free?**
A: Yes! Completely free and open source.

**Q: How accurate is the ATS score?**
A: It's a good guide (uses weighted algorithm), but real company ATS systems may vary. Use it as one tool among many.

**Q: Can I share this with others?**
A: Yes! Deploy it and share the URL + password.

**Q: How do I change the password?**
A: Edit `.streamlit/secrets.toml` locally, or update Secrets in Streamlit Cloud settings.

---

## 🎓 Learn More

### Recommended Tools:

* [Jobscan](https://www.jobscan.co/) - Professional ATS checker
* [Resume Worded](https://resumeworded.com/) - AI feedback
* [Grammarly](https://www.grammarly.com/) - Check grammar

### Useful Resources:

* [ATS Resume Tips](https://www.jobscan.co/blog/ats-resume/)
* [Action Verbs List](https://www.themuse.com/advice/185-powerful-verbs-that-will-make-your-resume-awesome)
* [Resume Writing Guide](https://www.indeed.com/career-advice/resumes-cover-letters/how-to-make-a-resume)

---

## 📝 License

Free to use and modify (MIT License)

---

## 🙌 Quick Reference Commands

```bash
# First time setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run app
streamlit run app.py

# Stop app
Ctrl+C

# Exit virtual environment
deactivate

# Deploy updates
git add .
git commit -m "updates"
git push
```

---

**Made with ❤️ for job seekers**

**Good luck with your applications! 🚀**

---

*Questions? Issues? Feedback? Open an issue on GitHub or contact us!*
