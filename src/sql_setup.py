import sqlite3
import pandas as pd


def create_database(df, db_name="data_jobs.db"):

    conn = sqlite3.connect(db_name)

    # Rename columns
    df = df.rename(columns={
        "Job Title": "job_title",
        "Skills": "skills"
    })

    # Main jobs table
    jobs_df = df.copy()
    jobs_df = jobs_df.drop(columns=["skills"])
    jobs_df.to_sql("jobs", conn, if_exists="replace", index=False)

    # Normalized skills table
    skills_df = df[["job_id", "job_title", "salary_avg", "skills"]].copy()
    skills_df["skills"] = skills_df["skills"].str.split(",")
    skills_df = skills_df.explode("skills")
    skills_df["skills"] = skills_df["skills"].str.strip()
    skills_df = skills_df.rename(columns={"skills": "skill"})

    skills_df.to_sql("job_skills", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print("Database rebuilt with proper job_id key.")


def export_tables_to_csv(db_name="data_jobs.db"):
    conn = sqlite3.connect(db_name)

    jobs_df = pd.read_sql_query("SELECT * FROM jobs", conn)
    skills_df = pd.read_sql_query("SELECT * FROM job_skills", conn)

    jobs_df.to_csv("output/jobs_table.csv", index=False)
    skills_df.to_csv("output/job_skills_table.csv", index=False)

    conn.close()
    print("Tables exported to output/ folder.")
