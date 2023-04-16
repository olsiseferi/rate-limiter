from flask import Flask, make_response
import schedule
import time
import uuid
from datetime import datetime,timedelta
from threading import Thread

window_size = 30 # in seconds
counter = 0 # counter for requests
window_max_requests = 10 # max requests per window
last_reset_time = datetime.now() # last time the counter was reset

def reset_counter():
    global counter,last_reset_time
    counter = 0
    last_reset_time = datetime.now()

app = Flask(__name__)

@app.before_first_request
def init():
    reset_counter()


@app.route('/fixed_window_counter')
def ping():
    global counter,window_max_requests
    if(counter < window_max_requests):
        counter += 1
        response_payload = {}
        response_payload['request_id'] =str(uuid.uuid4())
        response_payload['status'] = "success"
        response_payload['response_timestamp'] =str(datetime.now())
        response = make_response(response_payload)
        response.headers['X-RateLimit-Remaining'] = str(window_max_requests-counter)
        response.headers['X-RateLimit-Limit'] = str(window_max_requests)
        response.status_code = 200
        return response
    else:
        response_payload = {}
        response_payload['request_id'] =str(uuid.uuid4())
        response_payload['status'] = "failure"
        response_payload['response_timestamp'] = str(datetime.now())

        response = make_response(response_payload)
        response.headers['X-RateLimit-Retry-After'] = str((last_reset_time+timedelta(seconds=window_size))-datetime.now())
        response.status_code = 429
        return response

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
    
schedule.every(window_size).seconds.do(reset_counter)
thread = Thread(target=run_schedule)
thread.start()

