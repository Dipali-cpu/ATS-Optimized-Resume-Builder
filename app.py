import streamlit as st
from datetime import datetime
import hashlib
import json
import re
from io import BytesIO
import base64

# Password protection
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == hashlib.sha256(st.secrets["password"].encode()).hexdigest():
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Main application
st.set_page_config(page_title="ATS Resume Builder", page_icon="📄", layout="wide")

st.title("📄 ATS-Optimized Resume Builder")
st.markdown("Fill in your information to generate an ATS-friendly resume")

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {}
if 'photo_data' not in st.session_state:
    st.session_state.photo_data = None
if 'cv_text' not in st.session_state:
    st.session_state.cv_text = ""

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Fill Information", "🎯 ATS Analysis", "👁️ Preview & Download"])

with tab1:
    # CV Upload for Auto-generate Summary
    st.header("📄 Upload Existing CV (Optional)")
    st.markdown("Upload your existing CV to auto-generate professional summary")
    
    uploaded_cv = st.file_uploader("Upload CV (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])
    
    if uploaded_cv is not None:
        try:
            if uploaded_cv.type == "text/plain":
                st.session_state.cv_text = uploaded_cv.read().decode('utf-8')
            elif uploaded_cv.type == "application/pdf":
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_cv)
                st.session_state.cv_text = ""
                for page in pdf_reader.pages:
                    st.session_state.cv_text += page.extract_text()
            elif uploaded_cv.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                import docx
                doc = docx.Document(uploaded_cv)
                st.session_state.cv_text = "\n".join([para.text for para in doc.paragraphs])
            
            st.success("✅ CV uploaded successfully!")
            with st.expander("View extracted text"):
                st.text_area("Extracted CV Text", st.session_state.cv_text, height=200)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    st.header("Personal Information")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        full_name = st.text_input("Full Name*", key="name")
        email = st.text_input("Email*", key="email")
        phone = st.text_input("Phone Number*", key="phone")
        location = st.text_input("Location (City, State)", key="location")
        
    with col2:
        st.markdown("#### Upload Photo")
        photo = st.file_uploader("Profile Photo (Optional)", type=['jpg', 'jpeg', 'png'])
        if photo:
            st.session_state.photo_data = photo.read()
            st.image(st.session_state.photo_data, width=150)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        linkedin = st.text_input("LinkedIn URL", key="linkedin")
    with col2:
        github = st.text_input("GitHub URL", key="github")
    with col3:
        portfolio = st.text_input("Portfolio/Website", key="portfolio")
    
    st.header("Professional Summary")
    
    # Auto-generate button
    if st.session_state.cv_text:
        if st.button("🤖 Auto-Generate Summary from CV"):
            with st.spinner("Generating professional summary..."):
                # Simple extraction logic (you can enhance this)
                lines = st.session_state.cv_text.split('\n')
                summary_keywords = ['summary', 'profile', 'objective', 'about']
                extracted_summary = ""
                
                for i, line in enumerate(lines):
                    if any(keyword in line.lower() for keyword in summary_keywords):
                        # Get next few lines as summary
                        extracted_summary = ' '.join(lines[i+1:i+4])
                        break
                
                if extracted_summary:
                    st.session_state['summary_text'] = extracted_summary[:300]
                else:
                    st.session_state['summary_text'] = "Experienced professional with strong skills in various domains."
                st.success("✅ Summary generated! You can edit it below.")
    
    summary = st.text_area("Professional Summary (2-3 sentences)*", 
                          value=st.session_state.get('summary_text', ''),
                          height=100, key="summary")
    
    st.header("Work Experience")
    num_experiences = st.number_input("Number of work experiences", min_value=0, max_value=10, value=1)
    
    experiences = []
    for i in range(num_experiences):
        st.subheader(f"Experience {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input(f"Job Title*", key=f"job_title_{i}")
            company = st.text_input(f"Company Name*", key=f"company_{i}")
        with col2:
            start_date = st.text_input(f"Start Date (e.g., Jan 2020)*", key=f"start_{i}")
            end_date = st.text_input(f"End Date (e.g., Dec 2022 or Present)*", key=f"end_{i}")
        
        responsibilities = st.text_area(f"Key Responsibilities & Achievements (one per line)*", 
                                       height=100, key=f"resp_{i}")
        
        if job_title and company and start_date and end_date:
            experiences.append({
                "title": job_title,
                "company": company,
                "start": start_date,
                "end": end_date,
                "responsibilities": responsibilities.split('\n') if responsibilities else []
            })
    
    st.header("Education")
    num_education = st.number_input("Number of educational qualifications", min_value=1, max_value=5, value=1)
    
    education = []
    for i in range(num_education):
        st.subheader(f"Education {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            degree = st.text_input(f"Degree*", key=f"degree_{i}")
            institution = st.text_input(f"Institution Name*", key=f"institution_{i}")
        with col2:
            edu_start = st.text_input(f"Start Year*", key=f"edu_start_{i}")
            edu_end = st.text_input(f"End Year (or Expected)*", key=f"edu_end_{i}")
        
        gpa = st.text_input(f"GPA (optional)", key=f"gpa_{i}")
        
        if degree and institution and edu_start and edu_end:
            edu_entry = {
                "degree": degree,
                "institution": institution,
                "start": edu_start,
                "end": edu_end
            }
            if gpa:
                edu_entry["gpa"] = gpa
            education.append(edu_entry)
    
    st.header("Technical Skills")
    st.markdown("Enter your technical skills separated by commas")
    technical_skills = st.text_area("Technical Skills*", height=80, key="tech_skills",
                                   placeholder="Python, JavaScript, SQL, React, AWS, etc.")
    
    st.header("Projects")
    st.info("📌 Fixed Project Entry")
    project_fixed = {
        "name": "AI/ML Projects Portfolio",
        "technologies": "Python, TensorFlow, Scikit-learn, Pandas",
        "description": "Developed multiple AI/ML projects including predictive models and data analysis solutions"
    }
    
    st.header("Certifications")
    st.info("📌 Fixed Certification Entry")
    cert_fixed = "Bhartiya Vidya Bhavans Sardar Patel Institute Of Technology - Professional Certificate in Artificial Intelligence"
    
    # Additional certifications
    additional_certs = st.text_area("Additional Certifications (one per line, optional)", height=80, key="add_certs")
    
    # Save data
    if st.button("💾 Save Information", type="primary"):
        all_certs = [cert_fixed]
        if additional_certs:
            all_certs.extend([c.strip() for c in additional_certs.split('\n') if c.strip()])
        
        st.session_state.resume_data = {
            "name": full_name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio,
            "location": location,
            "summary": summary,
            "experiences": experiences,
            "education": education,
            "technical_skills": [s.strip() for s in technical_skills.split(',') if s.strip()],
            "projects": [project_fixed],
            "certifications": all_certs,
            "photo": st.session_state.photo_data
        }
        st.success("✅ Information saved! Go to other tabs to analyze and preview.")

with tab2:
    st.header("🎯 Advanced ATS Score Analysis")
    
    if st.session_state.resume_data:
        st.markdown("### Job Description")
        job_description = st.text_area("Paste the job description you're applying for:", 
                                       height=200, key="job_desc")
        
        if st.button("📊 Calculate ATS Score", type="primary"):
            if job_description:
                with st.spinner("Running advanced ATS analysis..."):
                    data = st.session_state.resume_data
                    
                    # Prepare resume text with weighted sections
                    resume_text = {
                        'summary': data.get('summary', '').lower(),
                        'experience': ' '.join([f"{exp.get('title', '')} {exp.get('company', '')} {' '.join(exp.get('responsibilities', []))}" 
                                               for exp in data.get('experiences', [])]).lower(),
                        'education': ' '.join([f"{edu.get('degree', '')} {edu.get('institution', '')}" 
                                              for edu in data.get('education', [])]).lower(),
                        'skills': ' '.join(data.get('technical_skills', [])).lower(),
                        'projects': ' '.join([f"{proj.get('name', '')} {proj.get('technologies', '')} {proj.get('description', '')}" 
                                             for proj in data.get('projects', [])]).lower()
                    }
                    
                    full_resume_text = ' '.join(resume_text.values())
                    job_desc_lower = job_description.lower()
                    
                    # Advanced keyword extraction with filtering
                    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'a', 'an', 
                                 'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
                                 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
                                 'these', 'those', 'from', 'into', 'through', 'during', 'before', 'after', 'above',
                                 'below', 'between', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
                                 'when', 'where', 'why', 'how', 'all', 'both', 'each', 'few', 'more', 'most', 'other',
                                 'some', 'such', 'only', 'own', 'same', 'than', 'too', 'very', 'just', 'about'}
                    
                    # Extract keywords from job description
                    job_words = re.findall(r'\b[a-z]+\b', job_desc_lower)
                    job_keywords = [w for w in job_words if len(w) > 3 and w not in stop_words]
                    
                    # Extract multi-word phrases (bigrams and trigrams)
                    job_phrases = []
                    words = job_desc_lower.split()
                    for i in range(len(words) - 1):
                        if len(words[i]) > 2 and len(words[i+1]) > 2:
                            phrase = f"{words[i]} {words[i+1]}"
                            if phrase not in stop_words:
                                job_phrases.append(phrase)
                    
                    # Common tech skills and certifications (weighted higher)
                    tech_skills = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'sql', 
                                  'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git', 'agile', 'scrum',
                                  'machine learning', 'artificial intelligence', 'data science', 'tensorflow',
                                  'pytorch', 'scikit-learn', 'pandas', 'numpy', 'html', 'css', 'api', 'rest',
                                  'graphql', 'typescript', 'c++', 'golang', 'rust', 'swift', 'kotlin']
                    
                    action_verbs = ['developed', 'managed', 'led', 'created', 'implemented', 'designed',
                                   'built', 'improved', 'increased', 'reduced', 'launched', 'delivered',
                                   'coordinated', 'analyzed', 'optimized', 'automated', 'established']
                    
                    # Scoring components
                    keyword_matches = []
                    tech_skill_matches = []
                    phrase_matches = []
                    action_verb_matches = []
                    
                    # Check single keywords
                    for keyword in set(job_keywords):
                        if keyword in full_resume_text:
                            keyword_matches.append(keyword)
                            if keyword in tech_skills:
                                tech_skill_matches.append(keyword)
                    
                    # Check phrases
                    for phrase in set(job_phrases):
                        if phrase in full_resume_text:
                            phrase_matches.append(phrase)
                    
                    # Check action verbs
                    for verb in action_verbs:
                        if verb in resume_text['experience']:
                            action_verb_matches.append(verb)
                    
                    # Calculate weighted scores
                    keyword_score = (len(keyword_matches) / max(len(set(job_keywords)), 1)) * 40
                    tech_score = (len(tech_skill_matches) / max(len([k for k in set(job_keywords) if k in tech_skills]), 1)) * 25 if any(k in tech_skills for k in job_keywords) else 0
                    phrase_score = (len(phrase_matches) / max(len(set(job_phrases)), 1)) * 20
                    action_verb_score = (len(action_verb_matches) / max(len(action_verbs), 1)) * 10
                    
                    # Format check (always full points for our template)
                    format_score = 5  # Our template is ATS-friendly
                    
                    # Calculate final score
                    total_score = min(100, int(keyword_score + tech_score + phrase_score + action_verb_score + format_score))
                    
                    # Additional checks
                    has_quantifiable = bool(re.search(r'\d+%|\d+\+|increased|decreased|improved|reduced', resume_text['experience']))
                    has_email = bool(data.get('email'))
                    has_phone = bool(data.get('phone'))
                    contact_complete = has_email and has_phone
                    
                    # Display comprehensive results
                    st.markdown("---")
                    
                    # Main score display
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Overall ATS Score", f"{total_score}%", 
                                 delta="Strong" if total_score >= 80 else "Good" if total_score >= 60 else "Weak")
                    with col2:
                        st.metric("Keywords Found", f"{len(keyword_matches)}/{len(set(job_keywords))}")
                    with col3:
                        st.metric("Tech Skills Match", f"{len(tech_skill_matches)}")
                    with col4:
                        st.metric("Phrases Matched", f"{len(phrase_matches)}")
                    
                    # Score interpretation
                    if total_score >= 80:
                        st.success("🎉 **Excellent Match!** Your resume is highly optimized for this position.")
                    elif total_score >= 60:
                        st.warning("⚠️ **Good Match** - Your resume is competitive but has room for improvement.")
                    else:
                        st.error("❌ **Needs Improvement** - Consider adding more relevant keywords and experience.")
                    
                    # Detailed breakdown
                    with st.expander("📊 Detailed Score Breakdown", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### Score Components")
                            st.progress(keyword_score / 40, text=f"Keywords: {int(keyword_score)}/40")
                            st.progress(tech_score / 25, text=f"Technical Skills: {int(tech_score)}/25")
                            st.progress(phrase_score / 20, text=f"Key Phrases: {int(phrase_score)}/20")
                            st.progress(action_verb_score / 10, text=f"Action Verbs: {int(action_verb_score)}/10")
                            st.progress(format_score / 5, text=f"Format: {int(format_score)}/5")
                        
                        with col2:
                            st.markdown("#### Quality Checks")
                            st.write("✅ Contact Information" if contact_complete else "❌ Missing Contact Info")
                            st.write("✅ Quantifiable Achievements" if has_quantifiable else "⚠️ Add Numbers/Metrics")
                            st.write(f"✅ Action Verbs Used: {len(action_verb_matches)}" if action_verb_matches else "⚠️ Use More Action Verbs")
                            st.write(f"✅ Technical Skills: {len(tech_skill_matches)}" if tech_skill_matches else "⚠️ Add Technical Skills")
                    
                    # Matched keywords
                    with st.expander("🔑 Matched Keywords & Skills", expanded=True):
                        if tech_skill_matches:
                            st.markdown("**🔧 Technical Skills Found:**")
                            st.info(", ".join(tech_skill_matches))
                        
                        if phrase_matches:
                            st.markdown("**📝 Key Phrases Found:**")
                            st.success(", ".join(phrase_matches[:15]))
                        
                        if action_verb_matches:
                            st.markdown("**💪 Action Verbs Used:**")
                            st.write(", ".join(action_verb_matches))
                        
                        if keyword_matches:
                            st.markdown("**🎯 Other Keywords:**")
                            other_keywords = [k for k in keyword_matches if k not in tech_skill_matches]
                            st.write(", ".join(other_keywords[:20]))
                    
                    # Recommendations
                    with st.expander("💡 Actionable Recommendations", expanded=True):
                        missing_keywords = list(set(job_keywords) - set(keyword_matches))
                        missing_tech = [k for k in job_keywords if k in tech_skills and k not in tech_skill_matches]
                        
                        recommendations = []
                        
                        if total_score < 80:
                            if missing_tech:
                                recommendations.append(f"**Add these technical skills:** {', '.join(missing_tech[:5])}")
                            
                            if missing_keywords:
                                top_missing = missing_keywords[:8]
                                recommendations.append(f"**Include these keywords:** {', '.join(top_missing)}")
                            
                            if not has_quantifiable:
                                recommendations.append("**Add quantifiable achievements:** Use numbers, percentages, and metrics (e.g., 'Increased efficiency by 30%')")
                            
                            if len(action_verb_matches) < 5:
                                recommendations.append("**Use more action verbs:** Start bullet points with strong verbs like 'Developed', 'Led', 'Implemented'")
                            
                            if len(phrase_matches) < 3:
                                recommendations.append("**Use exact phrases from job description:** Mirror the language used in the posting")
                        
                        if recommendations:
                            for i, rec in enumerate(recommendations, 1):
                                st.markdown(f"{i}. {rec}")
                        else:
                            st.success("✅ Your resume is well-optimized! Minor tweaks may still help.")
                    
                    # Compare with industry standards
                    st.markdown("---")
                    st.markdown("### 📈 Industry Benchmark")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Your Score", f"{total_score}%")
                    with col2:
                        st.metric("Average Score", "65%")
                    with col3:
                        st.metric("Top 10% Score", "85%+")
                    
                    if total_score >= 85:
                        st.success("🏆 You're in the top tier! Your resume stands out.")
                    elif total_score >= 65:
                        st.info("📊 You're at or above average. Keep refining!")
                    else:
                        st.warning("📉 Below average. Focus on adding relevant keywords and experience.")
            else:
                st.error("Please paste a job description first!")
    else:
        st.info("👈 Please fill in your information in the 'Fill Information' tab first.")

with tab3:
    if st.session_state.resume_data:
        data = st.session_state.resume_data
        
        # Convert photo to base64 if exists
        photo_base64 = ""
        if data.get('photo'):
            photo_base64 = base64.b64encode(data['photo']).decode()
        
        # Generate resume HTML with centered name and photo
        resume_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, Helvetica, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 850px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .profile-photo {{
                    width: 120px;
                    height: 120px;
                    border-radius: 50%;
                    object-fit: cover;
                    margin: 0 auto 15px;
                    display: block;
                    border: 3px solid #2c3e50;
                }}
                h1 {{
                    font-size: 32px;
                    margin: 10px 0 5px 0;
                    color: #2c3e50;
                    text-align: center;
                }}
                h2 {{
                    font-size: 18px;
                    border-bottom: 2px solid #2c3e50;
                    padding-bottom: 5px;
                    margin-top: 20px;
                    margin-bottom: 10px;
                    text-transform: uppercase;
                    color: #2c3e50;
                }}
                .contact {{
                    text-align: center;
                    margin-bottom: 20px;
                    font-size: 14px;
                }}
                .contact a {{
                    color: #2980b9;
                    text-decoration: none;
                }}
                .section {{
                    margin-bottom: 20px;
                }}
                .job, .edu, .project {{
                    margin-bottom: 15px;
                }}
                .job-header, .edu-header, .project-header {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 5px;
                }}
                .job-title, .degree, .project-name {{
                    font-weight: bold;
                    font-size: 16px;
                }}
                .company, .institution {{
                    font-style: italic;
                }}
                .date {{
                    color: #7f8c8d;
                    font-size: 14px;
                }}
                ul {{
                    margin: 5px 0;
                    padding-left: 20px;
                }}
                li {{
                    margin-bottom: 3px;
                }}
                .skills {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 5px;
                }}
                .skill {{
                    background: #ecf0f1;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                {f'<img src="data:image/png;base64,{photo_base64}" class="profile-photo" alt="Profile Photo">' if photo_base64 else ''}
                <h1>{data.get('name', '')}</h1>
            </div>
            <div class="contact">
                {data.get('location', '')} | {data.get('email', '')} | {data.get('phone', '')}
                {f" | <a href='{data.get('linkedin')}'>{data.get('linkedin')}</a>" if data.get('linkedin') else ''}
                {f" | <a href='{data.get('github')}'>{data.get('github')}</a>" if data.get('github') else ''}
                {f" | <a href='{data.get('portfolio')}'>{data.get('portfolio')}</a>" if data.get('portfolio') else ''}
            </div>
            
            <div class="section">
                <h2>Professional Summary</h2>
                <p>{data.get('summary', '')}</p>
            </div>
        """
        
        if data.get('experiences'):
            resume_html += "<div class='section'><h2>Work Experience</h2>"
            for exp in data['experiences']:
                resume_html += f"""
                <div class="job">
                    <div class="job-header">
                        <div>
                            <div class="job-title">{exp['title']}</div>
                            <div class="company">{exp['company']}</div>
                        </div>
                        <div class="date">{exp['start']} - {exp['end']}</div>
                    </div>
                    <ul>
                """
                for resp in exp['responsibilities']:
                    if resp.strip():
                        resume_html += f"<li>{resp.strip()}</li>"
                resume_html += "</ul></div>"
            resume_html += "</div>"
        
        if data.get('projects'):
            resume_html += "<div class='section'><h2>Projects</h2>"
            for proj in data['projects']:
                resume_html += f"""
                <div class="project">
                    <div class="project-header">
                        <div class="project-name">{proj['name']}</div>
                    </div>
                    <div><strong>Technologies:</strong> {proj['technologies']}</div>
                    <p>{proj['description']}</p>
                </div>
                """
            resume_html += "</div>"
        
        if data.get('education'):
            resume_html += "<div class='section'><h2>Education</h2>"
            for edu in data['education']:
                resume_html += f"""
                <div class="edu">
                    <div class="edu-header">
                        <div>
                            <div class="degree">{edu['degree']}</div>
                            <div class="institution">{edu['institution']}</div>
                        </div>
                        <div class="date">{edu['start']} - {edu['end']}</div>
                    </div>
                    {f"<div>GPA: {edu['gpa']}</div>" if edu.get('gpa') else ''}
                </div>
                """
            resume_html += "</div>"
        
        if data.get('technical_skills'):
            resume_html += "<div class='section'><h2>Technical Skills</h2><div class='skills'>"
            for skill in data['technical_skills']:
                resume_html += f"<span class='skill'>{skill}</span>"
            resume_html += "</div></div>"
        
        if data.get('certifications'):
            resume_html += "<div class='section'><h2>Certifications</h2><ul>"
            for cert in data['certifications']:
                resume_html += f"<li>{cert}</li>"
            resume_html += "</ul></div>"
        
        resume_html += "</body></html>"
        
        # Display preview
        st.markdown("### Resume Preview")
        st.components.v1.html(resume_html, height=800, scrolling=True)
        
        # Download button
        st.download_button(
            label="📥 Download Resume (HTML)",
            data=resume_html,
            file_name=f"{data.get('name', 'resume').replace(' ', '_')}_resume.html",
            mime="text/html"
        )
        
    else:
        st.info("👈 Please fill in your information in the 'Fill Information' tab first.")