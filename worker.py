import threading
import project_settings
from db_queue import *
from queue import Queue
from spider import Spider


class Worker:
    queue = Queue()
    DB = None

    def __init__(self, thread_count, project_name):
        Worker.DB = (lambda x: globals()[x])(project_settings.DB_CLASS_NAME)
        self.thread_count = thread_count
        self.project_name = project_name

    def create_threads(self):
        for _ in range(self.thread_count):
            t = threading.Thread(target=self.__run_thread)
            t.daemon = True
            t.start()

    def __run_thread(self):
        while True:
            url = self.queue.get()
            Spider.crawl_page(threading.current_thread().name, url)
            self.queue.task_done()

    def __create_jobs(self):
        for link in Worker.DB.get_pending_queue():
            self.queue.put(link)

        self.queue.join()
        self.crawl()

    def crawl(self):
        urls = Worker.DB.get_pending_queue()
        if len(urls) > 0:
            print(str(len(urls)) + ' urls in the queue')
            self.__create_jobs()
