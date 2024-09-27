import streamlit as st
import PyPDF2
from helper import generate_gemini_content, prompt_response, read_pdf

def main():
    st.set_page_config(page_title="HR Assistant for Interviews", page_icon=":briefcase:", layout="wide")

    # Main title
    st.title("HR Assistant for Interviews :briefcase:")

    # Instructions section
    st.markdown("""
        <style>
        .instructions {
            font-size: 18px;
            background-color: #f9f9f9;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        </style>
        <div class="instructions">
            Upload the job description and resume PDFs, then select the difficulty level to generate interview questions.
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state for storing generated questions
    if "generated_questions" not in st.session_state:
        st.session_state.generated_questions = ""

    # Layout
    col1, col2 = st.columns([2, 1])  # Adjusting the ratio to 2:1

    with col1:
        pdf_1 = st.file_uploader("Upload the Job Description", type=["pdf"], key="job_desc")
        pdf_2 = st.file_uploader("Upload the Resume", type=["pdf"], key="resume")
        skills = st.text_input("Write skills which you want to focus on:")
        difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"], index=1)

         # Display the generated questions even after the "Check Answer" button is clicked
        if st.session_state.generated_questions:
            st.subheader("Generated Interview Questions")
            st.write(st.session_state.generated_questions)

        if pdf_1 and pdf_2:
            with st.spinner("Processing PDFs..."):
                # Reading the PDF file
                job_d = read_pdf(pdf_1)
                resume = read_pdf(pdf_2)

            st.success("PDFs successfully processed!")

            if st.button("Form Questions"):
                with st.spinner("Generating interview questions..."):
                    prompt = f"""
                    I am providing you with a resume and the job description. Please formulate 10 interview questions 
                    based on the skills mentioned in the job description if it matches with the resume. First generate 3 {difficulty} level Coding questions with 3 test cases and their answers. Then start with these
                    mandatory skills {skills} then move to skills matching job description and resume. Organize the questions by topics starting with coding questions then mandatory skills then the topics should be according to the skills that matches resume and job description.
                    For each question, provide a detailed answer and adjust the difficulty of the questions to be {difficulty}.
    
                    The Job description is {job_d}. The resume is {resume}.
                    """

                    if skills:
                        prompt += f"\nFocus specifically on the following skills: {skills}."

                    sam = prompt_response(prompt)
                    st.session_state.generated_questions = sam  # Store generated questions in session state
                    st.subheader("Generated Interview Questions")
                    st.write(st.session_state.generated_questions)

        else:
            st.warning("Waiting for PDFs to be uploaded...")

    with col2:
        question = st.text_input("Enter the Question")
        test = st.text_input("Enter the Test cases")
        answer = st.text_area("Enter the Answer", height=150, key="answer_area")

        if st.button("Check Answer"):
            prompt2 = f"""I have a coding question and an answer I want to verify. Please check if the provided solution is correct and passes all the test cases.
            Coding Question: {question} , Test cases: {test} , The answer is {answer}."""
            sam2 = prompt_response(prompt2)
            st.subheader("Results")
            st.text_area("Questions and Answers", sam2, height=300, key="result_area")

       

if __name__ == "__main__":
    main()
