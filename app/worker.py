#!/usr/bin/env python3
'''foo'''
# pylint: disable=W0702,C0301

from datetime import datetime
import traceback
import logging
import subprocess
import sys
import os
import redis
from celery import Celery

try:
    DESTINATION_DIR = os.environ.get("DESTINATION_DIR")
    DOWNLOAD_PARAMETERS = os.environ.get("DOWNLOAD_PARAMETERS")
    REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    REDIS_DB = os.environ.get("REDIS_DB", 0)
except:
    print("Variables not set")
    sys.exit(1)

app = Celery('tasks', broker=f'redis://{REDIS_HOST}')
redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


@app.task
def add(url):
    '''runner'''
    today = datetime.today().strftime('%Y-%m-%d')
    domain = url.split("/")[2]

    try:
        redis_url = redisClient.get(url)
        if not redis_url:
            cmd_str = f"yt-dlp {DOWNLOAD_PARAMETERS} -o '{DESTINATION_DIR}/{today}/{domain}/%(title)s.%(id)s.%(ext)s' --download-archive /archive.list {url}"
            task = subprocess.run(cmd_str, shell=True, check=False)
            if task.returncode == 0:
                redisClient.set(url, url)
            return task.returncode
        return "already recorded in redis"

    except:
        logging.error(traceback.format_exc())
        return False
