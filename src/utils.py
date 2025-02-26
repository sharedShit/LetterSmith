from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI



# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("API_KEY")
# llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.9,
     google_api_key=api_key
)


template_for_extraction_jd = """This is the Job Description {job_description} extract only relevant information about Required Skills, Responsibilities, Job Title,Company Name
 ,Job Description or Role of candiadte in that job """
 
template_for_extraction_resume = """This is my Resume {resume} extract informations : Full name,Email Address , Phone Number , Experience ,Project Details, Skills ,Relevant Achievements
Certifications  and arrange them properly in the response. Important you should not miss any single detail from resume."""

template_final = """I am applying for a job and the description of job is {job_description_result} and details about my carrer {resume_result}
Please generate a well-structured, detailed, and personalized cover letter that highlights my skills, experience, and enthusiasm for this role.
###Instructions for the LLM:
Most Important: Use the job details to frame my skills, experience and my Projects in a way that makes me the perfect candidate.
Strictly Donot mention any other skill or experience that is not mentioned in my resume.
Do not write Company Address at the top start from Dear Hiring manager.
Use Company's name  whereever it is required donot just use "orginization"
Resonate my experience and skills with the job responsibilities and requirements provided.
Demonstrate how my background aligns with the company’s needs and how I can add value.

Use a professional but natural tone that aligns with my industry and career goals.

Write my full name ,email address and phone number at the end.
Use all of the above imformation to completely fill up the cover letter.
Ensure the letter is concise but impactful, around 250-350 words.
"""
# """Structure the cover letter with an engaging opening, a strong body showcasing skills and achievements, and a compelling closing statement."""

def generate_job_description(data):
  prompt = PromptTemplate.from_template(template_for_extraction_jd)
  chain_job_description = prompt | llm
  response = chain_job_description.invoke({"job_description": data})
  return response

def generate_resume_details (data):
  prompt = PromptTemplate.from_template(template_for_extraction_resume)
  chain_resume = prompt | llm
  response = chain_resume.invoke({"resume": data})
  return response

def generate_cover_letter_new(job_description,resume):
  job_description_result = generate_job_description(job_description)
  resume_result   = generate_resume_details(resume)
#   return """Tejaswee Kumar Singh
# /githubtejas122125 | /linkedin-intejaswee-singh
# /envel⌢petejasweekumarsingh@gmail.com | ♂phone+91 7205147088 | ♂¶ap-pinRourkela, India
# EDUCATION
# IIIT Bhubaneshwar Odisha,India
# Bachelor of Technology in Computer Science and Engineering Post 4th Semester (CGPA: 8.62/10) 2022 - 2026
# ODM Public School Bhubaneswar,Odisha,India
# 12th Board 96 % 2020 - 2022
# EXPERIENCE
# Intel Unnati Industrial Training Program May 2024 - June 2024
# •Developed a project that solved real world problems like automatic EDA, pattern and Insights generation
# from structured data fastening process of data analysis,under the guidance of industry experts from intel.
# •Gained hands on experience in AI, LLM, AWS and Machine Learning from industry experts.
# PROJECTS
# Insights Masters
# A web app to help in the task of data analysis
# •Developed a web app that incorporated automatic exploratory data analysis and preprocessing, delivering
# visual charts and generating actionable insights from datasets exceeding 6 million records while
# collaborating with Intel industry experts..
# •Engineered a robust QA bot capable of interpreting complex inquiries from large datasets while producing
# insightful visual representations,powered by Gemini LLM and Langchain library .
# •Deployed backend functionality using AWS services that reduced insights generation time by 50%
# making it secure and reliable for large datasets.
# Under-Water Image Enhancement
# A modified version of famous U-net architecture with DepthWise Convulutional layer and CBAM layers.
# •Pre-processed distorted underwater images to improve visibility and clarity by 39.57 % using WB
# balancing, unsharp masking and CLAHE .
# •Modified U-Net Architecture by using DepthWise Convulutional Layers and CBAM layers. These
# modification reduced the primary model size by 70% and trained with 10,000 images dataset.
# Football player performance analysis
# A fine tuned YOLO model for real time football player performance analysis
# •Implemented transfer learning from a state of art YOLO object detection model and fine-tuned it on
# custom dataset of 600 images.
# •Extracted key metrics like player’s speed,total distance and successful passes with real time tracking of
# players and football.
# TECHNICAL-SKILL
# •Programming Languages: C, C++,Go Lang, Python, JavaScript, Typescript, HTML5
# •Libraries & Frameworks: TensorFlow, Nodejs, Reactjs, Langchain
# •Tools & Technologies: Git, MLFlow, Docker, AWS,Apache, Kafka
# •Databases: MongoDB,PostgreSQL
# HONORS
# Finalist in International Bit N Build Hackathon 2024
# Fr. Conceicao Rodrigues College of Engineering
# Volunteering
# AI-ML Associate 2023 - 2024
# GDSC,IIIT Bhubaneswar
# heloooooooooo """

  prompt = PromptTemplate.from_template(template_final)
  chain_cover_letter = prompt | llm
  response = chain_cover_letter.invoke({"job_description_result": job_description_result,"resume_result":resume_result})
  print("testing",type(response))
  return response.content
