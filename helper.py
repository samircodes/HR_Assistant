import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import google.generativeai as genai
from openai import OpenAI
import PyPDF2
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_gemini_content(t_text,prompt):
    model=genai.GenerativeModel("gemini-1.0-pro")
    response= model.generate_content(prompt + t_text)
    return response.text

def prompt_response(prompt):
    """
    Calls the OpenAI API to generate a response based on the given prompt.
    
    Parameters:
    prompt : The prompt to send to the OpenAI API.
    
    Returns:
    The response from the OpenAI API.


    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
        ],
        temperature=0
    )
    
    response = completion.choices[0].message.content
    return response


def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text






