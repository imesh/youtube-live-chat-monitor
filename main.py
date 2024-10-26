from datetime import datetime
import re
import pytchat
import gspread
import emoji
import time
import configparser
from oauth2client.service_account import ServiceAccountCredentials

# Load configuration
config = configparser.ConfigParser()
config.read("config.conf")

# Google Sheets setup using configuration file
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

creds_path = config["GoogleSheets"]["creds_path"]
spreadsheet_name = config["GoogleSheets"]["spreadsheet_name"]
worksheet_name = config["GoogleSheets"]["worksheet_name"]

creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)
spreadsheet = client.open(spreadsheet_name)
sheet = spreadsheet.worksheet(worksheet_name)

# YouTube Chat setup using configuration file
video_id = config["YouTube"]["video_id"]

def initialize_chat():
    """Initialize the YouTube chat object."""
    return pytchat.create(video_id=video_id)

def is_repeated_emoji_pattern(message):
    # Regular expression to match repeated emoji patterns
    pattern = re.compile(r'(:[\w_]+:)+')
    match = pattern.fullmatch(message)
    return match is not None

def post_to_google_sheet(timestamp, author, message):
    try:
        if is_repeated_emoji_pattern(message):
            print('Repeated emoji pattern, message excluded')
            return
        
        # Convert emoji shortcodes to Unicode characters
        message_with_emoji = emoji.emojize(message)
        # Combine author and message in one cell, separated by a newline
        combined_text = f"{author}\n{message_with_emoji}"
        row = [timestamp, combined_text]
        sheet.append_row(row)
    except Exception as e:
        print(f"Error posting to Google Sheet: {e}")

def main():
    excluded_author = config["Application"]["excluded_author"]

    while True:  # Retry loop
        chat = initialize_chat()  # Initialize chat at the start

        try:
            while True:
                if not chat.is_alive():
                    print("Chat disconnected, reinitializing...")
                    chat = initialize_chat()  # Reinitialize if chat disconnected
                
                for c in chat.get().items:
                    if c.author.name == excluded_author:
                        print(f"Excluded message from {excluded_author}")
                        continue

                    # Use the actual timestamp from the chat message
                    timestamp = datetime.strptime(c.datetime, "%Y-%m-%d %H:%M:%S").strftime("%I:%M")
                    post_to_google_sheet(timestamp, c.author.name, c.message)
                    print(f"{timestamp}: {c.author.name}: {c.message}")

        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting...")
            break  # Exit the outer while loop on Ctrl+C

        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)  # Wait before retrying
            print("Retrying...")

if __name__ == "__main__":
    main()
