# app.py
import io
import os
import requests
from flask import Flask, make_response, send_file
from flask_restful import Api, Resource
from datetime import datetime
import pandas as pd
from scraper import Scraper
from listen import AnalyzeCall


# Authentication details# url input
connexone_api_url = "https://apigateway-balancedcomfortcoolingheatingandplumbing-cxm.cnx1.cloud/oauth2/token"
# url input
connexone_data_get_url = "https://apigateway-balancedcomfortcoolingheatingandplumbing-cxm.cnx1.cloud/voice/recording/{id}"
# headers input
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}
# client_id input adn other saved in .env
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
payload = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
}


# Function to authenticate and get the access token
def authenticate_and_get_token():
    try:
        response = requests.post(connexone_api_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for unsuccessful requests
        access_token = response.json().get("access_token")
        print("Token granted")
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error authenticating and getting token: {e}")
        return None

def save_audio_file(id, audio_data, folder_path, filename):
    try:
        # Check if the file already exists in the folder
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):
            print(f"File {filename} already exists in {folder_path}")
            return file_path

        # Save the audio data to a file
        audio_file_path = os.path.join(folder_path, filename)
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(audio_data)

        print(f"Audio file saved successfully at {audio_file_path}")
        return audio_file_path

    except Exception as e:
        print(f"Error saving audio file: {e}")
        return None

class PlaybackAudioResource(Resource):
    def get(self, id):
        audio_filename = f"audio_{id}.mp3"
        folder_path = os.path.abspath("./connex_audio_files")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        audio_file_path = os.path.join(folder_path, audio_filename)

        if os.path.exists(audio_file_path):
            print(f"Playback audio file {audio_filename} already exists")
            return send_file(audio_file_path, mimetype="audio/mpeg")

        access_token = authenticate_and_get_token()
        if access_token:
            data_get_headers = {
                "Authorization": f"Bearer {access_token}",
                "X-Authorization": f"Basic {os.environ.get('CXM_API_TOKEN')}",
            }
            try:
                response = requests.get(
                    connexone_data_get_url.format(id=id), headers=data_get_headers
                )
                response.raise_for_status()

                audio_data = response.content

                # Generate filename with customer, phone_number, and date
                date_obj = datetime.now()
                audio_filename = f"audio_{id}.mp3"  # Adjust as per your naming convention

                # Create folder path based on date (if needed)
                os.makedirs(folder_path, exist_ok=True)

                # Save the audio file
                saved_file_path = save_audio_file(id, audio_data, folder_path, audio_filename)
                if saved_file_path:
                    return send_file(saved_file_path, mimetype="audio/mpeg")
                else:
                    return {"error": "Failed to save audio file"}, 500

            except Exception as e:
                print(f"Error getting playback audio: {e}")
                return {"error": f"Failed to fetch sound waves - {e}"}, 500
        else:
            print("Failed to authenticate and get token.")
            return {"error": "Failed to authenticate and get token"}, 500

class ProcessExcelFile(Resource):
    def sanitize_filename(self, filename):
        # Replace invalid characters with underscores
        invalid_chars = ["|", ":", "\\", "/", "*", "?", '"', "<", ">", "| "]
        for char in invalid_chars:
            filename = filename.replace(char, "_")

        # Replace multiple underscores with a single underscore
        filename = "_".join(filename.split("_"))

        return filename

    def process_audio_file(self, row):
        file_id = row["File Name"]
        date_str = str(row["Date"])
        customer = row["Customer"]
        phone_number = row["Phone Number"]
        print(f"Processing file: {file_id}, Name: {customer}")

        try:
            access_token = authenticate_and_get_token()
            if access_token:
                data_get_headers = {
                    "Authorization": f"Bearer {access_token}",
                    "X-Authorization": f"Basic {os.environ.get('CXM_API_TOKEN')}",
                }

                response = requests.get(
                    connexone_data_get_url.format(id=file_id),
                    headers=data_get_headers
                )
                response.raise_for_status()

                audio_data = response.content

                # Generate filename with customer, phone_number, and date
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                audio_filename = self.sanitize_filename(
                    f"{customer}_{phone_number}_{date_obj.strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
                )

                # Create folder path based on date (if needed)
                folder_path = os.path.abspath(
                    os.path.join("./connex_audio_files/", date_obj.strftime("%Y-%m-%d"))
                )
                os.makedirs(folder_path, exist_ok=True)

                # Save the audio file
                saved_file_path = save_audio_file(file_id, audio_data, folder_path, audio_filename)
                if saved_file_path:
                    return saved_file_path
                else:
                    return None

            else:
                print("Failed to authenticate and get token.")

        except Exception as e:
            print(f"Error processing audio file: {e}")

        return None

    def get(self):
        try:
            # Load the Excel file
            excel_file_path = "./merged_file.xlsx"
            df = pd.read_excel(excel_file_path)

            for index, row in df.iterrows():
                saved_file_path = self.process_audio_file(row)
                if saved_file_path:
                    print(f"File saved at: {saved_file_path}")
                else:
                    print("Error processing audio file.")

        except Exception as e:
            print(f"Error processing Excel file: {e}")

        return {"message": "Audio files processed successfully."}

