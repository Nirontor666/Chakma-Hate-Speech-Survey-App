import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import time

# --- CONFIGURATION ---
SHEET_ID = "1exBP62qJfJTSxMT9m0khF439IFmzxIL1klflRaH8hyQ"
BATCH_SIZE = 50
TOTAL_COMMENTS = 10000
# Make sure "ADMIN_PASSWORD" is set in your .streamlit/secrets.toml file
ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"] 

# 🔴 PASTE YOUR YOUTUBE VIDEO LINK HERE 🔴
INSTRUCTION_VIDEO_URL = "https://youtu.be/amVz26U0wkM?si=_FjPoOFBo90vyJJK" 

# Page Config
st.set_page_config(page_title="Chakma Hate Speech Survey", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stRadio > label {font-weight: bold; font-size: 16px;}
    .block-container {padding-top: 2rem;}
    .success-msg {color: green; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def init_connection():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    return client

def get_data():
    client = init_connection()
    sh = client.open_by_key(SHEET_ID)
    worksheet = sh.sheet1
    data = worksheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    return df, worksheet

# --- LOGIC FUNCTIONS ---
def find_available_batch(df, username):
    total_rows = len(df)
    total_batches = (total_rows // BATCH_SIZE) + (1 if total_rows % BATCH_SIZE > 0 else 0)

    for batch_idx in range(total_batches):
        start_row = batch_idx * BATCH_SIZE
        end_row = min((batch_idx + 1) * BATCH_SIZE, total_rows)

        batch_df = df.iloc[start_row:end_row]

        u1_filled = batch_df['User1_Option_1'].str.strip().astype(bool).any()
        u1_user = batch_df['User1_Name'].iloc[0]

        u2_filled = batch_df['User2_Option_1'].str.strip().astype(bool).any()
        u2_user = batch_df['User2_Name'].iloc[0]

        u3_filled = batch_df['User3_Option_1'].str.strip().astype(bool).any()
        u3_user = batch_df['User3_Name'].iloc[0]

        if username in [u1_user, u2_user, u3_user]:
            continue

        if not u1_filled:
            return batch_idx, 1
        elif not u2_filled:
            return batch_idx, 2
        elif not u3_filled:
            return batch_idx, 3
            
    return None, None

def save_batch_data(worksheet, batch_idx, slot_num, username, answers):
    start_row = (batch_idx * BATCH_SIZE) + 2
    
    if slot_num == 1:
        col_start = 2
    elif slot_num == 2:
        col_start = 5
    elif slot_num == 3:
        col_start = 8
    else:
        return False

    cells_to_update = []
    
    for i, ans in enumerate(answers):
        row = start_row + i
        cells_to_update.append(gspread.Cell(row, col_start, username))
        cells_to_update.append(gspread.Cell(row, col_start + 1, ans['hate_label']))
        cells_to_update.append(gspread.Cell(row, col_start + 2, ans['mixed_label']))

    try:
        worksheet.update_cells(cells_to_update)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# --- USER INTERFACE ---
def user_interface():
    st.header("📝 Chakma Hate Speech Survey")
    
    # --- CHANGED SECTION: VIDEO INSTEAD OF MARKDOWN ---
    st.subheader("📋 Instructions / নির্দেশাবলী")

    # Change muted=False to muted=True
    st.video(INSTRUCTION_VIDEO_URL, autoplay=True, muted=False)
    st.caption("🔊 Tap the video volume icon to unmute.")

    # -------------------------------------------------

    if 'username' not in st.session_state:
        st.info("Please enter your name to start.")
        
        username_input = st.text_input("Enter Username", key="login_input")

        if st.button("Enter"):
            if username_input.strip() == "":
                st.error("Please type a username.")
            else:
                st.session_state['username'] = username_input.strip()
                st.rerun()
        return

    username = st.session_state['username']
    st.write(f"Logged in as: **{username}**")
    
    with st.spinner("Loading Survey Data..."):
        try:
            df, worksheet = get_data()
        except Exception:
            st.error("Failed to connect to Database. Please check internet connection.")
            return

    if 'current_batch' not in st.session_state:
        batch_idx, slot_num = find_available_batch(df, username)
        if batch_idx is None:
            st.success("🎉 All comments have been annotated! Thank you.")
            return
        st.session_state['current_batch'] = batch_idx
        st.session_state['current_slot'] = slot_num
    
    batch_idx = st.session_state['current_batch']
    slot_num = st.session_state['current_slot']
    
    start_row = batch_idx * BATCH_SIZE
    end_row = min((batch_idx + 1) * BATCH_SIZE, len(df))
    batch_data = df.iloc[start_row:end_row]

    st.info(f"You are annotating Batch #{batch_idx + 1} (Comments {start_row + 1} - {end_row})")
    st.warning("⚠️ If you close the browser before clicking 'Submit Batch', your progress will not be saved.")

    with st.form(key='annotation_form'):
        answers = []
        all_answered = True
        
        for idx, row in batch_data.iterrows():
            st.markdown(f"---")
            st.markdown(f"**Comment {idx + 1}:**")
            st.subheader(f"🗣️ {row['Original text']}")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                choice = st.radio(
                    "Select Category (Mandatory):",
                    options=["hate speech", "non-hate speech"],
                    index=None,
                    key=f"radio_{idx}",
                    horizontal=True
                )
            
            with col2:
                is_mixed = st.checkbox(
                    "Contains Mixed/Banglish words/others?",
                    key=f"check_{idx}"
                )
                mixed_val = "mixed word" if is_mixed else ""

            if choice is None:
                all_answered = False
            
            answers.append({
                'hate_label': choice,
                'mixed_label': mixed_val
            })

        st.markdown("---")
        submit_btn = st.form_submit_button("✅ Submit Batch", type="primary")

        if submit_btn:
            if not all_answered:
                st.error("❌ You must select a category for all comments.")
            else:
                with st.spinner("Saving..."):
                    success = save_batch_data(worksheet, batch_idx, slot_num, username, answers)
                    if success:
                        st.balloons()
                        st.success("Batch Submitted Successfully!")
                        time.sleep(2)
                        del st.session_state['current_batch']
                        st.cache_data.clear()
                        st.rerun()

# --- ADMIN INTERFACE ---
def admin_interface():
    st.header("🛡️ Admin Dashboard")
    
    password = st.text_input("Admin Password", type="password")

    if "admin_ok" not in st.session_state:
        if st.button("Enter"):
            if password == ADMIN_PASSWORD:
                st.session_state["admin_ok"] = True
                st.rerun()
            else:
                st.error("Incorrect password")
        return

    # Admin content
    st.success("Access Granted")

    if st.button("🔄 Refresh Data"):
        st.cache_resource.clear()
        st.rerun()

    try:
        df, _ = get_data()
        
        total_filled_u1 = df['User1_Option_1'].str.strip().astype(bool).sum()
        total_filled_u2 = df['User2_Option_1'].str.strip().astype(bool).sum()
        total_filled_u3 = df['User3_Option_1'].str.strip().astype(bool).sum()
        total_annotations = total_filled_u1 + total_filled_u2 + total_filled_u3
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Comments", len(df))
        col2.metric("Total Annotations", total_annotations)
        col3.metric("Completion %", f"{(total_annotations / (len(df)*3)) * 100:.2f}%")
        
        st.subheader("Raw Data Preview")
        st.dataframe(df)
        
        st.subheader("Download Data")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
            csv,
            "chakma_survey_results.csv",
            "text/csv",
            key='download-csv'
        )
        
        st.subheader("Active Users")
        users = pd.concat([df['User1_Name'], df['User2_Name'], df['User3_Name']]).unique()
        users = [u for u in users if u]
        st.write(users)

    except Exception as e:
        st.error(f"Error loading admin data: {e}")

# --- MAIN APP ---
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["User Survey", "Admin Login"])
    
    if page == "User Survey":
        user_interface()
    else:
        admin_interface()

if __name__ == "__main__":
    main()