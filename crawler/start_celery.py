from __future__ import absolute_import
from celery import Celery


app = Celery('crawler',
             broker='amqp://crawler:Passcrawler12@18.116.5.193:5672/crawler_vhost',
             backend='rpc://',
             include=['crawler.tasks'])
