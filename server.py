import os
import requests
import json
from flask import *
from werkzeug import secure_filename
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

class TextToSpeechService:
    """Wrapper on the Text to Speech service"""

    def __init__(self):
        """
        Construct an instance. Fetches service parameters from VCAP_SERVICES
        runtime variable for Bluemix, or it defaults to local URLs.
        """
        vcapServices = os.getenv("VCAP_SERVICES")
        # Local variables
        self.url = "<url>"
        self.username = "<username>"
        self.password = "<password>"

        if vcapServices is not None:
            print("Parsing VCAP_SERVICES")
            services = json.loads(vcapServices)
            svcName = "text_to_speech"
            if svcName in services:
                print("Text to Speech service found!")
                svc = services[svcName][0]["credentials"]
                self.url = svc["url"]
                self.username = svc["username"]
                self.password = svc["password"]
            else:
                print("ERROR: The Text to Speech service was not found")

    def synthesize(self, text, voice, accept):
        """
        Returns the get HTTP response by doing a GET to
        /v1/synthesize with text, voice, accept
        """

        return requests.get(self.url + "/v1/synthesize",
            auth=(self.username, self.password),
            params={'text': text, 'voice': voice, 'accept': accept},
            stream=True, verify=False
        )



@app.route('/', methods=['GET'])
def homepage():
    return render_template('theme.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/synthesize', methods=['GET'])
def synthesize():
    voice = request.args.get('voice', 'VoiceEnUsMichael')
    accept = request.args.get('accept', 'audio/ogg; codecs=opus')
    text = request.args.get('text', '')

    download = request.args.get('download', '')

    headers = {}

    if download:
        headers['content-disposition'] = 'attachment; filename=transcript.ogg'

    try:
        req = textToSpeech.synthesize(text, voice, accept)
        return Response(stream_with_context(req.iter_content()),
            headers=headers, content_type = req.headers['content-type'])
    except Exception,e:
        abort(500)




# page not found
@app.errorhandler(404)
def new_page(error):
    print str(error) + ' error. whack.'
    return redirect(url_for('homepage'))

# method not allowed
@app.errorhandler(405)
def new_page(error):
    print str(error) + ' error. weerd'
    return redirect(url_for('homepage'))

@app.errorhandler(500)
def internal_Server_error(error):
    print str(error) + ' error. whuuut'
    return redirect(url_for('homepage'))

# Global watson service wrapper
textToSpeech = None

if __name__ == "__main__":
    textToSpeech = TextToSpeechService()

    # Get host/port from the Bluemix environment, or default to local
    HOST_NAME = os.getenv("VCAP_APP_HOST", "127.0.0.1")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "3000"))

    app.run(host=HOST_NAME, port=int(PORT_NUMBER), debug=True)

    # Start the server
    print("Listening on %s:%d" % (HOST_NAME, port))
