"""
Flask application for emotion detection.

This module provides an endpoint to analyze emotions in text using 
the EmotionDetection package.
"""

from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

HTTP_BAD_REQUEST = 400

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_endpoint() -> jsonify:
    """
    Endpoint to detect emotions in the given text.
    
    Returns:
        JSON: Response containing emotion scores or error message.
    """
    # Get the input text from the request
    input_data = request.get_json()
    text = input_data.get('text', '')

    # Call the emotion detection function
    result, status_code = emotion_detector(text)

    # Handle blank or invalid input
    if status_code == HTTP_BAD_REQUEST:
        return jsonify({"response": "Invalid text! Please try again!"}), HTTP_BAD_REQUEST

    # Format the output
    response = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. The dominant emotion is "
        f"{result['dominant_emotion']}."
    )

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
