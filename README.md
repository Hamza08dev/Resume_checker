# Resume Checker
### *Built by Mohammed Hamza for Tata AI Internship*


A web application to process resumes, extract relevant information, and provide valuable insights using AI-powered tools. The website is hosted at: https://resume-checker-erld.onrender.com/
<br><br>

![image](https://github.com/user-attachments/assets/dccd2bd6-1ddc-4d6e-9bc5-c05b104624d5)
![image](https://github.com/user-attachments/assets/64a2ed9f-3f67-40f8-adea-bf05eadf6388)

## Features

- Upload and process multiple resumes.
- Extract important details such as:
  - Name 
  - Contact details : as in the resume 
  - University 
  - Year of Study 
  - Course
  -  Discipline
  -  CGPA/Percentage
  -  Key Skills
  -  Gen AI Experience Score
  -  AI/ML Experience Score 
  -  Supporting Information (e.g., certifications, internships, projects)

- Download Excel sheet and view a summary report. 

## Usage

- Visit the hosted website: https://resume-checker-erld.onrender.com/.

- Upload one or more resumes in supported formats (PDF).

- Click "Process" to extract and download excel sheet.

- There is also a Data Summary option to quickly summarize the resumes.

## Technologies Used

<li><b>Backend</b>: Flask (Python)

<li><b>Frontend</b>: HTML, CSS, JavaScript

<li><b>AI Integration</b>: Cohere API

<li><b>Deployment</b>: Render

## Local Installation and Setup

### Prerequisites

<li>Python 3.10 or later
<li>pip (Python package manager)

### Steps

#### Clone the repository:

`git clone https://github.com/yourusername/Resume_checker.git`

`cd Resume_checker`

#### Create a virtual environment and activate it:
`python -m venv venv` 
`source venv/bin/activa te`

On Windows, use: `venv\Scripts\activate`

#### Install dependencies:

`pip install -r requirements.txt`

#### Set up the Cohere API key:

- Get your API key from Cohere.

- Create a .env file in the root directory and add your API key:

- COHERE_API_KEY=your_api_key_here

#### Run the application locally:

`python app.py`

The app will be available at http://localhost:5000.

