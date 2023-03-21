import json
from flask import Flask
import event
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Start taking data from api in compile time
print("Initial Data process has been started. It'll take approximately 15 minutes")
event.getDataFromApi()


@app.route("/api/getAllEvents")
def get():
    return json.dumps([obj.__dict__ for obj in event.returnData])

