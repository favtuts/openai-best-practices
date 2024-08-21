class QueueClientType:
    intent_crawler_queue = "intent_crawler"
    intent_crawler_result_queue = "intent_crawler_result"

class MyQueue:
    crawler_progress = "crawler_progress"
    parse_queue = "parse_queue"

class Config:
    def __init__(self, url, match, selector, max_pages_to_crawl, output_file_name, path_intent_file, cookie=None, on_visit_page=None):
        self.url = url
        self.match = match
        self.selector = selector
        self.max_pages_to_crawl = max_pages_to_crawl
        self.output_file_name = output_file_name
        self.path_intent_file = path_intent_file
        self.cookie = cookie
        self.on_visit_page = on_visit_page

