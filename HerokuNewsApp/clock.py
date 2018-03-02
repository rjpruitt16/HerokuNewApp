from subprocess import call
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=7)
def ScrapeNewsWashingtonPost():
    call(["python3", "manage.py", "NewsScraper", "--url",
      "https://www.washingtonpost.com/",
      "--news", "WashingtonPost"])

@sched.scheduled_job('cron', hour=7)
def ScrapeNewsCNN():
    call(["python3", "manage.py", "NewsScraper", "--url", "https://www.cnn.com/",
      "--news", "CNN"])

@sched.scheduled_job('cron', hour=7)
def ScrapeNewsHuffingtonPost():
    call(["python3", "manage.py", "NewsScraper", "--url",
     "https://www.huffingtonpost.com/",
      "--news", "HuffingtonPost"])

@sched.scheduled_job('cron', hour=7)
def ScrapeNewsHuffingtonPost():
    call(["python3", "manage.py", "NewsScraper", "--url",
      "https://www.npr.org/sections/politics/", "--news", "NPR"])

@sched.scheduled_job('cron', hour=7)
def ScrapeNewsFox():
    call(["python3", "manage.py", "NewsScraper", "--url",
      "http://www.foxnews.com/", "--news", "FoxNews"])

@sched.scheduled_job('cron', hour=7)
def ScrapeNewsBloomberg():
    call(["python3", "manage.py", "NewsScraper", "--url",
      "https://www.bloomberg.com/", "--news", "Bloomberg"])

@sched.scheduled_job('cron', hour=20)
def test():
    call(["touch", "madeat730.txt"])

sched.start()
