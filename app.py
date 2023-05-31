import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACb74c8defd26d79470d130ec34290d876'
    TWILIO_SYNC_SERVICE_SID = 'ISe7ce5250181d231b8c61b2c449ae9abb'
    TWILIO_API_KEY = 'SKcaf68a534e46aa3483f480b06aa511eb'
    TWILIO_API_SECRET = 'sFitg3Sr9YdXlAp0W8YaKnwtO92xKG8y'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    
    text_from_notepad = request.form['text']

    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)

    path_to_store_text = 'workfile.txt'

    return send_file(path_to_store_text, as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
