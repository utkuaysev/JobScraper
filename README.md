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

## Run
You can add keywords to include or exclude as well. Select the keyword and paste to the include or exclude textbox. Selected job descriptions will be saved to output.csv 
![image](https://github.com/utkuaysev/JobScraper/assets/33395066/849c7ab8-a1a4-4b1b-9597-7d6e6c74fe60)
