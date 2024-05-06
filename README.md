# Guide: Updating Scraper and Data Filtering Processes

This guide outlines the steps to update your existing codebase. The updates include installation of required libraries, customization of the scraper for specific search terms and desired results based on hours old, updating files under core_skills, updating files under filter_data (keywords in the exclude discard job descriptions with these keywords, keywords in the include make them yellow), and updating it as a README file.

## Step 1: Installation of Required Libraries

Use the following command to install the libraries needed to run the project:

```bash
pip install -r requirements.txt
```
## Step 2: Scraper Customization
Update the scraper_jobspy.py file to customize it for specific search terms and desired results based on hours old.

## Step 3: Core Skills Update
Update the files under the core_skills directory to reflect the core skills of you.

## Step 4: Data Filtering Update
Update the files under the filter_data directory to filter out job descriptions with specific keywords (exclude) and highlight others in yellow (include). Identify relevant keywords and mark job descriptions based on these keywords.
## Step 5: Resume Update
In the current version, there is an opportunity to use different resumes for various job descriptions. If you want to save a job to apply, you can click either 'data' or 'backend'. Whenever a button is clicked, it creates a new folder named [company] under data/company and places the specified version of the resume from the data/ directory. This feature can be extended by adding new buttons and providing new resumes.
## Run
You can add keywords to include or exclude as well. Select the keyword and paste to the include or exclude textbox. Selected job descriptions will be saved to output.csv 
![image](https://github.com/utkuaysev/JobScraper/assets/33395066/849c7ab8-a1a4-4b1b-9597-7d6e6c74fe60)
![image](https://github.com/utkuaysev/JobScraper/assets/33395066/b3d3ec69-4ca7-45bb-8c85-34542aae11b6)


