from utils import queue_utils
from threading import Thread
from multiprocessing import freeze_support
from utils.queue_utils import QueueUtils
from utils.type import QueueClientType


class TypeThreadInit:
    l2_app = "l2_app"

def ready(type_thread = ""):
    freeze_support()
    print("Start with type : ", type_thread)
    
    if type_thread == TypeThreadInit.l2_app:
        listener0 = QueueUtils(QueueClientType.intent_crawler_queue, number_process=1)
        worker0 = queue_utils.MyThread(listener0)
        Thread(target=worker0.run).start()
