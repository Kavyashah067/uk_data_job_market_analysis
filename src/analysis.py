import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# -------------------------------------------------
# CONFIG
# -------------------------------------------------
DATA_PATH = "data/uk_data_jobs_raw.csv"
OUTPUT_PATH = "output/cleaned_uk_data_jobs.csv"


# -------------------------------------------------
# DATA LOADING & BASIC EDA
# -------------------------------------------------
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print("Dataset loaded successfully")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    return df


# -------------------------------------------------
# EXPLORATORY DATA ANALYSIS
# -------------------------------------------------
def basic_eda(df: pd.DataFrame) -> None:
    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())


# -------------------------------------------------
# DATE CLEANING
# -------------------------------------------------
def clean_date_column(df: pd.DataFrame) -> pd.DataFrame:
    df["days_since_posted"] = (
        df["Date"]
        .str.replace("d", "", regex=False)
        .str.replace("+", "", regex=False)
    )

    df["days_since_posted"] = pd.to_numeric(
        df["days_since_posted"], errors="coerce"
    )

    print("\nDate cleaning completed")
    return df


# -------------------------------------------------
# SALARY CLEANING
# -------------------------------------------------
def clean_salary_column(df: pd.DataFrame) -> pd.DataFrame:
    df["salary_cleaned"] = (
        df["Salary"]
        .str.replace("£", "", regex=False)
        .str.replace("(Employer est.)", "", regex=False)
        .str.replace("(Glassdoor est.)", "", regex=False)
        .str.replace("\xa0", "", regex=False)
        .str.strip()
    )

    df["salary_type"] = df["salary_cleaned"].apply(
        lambda x: "hourly" if isinstance(x, str) and "Per Hour" in x else "yearly"
    )

    df["salary_cleaned"] = (
        df["salary_cleaned"]
        .str.replace("Per Hour", "", regex=False)
        .str.replace("PerHour", "", regex=False)
    )

    salary_split = df["salary_cleaned"].str.split("-", expand=True)

    df["salary_min"] = salary_split[0].str.strip()
    df["salary_max"] = salary_split[1].str.strip()

    df["salary_min"] = pd.to_numeric(
        df["salary_min"].str.replace("K", "", regex=False),
        errors="coerce"
    )

    df["salary_max"] = pd.to_numeric(
        df["salary_max"].str.replace("K", "", regex=False),
        errors="coerce"
    )

    df.loc[df["salary_type"] == "yearly", ["salary_min", "salary_max"]] *= 1000

    df["salary_max"] = df["salary_max"].fillna(df["salary_min"])
    df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2
    df = df[(df["salary_avg"] >= 20000) & (df["salary_avg"] <= 200000)]

    print("\nSalary cleaning completed")
    print("Overall average salary:", df["salary_avg"].mean())

    return df


# -------------------------------------------------
# AGGREGATE ANALYSIS
# -------------------------------------------------
def analyze_jobs_and_locations(df: pd.DataFrame) -> None:
    print("\nTop 10 Job Titles:")
    print(df["Job Title"].value_counts().head(10))

    print("\nTop 10 Locations:")
    print(df["Location"].value_counts().head(10))

    location_stats = (
        df.groupby("Location")
        .agg(
            job_count=("salary_avg", "count"),
            avg_salary=("salary_avg", "mean")
        )
        .query("job_count >= 5")
        .sort_values("avg_salary", ascending=False)
    )

    print("\nReliable Highest Paying Locations (min 5 jobs):")
    print(location_stats.head(10))


# -------------------------------------------------
# SKILLS ANALYSIS
# -------------------------------------------------
def extract_skills(df: pd.DataFrame) -> pd.DataFrame:
    skills_df = df.dropna(subset=["Skills", "salary_avg"]).copy()
    skills_df["Skills"] = skills_df["Skills"].str.split(",")

    skills_exploded = skills_df.explode("Skills")
    skills_exploded["Skills"] = (
        skills_exploded["Skills"]
        .str.strip()
        .str.lower()
    )

    return skills_exploded


def analyze_skills(skills_exploded: pd.DataFrame) -> pd.Series:
    skill_counts = skills_exploded["Skills"].value_counts()

    print("\nTop 15 Most In-Demand Skills:")
    print(skill_counts.head(15))

    skill_salary = (
        skills_exploded.groupby("Skills")
        .agg(
            job_count=("salary_avg", "count"),
            avg_salary=("salary_avg", "mean")
        )
        .query("job_count >= 20")
        .sort_values("avg_salary", ascending=False)
    )

    print("\nTop Paying Skills (min 20 jobs):")
    print(skill_salary.head(15))

    return skill_counts


# -------------------------------------------------
# VISUALIZATION
# -------------------------------------------------
def plot_top_skills(skill_counts: pd.Series) -> None:
    top_skills = skill_counts.head(10)

    plt.figure()
    top_skills.plot(kind="bar")
    plt.title("Top 10 Most In-Demand Skills")
    plt.xlabel("Skills")
    plt.ylabel("Count")
    plt.xticks(rotation=90)
    plt.tight_layout()

    
    # Save chart
    plt.savefig("screenshots/top_10_skills.png", dpi=300)

    plt.show()

def plot_top_paying_skills(skills_exploded: pd.DataFrame) -> None:
    skill_salary = (
        skills_exploded.groupby("Skills")
        .agg(
            job_count=("salary_avg", "count"),
            avg_salary=("salary_avg", "mean")
        )
        .query("job_count >= 20")
        .sort_values("avg_salary", ascending=False)
        .head(10)
    )

    plt.figure()
    skill_salary["avg_salary"].plot(kind="bar")
    plt.title("Top 10 Highest Paying Skills (min 20 jobs)")
    plt.xlabel("Skills")
    plt.ylabel("Average Salary (£)")
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.savefig("screenshots/top_paying_skills.png", dpi=300)

    plt.show()

# -------------------------------------------------
# SAVE FINAL DATASET
# -------------------------------------------------
def save_cleaned_dataset(df: pd.DataFrame) -> None:
    final_columns = [
        "Company",
        "Company Score",
        "Job Title",
        "Location",
        "days_since_posted",
        "salary_min",
        "salary_max",
        "salary_avg",
        "salary_type",
        "Skills"
    ]

    df[final_columns].to_csv(OUTPUT_PATH, index=False)
    print("\nFinal cleaned dataset saved successfully")


# -------------------------------------------------
# HISTOGRAM + KDE
# -------------------------------------------------
import seaborn as sns
import matplotlib.pyplot as plt

def plot_salary_distribution(
    df,
    salary_column='salary_avg',
    bins=30,
    figsize=(10,6),
    title="UK Data Job Salary Distribution"
):
    sns.set_style("whitegrid")
    plt.figure(figsize=figsize)

    sns.histplot(
        df[salary_column].dropna(),
        bins=bins,
        kde=True
    )

    plt.title(title, fontsize=14)
    plt.xlabel("Salary (£)")
    plt.ylabel("Job Count")
    plt.tight_layout()

    plt.savefig("screenshots/salary_distribution.png", dpi=300)

    plt.show()


# -------------------------------------------------
# BOX PLOT
# -------------------------------------------------
def plot_salary_boxplot(
    df,
    salary_column='salary_avg',
    figsize=(8,5),
    title="UK Data Job Salary Boxplot"
):
    sns.set_style("whitegrid")
    plt.figure(figsize=figsize)

    sns.boxplot(
        x=df[salary_column].dropna()
    )

    plt.title(title, fontsize=14)
    plt.xlabel("Salary (£)")
    plt.tight_layout()

    plt.savefig("screenshots/salary_boxplot.png", dpi=300)

    plt.show()


# -------------------------------------------------
# SALARY BY LOCATION PLOT
# -------------------------------------------------
def plot_salary_by_location(
    df,
    location_column='Location',
    salary_column='salary_avg',
    top_n=10,
    figsize=(10,6),
    title="Top 15 UK Locations by Average Salary"
):
    sns.set_style("whitegrid")

    top_locations = (
        df.groupby(location_column)[salary_column]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=figsize)

    sns.barplot(
        x=top_locations.values,
        y=top_locations.index
    )

    plt.title(title, fontsize=14)
    plt.xlabel("Average Salary (£)")
    plt.ylabel("Location")
    plt.tight_layout()

    plt.savefig("screenshots/salary_by_location.png", dpi=300)

    plt.show()


# -------------------------------------------------
# REMOTE VS NON REMOTE
# -------------------------------------------------
def feature_engineering(df):
    df['is_remote'] = df['Location'].str.contains(
        'Remote',
        case=False,
        na=False
    )
    return df

def plot_remote_salary_comparison(
    df,
    remote_column='is_remote',
    salary_column='salary_avg',
    figsize=(8,5),
    title="Remote vs Non-Remote Salary Comparison"
):
    sns.set_style("whitegrid")
    plt.figure(figsize=figsize)

    sns.boxplot(
        x=df[remote_column],
        y=df[salary_column]
    )

    plt.title(title, fontsize=14)
    plt.xlabel("Remote Role")
    plt.ylabel("Salary (£)")
    plt.tight_layout()

    plt.savefig("screenshots/remote_vs_nonremote.png", dpi=300)

    plt.show()


# -------------------------------------------------
# SKILL VS SALARY
# -------------------------------------------------
def plot_skill_salary_correlation(
    skills_df,
    skill_column='Skills',
    salary_column='salary_avg',
    min_jobs=30,
    top_n=10,
    figsize=(10,6),
    title="Top Paying Data Skills in the UK"
):
    sns.set_style("whitegrid")

    skill_stats = (
        skills_df.groupby(skill_column)[salary_column]
        .agg(['count', 'mean'])
        .query(f"count >= {min_jobs}")
        .sort_values('mean', ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=figsize)

    sns.barplot(
        x=skill_stats['mean'],
        y=skill_stats.index
    )

    plt.title(title, fontsize=14)
    plt.xlabel("Average Salary (£)")
    plt.ylabel("Skill")
    plt.tight_layout()

    plt.savefig("screenshots/skills_vs_salary.png", dpi=300)

    plt.show()

