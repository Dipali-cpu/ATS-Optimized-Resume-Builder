import streamlit as st
from datetime import datetime
import hashlib
import json
import re
from io import BytesIO
import base64
from pypdf import PdfReader

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

# All available projects
ALL_PROJECTS = [
    {
        "title": "Python Data Science Foundations Project",
        "description": "Built foundational data-science skills through Python by practicing variables, operators, loops, functions, exceptions, and object-oriented concepts. Explored data structures, logical problem-solving, and clean code habits. Strengthened analytical thinking, automation abilities, and readiness for real-world data workflows—laying a solid base for advanced analytics, machine learning, and data-driven decision-making",
        "keywords": ["python", "data science", "programming", "analytics", "foundations", "oop"]
    },
    {
        "title": "Python Programming & Data Handling Project",
        "description": "Developed strong Python skills by working with lists, dictionaries, functions, loops, and file handling to process and analyze data efficiently. Practiced writing modular, error-resistant code and automating repetitive tasks. Strengthened logical thinking, data manipulation techniques, and foundational problem-solving abilities essential for data science and real-world analytical workflows.",
        "keywords": ["python", "data handling", "file handling", "automation", "data manipulation", "programming"]
    },
    {
        "title": "Advanced Python Data Processing Project",
        "description": "Enhanced data-science skills by using tuples, sets, comprehensions, and lambda functions to streamline data processing tasks. Built efficient, reusable code for organizing, transforming, and analyzing datasets. Strengthened logical reasoning, pattern recognition, and automation techniques essential for data cleaning, preprocessing, and building reliable analytical pipelines in real-world data-science projects",
        "keywords": ["python", "data processing", "lambda", "comprehensions", "preprocessing", "data cleaning"]
    },
    {
        "title": "Python Data Transformation & Automation Project",
        "description": "Applied advanced Python techniques including string manipulation, regular expressions, modules, and file operations to clean and structure raw data. Built automated scripts for extracting patterns, validating inputs, and improving data quality. Strengthened analytical thinking, precision, and workflow efficiency essential for data preprocessing, feature engineering, and real-world data-science tasks.",
        "keywords": ["python", "automation", "regex", "data transformation", "feature engineering", "etl"]
    },
    {
        "title": "Python Data Analysis & Visualization Foundations Project",
        "description": "Explored core data-science techniques using Python by practicing data organization, conditional logic, loops, and basic visualization. Applied structured problem-solving to clean, transform, and interpret datasets. Strengthened analytical thinking, automation skills, and the ability to build clear, functional scripts—forming a strong foundation for advanced analytics, machine learning, and real-world data workflows.",
        "keywords": ["python", "data analysis", "visualization", "analytics", "machine learning", "matplotlib"]
    },
    {
        "title": "Python Exploratory Data Processing & Automation Project",
        "description": "Strengthened data-science foundations by working with Python functions, loops, comprehensions, and file operations to clean, organize, and transform datasets. Practiced writing efficient, modular code for automating routine tasks and extracting meaningful patterns. Enhanced logical reasoning, problem-solving, and data-handling skills essential for exploratory analysis, preprocessing, and building reliable analytical workflows.",
        "keywords": ["python", "exploratory analysis", "automation", "data processing", "eda"]
    },
    {
        "title": "Python Data Cleaning & Workflow Optimization Project",
        "description": "Applied Python techniques such as functions, loops, conditional logic, and data structures to clean, filter, and organize datasets. Built efficient, reusable code to automate common tasks and improve processing speed. Strengthened analytical thinking, data-handling precision, and problem-solving abilities essential for preparing high-quality data and supporting accurate, real-world data-science workflows.",
        "keywords": ["python", "data cleaning", "optimization", "workflow", "automation"]
    },
    {
        "title": "Python Data Processing & Function Optimization Project",
        "description": "Developed strong data-science foundations by creating optimized functions, using loops, conditional logic, and list comprehensions to transform and analyze data. Practiced modular coding, error handling, and workflow automation. Strengthened problem-solving, pattern recognition, and data-handling efficiency—key skills for building scalable analytical processes and preparing datasets for deeper statistical and machine-learning tasks.",
        "keywords": ["python", "optimization", "functions", "data processing", "scalability"]
    },
    {
        "title": "Statistical Foundations & Data Interpretation Project",
        "description": "Built core statistical skills by exploring measures of central tendency, variability, and data distribution. Applied Python to calculate, visualize, and interpret statistical patterns. Strengthened analytical thinking, numerical reasoning, and data-driven decision-making—key abilities for understanding datasets, identifying trends, and supporting reliable insights in real-world data-science applications.",
        "keywords": ["statistics", "python", "data interpretation", "analytics", "patterns", "visualization"]
    },
    {
        "title": "Exploratory Statistics & Data Pattern Analysis Project",
        "description": "Strengthened statistical understanding by analyzing distributions, variability, and relationships within datasets. Used Python to compute descriptive statistics, visualize patterns, and interpret meaningful trends. Enhanced analytical reasoning, data-cleaning precision, and insight-generation skills essential for preparing datasets, validating assumptions, and supporting accurate decision-making in real-world data-science environments.",
        "keywords": ["statistics", "eda", "python", "data analysis", "patterns"]
    },
    {
        "title": "Probability Concepts & Statistical Insight Development Project",
        "description": "Explored foundational probability principles, including events, outcomes, and rule-based calculations. Applied Python to model scenarios, compute probabilities, and interpret results. Strengthened logical reasoning, analytical thinking, and quantitative problem-solving—building essential skills for uncertainty analysis, predictive modeling, and data-driven decision-making in real-world data-science applications.",
        "keywords": ["probability", "statistics", "python", "modeling", "predictive analytics"]
    },
    {
        "title": "Probability Distributions & Data Interpretation Project",
        "description": "Studied key probability distributions and applied Python to compute, visualize, and interpret them. Gained practical experience analyzing randomness, variability, and real-world data behavior. Strengthened quantitative reasoning, statistical modeling skills, and the ability to draw meaningful insights—essential for building accurate predictive models and performing rigorous data-science analysis.",
        "keywords": ["probability", "distributions", "statistics", "python", "modeling", "predictive"]
    },
    {
        "title": "Statistical Inference & Data Variation Analysis Project",
        "description": "Explored statistical inference concepts using Python to analyze variability, sampling behavior, and confidence measures. Practiced interpreting patterns, validating assumptions, and understanding dataset uncertainty. Strengthened analytical reasoning, data-interpretation accuracy, and foundational statistical skills essential for drawing reliable conclusions and supporting evidence-based decision-making in data-science workflows.",
        "keywords": ["statistics", "inference", "python", "data validation", "analytics"]
    },
    {
        "title": "Hypothesis Testing & Statistical Decision-Making Project",
        "description": "Applied core hypothesis-testing techniques using Python to compare datasets, evaluate significance, and draw evidence-based conclusions. Explored p-values, test statistics, and error types to understand real-world uncertainty. Strengthened analytical judgment, statistical reasoning, and data-validation skills essential for accurate insights and scientifically grounded decision-making in data-science applications.",
        "keywords": ["hypothesis testing", "statistics", "python", "data validation", "analytics", "a/b testing"]
    },
    {
        "title": "Multivariable Statistical Testing & Comparative Analysis Project",
        "description": "Performed advanced statistical tests on three or more paired variables using Python to evaluate differences, relationships, and significance. Strengthened understanding of variance, dependency, and multivariable behavior. Enhanced analytical precision, data interpretation, and statistical reasoning—key skills for modeling complex datasets and generating reliable insights in real-world data-science environments.",
        "keywords": ["statistics", "multivariable analysis", "python", "anova", "comparative analysis"]
    },
    {
        "title": "Generative AI Exploration & Model Interaction Project",
        "description": "Explored foundational generative AI concepts by interacting with Gemini models to generate text, analyze outputs, and understand prompt engineering. Strengthened skills in automation, creativity, and data interpretation. Gained practical experience leveraging AI tools for insights, content generation, and problem-solving—building essential capabilities for modern data-science and AI-driven workflows.",
        "keywords": ["ai", "generative ai", "machine learning", "nlp", "prompt engineering", "llm"]
    },
    {
        "title": "Prompt Engineering & Generative AI Optimization Project",
        "description": "Developed effective prompt-engineering techniques to guide generative AI models in producing accurate, structured outputs. Explored instruction tuning, context design, and iterative refinement. Strengthened analytical reasoning, problem decomposition, and AI-assisted automation skills—key abilities for enhancing model performance, improving data workflows, and leveraging generative systems in modern data-science environments",
        "keywords": ["prompt engineering", "ai", "generative ai", "optimization", "nlp", "llm"]
    },
    {
        "title": "SQL Database Management & Data Querying Project",
        "description": "Built strong foundational skills in database management by working with SQLite to create tables, insert records, and perform essential SQL queries. Strengthened understanding of structured data, relational design, and efficient data retrieval. Enhanced analytical thinking and data-handling accuracy—core abilities for real-world data science, reporting, and data-driven decision-making",
        "keywords": ["sql", "database", "data management", "queries", "sqlite", "rdbms"]
    },
    {
        "title": "NoSQL Database Operations & Document Data Management Project",
        "description": "Gained hands-on experience with MongoDB by creating collections, inserting documents, and performing query operations. Strengthened understanding of unstructured data, schema flexibility, and efficient retrieval techniques. Enhanced analytical thinking, data organization, and database-handling skills essential for modern data-science workflows involving large-scale, semi-structured, or rapidly evolving datasets.",
        "keywords": ["nosql", "mongodb", "database", "data management", "document database", "json"]
    },
    {
        "title": "Data Visualization & Insight Communication Using Matplotlib",
        "description": "Created clear, meaningful visualizations using Matplotlib to analyze patterns, compare variables, and communicate insights effectively. Practiced plotting techniques, customization, and visual storytelling. Strengthened analytical reasoning, data interpretation, and presentation skills—core abilities for transforming raw data into understandable narratives in real-world data-science and decision-making environments.",
        "keywords": ["matplotlib", "data visualization", "python", "analytics", "storytelling", "charts"]
    },
    {
        "title": "Advanced Data Visualization & Pattern Exploration with Matplotlib",
        "description": "Developed advanced visualization skills using Matplotlib to explore trends, compare relationships, and present complex insights clearly. Practiced customizing plots, handling datasets, and choosing effective visual formats. Strengthened analytical interpretation, storytelling abilities, and data-driven communication—key capabilities for delivering meaningful insights in professional data-science and business decision-making environments.",
        "keywords": ["matplotlib", "visualization", "analytics", "python", "data science", "dashboards"]
    },
    {
        "title": "Data Manipulation & Analysis Using Pandas",
        "description": "Built strong data-science skills by using Pandas to clean, filter, transform, and analyze structured datasets. Practiced handling DataFrames, performing aggregations, managing missing values, and deriving insights. Strengthened analytical thinking, data-wrangling efficiency, and problem-solving—foundational abilities for preparing high-quality data and supporting accurate, real-world analytical and machine-learning workflows.",
        "keywords": ["pandas", "python", "data analysis", "data wrangling", "dataframes", "etl"]
    },
    {
        "title": "Numerical Computing & Array Operations Using NumPy",
        "description": "Developed strong numerical analysis skills by working with NumPy arrays, vectorized operations, indexing, and mathematical functions. Practiced efficient data handling, transformations, and computations essential for large datasets. Strengthened analytical reasoning, performance-focused coding, and foundational quantitative abilities crucial for machine learning, scientific computing, and real-world data-science applications.",
        "keywords": ["numpy", "python", "numerical computing", "arrays", "machine learning", "linear algebra"]
    },
    {
        "title": "Data Import, Export & File Handling Automation Project",
        "description": "Strengthened data-engineering skills by reading, writing, and managing files in multiple formats using Python. Automated data-loading workflows, cleaned raw inputs, and organized datasets for analysis. Enhanced accuracy, efficiency, and problem-solving abilities—core capabilities for building reliable data pipelines and supporting real-world data-science and machine-learning processes.",
        "keywords": ["python", "file handling", "automation", "data engineering", "etl", "pipelines"]
    },
    {
        "title": "Machine Learning Model Development & Predictive Analysis Project",
        "description": "Built and evaluated machine-learning models using Python to understand classification, regression, and performance metrics. practiced data preprocessing, feature selection, and model tuning to improve accuracy. Strengthened analytical reasoning, algorithmic understanding, and predictive insight—key skills for solving real-world problems and delivering data-driven solutions in professional data-science environments.",
        "keywords": ["machine learning", "python", "predictive modeling", "classification", "regression", "sklearn"]
    },
    {
        "title": "Advanced Machine Learning Techniques & Model Optimization Project",
        "description": "Explored advanced machine-learning concepts by building and tuning models, evaluating performance, and applying preprocessing techniques. Strengthened skills in feature engineering, algorithm selection, and interpreting model outcomes. Enhanced analytical decision-making, predictive accuracy, and problem-solving abilities—crucial for developing reliable, high-performing machine-learning solutions in real-world data-science environments",
        "keywords": ["machine learning", "optimization", "feature engineering", "python", "modeling", "hyperparameter tuning"]
    },
    {
        "title": "Model Evaluation & Performance Improvement in Machine Learning",
        "description": "Practiced evaluating machine-learning models using metrics, validation techniques, and error analysis to improve predictive performance. Applied preprocessing, feature scaling, and algorithm comparison to understand model behavior. Strengthened analytical reasoning, optimization skills, and data-driven decision-making—key abilities for building accurate, reliable machine-learning systems in real-world data-science applications.",
        "keywords": ["machine learning", "model evaluation", "optimization", "python", "metrics", "cross-validation"]
    }
]

# Main application
st.set_page_config(page_title="ATS Resume Builder", page_icon="📄", layout="wide")

st.title("📄 ATS-Optimized Resume Builder v4.0")
st.markdown("Smart resume builder with AI-powered project selection and interview preparation")

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {}
if 'photo_data' not in st.session_state:
    st.session_state.photo_data = None
if 'cv_text' not in st.session_state:
    st.session_state.cv_text = ""
if 'selected_projects' not in st.session_state:
    st.session_state.selected_projects = []
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Fill Information", "🎯 ATS Analysis & Smart Projects", "❓ Interview Prep", "👁️ Preview & Download"])

with tab1:
    st.header("📄 Upload Existing CV (Optional)")
    st.markdown("Upload your existing CV to **auto-fill the entire form** and extract all information")
    
    uploaded_cv = st.file_uploader("Upload CV (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'], key="cv_uploader")
    
    if uploaded_cv is not None:
        try:
            if uploaded_cv.type == "text/plain":
                st.session_state.cv_text = uploaded_cv.read().decode('utf-8')
                st.success("✅ CV uploaded successfully!")
            elif uploaded_cv.type == "application/pdf":
                try:
                    # Try pypdf first (newer)
                    try:
                        from pypdf import PdfReader
                        pdf_reader = PdfReader(uploaded_cv)
                        st.session_state.cv_text = ""
                        for page in pdf_reader.pages:
                            st.session_state.cv_text += page.extract_text() + "\n"
                        st.success("✅ PDF uploaded successfully!")
                    except ImportError:
                        # Fallback to PyPDF2 (older)
                        import PyPDF2
                        pdf_reader = PyPDF2.PdfReader(uploaded_cv)
                        st.session_state.cv_text = ""
                        for page in pdf_reader.pages:
                            st.session_state.cv_text += page.extract_text() + "\n"
                        st.success("✅ PDF uploaded successfully!")
                except Exception as pdf_error:
                    st.error(f"PDF reading error: {str(pdf_error)}")
                    st.warning("💡 To fix: Run `pip install pypdf` or `pip install PyPDF2` in terminal")
            elif uploaded_cv.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                try:
                    import docx
                    doc = docx.Document(uploaded_cv)
                    st.session_state.cv_text = "\n".join([para.text for para in doc.paragraphs])
                    st.success("✅ DOCX uploaded successfully!")
                except Exception as docx_error:
                    st.error(f"DOCX reading error: {str(docx_error)}")
                    st.warning("💡 To fix: Run `pip install python-docx` in terminal")
            
            if st.session_state.cv_text:
                with st.expander("View extracted text"):
                    st.text_area("Extracted CV Text", st.session_state.cv_text, height=200, disabled=True)
                
                # Auto-fill button
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🤖 Auto-Fill Form from CV", type="primary", use_container_width=True):
                        with st.spinner("Analyzing CV and extracting information..."):
                            cv_text = st.session_state.cv_text.lower()
                            lines = st.session_state.cv_text.split('\n')
                            
                            # Extract email
                            email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', st.session_state.cv_text)
                            if email_match and 'auto_email' not in st.session_state:
                                st.session_state['auto_email'] = email_match.group()
                            
                            # Extract phone
                            phone_match = re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', st.session_state.cv_text)
                            if phone_match and 'auto_phone' not in st.session_state:
                                st.session_state['auto_phone'] = phone_match.group().strip()
                            
                            # Extract name (usually first line or after "Name:")
                            name_keywords = ['name:', 'candidate:', 'applicant:']
                            auto_name = ""
                            for line in lines[:10]:
                                line_lower = line.lower().strip()
                                if any(kw in line_lower for kw in name_keywords):
                                    auto_name = line.split(':', 1)[1].strip() if ':' in line else ""
                                    break
                                elif len(line.strip()) > 0 and len(line.strip().split()) <= 4 and not '@' in line and not any(c.isdigit() for c in line):
                                    auto_name = line.strip()
                                    break
                            
                            if auto_name and 'auto_name' not in st.session_state:
                                st.session_state['auto_name'] = auto_name
                            
                            # Extract location
                            location_keywords = ['location:', 'address:', 'city:', 'residence:']
                            for line in lines:
                                if any(kw in line.lower() for kw in location_keywords):
                                    location = line.split(':', 1)[1].strip() if ':' in line else ""
                                    if location and 'auto_location' not in st.session_state:
                                        st.session_state['auto_location'] = location
                                    break
                            
                            # Extract LinkedIn
                            linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', st.session_state.cv_text, re.IGNORECASE)
                            if linkedin_match and 'auto_linkedin' not in st.session_state:
                                st.session_state['auto_linkedin'] = f"https://{linkedin_match.group()}" if not linkedin_match.group().startswith('http') else linkedin_match.group()
                            
                            # Extract GitHub
                            github_match = re.search(r'github\.com/[\w-]+', st.session_state.cv_text, re.IGNORECASE)
                            if github_match and 'auto_github' not in st.session_state:
                                st.session_state['auto_github'] = f"https://{github_match.group()}" if not github_match.group().startswith('http') else github_match.group()
                            
                            # Extract skills
                            skill_section = ""
                            capture = False
                            for i, line in enumerate(lines):
                                if 'skill' in line.lower() or 'technical' in line.lower() or 'technologies' in line.lower():
                                    capture = True
                                    continue
                                if capture:
                                    if any(kw in line.lower() for kw in ['experience', 'education', 'project', 'certification', 'work']):
                                        break
                                    skill_section += line + " "
                                    if i > 100:  # Don't go too far
                                        break
                            
                            if skill_section and 'auto_skills' not in st.session_state:
                                # Clean and format skills
                                skills = re.sub(r'[•\-\*]', '', skill_section)
                                skills = ', '.join([s.strip() for s in skills.split(',') if s.strip()])
                                st.session_state['auto_skills'] = skills if skills else "Python, Data Analysis, Machine Learning"
                            
                            # Extract summary
                            summary_keywords = ['summary', 'profile', 'objective', 'about']
                            extracted_summary = ""
                            for i, line in enumerate(lines):
                                if any(keyword in line.lower() for keyword in summary_keywords):
                                    extracted_summary = ' '.join(lines[i+1:i+4])
                                    break
                            
                            if extracted_summary and 'auto_summary' not in st.session_state:
                                st.session_state['auto_summary'] = extracted_summary[:300]
                            elif 'auto_summary' not in st.session_state:
                                st.session_state['auto_summary'] = "Experienced professional with strong technical skills and proven track record in data science and analytics."
                            
                            st.success("✅ Form auto-filled! Scroll down to review and edit the extracted information.")
                            st.info("💡 Please review all fields and make any necessary corrections before saving.")
                            st.rerun()
                
                with col2:
                    if st.button("🔄 Clear Auto-Fill Data", use_container_width=True):
                        keys_to_clear = ['auto_name', 'auto_email', 'auto_phone', 'auto_location', 
                                        'auto_linkedin', 'auto_github', 'auto_skills', 'auto_summary']
                        for key in keys_to_clear:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.success("✅ Auto-fill data cleared!")
                        st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.info("Supported formats: PDF, DOCX, TXT")
    
    st.header("Personal Information")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        full_name = st.text_input("Full Name*", key="name", value=st.session_state.get('auto_name', ''))
        email = st.text_input("Email*", key="email", value=st.session_state.get('auto_email', ''))
        phone = st.text_input("Phone Number*", key="phone", value=st.session_state.get('auto_phone', ''))
        location = st.text_input("Location (City, State)", key="location", value=st.session_state.get('auto_location', ''))
        
    with col2:
        st.markdown("#### Upload Photo")
        photo = st.file_uploader("Profile Photo (Optional)", type=['jpg', 'jpeg', 'png'])
        if photo:
            st.session_state.photo_data = photo.read()
            st.image(st.session_state.photo_data, width=150)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        linkedin = st.text_input("LinkedIn URL", key="linkedin", value=st.session_state.get('auto_linkedin', ''))
    with col2:
        github = st.text_input("GitHub URL", key="github", value=st.session_state.get('auto_github', ''))
    with col3:
        portfolio = st.text_input("Portfolio/Website", key="portfolio")
    
    st.header("Professional Summary")
    
    if st.session_state.cv_text:
        if st.button("🤖 Auto-Generate Summary from CV"):
            with st.spinner("Generating professional summary..."):
                lines = st.session_state.cv_text.split('\n')
                summary_keywords = ['summary', 'profile', 'objective', 'about']
                extracted_summary = ""
                
                for i, line in enumerate(lines):
                    if any(keyword in line.lower() for keyword in summary_keywords):
                        extracted_summary = ' '.join(lines[i+1:i+4])
                        break
                
                if extracted_summary:
                    st.session_state['summary_text'] = extracted_summary[:300]
                else:
                    st.session_state['summary_text'] = "Experienced professional with strong technical and analytical skills."
                st.success("✅ Summary generated! Edit it below.")
                st.rerun()
    
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
                                   value=st.session_state.get('auto_skills', ''),
                                   placeholder="Python, JavaScript, SQL, Machine Learning, AWS, etc.")
    
    st.header("Certifications")
    st.info("📌 Fixed Certification: Bhartiya Vidya Bhavans Sardar Patel Institute Of Technology - Professional Certificate in Artificial Intelligence")
    
    additional_certs = st.text_area("Additional Certifications (one per line, optional)", height=80, key="add_certs")
    
    if st.button("💾 Save Information", type="primary"):
        cert_fixed = "Bhartiya Vidya Bhavans Sardar Patel Institute Of Technology - Professional Certificate in Artificial Intelligence"
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
            "projects": st.session_state.selected_projects,
            "certifications": all_certs,
            "photo": st.session_state.photo_data
        }
        st.success("✅ Information saved! Proceed to ATS Analysis tab.")

with tab2:
    st.header("🎯 Advanced ATS Analysis & Smart Project Selection")
    
    if st.session_state.resume_data:
        st.markdown("### Job Description")
        job_description = st.text_area("Paste the complete job description:", 
                                       height=250, key="job_desc_input",
                                       value=st.session_state.job_description)
        
        if st.button("📊 Analyze Resume & Select Best Projects", type="primary"):
            if job_description:
                st.session_state.job_description = job_description
                
                with st.spinner("Running AI-powered analysis..."):
                    data = st.session_state.resume_data
                    
                    # Prepare resume text
                    resume_text = {
                        'summary': data.get('summary', '').lower(),
                        'experience': ' '.join([f"{exp.get('title', '')} {exp.get('company', '')} {' '.join(exp.get('responsibilities', []))}" 
                                               for exp in data.get('experiences', [])]).lower(),
                        'education': ' '.join([f"{edu.get('degree', '')} {edu.get('institution', '')}" 
                                              for edu in data.get('education', [])]).lower(),
                        'skills': ' '.join(data.get('technical_skills', [])).lower()
                    }
                    
                    full_resume_text = ' '.join(resume_text.values())
                    job_desc_lower = job_description.lower()
                    
                    # Stop words
                    stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'a', 'an', 
                                 'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
                                 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
                                 'these', 'those', 'from', 'into', 'through', 'during', 'before', 'after', 'above',
                                 'below', 'between', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
                                 'when', 'where', 'why', 'how', 'all', 'both', 'each', 'few', 'more', 'most', 'other',
                                 'some', 'such', 'only', 'own', 'same', 'than', 'too', 'very', 'just', 'about'}
                    
                    # Extract keywords
                    job_words = re.findall(r'\b[a-z]+\b', job_desc_lower)
                    job_keywords = [w for w in job_words if len(w) > 3 and w not in stop_words]
                    
                    # Extract phrases
                    job_phrases = []
                    words = job_desc_lower.split()
                    for i in range(len(words) - 1):
                        if len(words[i]) > 2 and len(words[i+1]) > 2:
                            phrase = f"{words[i]} {words[i+1]}"
                            job_phrases.append(phrase)
                    
                    # Tech skills list
                    tech_skills = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'sql', 
                                  'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git', 'agile', 'scrum',
                                  'machine learning', 'artificial intelligence', 'data science', 'tensorflow',
                                  'pytorch', 'scikit-learn', 'sklearn', 'pandas', 'numpy', 'html', 'css', 'api', 'rest',
                                  'graphql', 'typescript', 'c++', 'golang', 'rust', 'swift', 'kotlin', 'deep learning',
                                  'nlp', 'computer vision', 'data analysis', 'statistical analysis', 'matplotlib', 'seaborn']
                    
                    # Action verbs
                    action_verbs = ['developed', 'managed', 'led', 'created', 'implemented', 'designed',
                                   'built', 'improved', 'increased', 'reduced', 'launched', 'delivered',
                                   'coordinated', 'analyzed', 'optimized', 'automated', 'established']
                    
                    # Calculate matches
                    keyword_matches = []
                    tech_skill_matches = []
                    phrase_matches = []
                    action_verb_matches = []
                    
                    for keyword in set(job_keywords):
                        if keyword in full_resume_text:
                            keyword_matches.append(keyword)
                            if keyword in tech_skills:
                                tech_skill_matches.append(keyword)
                    
                    for phrase in set(job_phrases):
                        if phrase in full_resume_text:
                            phrase_matches.append(phrase)
                    
                    for verb in action_verbs:
                        if verb in resume_text['experience']:
                            action_verb_matches.append(verb)
                    
                    # Calculate scores
                    keyword_score = (len(keyword_matches) / max(len(set(job_keywords)), 1)) * 40
                    tech_score = (len(tech_skill_matches) / max(len([k for k in set(job_keywords) if k in tech_skills]), 1)) * 25 if any(k in tech_skills for k in job_keywords) else 0
                    phrase_score = (len(phrase_matches) / max(len(set(job_phrases)), 1)) * 20
                    action_verb_score = (len(action_verb_matches) / max(len(action_verbs), 1)) * 10
                    format_score = 5
                    
                    total_score = min(100, int(keyword_score + tech_score + phrase_score + action_verb_score + format_score))
                    
                    # Quality checks
                    has_quantifiable = bool(re.search(r'\d+%|\d+\+|increased|decreased|improved|reduced', resume_text['experience']))
                    has_email = bool(data.get('email'))
                    has_phone = bool(data.get('phone'))
                    contact_complete = has_email and has_phone
                    
                    # Smart Project Selection
                    st.markdown("---")
                    st.markdown("## 🚀 AI-Powered Project Selection")
                    st.info("Analyzing all 27 projects and selecting the top 5 that best match this job...")
                    
                    project_scores = []
                    for project in ALL_PROJECTS:
                        score = 0
                        project_text = f"{project['title']} {project['description']}".lower()
                        
                        # Match job keywords in project
                        for keyword in job_keywords:
                            if keyword in project_text:
                                score += 2
                        
                        # Bonus for project keywords matching job
                        for pk in project['keywords']:
                            if pk in job_desc_lower:
                                score += 5
                        
                        # Extra bonus for tech skills match
                        for tech in tech_skill_matches:
                            if tech in project_text:
                                score += 3
                        
                        project_scores.append((project, score))
                    
                    # Sort and select top 5
                    project_scores.sort(key=lambda x: x[1], reverse=True)
                    top_projects = [p[0] for p in project_scores[:5]]
                    st.session_state.selected_projects = top_projects
                    
                    # Update resume data with selected projects
                    st.session_state.resume_data['projects'] = top_projects
                    
                    st.success("✅ Top 5 Projects Selected Based on Job Requirements!")
                    
                    for i, proj in enumerate(top_projects, 1):
                        relevance_score = project_scores[i-1][1]
                        with st.expander(f"🔹 Project {i}: {proj['title']} (Relevance: {relevance_score} points)", expanded=i<=2):
                            st.markdown(f"**Description:**")
                            st.write(proj['description'])
                            st.markdown(f"**Key Skills:** {', '.join(proj['keywords'])}")
                    
                    # ATS Score Display
                    st.markdown("---")
                    st.markdown("## 📊 Comprehensive ATS Score Analysis")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Overall Score", f"{total_score}%", 
                                 delta="Excellent" if total_score >= 85 else "Strong" if total_score >= 70 else "Good" if total_score >= 60 else "Needs Work")
                    with col2:
                        st.metric("Keywords", f"{len(keyword_matches)}/{len(set(job_keywords))}")
                    with col3:
                        st.metric("Tech Skills", f"{len(tech_skill_matches)}")
                    with col4:
                        st.metric("Phrases", f"{len(phrase_matches)}")
                    
                    if total_score >= 85:
                        st.success("🏆 **Outstanding Match!** You're in the top 10%. Your resume is perfectly optimized.")
                    elif total_score >= 70:
                        st.success("✅ **Strong Match!** Your resume is highly competitive for this role.")
                    elif total_score >= 60:
                        st.warning("⚠️ **Good Match** - Solid foundation, but room for improvement exists.")
                    else:
                        st.error("❌ **Needs Improvement** - Add more relevant keywords and tailor your experience.")
                    
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
                            st.write("✅ Contact Info Complete" if contact_complete else "❌ Add Contact Info")
                            st.write("✅ Quantifiable Results" if has_quantifiable else "⚠️ Add Metrics/Numbers")
                            st.write(f"✅ {len(action_verb_matches)} Action Verbs" if action_verb_matches else "⚠️ Use Action Verbs")
                            st.write(f"✅ {len(tech_skill_matches)} Tech Skills" if tech_skill_matches else "⚠️ List Tech Skills")
                            st.write(f"✅ {len(top_projects)} Relevant Projects")
                    
                    with st.expander("🔑 Matched Keywords & Skills"):
                        if tech_skill_matches:
                            st.markdown("**🔧 Technical Skills Found:**")
                            st.info(", ".join(sorted(set(tech_skill_matches))))
                        
                        if phrase_matches:
                            st.markdown("**📝 Key Phrases Found:**")
                            st.success(", ".join(list(set(phrase_matches))[:15]))
                        
                        if action_verb_matches:
                            st.markdown("**💪 Action Verbs Used:**")
                            st.write(", ".join(sorted(set(action_verb_matches))))
                    
                    with st.expander("💡 Personalized Recommendations"):
                        missing_keywords = list(set(job_keywords) - set(keyword_matches))
                        missing_tech = [k for k in job_keywords if k in tech_skills and k not in tech_skill_matches]
                        
                        recommendations = []
                        
                        if missing_tech:
                            recommendations.append(f"**🔧 Add Technical Skills:** {', '.join(missing_tech[:5])}")
                        
                        if missing_keywords and len(missing_keywords) > 5:
                            recommendations.append(f"**🎯 Include Keywords:** {', '.join(missing_keywords[:8])}")
                        
                        if not has_quantifiable:
                            recommendations.append("**📊 Add Metrics:** Include numbers (e.g., 'Increased efficiency by 30%', 'Processed 10,000+ records')")
                        
                        if len(action_verb_matches) < 5:
                            recommendations.append("**💪 Use Action Verbs:** Start bullets with: Developed, Led, Implemented, Optimized, Delivered")
                        
                        if len(phrase_matches) < 5:
                            recommendations.append("**📝 Mirror Job Language:** Use exact phrases from the job description")
                        
                        if recommendations:
                            for i, rec in enumerate(recommendations, 1):
                                st.markdown(f"{i}. {rec}")
                        else:
                            st.success("✨ Excellent! Your resume is well-optimized. Consider minor tweaks for perfection.")
                    
                    st.markdown("---")
                    st.markdown("### 📈 Industry Benchmark Comparison")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Your Score", f"{total_score}%")
                    with col2:
                        st.metric("Industry Average", "65%")
                    with col3:
                        st.metric("Top 10% Threshold", "85%+")
                    
                    if total_score >= 85:
                        st.balloons()
                        st.success("🏆 **You're in the Top 10%!** Your resume stands out from the competition.")
                    elif total_score >= 65:
                        st.info("📊 **Above Average** - You're competitive. Keep refining for top tier!")
                    else:
                        st.warning("📉 **Below Average** - Focus on keywords, skills, and tailoring to this specific role.")
            else:
                st.error("⚠️ Please paste a job description to analyze!")
    else:
        st.info("👈 Please fill your information in Tab 1 first.")

with tab3:
    st.header("❓ AI-Powered Interview Preparation")
    
    if st.session_state.resume_data and st.session_state.selected_projects:
        data = st.session_state.resume_data
        projects = st.session_state.selected_projects
        
        st.markdown("### Generate Personalized Interview Questions")
        st.info("Get the top 10 interview questions with detailed answers tailored to YOUR profile and the job you're applying for!")
        
        if st.button("🎯 Generate Interview Q&A", type="primary"):
            job_titles = [exp.get('title', '') for exp in data.get('experiences', [])]
            primary_role = job_titles[0] if job_titles else "Data Professional"
            skills_list = data.get('technical_skills', [])[:5]
            cert_name = "Professional Certificate in Artificial Intelligence from Bhartiya Vidya Bhavans Sardar Patel Institute Of Technology"
            
            with st.spinner("Generating personalized interview preparation..."):
                st.success("✅ Your Personalized Interview Prep is Ready!")
                
                questions = [
                    {
                        "category": "Introduction",
                        "q": f"Tell me about yourself and your experience as a {primary_role}.",
                        "a": f"I'm a passionate {primary_role} with expertise in {', '.join(skills_list)}. {data.get('summary', '')} Throughout my career, I've completed {len(projects)} significant projects, including {projects[0]['title']}, where {projects[0]['description'][:120]}... I hold a {cert_name}, which has strengthened both my theoretical foundation and practical skills. I'm excited about applying my experience to drive results in this role.",
                        "tip": "Keep it to 2-3 minutes. Structure: Present → Past experience → Why you're interested in this role."
                    },
                    {
                        "category": "Strengths",
                        "q": f"What is your greatest strength as a {primary_role}?",
                        "a": f"My greatest strength is my ability to combine technical expertise with practical problem-solving. I'm proficient in {', '.join(skills_list)}, and I've demonstrated this through projects like {projects[0]['title']}, where I {projects[0]['description'][:100]}... This combination of technical depth and hands-on experience allows me to tackle complex challenges effectively and deliver measurable results.",
                        "tip": "Choose a strength relevant to the job. Back it up with a specific example and quantifiable results."
                    },
                    {
                        "category": "Project Experience",
                        "q": "Can you describe a challenging project you worked on and how you overcame obstacles?",
                        "a": f"One of my most challenging projects was {projects[1]['title'] if len(projects) > 1 else projects[0]['title']}. {projects[1]['description'] if len(projects) > 1 else projects[0]['description']} The main challenge was balancing efficiency with accuracy while working with complex data. I overcame this by breaking down the problem, applying {', '.join(projects[1]['keywords'][:3] if len(projects) > 1 else projects[0]['keywords'][:3])} techniques, and iterating based on results. The project taught me the importance of systematic problem-solving and continuous testing.",
                        "tip": "Use STAR method: Situation, Task, Action, Result. Emphasize what YOU did and the outcome."
                    },
                    {
                        "category": "Technical Skills",
                        "q": f"What technical skills make you a strong candidate for this {primary_role} position?",
                        "a": f"I bring a comprehensive technical toolkit including {', '.join(skills_list)}. I have hands-on experience with these across multiple projects: in {projects[0]['title']}, I applied {', '.join(projects[0]['keywords'][:2])}; in {projects[2]['title'] if len(projects) > 2 else projects[1]['title']}, I utilized {', '.join(projects[2]['keywords'][:2] if len(projects) > 2 else projects[1]['keywords'][:2])}. I'm also committed to continuous learning—I recently completed {cert_name}. This combination of practical experience and formal training makes me well-prepared for the technical demands of this role.",
                        "tip": "Match your skills to the job requirements. Provide specific examples of when you used each skill."
                    },
                    {
                        "category": "Problem Solving",
                        "q": "How do you approach complex problem-solving in your work?",
                        "a": f"I follow a systematic approach: First, I thoroughly understand the requirements and define the problem clearly. Then, I break it down into manageable components. As demonstrated in {projects[2]['title'] if len(projects) > 2 else projects[0]['title']}, I {projects[2]['description'][:110] if len(projects) > 2 else projects[0]['description'][:110]}... I believe in iterative development, rigorous testing, and maintaining clean, well-documented code. I also collaborate with team members to get different perspectives and ensure the solution is robust and scalable.",
                        "tip": "Show your structured thinking. Mention collaboration and how you validate your solutions."
                    },
                    {
                        "category": "Data Experience",
                        "q": "Describe your experience working with data analysis and what methodologies you use.",
                        "a": f"I have extensive data experience through projects like {projects[3]['title'] if len(projects) > 3 else projects[1]['title']}. {projects[3]['description'][:130] if len(projects) > 3 else projects[1]['description'][:130]}... My approach involves: 1) Data collection and cleaning, 2) Exploratory analysis to understand patterns, 3) Applying appropriate statistical/ML techniques, 4) Validation and testing, 5) Clear visualization and communication of insights. I'm proficient with {', '.join([s for s in skills_list if 'pandas' in s.lower() or 'numpy' in s.lower() or 'python' in s.lower()][:3])}, which enables me to handle complex datasets efficiently.",
                        "tip": "Show your end-to-end data workflow. Emphasize both technical skills and business insights."
                    },
                    {
                        "category": "Python & Programming",
                        "q": "What's your experience with Python, and which libraries are you most comfortable with?",
                        "a": f"Python is my primary programming language, and I've used it extensively across {len(projects)} projects. I'm highly proficient in {', '.join([s for s in skills_list if 'python' in s.lower() or 'pandas' in s.lower() or 'numpy' in s.lower()][:4])}. For example, in {projects[4]['title'] if len(projects) > 4 else projects[0]['title']}, I {projects[4]['description'][:120] if len(projects) > 4 else projects[0]['description'][:120]}... I focus on writing clean, efficient, and maintainable code following PEP 8 standards and best practices.",
                        "tip": "Be specific about libraries and frameworks. Mention code quality and best practices."
                    },
                    {
                        "category": "Continuous Learning",
                        "q": "How do you stay current with technology trends and continue developing your skills?",
                        "a": f"I'm committed to continuous learning through multiple channels: 1) Formal education—I completed {cert_name}, 2) Hands-on projects—I've worked on diverse projects like {', '.join([p['title'][:40] for p in projects[:3]])}, 3) Online resources—I follow industry blogs, research papers, and technical documentation, 4) Community engagement—I participate in technical forums and GitHub repositories. I believe staying current is essential in our rapidly evolving field, and I dedicate time weekly to learning new tools and techniques.",
                        "tip": "Show you're proactive about learning. Mention specific resources or recent topics you've explored."
                    },
                    {
                        "category": "Machine Learning / AI",
                        "q": "Can you explain your experience with machine learning or AI technologies?",
                        "a": f"I have practical ML/AI experience through projects like {projects[-2]['title'] if len(projects) > 1 else projects[0]['title']} and {projects[-1]['title']}. {projects[-1]['description']} I understand the full ML workflow: data preprocessing, feature engineering, model selection, training, evaluation, and deployment. I've worked with algorithms including regression, classification, clustering, and neural networks. My {cert_name} has given me a strong theoretical foundation in AI concepts, which I've applied in real-world scenarios to solve business problems and generate actionable insights.",
                        "tip": "Cover both theory and practice. Mention specific algorithms and real outcomes."
                    },
                    {
                        "category": "Closing",
                        "q": "Why should we hire you for this position?",
                        "a": f"You should hire me because I offer a unique combination of proven technical skills, diverse project experience, and a growth mindset. My expertise in {', '.join(skills_list)} combined with hands-on experience in {len(projects)} projects—from {projects[0]['title']} to {projects[-1]['title']}—demonstrates my ability to deliver results. I'm passionate about {primary_role.lower()} work, detail-oriented, and thrive in collaborative environments. My {cert_name} shows my commitment to professional development. I'm not just looking for a job; I'm looking to contribute meaningfully to your team's success and grow with the organization. I'm confident I can bring immediate value while continuing to learn and adapt.",
                        "tip": "Tie everything together. Show enthusiasm, mention cultural fit, and express genuine interest in the company."
                    }
                ]
                
                for i, qa in enumerate(questions, 1):
                    with st.expander(f"❓ Question {i} [{qa['category']}]: {qa['q']}", expanded=i<=2):
                        st.markdown("### 💬 Your Answer:")
                        st.write(qa['a'])
                        st.markdown("---")
                        st.markdown("### 💡 Interview Tip:")
                        st.info(qa['tip'])
                
                st.markdown("---")
                st.markdown("## 📚 Complete Interview Preparation Guide")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    ### 📋 Before the Interview
                    
                    - ✅ **Research the company** (products, culture, recent news)
                    - ✅ **Review all your projects** in detail
                    - ✅ **Prepare questions** to ask interviewer
                    - ✅ **Practice answers** out loud (record yourself!)
                    - ✅ **Test tech setup** (if virtual interview)
                    - ✅ **Print extra resumes** (if in-person)
                    - ✅ **Plan your outfit** (professional attire)
                    - ✅ **Get good sleep** the night before
                    """)
                with col2:
                    st.markdown("""
                    ### 💼 During the Interview
                    
                    - 🎯 **Be authentic** and confident
                    - 🎯 **Use STAR method** for behavioral questions
                    - 🎯 **Give specific examples** with numbers
                    - 🎯 **Show enthusiasm** for the role
                    - 🎯 **Ask thoughtful questions**
                    - 🎯 **Take notes** during conversation
                    - 🎯 **Thank the interviewer** at the end
                    - 🎯 **Follow up** with thank-you email within 24hrs
                    """)
                
                st.markdown("### 🎭 Common Follow-up Questions to Prepare For:")
                st.markdown("""
                - "Tell me about a time you failed" → Focus on what you learned
                - "Where do you see yourself in 5 years?" → Show ambition + loyalty
                - "Why are you leaving your current role?" → Stay positive
                - "What's your expected salary?" → Have a range researched
                - "Do you have any questions for us?" → ALWAYS have 3-5 prepared
                """)
                
                st.success("🎉 You're well-prepared! Review these answers, practice out loud, and go confidently into your interview!")
    else:
        st.info("👈 Please complete Tab 1 (Fill Information) and Tab 2 (ATS Analysis) first to generate interview questions.")

with tab4:
    st.header("👁️ Resume Preview & Download")
    
    if st.session_state.resume_data:
        data = st.session_state.resume_data
        
        # Convert photo to base64
        photo_base64 = ""
        if data.get('photo'):
            photo_base64 = base64.b64encode(data['photo']).decode()
        
        # Generate HTML
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
                    line-height: 1.8;
                }}
                .contact a {{
                    color: #2980b9;
                    text-decoration: none;
                    font-weight: 500;
                }}
                .contact a:hover {{
                    text-decoration: underline;
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
                .project-desc {{
                    margin-top: 5px;
                    text-align: justify;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                {f'<img src="data:image/png;base64,{photo_base64}" class="profile-photo">' if photo_base64 else ''}
                <h1>{data.get('name', 'Your Name')}</h1>
            </div>
            <div class="contact">
                {f"{data.get('location', '')}" if data.get('location') else ''}
                {f" | {data.get('phone', '')}" if data.get('phone') else ''}
                {f" | {data.get('email', '')}" if data.get('email') else ''}
                {f" | <a href='{data.get('linkedin')}' target='_blank'>LinkedIn</a>" if data.get('linkedin') else ''}
                {f" | <a href='{data.get('github')}' target='_blank'>GitHub</a>" if data.get('github') else ''}
                {f" | <a href='{data.get('portfolio')}' target='_blank'>Portfolio</a>" if data.get('portfolio') else ''}
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
        
        if data.get('projects') and len(data['projects']) > 0:
            resume_html += "<div class='section'><h2>Key Projects</h2>"
            for proj in data['projects']:
                resume_html += f"""
                <div class="project">
                    <div class="project-name">{proj['title']}</div>
                    <p class="project-desc">{proj['description']}</p>
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
        
        # Preview
        st.markdown("### 📄 Your Professional Resume")
        st.components.v1.html(resume_html, height=800, scrolling=True)
        
        # Download
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Resume (HTML)",
                data=resume_html,
                file_name=f"{data.get('name', 'resume').replace(' ', '_')}_ATS_Resume.html",
                mime="text/html",
                type="primary"
            )
        with col2:
            st.info("💡 **To convert to PDF:** Open the HTML file in a browser, press Ctrl+P, and select 'Save as PDF'")
        
        if st.session_state.get('selected_projects'):
            st.success(f"✅ Resume includes {len(st.session_state.selected_projects)} AI-selected projects optimized for your target role!")
    else:
        st.info("👈 Please complete Tab 1 (Fill Information) to generate your resume.")