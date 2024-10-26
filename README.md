# Youtube Live Chat Monitor
Copy messages from Youtube live chat to a Google spreadsheet.

## Getting Started
1. Create a GCP service account, generate a key and download a JSON file, name it as `creds.json`.
2. Add above service account's email address to the spreadsheet as as editor. This service account will provide write access to this program for posting messages.
   
3. Create a config.conf file and populate following values:
   ```
   [GoogleSheets]
   creds_path = ./creds.json
   spreadsheet_name = # spreadsheet name
   worksheet_name = # worksheet name

   [YouTube]
   video_id = # video  id

   [Application]
   excluded_author = # youtube channel's username, for excluding messages posted by the author to the sheet
   ```
   
4. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   pip install pytchat gspread oauth2client emoji
   ```

5. Start the program:
   ```
   source venv/bin/activate
   python main.py
   ```
