"""
This script is a basic Flask application that utilizes Redis for caching.
It defines a route '/' that returns a message along with the number of times
it has been accessed.

Usage:
- Make sure you have Redis and Flask installed.
- Run this script using Docker Compose.

Example:
    $ docker-compose up

Requirements:
    - Redis
    - Flask
    - Docker

Attributes:
    app (Flask): The Flask application instance.
    cache (redis.Redis): The Redis cache connection.

Functions:
    get_hist_count: Increments and retrieves the 'hits' count
    from the Redis cache.
        Returns:
            int: The updated count.

Routes:
    '/':
        Returns a message along with the number of times it has been accessed.

"""
import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hist_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hist_count()
    return f'Hello World! I have been seen {count} times'
