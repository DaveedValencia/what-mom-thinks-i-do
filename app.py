import streamlit as st
from openai import OpenAI
import os


# Get API key from environment variable
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize OpenAI client with error handling
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error(f"Failed to initialize OpenAI client: {str(e)}")
    st.stop()

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
# Removed last_request_time as it's no longer needed
if "request_count" not in st.session_state:
    st.session_state.request_count = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "job_title_input" not in st.session_state:
    st.session_state.job_title_input = ""
if "job_perspectives" not in st.session_state:
    st.session_state.job_perspectives = ""

# Check for a job in query parameters
if "job" in st.query_params and not st.session_state.submitted:
    st.session_state.job_title_input = st.query_params["job"]
    st.session_state.submitted = True

# Function to handle job title submission
def submit_job():
    st.session_state.submitted = True

# Always allow requests (no cooldown)
def can_make_request():
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
    on_change=submit_job
)

# Function to call OpenAI API with proper error handling
def generate_job_perspectives(job_title):
    try:
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
        return response.choices[0].message.content
    
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower():
            return "ERROR: Invalid or missing API key. Please check your OpenAI API key configuration."
        elif "rate limit" in error_msg.lower():
            return "ERROR: Rate limit exceeded. Please try again in a few moments."
        else:
            return f"ERROR: Could not generate response: {error_msg}"

# Generate response
if st.button("Generate job perspectives 🤔") or st.session_state.submitted:
    # Reset the submitted state for next use
    st.session_state.submitted = False
    
    if job_title:
        if can_make_request():
            with st.spinner("Generating your job reality check..."):
                # Only track request count, cooldown removed
                st.session_state.request_count += 1
                
                # Call the OpenAI API
                job_perspectives = generate_job_perspectives(job_title)
                
                # Store result in session state
                st.session_state.job_perspectives = job_perspectives
    else:
        st.warning("Please enter your job title first! ✨")

# Display results if available
if st.session_state.job_perspectives:
    if st.session_state.job_perspectives.startswith("ERROR:"):
        st.error(st.session_state.job_perspectives)
    else:
        # Display in a nice box with preserved formatting
        st.success("### Your Job Reality:")
        
        # Ensure Markdown formatting is preserved with whitespace
        formatted_perspectives = st.session_state.job_perspectives.replace("\n", "\n\n").replace("\n\n\n\n", "\n\n")
        st.markdown(f"{formatted_perspectives}")
        
        # Add button to generate again
        if st.button("Try another job title", key="try_again"):
            # Clear the input field and result
            st.session_state.job_title_input = ""
            st.session_state.job_perspectives = ""
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
**Created by David Valencia** - Follow me: [X](https://x.com/DaveedValencia) | [IG](https://instagram.com/DaveedValencia) 🚀  
opensource available on [GitHub](https://github.com/DaveedValencia/what-mom-thinks-i-do)
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
