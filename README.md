# Job Search

Utility to help manage my job search.

1. Automate folder creation of folderfor each new job application following the naming schema of date_job_title
    * [DONE] Google Drive
    * [DONE] Locally 
2. Download the job description based on the title
3. Extract key informations such skills requried matches my interest and application deadline for example
    * [DONE] Define AI model API to use
    * Add validation to the extacted information (Pydantic)
4. Subscrib and extract new job applications automatically from preconfigured websites.
    * S1: Via email alarts: Sign up for their daily alarts after refining the search
    * S2: Sign up for their RSS feed if available
    * S3: Examin website for JSON
    * S4: Scape website using Playwright
5. Build a database to hold these information
6. Convert this app to use event driven architecture.


# Issues
1. Resolve relative urls to absolute urls such as in the case of citylitics
2. How to handle single page websites when the links are JS. Winnipeg City Jobs
3. [Done] Add regex to match in label in Playwright
4. Add support for next page navigation by increasing digits. Canada Post