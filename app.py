import streamlit as st
from datetime import datetime
import hashlib
import json

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

# Create tabs
tab1, tab2 = st.tabs(["📝 Fill Information", "👁️ Preview & Download"])

with tab1:
    st.header("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input("Full Name*", key="name")
        email = st.text_input("Email*", key="email")
        phone = st.text_input("Phone Number*", key="phone")
        
    with col2:
        linkedin = st.text_input("LinkedIn URL", key="linkedin")
        github = st.text_input("GitHub URL", key="github")
        portfolio = st.text_input("Portfolio/Website", key="portfolio")
    
    location = st.text_input("Location (City, State)", key="location")
    
    st.header("Professional Summary")
    summary = st.text_area("Write a brief professional summary (2-3 sentences)*", 
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
    
    st.header("Skills")
    st.markdown("Enter your skills separated by commas")
    technical_skills = st.text_area("Technical Skills*", height=80, key="tech_skills",
                                   placeholder="Python, JavaScript, SQL, React, AWS, etc.")
    soft_skills = st.text_area("Soft Skills", height=80, key="soft_skills",
                              placeholder="Leadership, Communication, Problem-solving, etc.")
    
    st.header("Projects (Optional)")
    num_projects = st.number_input("Number of projects", min_value=0, max_value=10, value=0)
    
    projects = []
    for i in range(num_projects):
        st.subheader(f"Project {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input(f"Project Name*", key=f"proj_name_{i}")
            project_url = st.text_input(f"Project URL (optional)", key=f"proj_url_{i}")
        with col2:
            project_tech = st.text_input(f"Technologies Used*", key=f"proj_tech_{i}")
        
        project_desc = st.text_area(f"Project Description*", height=80, key=f"proj_desc_{i}")
        
        if project_name and project_tech and project_desc:
            proj_entry = {
                "name": project_name,
                "technologies": project_tech,
                "description": project_desc
            }
            if project_url:
                proj_entry["url"] = project_url
            projects.append(proj_entry)
    
    st.header("Certifications (Optional)")
    certifications = st.text_area("List your certifications (one per line)", height=80, key="certs")
    
    # Save data
    if st.button("💾 Save Information", type="primary"):
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
            "soft_skills": [s.strip() for s in soft_skills.split(',') if s.strip()],
            "projects": projects,
            "certifications": [c.strip() for c in certifications.split('\n') if c.strip()]
        }
        st.success("✅ Information saved! Go to 'Preview & Download' tab to see your resume.")

with tab2:
    if st.session_state.resume_data:
        data = st.session_state.resume_data
        
        # Generate resume HTML
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
                h1 {{
                    font-size: 28px;
                    margin-bottom: 5px;
                    color: #2c3e50;
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
            <h1>{data.get('name', '')}</h1>
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
                    {f"<div><a href='{proj['url']}'>{proj['url']}</a></div>" if proj.get('url') else ''}
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
        
        if data.get('soft_skills'):
            resume_html += "<div class='section'><h2>Soft Skills</h2><div class='skills'>"
            for skill in data['soft_skills']:
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