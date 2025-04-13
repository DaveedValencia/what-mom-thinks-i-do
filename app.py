import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set page config with enhanced metadata
st.set_page_config(
    page_title="what mom thinks i do - Job Title Reality Check",
    page_icon="🔥",
    layout="centered",
    menu_items={
        'About': "# What I Actually Do\nThe job title reality check nobody asked for!\nCreated by David Valencia"
    }
)

# Initialize session state variables
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = time.time() - 10
if "request_count" not in st.session_state:
    st.session_state.request_count = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "job_title_input" not in st.session_state:
    st.session_state.job_title_input = ""

# Check for a job in query parameters
if "job" in st.query_params and not st.session_state.submitted:
    st.session_state.job_title_input = st.query_params["job"]
    st.session_state.submitted = True

# Function to handle job title submission
def submit_job():
    st.session_state.submitted = True

# Simple rate limiting function
def can_make_request():
    current_time = time.time()
    if current_time - st.session_state.last_request_time < 5:  # 5 second cooldown
        return False
    return True

# App title and description
st.title("What Mom Thinks I Do 🔥")
st.subheader("The job title reality check nobody asked for")

st.markdown("""
Enter your job title below and watch your career aspirations crumble in real-time! ✨  
Four POVs that will make you laugh, cry, and update your LinkedIn profile simultaneously.
""")

# Input field for job title
job_title = st.text_input(
    "Enter your job title:", 
    max_chars=100, 
    placeholder="e.g., Data Scientist, UX Designer, DevOps Engineer",
    on_change=submit_job,
    key="job_title_input"
)

# Generate response
if st.button("Generate job perspectives 🤔") or st.session_state.submitted:
    # Reset the submitted state for next use
    st.session_state.submitted = False
    
    if job_title:
        if can_make_request():
            with st.spinner("Generating your job reality check..."):
                try:
                    # Update rate limiting
                    st.session_state.last_request_time = time.time()
                    st.session_state.request_count += 1
                    
                    # Call the OpenAI API
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": """Create a humorous 'What I Actually Do' response for a job title with these four parts. Make sure each part is on its own lines with proper spacing between sections:

1. What my mom thinks I do:
Create a brief, funny quote (20-30 words) with emoji 🧓 from a loving boomer mom who's not tech-savvy but tries to understand. Use slightly outdated references, genuine pride, and practical concerns about benefits/stability.

2. What my friends think I do:
Create a brief, funny quote (20-30 words) with emoji 💻 that shows how friends typically overestimate or misunderstand the job's prestige, salary, or excitement.

3. What I think I do:
Write a brief, empowered self-perception statement (20-30 words) with emoji 🧠 using industry jargon and confidence.

4. What I actually do:
Create a humorous reality check (20-40 words) with emoji 🔥 describing mundane, frustrating, or absurd actual day-to-day tasks of the job.

Format exactly like this example with proper line breaks between each section and bold headers:
**What my mom thinks I do:**
🧓 "Are you still doing tech support?"

**What my friends think I do:**
💻 "He's probably making bank with some crypto startup."

**What I think I do:**
🧠 Mastermind of logistics, automation, and digital domination.

**What I actually do:**
🔥 Fix broken discount codes at 11 PM while refreshing FedEx tracking and eating dinner over a Slack huddle."""},
                            {"role": "user", "content": f"Create a 'What I Actually Do' response for: {job_title}"}
                        ],
                        max_tokens=400,
                        temperature=0.8
                    )
                    
                    # Extract the response
                    job_perspectives = response.choices[0].message.content
                    
                    # Display in a nice box with preserved formatting
                    st.success("### Your Job Reality:")
                    
                    # Ensure Markdown formatting is preserved with whitespace
                    formatted_perspectives = job_perspectives.replace("\n", "\n\n").replace("\n\n\n\n", "\n\n")
                    st.markdown(f"{formatted_perspectives}")
                    
                    # Add button to generate again
                    if st.button("Try another job title", key="try_again"):
                        # Clear the input field
                        st.session_state.job_title_input = ""
                        st.rerun()
                    
                except Exception as e:
                    st.error(f"Oops! Something went wrong. Please try again. Error: {str(e)}")
        else:
            st.warning(f"Please wait a moment before generating another response!")
    else:
        st.warning("Please enter your job title first! ✨")

# Footer
st.markdown("---")
st.markdown("""
**Created by David Valencia** - Follow me: [X](https://x.com/DaveedValencia) | [IG](https://instagram.com/DaveedValencia) 🚀  
<br>this project is opensource available on [GitHub](https://github.com/DaveedValencia/what-mom-thinks-i-do)
""")

# Sidebar meme content
st.sidebar.markdown("### Corporate Survival Guide")
st.sidebar.markdown("""
* **Monday morning**: When your soul leaves your body but your caffeine addiction shows up
* **LinkedIn**: Where everyone is a "visionary" despite doing the same tasks as you
* **"Let's circle back"**: Ancient spell to escape any conversation
* **"Per my last email"**: Professional way of saying "Can you read?"
* **"Quick call"**: A mythical 5-minute meeting that has never existed
* **Slack status**: The modern mood ring no one respects
* **"Just checking in"**: Your boss's way of asking why you haven't responded in 3.7 minutes
""")
