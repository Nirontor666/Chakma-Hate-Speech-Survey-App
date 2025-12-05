Chakma Hate Speech Annotation Survey

This is a Streamlit web application designed to collect annotations for Chakma language hate speech detection. It allows native speakers to label comments as "Hate Speech" or "Non-Hate Speech" and identify mixed-language content.

🌟 Key Features

Batching System: Automatically divides 10,000 comments into batches of 50.

Concurrency Control: Ensures the same batch is not annotated by more than 3 distinct users.

Crash Handling: Progress is safe until submission; if a user disconnects, the batch resets for others.

Admin Panel: Separate login to track progress and download results without modifying data.

Google Sheets Integration: Real-time database storage.

🛠️ Prerequisites

Windows 10/11

Python 3.8 or higher (You are using 3.13.5)

A Google Cloud Service Account JSON key

🚀 Installation & Setup

1. Project Setup

Open your terminal (Command Prompt or PowerShell) and navigate to your project folder:

cd D:\chakma_survey_app


2. Install Libraries

Run the following command to install the required Python packages:

pip install streamlit pandas gspread google-auth


3. Google Sheet Setup (CRITICAL STEP)

Most errors happen here. Follow these steps exactly:

Create a new Google Sheet at sheets.new.

Name it: Chakma_Final_Database (or similar).

Copy and Paste these exact headers into Row 1 (Cells A1 to J1):

Original text | User1_Name | User1_Option_1 | User1_Option_2 | User2_Name | User2_Option_1 | User2_Option_2 | User3_Name | User3_Option_1 | User3_Option_2


(Ensure each is in its own column, A through J).

Paste your 10,000 comments into Column A (Original text) starting from Row 2.

Click Share (top right) > Paste your Service Account Email:
chakma-annotations-sa@socialapp-e3e52.iam.gserviceaccount.com

Set permission to Editor > Click Send.

Copy the Sheet ID from the URL (the string between /d/ and /edit) and paste it into app.py at line 8: SHEET_ID = "...".

4. Secrets Configuration

Streamlit needs your API keys to talk to Google.

Create a folder named .streamlit inside your project folder.

Inside that folder, create a file named secrets.toml.

Paste your Google Service Account credentials into secrets.toml in this format:

[gcp_service_account]
type = "service_account"
project_id = "socialapp-e3e52"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "..."
client_id = "..."
# ... (add the rest of your JSON file content here)


▶️ Running the App

In your terminal, run:

streamlit run app.py


A browser window will open automatically.

🛡️ Admin Access

Navigation: Select "Admin Login" from the sidebar.

Password: Jamwa_tribal_adam_1984@ (Change this in app.py if needed).

Capabilities: View progress metrics, active users, and download the full dataset as CSV.

❓ Troubleshooting

Error

Solution

APIError: [400]... not supported

You are using an .xlsx (Excel) file. Create a new Google Sheet and copy your data there.

KeyError: 'User1_Option_1'

Your Google Sheet is missing headers. Copy the headers listed in Step 3 above into Row 1.

gspread.exceptions.SpreadsheetNotFound

The SHEET_ID in app.py is wrong OR you haven't shared the sheet with the Service Account email.

📦 Deployment (Streamlit Cloud)

Push your code to GitHub.

Connect your repository to Streamlit Community Cloud.

In the Streamlit Cloud dashboard, go to App Settings > Secrets.

Copy the contents of your local secrets.toml and paste them into the Cloud Secrets area.