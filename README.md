
# Rate Limiter via python

A simple repo implementing different rate limiting algorithms using only python, flask and schedule library.
 - tocken bucket
 - leaking bucket
 - fixed window counter 
 - sliding window counter

[![System Design](https://img.shields.io/badge/system--design-rate--limiter-brightgreen?style=for-the-badge)]()

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-green.svg)](https://opensource.org/licenses/)


## API Reference

#### Token Bucket rate limiting algorithm implementation

```http
  GET /token_bucket
```
The token bucket algorithm is a very simple algorithm that allows a certain number of requests per second. The algorithm works by adding X number of tokens (max number of requests) to the bucket every Y seconds/minutes/etc(refill time) . If the bucket is full, the request is dropped. If the bucket is empty, the request is dropped. If the bucket has tokens, the request is allowed and a token is removed from the bucket.

| Configuration parameter | Description                          |
| :---------------------- | :----------------------------------- |
| `bucket`                | **Required**. bucket size            |
| `refill_time`           | **Required**. refill rate per second |

#### Leaking bucket rate limiting algorithm implementation

```http
  GET /token_bucket
```

The leaking bucket algorithm is a very similar to the token bucket algorithm, except that the requests are processed at a constant rate. The requests get processed at a rate of X requests per second (leaking rate). If the queue is full, the request is dropped. 

| Configuration parameter | Description                                  |
| :---------------------- | :------------------------------------------- |
| `bucket`                | **Required**. current bucket size            |
| `max_bucket_size`       | **Required**. maximum bucket size per second |
| `reset_time`            | **Required**. bucket reset rate per second   |

#### Fixed window counter rate limiting algorithm implementation


```http
  GET /fixed_window_counter
```

The fixed window counter works by dividing the time into fixed intervals. Each interval has a counter that counts the number of requests that have been made in that interval. If the counter exceeds the limit, the request is dropped. 

| Configuration parameter | Description                                             |
| :---------------------- | :------------------------------------------------------ |
| `window_size`           | **Required**. time window size in seconds               |
| `counter`               | **Required**. current window counter                    |
| `window_max_requests`   | **Required**. maximum request threshold for each window |

#### Sliding window log rate limiting algorithm implementation


```http
  GET /sliding_window_counter
```

The sliding window counter works by dividing the time into fixed intervals. Each interval has a counter that counts the number of requests that have been made in that interval. If the counter exceeds the limit, the request is dropped. However, the difference between the sliding window counter and the fixed window counter is that the sliding window counter moves the window forward and based on that a new formula for calculating the threshold is used. 

```
requests_in_current_window + ( requests_in_previous_window * [percentage of the rolling window - current elapsed window] )
```
| Configuration parameter | Description                                             |
| :---------------------- | :------------------------------------------------------ |
| `window_size`           | **Required**. time window size in seconds               |
| `counter`               | **Required**. current window counter                    |
| `window_max_requests`   | **Required**. maximum request threshold for each window |


## Installation

Its a prerequisite that you have python and pip installed.

First clone this repository, after that you need to create a virtual environment using venv, and activate it. (For python3 there's no additional installation required)

```bash
python3 -m venv venv

source venv/bin/activate
```
After that you can install all the required dependencies.

```bash
pip3 install -r requirements.txt
```

Run the specific file
```bash
FLASK_APP={rate_limit_scipt_name}.py flask run

Example:
FLASK_APP=tokenbucket.py flask run
```


    
## Authors

- [@olsiseferi](https://www.linkedin.com/in/olsi-seferi/)


