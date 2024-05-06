import csv
import tkinter as tk
import pandas as pd
import re

import application_filler

class LinkedInJobScraperApp:
    def __init__(self, root, data):
        self.root = root
        self.root.title("LinkedIn Job Scraper")
        self.data = data
        keywords_to_filter = []

        # Read skills from file
        with open('./data/filter_data/exclude.txt', 'r') as file:
            # Read each line (skill) from the file
            for line in file:
                # Remove leading and trailing whitespaces and append the skill to the list
                keywords_to_filter.append(line.strip())

        keywords_to_filter_title = [
            "lead", "sr", "senior", "qa", "qa", "sr.", "analyst", "mandarin", "mobile", "asp.net", ".net", "c#", "php", "TS/SCI", "principal", "iot", "golang"
        ]

        keywords_to_filter_company = [
            "accenture","microsoft", "state farm", "apple", "oracle", "arkansas blue cross blue shield", "tiktok"
        ]

        # Initialize an empty list to store skills
        self.skills_to_highlight = []

        # Read skills from file
        with open('./data/filter_data/include.txt', 'r') as file:
            # Read each line (skill) from the file
            for line in file:
                # Remove leading and trailing whitespaces and append the skill to the list
                self.skills_to_highlight.append(line.strip())

        df = pd.DataFrame(data)
        self.filtered_df = df[
            df['description'].apply(lambda x:not any(keyword.lower() in str(x).lower() for keyword in keywords_to_filter))
        ].to_dict('records')
        self.filtered_df = [job for job in self.filtered_df
                            if job['job_url'] not in self.load_shown_job_urls()]

        # Define a function to check if any word in the title is in the keywords_to_filter_title list
        def should_filter_title(title_words, keywords_to_filter):
            for word in title_words:
                if word.lower() in keywords_to_filter:
                    return True
            return False

        # Filter the DataFrame based on individual words in the title
        filtered_jobs = []
        for job in self.filtered_df:
            title_words = job['title'].lower().split()  # Split title into words
            if not should_filter_title(title_words, keywords_to_filter_title):
                filtered_jobs.append(job)

        # Assign the filtered list back to self.filtered_df
        self.filtered_df = filtered_jobs
        self.filtered_df = [job for job in self.filtered_df
                            if str(job['company']).lower() not in keywords_to_filter_company]
        # List to store approved job descriptions
        self.approved_jobs = []

        self.current_index = 0

        self.skills_to_add_resume = set()

        # Create GUI components
        self.include_text = tk.Text(self.root, height=1, width=30)
        self.include_text.pack(side=tk.TOP, padx=1, pady=1)

        self.include_button = tk.Button(self.root, text="Include", command=self.include_keywords)
        self.include_button.pack(side=tk.TOP, padx=1, pady=1)

        self.exclude_text = tk.Text(self.root, height=1, width=30)
        self.exclude_text.pack(side=tk.TOP, padx=1, pady=1)

        self.exclude_button = tk.Button(self.root, text="Exclude", command=self.exclude_keywords)
        self.exclude_button.pack(side=tk.TOP, padx=1, pady=1)

        self.job_text = tk.Text(self.root, height=30, width=170)  # Full-screen size
        self.job_text.pack(pady=1)

        self.highlight_count_text = tk.Text(self.root, height=8, width=50)
        self.highlight_count_text.pack(pady=10)

        # Data Button
        self.data_button = tk.Button(self.root, text="Data", command=lambda param="Data": self.approve_job(param))
        self.data_button.pack(side=tk.LEFT, padx=20)

        # Backend Button
        self.backend_button = tk.Button(self.root, text="Backend", command=lambda param="Backend": self.approve_job(param))
        self.backend_button.pack(side=tk.LEFT, padx=20)


        self.reject_button = tk.Button(self.root, text="Reject", command=self.reject_job)
        self.reject_button.pack(side=tk.RIGHT, padx=20)

        self.show_job()

    # Function to include keywords
    # Function to include keywords
    def include_keywords(self):
        include_keyword = self.include_text.get("1.0", tk.END).replace("\n","")
        self.skills_to_highlight.append(include_keyword)
        self.skills_to_add_resume.add(include_keyword)
        with open('./data/filter_data/include.txt', 'a') as file:
            file.write(include_keyword + '\n')
        # Clear the include text field
        self.include_text.delete("1.0", tk.END)

    # Function to exclude keywords
    def exclude_keywords(self):
        exclude_keyword = self.exclude_text.get("1.0", tk.END)
        with open('./data/filter_data/exclude.txt', 'a') as file:
            file.write(exclude_keyword)
        # Clear the exclude text field
        self.exclude_text.delete("1.0", tk.END)
        self.update_filtered_df()

    def update_filtered_df(self):
        df = pd.DataFrame(self.data)
        keywords_to_filter = []

        with open('./data/filter_data/exclude.txt', 'r') as file:
            for line in file:
                keywords_to_filter.append(line.strip())

        keywords_to_filter_title = [
            "lead", "sr", "senior", "QA Engineer", "QA", "C++ Developer"
        ]

        self.filtered_df = df[
            df['description'].apply(lambda x:not any(keyword.lower() in x.lower() for keyword in keywords_to_filter))
        ].to_dict('records')
        self.filtered_df = [job for job in self.filtered_df
                            if job['job_url'] not in self.load_shown_job_urls()]
        self.filtered_df = [job for job in self.filtered_df
                            if job['title'] not in keywords_to_filter_title]
        self.current_index = 0

    def load_shown_job_urls(self):
        try:
            with open('./data/shown_jobs.txt', 'r') as f:
                return f.read().splitlines()
        except FileNotFoundError:
            return []

    def save_shown_job_url(self, job_url):
        with open('./data/shown_jobs.txt', 'a') as f:
            f.write(job_url + '\n')

    def show_job(self):
        self.job_text.delete("1.0", tk.END)
        job_description = self.get_current_job_description()
        price = self.get_price()
        location = self.get_location()
        title = self.get_title()
        job_url = self.get_current_job_url()
        company = self.get_company()

        # Display job description
        self.job_text.insert(tk.END, job_description)

        # Highlight skills in yellow
        self.highlight_skills()

        self.highlight_sponsor_skills()

        # Count and display highlighted skills
        highlighted_count = self.count_highlighted_skills(job_description)
        self.highlight_count_text.delete("1.0", tk.END)
        self.highlight_count_text.insert(tk.END, f"Highlighted Skills: {highlighted_count} \n")
        self.highlight_count_text.insert(tk.END, f"Total count of skills: 42\n")
        self.highlight_count_text.insert(tk.END, f"{price} \n")
        self.highlight_count_text.insert(tk.END, f"Location: {location} \n")
        self.highlight_count_text.insert(tk.END, f"Title: {title} \n")
        self.highlight_count_text.insert(tk.END, f"Company: {company} \n")
        if job_url != "No more jobs to show!":
            self.save_shown_job_url(job_url)

    def highlight_skills(self):
        for skill in self.skills_to_highlight:
            start_index = "1.0"
            while True:
                # Search for the next occurrence of 'skill' starting from start_index
                pos = self.job_text.search(skill, start_index, stopindex=tk.END, nocase=True, exact=True)

                if not pos:
                    break

                # Calculate the end index of the found match
                end_index = f"{pos}+{len(skill)}c"

                # Retrieve the text at the found position
                text_at_pos = self.job_text.get(pos, end_index)

                # Check if the retrieved text matches 'skill' exactly (case-insensitive)
                if text_at_pos.lower() == skill.lower():
                    # Add a yellow highlight tag to the exact match
                    self.job_text.tag_add("highlight", pos, end_index)
                    self.job_text.tag_config("highlight", background="yellow")
                    self.skills_to_add_resume.add(skill)

                # Update the start_index to search for the next occurrence after the current match
                start_index = end_index

    def highlight_sponsor_skills(self):
        sponsor_keywords = ["sponsor", "sponsorship", "local", "contract"]  # List of keywords to highlight in blue

        for keyword in sponsor_keywords:
            start_index = "1.0"
            while True:
                # Search for the next occurrence of 'keyword' starting from start_index
                pos = self.job_text.search(keyword, start_index, stopindex=tk.END, nocase=True, exact=True)

                if not pos:
                    break

                # Calculate the end index of the found match
                end_index = f"{pos}+{len(keyword)}c"

                # Retrieve the text at the found position
                text_at_pos = self.job_text.get(pos, end_index)

                # Check if the retrieved text matches 'keyword' exactly (case-insensitive)
                if text_at_pos.lower() == keyword.lower():
                    # Add a blue highlight tag to the exact match
                    self.job_text.tag_add("highlight_blue", pos, end_index)
                    self.job_text.tag_config("highlight_blue", background="blue")

                # Update the start_index to search for the next occurrence after the current match
                start_index = end_index

    def count_highlighted_skills(self, text):
        count = 0
        for skill in self.skills_to_highlight:
            count += len(re.findall(f"(?i){re.escape(skill)}", text))
        return count

    def get_current_job_description(self):
        if self.current_index < len(self.filtered_df):
            job = self.filtered_df[self.current_index]
            return job['description']
        else:
            return "No more jobs to show!"

    def get_price(self):
        if self.current_index < len(self.filtered_df):
            job = self.filtered_df[self.current_index]
            return str(job["min_amount"]) + "\n" + str(job["max_amount"])
        else:
            return "No more jobs to show!"

    def get_location(self):
        if self.current_index < len(self.filtered_df):
            job = self.filtered_df[self.current_index]
            return job["location"]
        else:
            return "No more jobs to show!"

    def get_title(self):
        if self.current_index < len(self.filtered_df):
            job = self.filtered_df[self.current_index]
            return job["title"]
        else:
            return "No more jobs to show!"

    def get_current_job_url(self):
        if self.current_index < len(self.filtered_df):
            job = self.filtered_df[self.current_index]
            return job['job_url']
        else:
            return "No more jobs to show!"

    def get_company(self):
        if self.current_index < len(self.filtered_df):
            job = self.filtered_df[self.current_index]
            return job['company']
        else:
            return "No more jobs to show!"

    def read_data_core_skills(self):
        with open('data/core_skills/data.txt', 'r') as file:
            content = file.read()

        # Split the content by comma and store in an array
        skills_array = content.split(',')
        return set(skills_array)

    def read_backend_core_skills(self):
        with open('data/core_skills/backend.txt', 'r') as file:
            content = file.read()

        # Split the content by comma and store in an array
        skills_array = content.split(',')
        return set(skills_array)

    def approve_job(self, case):
        job = self.filtered_df[self.current_index]
        self.approved_jobs.append(job)
        if case == "Data":
            skills_core = self.read_data_core_skills()
        elif case == "Backend":
            skills_core = self.read_backend_core_skills()
        self.skills_to_add_resume = {skill.lower().strip() for skill in self.skills_to_add_resume}
        skills_core_lower = {skill.lower().strip() for skill in skills_core}
        final_skills = list(self.skills_to_add_resume - skills_core_lower)
        application_filler.upload(job, final_skills, case)
        self.skills_to_add_resume = set()
        self.current_index += 1
        self.show_job()


    def reject_job(self):
        self.skills_to_add_resume = set()
        self.current_index += 1
        self.show_job()

    def print_approved_jobs(self):
        # CSV file name
        filename = './data/output.csv'
        from datetime import datetime
        current_date = datetime.now().date()
        # Open CSV file for writing
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            for job in self.approved_jobs:
                writer.writerow([job['job_url'], job['company'], job['title'], job['location'],
                                 job['min_amount'], job['max_amount'], current_date])


def run(data):
    root = tk.Tk()
    app = LinkedInJobScraperApp(root, data)
    root.mainloop()

    # After the mainloop exits, print the approved jobs
    app.print_approved_jobs()
    application_filler.convert_all()


# Sample data
data = {
    'job_url': ['url1', 'url2', 'url3', 'url4'],
    'title': ['Senior Java Developer', 'React Developer', 'Backend Developer', 'Backend Developer'],
    'description': [
        'Senior Java Developer with 5 years of experience and Java skills',
        'React Developer with 6+ years of experience and JavaScript skills',
        'F Developer with Java and Python and Google Cloud Platform scalable',
        'F Developer with Java and Python requesting API GATEWAY information and OOP and GCP scala and requires sponsorship'
    ],
    'min_amount': [24,24,24,24],
    'max_amount': [28,28,28,24],
    'interval': ["hour","hour","hour","hour"],
    'location': ['IA','IA','IA','IA'],
    'company': ["C1","C1","C1","C1"]
}

#run(data)
