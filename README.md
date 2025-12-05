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

Python 3.8 or higher

A Google Cloud Service Account JSON key

🚀 Installation & Setup

Project Setup

Open your terminal and navigate to your project folder:

cd D:\chakma_survey_app


Install Libraries

pip install streamlit pandas gspread google-auth


Google Sheet Setup (CRITICAL STEP)

Create a new Google Sheet.

Copy and paste these headers into Row 1 (A1 to J1):

Original text | User1_Name | User1_Option_1 | User1_Option_2 | User2_Name | User2_Option_1 | User2_Option_2 | User3_Name | User3_Option_1 | User3_Option_2


Paste your comments into Column A starting from Row 2.

Share the sheet with your Service Account email and give Editor permission.

Copy the Sheet ID from the URL and paste it into app.py at line 8:

SHEET_ID = "YOUR_SHEET_ID_HERE"


Secrets Configuration

Create a folder named .streamlit in your project folder.

Inside it, create secrets.toml with your Service Account credentials:

[gcp_service_account]
type = "service_account"
project_id = "YOUR_PROJECT_ID"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n..."
client_email = "YOUR_SERVICE_ACCOUNT_EMAIL"
client_id = "..."
# ... rest of JSON content


▶️ Running the App

streamlit run app.py


A browser window will open automatically.

🛡️ Admin Access

Navigation: Select "Admin Login" from the sidebar.

Password: Set in app.py as:

ADMIN_PASSWORD = "YOUR_NEW_PASSWORD"


Capabilities: View progress metrics, active users, and download the dataset as CSV.

❓ Troubleshooting

Error	Solution
APIError: [400]...	Use a Google Sheet instead of an Excel file.
KeyError: 'User1_Option_1'	Ensure headers are correctly in Row 1.
gspread.exceptions.SpreadsheetNotFound	Check the SHEET_ID and that the sheet is shared with the Service Account.

📦 Deployment (Streamlit Cloud)

Push your code to GitHub.

Connect your repository to Streamlit Community Cloud.

In the Streamlit Cloud dashboard, go to App Settings > Secrets and paste the contents of your secrets.toml.