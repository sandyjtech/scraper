from flask import Flask, make_response, request, jsonify
from flask_restful import Api, Resource, reqparse
import assemblyai as aai
import json
from dotenv import load_dotenv
import os

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

# Set your AssemblyAI API key
aai.settings.api_key = os.environ.get('ASSEMBLYAI_API_KEY')

# Text analysis function
def analyze_text(text, lemur_response, terms):
    text = text.lower()

    # Check for voicemail
    voicemail_detected = "your call has been forwarded to an automatic voice message system" in text

    # Check for active listening and empathy
    active_listening = any(keyword in text for keyword in terms["brand_opportunity_terms"]["active listening"])
    empathy = any(keyword in text for keyword in terms["brand_opportunity_terms"]["empathy"])

    # Check opening greeting
    good_opening = any(keyword in text for keyword in ["hi", "hello", "welcome", "thank you for calling", "help", "assist"]) and "balanced comfort" in text.lower()

    # Check for product upsell opportunity
    upsell_opportunity = any(keyword in text for keyword in terms["brand_opportunity_terms"]["upsell opportunities"])

    # Check if appointment was booked or opportunity to do so
    appointment_booked = any(term in text for term in terms["appointment_terms"])
    appointment_opportunity = any(term in text for term in terms["reschedule_terms"])

    department = "Unknown"
    service_type = "Unknown"
    brand_mentions = 0
    opportunity_keywords = {}

    for category, terms_list in terms.items():
        if category == "hvac_terms" and any(term in text for term in terms_list):
            department = "HVAC"
        elif category == "plumbing_terms" and any(term in text for term in terms_list):
            department = "Plumbing"
        elif category == "install_terms" and any(term in text for term in terms_list):
            service_type = "Installation"
        elif category == "brand_terms":
            brand_mentions = sum(text.count(term) for term in terms_list)
        else:
            count = sum(text.count(keyword) for keyword in terms_list)
            if count > 0:
                opportunity_keywords[category] = count

    transcript_summary = ""
    if isinstance(lemur_response, dict) and 'summary' in lemur_response:
        transcript_summary = lemur_response['summary']

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
        "transcript_summary": transcript_summary
    }

# Define resource classes
class AnalyzeCall(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file_url', type=str, required=True, help="File URL is required")
        args = parser.parse_args()
        
        file_url = args['file_url']

        # Configuration for transcription
        config = aai.TranscriptionConfig(auto_highlights=True, speaker_labels=True)

        # Create a transcriber instance
        transcriber = aai.Transcriber()

        # Transcribe the file
        transcript = transcriber.transcribe(file_url, config=config)

        # Check if the transcription was successful
        if transcript.status == aai.TranscriptStatus.error:
            return {'error': transcript.error}, 500

        transcript_text = transcript.text

        # Lemur task prompt
        prompt = """
        Provide a brief summary of the transcript and tell me if there was an opportunity for scheduling an appointment or if an appointment was scheduled. 
        Assess the emotional sentiment of the conversation. Are they a new customer or an existing one? 
        Identify any mentions of HVAC or plumbing, and whether it was related to water leakage or installation.
        Check if 'Balanced Comfort' was mentioned more than twice and look for keywords indicating brand opportunity, active listening, empathy, clarity, warranties, problem solving skills, and upsell opportunities like membership or subscription to Comfort Club.
        """

        result = transcript.lemur.task(prompt)

        # Analyze the transcript text
        analysis_result = analyze_text(transcript_text, result.response, terms)

        # Create the JSON response
        response = {
            "transcript": transcript_text,
            "lemur_response": result.response,
            "analysis": analysis_result
        }

        return make_response(response)


