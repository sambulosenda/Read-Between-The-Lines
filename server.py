from flask import *
import os
import requests
import json
from werkzeug import secure_filename
import secrets
import stripe
import sendgrid

stripe.api_key = secrets.stripe_key

sg = sendgrid.SendGridClient(secrets.sendgrid_uname, secrets.sendgrid_pass)


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
    return render_template('theme.html', stripe_pubkey=secrets.stripe_pubkey)

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
                        headers=headers,
                        content_type = req.headers['content-type']
                        )
    except Exception,e:
        abort(500)

# Route that will process the file upload
@app.route('/charge', methods=['POST'])
def upload():
    print 'CHARGING CARD. MONEY BEING MADE SON.'
    # read the audio book from the page
    print request.form
    stripeToken = request.form['stripeToken']
    stripeEmail = request.form['stripeEmail']
    try:
        stripe.Charge.create(
          amount=100,
          currency="usd",
          source=stripeToken, # obtained with Stripe.js
          description="Charge for "+ stripeEmail
        )
        pass
    except stripe.error.CardError, e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err  = body['error']

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err['type']
        print "Code is: %s" % err['code']
        # param is '' in this case
        print "Param is: %s" % err['param']
        print "Message is: %s" % err['message']
    except stripe.error.InvalidRequestError, e:
        # Invalid parameters were supplied to Stripe's API
        print e
        pass
    except stripe.error.AuthenticationError, e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        print e
        pass
    except stripe.error.APIConnectionError, e:
        # Network communication with Stripe failed
        print e
        pass
    except stripe.error.StripeError, e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        message = sendgrid.Mail()
        message.add_to('David Awad <davidawad64@email.com>')
        message.set_subject('Weird Stripe Error')
        ##message.set_html()
        message.set_text('received a python exception from Stripe : ' + str(e) )
        message.set_from('Read Between the Lines <admin@rbtl.com>')
        status, msg = sg.send(message)
        print e
        pass
    except Exception, e:
        # Something else happened, completely unrelated to Stripe
        print e
        pass
    return render_template('theme.html', paid=True)

@app.route('/contact', methods=['POST'])
def contact():
    message = sendgrid.Mail()
    message.add_to('David Awad <davidawad64@email.com>')
    message.set_subject('Contact from Read Between the Lines')
    message.add_cc( request.form['email'] )
    message.set_text( request.form['message'] )
    message.set_from( request.form['name'] +' <' + request.form['email'] + '>')
    status, msg = sg.send(message)
    return render_template('theme.html', email=True )


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

# internal_Server_error
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
    #print("Listening on %s:%d" % (HOST_NAME, port))
