import os
import pdfplumber
import pandas as pd
from flask import Flask, render_template, request, send_file, redirect, url_for
import cohere
import re
import json
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["RESULTS_FOLDER"] = "results/"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESULTS_FOLDER"], exist_ok=True)


co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

def process_resumes(resume_files):
    results = []
    for file in resume_files:
        with pdfplumber.open(file) as pdf:
            text = ''.join(page.extract_text() for page in pdf.pages)
        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[
                {
                    "role": "user",
                    "content": f"Extract the following fields from the resume:\n"
                               f"- Name\n"
                               f"- Contact details\n"
                               f"- University\n"
                               f"- Year of Study\n"
                               f"- Course\n"
                               f"- Discipline\n"
                               f"- CGPA/Percentage\n"
                               f"- Key Skills\n"
                               f"- Supporting Information(e.g, certification, internships, projects)\n"
                               f"- Gen AI Experience Score (1-3)\n"
                               f"- AI/ML Experience Score (1-3)\n"
                               f"Provide the output as JSON.\n\n"
                               f"Resume Text: {text}",
                }
            ]
        )

        raw_text = response.message.content[0].text
        try:
            json_match = re.search(r'{.*}', raw_text, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group(0))
                results.append(extracted_data)
            else:
                print(f"No JSON found in response: {raw_text}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_files = request.files.getlist("resumes")
        resume_paths = []
        for file in uploaded_files:
            if file.filename.endswith(".pdf"):
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(file_path)
                resume_paths.append(file_path)

        extracted_data = process_resumes(resume_paths)
        df = pd.DataFrame(extracted_data)

        # Save Excel file in RESULTS_FOLDER with a unique name
        excel_path = os.path.join(app.config["RESULTS_FOLDER"], "Resume_Analysis.xlsx")
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        # Pass file_path to results.html
        return render_template("results.html", file_generated=True, file_path="Resume_Analysis.xlsx")

    return render_template("index.html")


@app.route("/results/<file_path>")
def results(file_path):
    file_url = os.path.join(app.config["RESULTS_FOLDER"], file_path)
    return render_template("results.html", file_path=file_path, file_url=file_url)

@app.route("/download/<file_path>")
def download(file_path):
    file_path_full = os.path.join(app.config["RESULTS_FOLDER"], file_path)
    try:
        return send_file(
            file_path_full,
            as_attachment=True,
            download_name="Resume_Analysis.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except FileNotFoundError:
        return "File not found. Please process resumes again."


@app.route("/summary")
def summary():
    excel_path = os.path.join(app.config["RESULTS_FOLDER"], "Resume_Analysis.xlsx")
    try:
        df = pd.read_excel(excel_path)
    except FileNotFoundError:
        return "No analysis data available. Please upload resumes first."

    # Ensure required columns exist
    required_columns = ["gen_ai_experience_score", "ai_ml_experience_score", "name", "key_skills"]
    for col in required_columns:
        if col not in df.columns:
            return f"Missing required column: {col}"

    # Find individuals with top scores
    top_gen_ai_score = df["gen_ai_experience_score"].max()
    top_gen_ai_people = df[df["gen_ai_experience_score"] == top_gen_ai_score]["name"].tolist()

    top_ai_ml_score = df["ai_ml_experience_score"].max()
    top_ai_ml_people = df[df["ai_ml_experience_score"] == top_ai_ml_score]["name"].tolist()

    # Basic visualization data
    summary = {
        "total_resumes": len(df),
        "top_gen_ai_score": top_gen_ai_score,
        "top_gen_ai_people": top_gen_ai_people,
        "top_ai_ml_score": top_ai_ml_score,
        "top_ai_ml_people": top_ai_ml_people,
        "key_skills": df["key_skills"].value_counts().head(5).to_dict(),
    }
    return render_template("summary.html", summary=summary)



if __name__ == "__main__":
    app.run(debug=True)

