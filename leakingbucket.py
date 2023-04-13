from flask import Flask, make_response
import schedule
import time
import uuid

from datetime import datetime,timedelta
from threading import Thread

refill_time = 30;
bucket = 0
last_refill_time=datetime.now()
run_queue = [];
leaking_rate = 1;

def refill():
    global bucket,last_refill_time
    bucket = 5
    last_refill_time=datetime.now()


app = Flask(__name__)

@app.before_first_request
def my_func():
    refill()


@app.route('/leaking_bucket')
def ping():
    global bucket,last_refill_time,run_queue
    if(bucket > 0):
        bucket -= 1

        response_payload = {}
        response_payload['request_id'] =str(uuid.uuid4())
        response_payload['status'] = "success"
        response_payload['request_timestamp']= str(datetime.now())
        
        run_queue.append(response_payload)

        while(check_request_exists(response_payload)==True):
            time.sleep(1)
           
        response_payload['response_timestamp'] =str(datetime.now())
        response = make_response(response_payload)

        response.headers['X-RateLimit-Remaining'] = str(bucket)
        response.headers['X-RateLimit-Limit'] = '5'
        response.status_code = 200
        return response
    else:
        response_payload = {}
        response_payload['request_id'] =str(uuid.uuid4())
        response_payload['status'] = "failure"
        response_payload['response_timestamp'] = str(datetime.now())

        response = make_response(response_payload)
        response.headers['X-RateLimit-Retry-After'] = str((last_refill_time+timedelta(seconds=refill_time))-datetime.now())
        response.status_code = 429
        return response

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_request():
    global run_queue
    while True:
        if(len(run_queue) > 0):
            #dequeue front element
            run_queue.pop(0)
        time.sleep(1)

def check_request_exists(request):
    global run_queue
    #check request is in queue
    for req in run_queue:
        if(req == request):
            return True

schedule.every(refill_time).seconds.do(refill)
thread = Thread(target=run_schedule)
thread.start()
queue_thread = Thread(target=run_request)
queue_thread.start()

