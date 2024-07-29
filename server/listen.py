from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import assemblyai as aai
import json
from dotenv import load_dotenv
import os
import re
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Load terms from terms.json
try:
    with open('terms.json', 'r') as file:
        terms = json.load(file)
except FileNotFoundError:
    print("Error: terms.json file not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding terms.json: {str(e)}")

# Load environment variables
load_dotenv()

# Set your AssemblyAI API key
aai.settings.api_key = os.environ.get('ASSEMBLYAI_API_KEY')

def extract_appointment_date(text):
    date_pattern = r'(?:\b(?:on|at)\s*)?(\d{1,2}(?:st|nd|rd|th)?(?:\s*(?:of)?\s*\w+)?(?:,\s*\d{4})?)'
    time_pattern = r'(?:\bat\s*)?(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)'

    dates = re.findall(date_pattern, text, re.IGNORECASE)
    times = re.findall(time_pattern, text, re.IGNORECASE)

    if dates:
        parsed_dates = []
        for date_str in dates:
            try:
                parsed_date = datetime.strptime(date_str, '%d %B %Y')  # Example format: 14 July 2024
                parsed_dates.append(parsed_date)
            except ValueError:
                pass  # Handle other date formats if needed

        if parsed_dates:
            earliest_date = min(parsed_dates)
            return earliest_date.strftime('%d %B %Y')

    return None

# Text analysis function
def analyze_text(text, lemur_response, terms):
    text = text.lower()

    voicemail_phrases = [
        "voice message system",
        "message after the beep",
        "mailbox",
        "message after the tone",
        "voicemail",
        "you have reached the voicemail of"
    ]
    voicemail_detected = any(phrase in text for phrase in voicemail_phrases)

    active_listening = any(keyword in text for keyword in terms["brand_opportunity_terms"]["active listening"])
    empathy = any(keyword in text for keyword in terms["brand_opportunity_terms"]["empathy"])

    good_opening = any(keyword in text for keyword in ["hi", "hello", "welcome", "thank you for calling", "help", "assist"]) and "balanced comfort" in text

    upsell_opportunity = any(keyword in text for keyword in terms["brand_opportunity_terms"]["upsell opportunities"])

    appointment_booked = any(term in text for term in terms["appointment_terms"])
    appointment_opportunity = any(term in text for term in terms["reschedule_terms"])

    department = "Unknown"
    service_type = "Unknown"
    brand_mentions = 0
    opportunity_keywords = {}
    complaint_about_employee = False
    asked_how_heard = False
    hvac_system_age = None
    hvac_issue = None
    water_issue = None

    for category, terms_list in terms.items():
        if category == "hvac_terms" and any(term in text for term in terms_list):
            department = "HVAC"
            break
        elif category == "plumbing_terms" and any(term in text for term in terms_list):
            department = "Plumbing"
            break
        elif category == "install_terms" and any(term in text for term in terms_list):
            service_type = "Installation"
            break
        elif category == "dryer_terms" and any(term in text for term in terms_list):
            service_type = "Dryer Issues"
            break
        elif category == "brand_terms":
            brand_mentions = sum(text.count(term) for term in terms_list)
        elif category == "leak_terms" and any(term in text for term in terms_list):
            water_issue = "Leak"
        elif category == "appointment_terms":
            appointment_booked = any(term in text for term in terms_list)
        elif category == "reschedule_terms":
            appointment_opportunity = any(term in text for term in terms_list)
        else:
            # Count terms for other categories
            count = sum(text.count(keyword) for keyword in terms_list)
            if count > 0:
                opportunity_keywords[category] = count

# Secondary check for service type if not set by main categories
    if service_type is None:
        for category, terms_list in terms.items():
            if any(term in text for term in terms_list):
                service_type = category
                break

# Additional logic to map service_type to human-readable format if needed
    service_type_mapping = {
        "hvac_terms": "HVAC",
        "plumbing_terms": "Plumbing",
        "install_terms": "Installation",
        "dryer_terms": "Dryer Issues"
        # Add more mappings if necessary
    }

    if service_type in service_type_mapping:
        service_type = service_type_mapping[service_type]
    
    transcript_summary = ""
    if isinstance(lemur_response, dict):
        transcript_summary = lemur_response.get('summary', "")
        complaint_about_employee = "complaint" in lemur_response.get('sentiment', "").lower()
        asked_how_heard = "how did you hear about us" in text.lower()
        hvac_system_age = lemur_response.get('hvac_system_age')
        hvac_issue = lemur_response.get('hvac_issue')

    # Extract soonest or earliest appointment date
    earliest_appointment_date = extract_appointment_date(text)

    # Handle different types of lemur_response
    if isinstance(lemur_response, dict):
        appointment_booked = lemur_response.get('appointment_booked', appointment_booked)
        appointment_opportunity = lemur_response.get('opportunity_to_book_appointment', appointment_opportunity)
        active_listening = lemur_response.get('active_listening_detected', active_listening)
        empathy = lemur_response.get('empathy_detected', empathy)
        # Add other overrides as needed based on Lemur response

    notes = {
        "brief_summary": transcript_summary,
        "opportunity_to_book_appointment": appointment_opportunity,
        "appointment_booked": appointment_booked,
        "appointment_rescheduled": "reschedule" in text,
        "appointment_canceled": "cancel" in text,
        "warranties_told": "warranty" in text,
        "complaint_about_employee": complaint_about_employee,
        "asked_how_heard": asked_how_heard,
        "hvac_system_age": hvac_system_age,
        "hvac_issue_not_cooling": any(term in text for term in ["not cooling", "cooling issue", "AC problem"]),
        "hvac_issue_not_heating": any(term in text for term in ["not heating", "heating issue", "heater problem"]),
        "hvac_issue_not_working": any(term in text for term in ["not working", "not functioning", "not turning on"]),
        "water_issue_leak": any(term in text for term in ["leak", "leaking", "leakage"]),
        "water_issue_flooding": any(term in text for term in ["flooding", "flood", "flooded"]),
        "water_issue_water_damage": any(term in text for term in ["water damage", "damage due to water", "water affected"]),
        "water_issue_mold": any(term in text for term in ["mold", "moldy", "mildew"]),
        "water_issue_remodeling": any(term in text for term in ["remodeling", "renovation due to water", "remodel"]),
        "empathy_detected": empathy or any(keyword in text for keyword in ["understand", "empathize", "concern", "sorry", "apologize"]),
        "problem_solving_skills": any(term in text for term in ["solve", "fixed", "solution", "resolve", "that work", "resolved", "fixed the issue"]),
        "active_listening_detected": active_listening or any(keyword in text for keyword in ["listening", "heard", "attentive", "understood", "acknowledge", "is that correct"])
    }

    if earliest_appointment_date:
        notes["offered_appointment_date"] = earliest_appointment_date
    else:
        notes["offered_appointment_date"] = None

    return {
        "voicemail_detected": voicemail_detected,
        "active_listening": active_listening,
        "empathy": empathy,
        "good_opening": good_opening,
        "upsell_opportunity": upsell_opportunity,
        "appointment_booked": appointment_booked,
        "appointment_opportunity": appointment_opportunity,
        "department": department,
        "service_type": service_type,
        "brand_mentions": brand_mentions,
        "opportunity_keywords": opportunity_keywords,
        "transcript_summary": transcript_summary,
        "complaint_about_employee": complaint_about_employee,
        "asked_how_heard": asked_how_heard,
        "hvac_system_age": hvac_system_age,
        "hvac_issue": hvac_issue,
        "water_issue": water_issue,
        "notes": notes
    }

# Define the function to format transcript by speaker
def format_transcript_by_speaker(transcript):
    speaker_transcript = []
    current_speaker = None
    current_text = []

    # Extract words and segments
    words = transcript.words
    segments = getattr(transcript, 'segments', None)

    if segments:
        # Iterate over segments to handle speaker changes
        for segment in segments:
            speaker_label = segment['speaker_label']
            start_index = segment['start']
            end_index = segment['end']

            # Extract words within the segment
            segment_words = words[start_index:end_index]

            if speaker_label != current_speaker:
                if current_speaker is not None:
                    speaker_transcript.append(f"{current_speaker}: {' '.join(current_text)}")
                current_speaker = speaker_label
                current_text = segment_words
            else:
                current_text.extend(segment_words)
        
        # Add the last speaker's text
        if current_speaker is not None:
            speaker_transcript.append(f"{current_speaker}: {' '.join(current_text)}")
    else:
        # If no segments available, treat the entire transcript as one speaker
        speaker_transcript.append(f"Speaker 1: {' '.join(words)}")

    return '\n'.join(speaker_transcript)

# Define the AnalyzeCall class as a Flask Resource
class AnalyzeCall(Resource):
    def post(self):
        data = request.get_json()
        file_url = data.get('file_url', None)

        if not file_url:
            return {'error': 'File URL is required'}, 400

        # Configuration for transcription
        config = aai.TranscriptionConfig(auto_highlights=True, speaker_labels=True)

        # Create a transcriber instance
        transcriber = aai.Transcriber()

        try:
            # Transcribe the file
            transcript = transcriber.transcribe(file_url, config=config)

            # Check if the transcription was successful
            if transcript.status == aai.TranscriptStatus.error:
                return {'error': transcript.error}, 500

            # Format transcript by speaker
            formatted_transcript = format_transcript_by_speaker(transcript)

            # Lemur task prompt
            prompt = """
Provide a brief summary of the transcript. Indicate if there was an opportunity for scheduling an appointment, or if an appointment was scheduled or rescheduled. 
Assess the emotional sentiment of the conversation. Determine if the customer is new or existing. 
Identify any mentions of HVAC or plumbing, specifying if it was related to water leakage, damage, remodeling, or installation.
Check if 'Balanced Comfort' was mentioned and count the number of mentions.
Look for keywords indicating active listening, empathy, clarity, warranties, problem-solving skills, and upsell opportunities such as membership or subscription to Comfort Club. 
Determine the recommended soonest or earliest available appointment date and time.
Check if the agent asked how the customer heard about the service.
If HVAC was mentioned, note if the unit was not cooling, heating, or working/turning on, and determine the age of the AC unit. 
Check for any complaints about an employee. Separate the transcript by speaker with new line
"""
            # Lemur task processing
            result = transcript.lemur.task(prompt)

            # Analyze the transcript text
            analysis_result = analyze_text(transcript.text, result.response, terms)  # Assuming 'terms' is defined somewhere

            # Create the JSON response
            response = {
                "transcript": formatted_transcript,
                "lemur_response": result.response,
                "analysis": analysis_result
            }

            return jsonify(response), 200

        except Exception as e:
            return {'error': str(e)}, 500
    
        