import requests
import json

def emotion_detector(text_to_analyze):
       # Handle blank input
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }, 400
    # Define the URL and headers
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    # Prepare the input JSON
    input_json = {"raw_document": {"text": text_to_analyze}}
    
    # Make the POST request
    response = requests.post(url, json=input_json, headers=headers)
    response.raise_for_status()  # Ensure the request was successful
    
    # Parse the response JSON
    response_data = response.json()
    
    # Log the raw response for debugging purposes
    print("Response Data:", json.dumps(response_data, indent=2))
    
    # Extract relevant emotions
    try:
        # Access the correct key in the response
        emotion_data = response_data['emotionPredictions'][0]['emotion']
        anger = emotion_data['anger']
        disgust = emotion_data['disgust']
        fear = emotion_data['fear']
        joy = emotion_data['joy']
        sadness = emotion_data['sadness']
    except (KeyError, IndexError):
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }, 400
    
    # Determine the dominant emotion
    emotion_scores = {
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'joy': joy,
        'sadness': sadness,
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    
    # Return the formatted output
    return {
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'joy': joy,
        'sadness': sadness,
        'dominant_emotion': dominant_emotion
    }, 200
