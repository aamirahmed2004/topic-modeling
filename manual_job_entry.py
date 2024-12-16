# Script for manually entering job descriptions into the jobs.csv file
# Main functions: normalize whitespace, check for duplicates, replace some characters for better CSV presentation
# NOTE: for intentional duplicates (multiple job postings for the same role, e.g. different locations), just copy paste the rows manually 

from textacy import preprocessing

# Enter information into the following variables

company_name = "Orennia"   
job_title = "Data Engineer"
job_desc = """What You’ll Do 

Analyze, design, develop, test, review, document and troubleshoot data pipeline / ELT solutions against multiple structured and unstructured data sources.
Support our team of analysts through developing requirements and delivering solutions. 
Develop code to scrape public websites for data and perform ELT processes.
Maintain, monitor, and support production ELT processes and respond to error and emergency issues. 

 Who You Are 

You have excellent knowledge and experience with Big Data concepts like data lakes, data warehouses, ELT strategies, and best practices.
You have a strong understanding of relational and dimensional data modeling.
You possess strong analytical and problem-solving skills.
You have experience with DBT and SQL, and are proficent with Python.
You have extensive experience with cloud-based data processing and warehousing technologies (Databricks, Snowflake, etc)
You have experience with Lean and Agile development methodologies (such as Kanban or SCRUM).
You are comfortable in entrepreneurial, self-starting, and fast-paced environment, working both independently and with our highly skilled teams.
You have experience with other Big Data processing technologies and cloud services (AWS, GCP, Snowflake, Hive, Hadoop, MS SQL, etc.).
You have experience with JIRA and similar organizational tools.
You have experience building web-scraping tools against publicly available datasets (considered an asset).
You have experience with GIS/geospatial data processing, integration, and analysis is (considered an asset).
You have experience building or supporting data visualizations (considered an asset).
Deep intellectual curiosity with a results-focused relentless pursuit of answers. Ability to work in a fast-paced start-up environment, embrace change and ambiguity."""

job_desc = preprocessing.normalize.whitespace(job_desc.replace("\n", " "))
# Replace some characters which don't show up correctly in the CSV (not relevant to analysis, just for presentation)
job_desc = job_desc.replace("…", ":").replace("’", "'").replace("–", "-").replace("●", " ")

new_row = {
    "company_name": company_name,
    "job_title": job_title.replace(",", ""),                 # Some job titles have commas in them
}

# List of dictionaries, where each dictionary is a row
csv_rows = []
with open("jobs.csv", "r", encoding="UTF-8") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(",")
        # print(line)
        csv_rows.append({
            "company_name": line[0],
            "job_title": line[1],
        })
    
if new_row not in csv_rows:
    with open("jobs.csv", "a") as file:
        file.write(f"{new_row['company_name']}, {new_row['job_title']}, \"{job_desc}\"\n")

