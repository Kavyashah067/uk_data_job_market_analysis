from analysis import (
    load_data,
    basic_eda,
    clean_date_column,
    clean_salary_column,
    analyze_jobs_and_locations,
    extract_skills,
    analyze_skills,
    plot_top_skills,
    plot_top_paying_skills,
    plot_salary_distribution,
    plot_salary_boxplot,
    plot_salary_by_location,
    feature_engineering,
    plot_remote_salary_comparison,
    plot_skill_salary_correlation,
    save_cleaned_dataset
)

from sql_setup import create_database, export_tables_to_csv
from sql_queries import (
    avg_salary_per_skill,
    remote_salary_comparison,
    top_paying_job_titles,
    top_in_demand_skills,
    highest_paying_skill,
    plot_top_skills
)


DATA_PATH = "data/uk_data_jobs_raw.csv"


def run_full_analysis():
    df = load_data(DATA_PATH)
    basic_eda(df)

    df = clean_date_column(df)
    df = clean_salary_column(df)

    analyze_jobs_and_locations(df)

    skills_exploded = extract_skills(df)
    skill_counts = analyze_skills(skills_exploded)

    plot_top_skills(skill_counts)
    plot_top_paying_skills(skills_exploded)
    plot_salary_distribution(df)
    plot_salary_boxplot(df)
    plot_salary_by_location(df)

    df = feature_engineering(df)
    plot_remote_salary_comparison(df)

    plot_skill_salary_correlation(skills_exploded)

    save_cleaned_dataset(df)

    return df


def run_sql_setup():
    df = load_data(DATA_PATH)
    df = clean_date_column(df)
    df = clean_salary_column(df)
    df = feature_engineering(df)

    # Create unique job_id
    df = df.reset_index(drop=True)
    df["job_id"] = df.index + 1

    create_database(df)
    export_tables_to_csv()


def run_sql_analysis():
    print("\nSQL Analysis Options:")
    print("1. Average Salary Per Skill")
    print("2. Remote vs Non-Remote Salary Comparison")
    print("3. Top 10 Highest Paying Job Titles")
    print("4. Top 10 Most In-Demand Skills")
    print("5. Highest Paying Skill")
    print("6. Visualize Top Skills")

    choice = input("Select an option: ")

    if choice == "1":
        result = avg_salary_per_skill()
        print("\nTop Skills by Average Salary:\n")
        print(result.head(10))

    elif choice == "2":
        result = remote_salary_comparison()
        print("\nRemote vs Non-Remote Salary Summary:\n")
        print(result)

    elif choice == "3":
        result = top_paying_job_titles()
        print("\nTop 10 Highest Paying Job Titles:\n")
        print(result)

    elif choice == "4":
        result = top_in_demand_skills()
        print("\nTop 10 Most In-Demand Skills")
        print(result)

    elif choice == "5":
        result = highest_paying_skill()
        print("\nHighest Paying Skill:\n")
        print(result)

    elif choice == "6":
        plot_top_skills()

    else:
        print("Invalid option.")

def main_menu():
    print("\n===== UK Data Job Market Analysis =====")
    print("1. Run Full Analysis")
    print("2. Setup SQLite Database")
    print("3. Run SQL Analysis")
    print("4. Exit")

    choice = input("\nSelect an option (1-4): ")

    if choice == "1":
        run_full_analysis()

    elif choice == "2":
        run_sql_setup()

    elif choice == "3":
        run_sql_analysis()

    elif choice == "4":
        print("Exiting program.")
        exit()

    else:
        print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    while True:
        main_menu()

