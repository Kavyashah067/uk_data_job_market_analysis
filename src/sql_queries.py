import sqlite3
import pandas as pd

DB_PATH = "data_jobs.db"


def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def avg_salary_per_skill():
    query = """
        SELECT
            skill,
            ROUND(AVG(salary_avg), 2) AS avg_salary,
            COUNT(*) AS job_count
        FROM job_skills
        WHERE salary_avg IS NOT NULL
        GROUP BY skill
        HAVING COUNT(*) >= 5
        ORDER BY avg_salary DESC;
    """
    return run_query(query)

def remote_salary_comparison():
    query = """
        SELECT
            is_remote,
            COUNT(*) AS job_count,
            ROUND(AVG(salary_avg), 2) AS avg_salary,
            ROUND(MIN(salary_avg), 2) AS min_salary,
            ROUND(MAX(salary_avg), 2) AS max_salary
        FROM jobs
        WHERE salary_avg IS NOT NULL
        GROUP BY is_remote
        ORDER BY avg_salary DESC;
    """
    return run_query(query)

def top_paying_job_titles():
    query = """
        SELECT
            job_title,
            COUNT(*) AS job_count,
            ROUND(AVG(salary_avg), 2) AS avg_salary
        FROM jobs
        WHERE salary_avg IS NOT NULL
        GROUP BY job_title
        HAVING COUNT(*) >= 5
        ORDER BY avg_salary DESC
        LIMIT 10;
    """
    return run_query(query)

def top_in_demand_skills():
    query = """
        SELECT
            skill,
            COUNT(*) AS demand_count
        FROM job_skills
        WHERE skill IS NOT NULL
        GROUP BY skill
        ORDER BY demand_count DESC
        LIMIT 10;
    """
    return run_query(query)

def highest_paying_skill():
    query = """
        SELECT
            skill,
            COUNT(*) AS job_count,
            ROUND(AVG(salary_avg), 2) AS avg_salary
        FROM job_skills
        WHERE salary_avg IS NOT NULL
        GROUP BY skill
        HAVING COUNT(*) >= 5
        ORDER BY avg_salary DESC
        LIMIT 1;
    """
    return run_query(query)

import matplotlib.pyplot as plt

def plot_top_skills():

    df = top_in_demand_skills()

    plt.figure()
    plt.barh(df["skill"], df["demand_count"])
    plt.xlabel("Demand Count")
    plt.ylabel("Skill")
    plt.title("Top 10 Most In-Demand Skills (SQL)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("screenshots/top_skills_sql.png", dpi=300)
    plt.show()
