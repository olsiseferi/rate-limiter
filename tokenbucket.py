from flask import Flask, make_response
import schedule
import time
import uuid
from datetime import datetime,timedelta
from threading import Thread

refill_time = 30;
bucket = 0
last_refill_time=datetime.now()

def refill():
    global bucket,last_refill_time
    bucket = 5
    last_refill_time=datetime.now()


app = Flask(__name__)

@app.before_first_request
def my_func():
    refill()


@app.route('/token_bucket')
def ping():
    global bucket,last_refill_time
    if(bucket > 0):
        bucket -= 1
        response_payload = build_success_response()
        response = make_response(response_payload)
        response.headers['X-RateLimit-Remaining'] = str(bucket)
        response.headers['X-RateLimit-Limit'] = '5'
        response.status_code = 200
        return response
    else:
        response_payload = build_failure_response()
        response = make_response(response_payload)
        response.headers['X-RateLimit-Retry-After'] = str((last_refill_time+timedelta(seconds=refill_time))-datetime.now())
        response.status_code = 429
        return response

def build_failure_response():
    response_payload = {}
    response_payload['request_id'] =str(uuid.uuid4())
    response_payload['status'] = "failure"
    response_payload['response_timestamp'] = str(datetime.now())
    return response_payload

def build_success_response():
    response_payload = {}
    response_payload['request_id'] =str(uuid.uuid4())
    response_payload['status'] = "success"
    response_payload['response_timestamp']= str(datetime.now())
    return response_payload

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
    
schedule.every(refill_time).seconds.do(refill)
thread = Thread(target=run_schedule)
thread.start()

