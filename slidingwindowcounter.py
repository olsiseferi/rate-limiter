from flask import Flask, make_response
import schedule
import time
import uuid
from datetime import datetime,timedelta
from threading import Thread

window_size = 30 # in seconds
counter = 0 # counter for requests
previous_window_counter = 0 # counter for requests in previous window
window_max_requests = 10 # max requests per window
last_reset_time = datetime.now() # last time the counter was reset
successul_requests= []

def reset_counter():
    global counter,last_reset_time,previous_window_counter
    previous_window_counter = counter
    counter = 0
    last_reset_time = datetime.now()

app = Flask(__name__)

@app.before_first_request
def init():
    reset_counter()


@app.route('/sliding_window_counter')
def ping():
    global counter,window_max_requests
    if(is_request_allowed()):
        counter += 1
        response_payload = {}
        response_payload['request_id'] =str(uuid.uuid4())
        response_payload['status'] = "success"
        response_payload['response_timestamp'] =str(datetime.now())
        successul_requests.append(response_payload)
        response = make_response(response_payload)
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

def get_percentage_of_elapsed_window():
    global last_reset_time, window_size
    percentage =  ((datetime.now()-last_reset_time).seconds*100)/window_size
    return percentage/100

def get_remaining_window_percentage():
    return 1 - get_percentage_of_elapsed_window()

def is_request_allowed():
    global counter, window_max_requests, previous_window_counter
    if(counter + (previous_window_counter*get_remaining_window_percentage()) <= window_max_requests):
        return True
    else:
        return False
    


schedule.every(window_size).seconds.do(reset_counter)
thread = Thread(target=run_schedule)
thread.start()

