# [Read Between the Lines](http://readbtl.mybluemix.net/)

This is an app that allows you to upload text documents and convert them into AudioBooks. It uses Machine learning to create emphasis in the correct places so it feel like the book is actually being read to you.

You're also given the option to donate using stripe! 

It's built using Python Flask, IBM Watson, PDFJS, and the Stripe api to process payments for the books.

## IN ACTIVE DEVELOPMENT.

You can use and try out the service [here](http://readbtl.mybluemix.net/).

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/DavidAwad/Read-Between-The-Lines)


## Running locally
  The application uses [Python](https://www.python.org) and [pip](https://pip.pypa.io/en/latest/installing.html) so you will have to download and install them as part of the steps below. This app also uses the IBM Bluemix text to speech service from IBM Watson. You'll need credentials to run it locally.

1. Copy the credentials from your `text-to-speech-service` service in Bluemix to `server.py`, you can see the credentials using:

  ```sh
  $ cf env <application-name>
  ```
    Example output:
  ```sh
  System-Provided:
  {
    "VCAP_SERVICES": {
      "text_to_speech": [{
          "credentials": {
            "url": "<url>",
            "password": "<password>",
            "username": "<username>"
          },
        "label": "text_to_speech",
        "name": "text-to-speech-service",
        "plan": "text_to_speech_free_plan"
     }]
    }
  }
  ```

    You need to copy `username`, `password` and `url`.

2. Install [Python 2.7.9 or later](https://www.python.org/downloads/)
3. Go to the project folder in a terminal and run:
  `pip install -r requirements.txt`
4. Start the application
  `python server.py`
5. Go to
  `http://localhost:3000`

## Resources
- http://jsfiddle.net/go279m0h/
- http://stackoverflow.com/questions/1554280/extract-text-from-pdf-in-javascript

## License

  This sample code is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).
