import csv
from jobspy import scrape_jobs

from gui import run

jobs = scrape_jobs(
    site_name=["indeed","glassdoor"],
    search_term="Software Engineer",
    location="United States",
    results_wanted=100,
    hours_old=72, # (only Linkedin/Indeed is hour specific, others round up to days old)
    country_indeed='USA',  # only needed for indeed / glassdoor,
    linkedin_fetch_description=True,
    job_type="fulltime",
    offset=0
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
# jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_xlsx
run(jobs)