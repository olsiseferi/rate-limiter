from flask import Flask, make_response
import schedule
import time
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


@app.route('/tocken_bucket')
def ping():
    global bucket,last_refill_time
    if(bucket > 0):
        bucket -= 1
        response = make_response("success")
        response.headers['X-RateLimit-Remaining'] = str(bucket)
        response.headers['X-RateLimit-Limit'] = '5'
        response.status_code = 200
        return response
    else:
        response = make_response("failure")
        response.headers['X-RateLimit-Retry-After'] = str((last_refill_time+timedelta(seconds=refill_time))-datetime.now())
        response.status_code = 429
        return response

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
    
schedule.every(refill_time).seconds.do(refill)
thread = Thread(target=run_schedule)
thread.start()

