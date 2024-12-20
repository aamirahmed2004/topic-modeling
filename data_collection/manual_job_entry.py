# Script for manually entering job descriptions into the jobs.csv file
# Main functions: normalize whitespace, check for duplicates, replace some characters for better CSV presentation
# NOTE: for intentional duplicates (multiple job postings for the same role, e.g. different locations), just copy paste the rows manually 

from textacy import preprocessing

# Enter information into the following variables

company_name = "Intuit"    
job_title = "Senior AI/ML Software Engineer"
job_desc = """What You’ll Do

Apply statistical and machine learning techniques to process and analyze unstructured textual data
Develop and finetune machine learning models for tasks such as entity recognition, classification, and text generation
Utilize pretrained language models (e.g. GPT, LLAMA) and adapt them for specific use cases
Optimize the models for production usage, including considerations for scalability, latency, and resource
Monitor and refine deployed models for performance and efficiency, and conduct troubleshooting when necessary
Work closely with interdisciplinary teams to deliver high-quality features and solutions
Stay current with advancements in NLP research, methodologies, and best practices
Be consistently productive and operate with a high degree of autonomy

What You’ll Bring

A bachelor’s degree in Statistics, Computer Science, related technical field, or equivalent practical experience
A minimum of 6 years of experience in a quantitative role, with ideally much of that as a machine learning engineer or a data scientist
Knowledge of and expertise in Natural Language Processing (NLP)
Proficiency in a data query language (e.g. SQL), and a programming language (e.g. Python) 
Demonstrable experience with the full lifecycle of machine learning models - from development to deployment and monitoring
Being an excellent team player with a proven ability to work effectively in cross-functional teams, showing a high degree of collaboration, flexibility, and respect for diverse perspectives
An ability to be self-directed after work is assigned and help less experienced team members to get unblocked

An advanced degree (master or PhD) in a quantitative field
A deep understanding of deep learning, reinforcement learning, and natural language processing
Experience with cloud platforms such as AWS, Google Cloud, or Azure, and familiarity with related machine learning services
Experience with big data technologies like Hadoop, Spark, or similar
Demonstrated prior experience with large language models, and generative AI 
"""

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

