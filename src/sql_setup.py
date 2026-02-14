import sqlite3
import pandas as pd


def create_database(df, db_name="data_jobs.db"):

    conn = sqlite3.connect(db_name)

    # Rename columns for main jobs table
    df = df.rename(columns={
        "Job Title": "job_title",
        "Skills": "skills"
    })

    # Save main jobs table
    df.to_sql("jobs", conn, if_exists="replace", index=False)

    # Create normalized skills table
    skills_df = df.copy()
    skills_df["skills"] = skills_df["skills"].str.split(",")
    skills_df = skills_df.explode("skills")
    skills_df["skills"] = skills_df["skills"].str.strip()

    skills_df = skills_df[["job_title", "salary_avg", "skills"]]
    skills_df = skills_df.rename(columns={"skills": "skill"})

    skills_df.to_sql("job_skills", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print("Database created with tables: jobs, job_skills")


