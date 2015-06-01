# Read Between the Lines

This is an app that allows you to upload files and convert them into AudioBooks.

The [Text to Speech][service_url] service uses IBM's speech synthesis capabilities to convert English or Spanish text to an audio signal. The audio is streamed back to the client with minimal delay. The service can be accessed via a REST interface.

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/watson-developer-cloud/text-to-speech-python)


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


## License

  This sample code is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).
