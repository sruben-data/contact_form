"""
    To run file:
    [.venv/Scripts/activate]
    uv run main.py
"""
import inspect, os, logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from flask import Flask, json, send_file
from flask import request # global proxy object that intercepts the HTTP request
from flask import Response
# will need to import flask-cors at some point if you have browser talking to Flask app - adds CORS headers to response and allows cross-origin HTTP requests to your API
# from flask-cors import CORS

print('how many times is this file executed')

app: Flask = Flask(__name__) # type annotation - app of type Flask
app.logger.setLevel(logging.DEBUG)

app.logger.debug(inspect.getsourcefile(Flask))
app.logger.debug(inspect.getsourcefile(type(request)))
app.logger.debug(inspect.getsourcefile(json))

BASE_DIR = os.path.dirname(__file__)

@app.route('/')
def serve_form():
    return send_file(os.path.join(BASE_DIR,'index.html'))

@app.route('/submit', methods=['POST'])
def handle_form_submission() -> Response:
    """
    receiving Content-Type: multipart/form-data from JS FormData object"""
    # HTTP POST Request - Form Submission from index.html
    data: dict = request.form.to_dict() # converts request.form MultiDict object (immutable) to regular dictionary
    app.logger.debug(type(request.form))
    app.logger.debug(inspect.getsourcefile(type(request.form)))
    app.logger.debug(dir(request.form))
    app.logger.debug(inspect.getsourcefile(request.form.to_dict))
    app.logger.debug(type(data))
    app.logger.debug(dir(data))
    app.logger.debug(data)

    # CORS Headers need to be applied here in cases where domain name for scriptURL does not match browser url (localhost != )
    # HTTP Response - manual reassignment of custom attributes
    resp = json.jsonify({'status': 'received', 'data': data}) # constructs Response object, serializes Python dict into JSON string using json.dumps, resp.set_data()
    # status = 201
    resp.status_code = 201
    app.logger.debug(resp.status)
    # headers - includes 'X-Debug-Info' = 'form processed'
    resp.headers['X-Debug-Info'] = 'form processed by Flask'
    app.logger.debug(resp.mimetype)
    app.logger.debug(resp.headers)
    # body - already set in json.jsonify
    app.logger.debug(resp.data)

    return resp # serialize Python JSON string with Content-Type: application/json
    # tuple return format - (response, status) -> tuple[Response, int] or (response, status, headers) -> tuple[Response, int, dict]
    # return json.jsonify({'status': 'received', 'data': data}), 201, {'X-Debug-Info': 'form processed'}

@app.route('/contact/<int:contact_id>', methods=['GET'])
def get_contact(contact_id: int) -> Response:
    """GET endpoint to play with URL parameters - includes a Flask converter to restrict
    the parameter to an int value."""
    return json.jsonify({'id': contact_id, 'name': '...'})

if __name__ == '__main__':
    app.run(debug=True) # automatically loads from .env or .flaskenv file