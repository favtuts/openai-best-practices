from config import local_settings
from glob import glob, escape
from urllib.parse import urlparse
from datetime import datetime
from json import JSONEncoder
from threading import Thread, Lock
from playwright.async_api import async_playwright
from urllib.parse import unquote
from utils.type import *
from qa_robot.faq_engin import *
from qa_robot.extract_texts_from_file import *
from utils import dict_helper

import os
import time
import json
import queue
import pika
import uuid
import asyncio
import threading
import fnmatch
import requests
from openai import OpenAI
import traceback

model="gpt-3.5-turbo"

class MyThread:
    def __init__(self, queue_utils_ob) -> None:
        self._queue_utils = queue_utils_ob
        pass

    def run(self):
        self._queue_utils.connect()
        self._queue_utils.listen()

class QueueUtils:
    def __init__(self, queue_type = "", routing_key = MyQueue.crawler_progress , number_process = 1) -> None:
        """
        queue_type : for subcriber (Listen)
        routing_key : for publisher 
        """
        self.number_process = number_process
        self.queue_type = queue_type
        self._conn = None
        self._channel = None
        self._queue = routing_key
        self._routing_key = routing_key
        
        self.intent_thread = ProcessQueue(queue_type, self.number_process)

    def connect(self):
        print("Initial Connection!!")
        credentials = pika.credentials.PlainCredentials(
            local_settings.RABBIT_USER,
            local_settings.RABBIT_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=local_settings.RABBIT_IP,
            port=local_settings.RABBIT_PORT,
            virtual_host='/',
            credentials=credentials,
            heartbeat=590,
            blocked_connection_timeout=300))
        self._conn = connection
        self._channel = self._conn.channel()
        return connection

    def reconnect(self):
        if self._conn.is_closed:
            try:
                self.connect()
            except Exception as e:
                tb = traceback.format_exc()
                print(f"Cant reconnect! \n{tb}")

    def close(self):
        try:
            if self._conn and self._conn.is_open:
                print('closing queue connection')
                self._conn.close()
                return
            self._conn.close()
        except:
            tb = traceback.format_exc()
            print(f"[Exception] Fail to close!! \n{tb}")

    @staticmethod
    def send(data = "", routing_key = ""):
        intent_credentials = pika.credentials.PlainCredentials(local_settings.RABBIT_USER, local_settings.RABBIT_PASS)
        intent_connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=local_settings.RABBIT_IP,
            port=local_settings.RABBIT_PORT,
            credentials=intent_credentials
        ))
        try:
            channel_video = intent_connection.channel()
            channel_video.queue_declare(routing_key, durable=True)
        except:
            channel_video = intent_connection.channel()
            channel_video.queue_declare(routing_key, durable=False)

        channel_video.basic_publish(exchange='', routing_key= routing_key, body=data)
        intent_connection.close()

    def _publish(self, msg):
        print(f"Start basic publish!{self._routing_key}")
        try:
            self._channel.basic_publish(exchange='',
                                        routing_key=self._routing_key,
                                        body=(msg))
            print(f'[NOTE] Message sent: {msg}')
        except Exception as e :
            tb = traceback.format_exc()
            print(f"[Exception] Fail to publish \n{tb}")

    def publish(self, msg = ""):
        """Publish msg, reconnecting if necessary."""
        try:
            self._publish(msg)
        except pika.exceptions.ConnectionClosed:
            tb = traceback.format_exc()
            print(f'reconnecting to queue: \n{tb}')
            self.connect()
            self._publish(msg)

    def _get_connection(self):
        print("Get connection!!")
        credentials = pika.credentials.PlainCredentials(
            local_settings.RABBIT_USER,
            local_settings.RABBIT_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=local_settings.RABBIT_IP,
            port=local_settings.RABBIT_PORT,
            virtual_host='/',
            credentials=credentials,
            heartbeat=590,
            blocked_connection_timeout=300))

        self._conn = connection
        self._channel = connection.channel()
        return connection

    def listen(self ):
        print("Start listen!" + self.queue_type)
        self._conn = self._get_connection
        try:
            self._channel.queue_declare(self.queue_type, durable=True)
        except:
            self._channel.queue_declare(self.queue_type, durable=False)
        self._channel.basic_qos(prefetch_count=1)

        self._channel.basic_consume(
            on_message_callback=self.callback,
            queue= self.queue_type)
        print(f"Start consuming! {self.queue_type}\n")
        self._channel.start_consuming()
        print("Exit Listening!!")

    def callback(self, ch, method, properties, body):
        print(f"[INFO]Start callback! {self.queue_type} time = {str(datetime.now())} " )
        print(f"Start callback {self.queue_type}")
        print(f"Body : {str(body)}, ch: {str(ch)}, method {str(method)}, porperties : {str(properties)} " )

        self.intent_thread.queue(self.queue_type, ch, method, properties, body)
        try:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except:
            tb = traceback.format_exc()
            print("*********************************************")
            print(f"Fail to basic_ack! \n{tb}")
        print("Finish call back of listening")

class ProcessQueue:
    def __init__(self, queue_type, number_process = 1) -> None:
        self.queue_type = queue_type
        self.lock = threading.Lock()
        self.botName = ""
        self.api_key = ""
        self.assistantID = ""
        self.requestID = ""
        self.genIntent = False
        self.feedIntent = False
        self.intent_file = ""
        self.urls_list = list()
        self.urls_list_process = list()
        self.docs_list = list()
        self.NUMBER_OF_PROCESSES = number_process
        self.task_queue = queue.Queue()         # init a queue
        print("[INFO] Start thread!")
        if queue_type == QueueClientType.intent_crawler_queue:
            self.queue_name = "FACE"

        for i in range(self.NUMBER_OF_PROCESSES):
            print(f"[INFO] Start thread {i}")
            print(f"Start thread : {i}")
            threading.Thread(target=self.run, daemon=True).start()

    def queue(self, queue_type, ch, method, properties, body):
        print(f"[INFO] Put Queue : {queue_type} {datetime.now()} ")
        try:
            self.ch = ch
            self.method = method
            message = json.loads(body)
            self.botName = message.get('botName')
            self.api_key = message.get('apiKey')
            self.assistantID = message.get('assistantId')
            self.requestID = message.get('requestId')
            self.urls_list = message.get('urls')
            self.docs_list = message.get('fileUrls')
            self.genIntent = message.get('genIntent')
            self.feedIntent = message.get('feedIntent')
            self.upload_file_paths = []
            self.crawl_result_files = []
            self.output_json = []
            self.questions = []
            self.answers = []
            self.sync = 1
            # task_type = "code_interpreter"
            task_type = "retrieval"

            try:
                # TVT Fixed: 20240812
                self.client = OpenAI(api_key=self.api_key)
                
                if self.assistantID == "":                       
                    # Create assistant ID
                    assistantName = f"Created_assistant_{self.botName}"
                    response = self.client.beta.assistants.create(
                        name=assistantName,
                        model=model,
                        instructions=instruction_assis_pre_prompt,
                        # tools=[{"type":task_type}]
                        tools=[{"type": "file_search"}],
                    )
                    self.assistantID = response.id
                    print(f"assistantId created {self.assistantID}")

            except Exception as ea:
                tb = traceback.format_exc()
                print(f"Error when creating assistantId: \n{tb}")
                raise

            # TVT Fixed: 20240815
            # Generate intent_file with TXT extension
            self.intent_file = os.path.join(os.environ['INTENT_STORE'], self.assistantID + ".txt")
            
            if os.path.exists(self.intent_file):
                os.remove(self.intent_file)

            if not os.path.exists("uploads"):
                os.makedirs("uploads")

            path_sub = f"uploads/{self.requestID}"
            if not os.path.exists(path_sub):
                os.makedirs(path_sub)

            # Process a queue for crawling content from urls
            if queue_type == QueueClientType.intent_crawler_queue:
                self.reset_task_queue()
            else:
                print(f"Put!!{body}")
                self.task_queue.put(body)
            if len(self.docs_list) == 0:
                self.sync = 2
                print("No file uploaded")
            else:
                # Process for download files
                for file_url in self.docs_list:
                    try:
                        response = requests.get(file_url)
                        if response.status_code == 200:
                            content_disposition = response.headers.get('Content-Disposition')
                            filename = None
                            if content_disposition:
                                index = content_disposition.find('filename=')
                                if index != -1:
                                    filename = content_disposition[index + len('filename='):].strip('"')
                                    filename = unquote(filename)
                            if not filename:
                                filename = file_url.split("/")[-1]
                            local_file_path = f"uploads/{self.requestID}/{filename}"
                            with open(local_file_path, 'wb') as file:
                                file.write(response.content)
                            self.upload_file_paths.append(local_file_path)
                            print(f"Download file successfully: {local_file_path}")
                        else:
                            print(f"Can't download file from URL: {file_url}. Error: {response.status_code}")
                    except Exception as ed:
                        tb = traceback.format_exc()
                        print(f"Error downloading from URL: {file_url}. Error:\n{tb}")
                        raise
                self.process_files_upload()

        except Exception as e:
            tb = traceback.format_exc()
            print("*********************************************")
            print(f"[ERROR] Fail to put queue \n{tb}")
            pass
        print("Continue...")

    def reset_task_queue(self):
        print("[INFO] reset task queue...")

        try:
            with self.task_queue.mutex: 
                self.task_queue.queue.clear()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"[ERROR]fail to reset queue: \n{tb}")

        try:
            if len(self.urls_list) == 0:
                self.sync = 2
                print("No url to crawl")
            else:
                print("[INFO] Start put links to task_queue!")
                # for i in range(len(self.urls_list)):
                #     self.task_queue.put(self.urls_list[i])
                for item in self.urls_list:
                    self.task_queue.put(item)
                    print(item)

        except Exception as e:
            tb = traceback.format_exc()
            print("*********************************************")
            print(f"[ERROR] Fail to put queue!\n{tb}")
        print("[INFO] Finish reset task queue!")

    def run(self):
        count = 1
        while True:
            print("[INFO] LISTENING......")
            print("[INFO] Waiting for msg at task_queue !")
            body = self.task_queue.get()
            self.task_queue.task_done()

            print(f"\n\n\n[INFO] Start get Body :{body} queue_type: {self.queue_type}")

            if self.queue_type == QueueClientType.intent_crawler_queue:
                self.lock.acquire()
                self.urls_list_process.append(body) 
                print(f"[NOTE] Crawler processing! {self.urls_list_process}")
                self.lock.release()

            print("[NOTE] Start Call Back Function!")
            print("[NOTE] ===================================")
            print(f"Queue: {self.queue_type}")
            if self.queue_type == QueueClientType.intent_crawler_queue:
                self.callback_l2_app(body)
                try:
                    self.urls_list_process.remove((body))
                    print(f"[INFO] Remove an item of crawler processing!")
                except Exception as e:
                    tb = traceback.format_exc()
                    print(f"[ERROR]Fail to remove element of crawler proceessing!\n{tb}")

            print("[NOTE] Task done!!!")
            if count == len(self.urls_list):
                self.process_crawler_results()
            else:
                count += 1

    def publish_output(self):
        if self.genIntent:
            print("Publish json to result queue")
            json_data = {
                "assistantId":f"{self.assistantID}",
                "requestID": f"{self.requestID}",
                "questions": self.questions,
                "answers": self.answers
            }
            json_string = json.dumps(json_data, indent=4)
            # print(json_string)

            try:
                QueueUtils.send(json_string,QueueClientType.intent_crawler_result_queue)
            except Exception as e:
                tb = traceback.format_exc()
                print("*********************************************")
                print(f"Fail to init connct and publish \n{tb}")

        if self.feedIntent:
            try:
                # TVT Fixed: 20240812
                # 1. First load assistant object by Id
                assistant_response = self.client.beta.assistants.retrieve(assistant_id=self.assistantID)
                print(f"Retrieved assistant object: \n{assistant_response}")
                
                # 2. Extract the vector_store_id attached to the assistant
                assistant_model = None
                vector_store_id = None
                if assistant_response is not None:
                    assistant_model = assistant_response.model_dump()
                    vector_store_list = dict_helper.deep_get(assistant_model, ['tool_resources', 'file_search', 'vector_store_ids'], default=None)    
                    vector_store_id = vector_store_list[0] if vector_store_list is not None and len(vector_store_list) > 0 else None                
                
                # Create a new Vector Store if not found in the assistant
                if vector_store_id is None:
                    print(f"The Assistant {self.assistantID} has no Vector Store, creating new VS object...")
                    new_vector_store = self.client.beta.vector_stores.create()
                    vector_store_id = new_vector_store.id
                    print(f"New Vector Store is created with ID = {vector_store_id}")
                else:
                    print(f"The extracted Vector Store Id = {vector_store_id}")
                                                         
                # 3. Clean old files in Vector Store                
                vector_store_files_response = self.client.beta.vector_stores.files.list(vector_store_id=vector_store_id)                    
                vector_store_files_list = dict_helper.deep_get(vector_store_files_response.model_dump(), ['data'], default=None)
                if vector_store_files_list is not None and len(vector_store_files_list) > 0:
                    for file_item in vector_store_files_list:
                        file_id = dict_helper.deep_get(file_item, ['id'], default=None)
                        print(f"Processing to remove File {file_id} from Vector Store {vector_store_id}")
                        if file_id is not None:                            
                            # Remove the file from Vector Store
                            print(f"Removing File {file_id} from Vector Store {vector_store_id}")
                            self.client.beta.vector_stores.files.delete(file_id=file_id, vector_store_id=vector_store_id)
                            # Delete the file from File Storage
                            print(f"Deleting File {file_id} from File Storage")
                            self.client.files.delete(file_id=file_id)
                else:
                    print(f"No files to clean on Vector Store {vector_store_id}")                      
          
                # 4. Upload a file with an "assistants" purpose
                # Ready the files for upload to OpenAI                

                # Use the upload and poll SDK helper to upload the files, add them to the vector store,
                # and poll the status of the file batch for completion.                
                
                # currently the upload_and_poll not WORK
                # file_paths = [self.intent_file]
                # print(f"Uploading files {file_paths} to Vector Store {vector_store_id}...")
                # file_streams = [open(path, "rb") for path in file_paths]
                # file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
                #     vector_store_id=vector_store_id, files=file_streams
                # )
                
                print(f"Uploading intent file with assistants purpose...\n{self.intent_file}.")
                my_file = self.client.files.create(
                    file=open(self.intent_file, "rb"),
                    purpose='assistants'
                )
                print(f"Uploading file {my_file.id} to Vector Store {vector_store_id}...")
                file_batch = self.client.beta.vector_stores.file_batches.create(
                    vector_store_id=vector_store_id,
                    file_ids=[my_file.id]
                    )
                
                # monitor the file batch status
                is_file_uploaded = False
                while file_batch.status != "completed":
                    file_batch = self.client.beta.vector_stores.file_batches.retrieve(
                        batch_id=file_batch.id, 
                        vector_store_id=vector_store_id
                        )
                    
                    print(f"My batch file {file_batch.id} has status: {file_batch.status}")
                    if file_batch.status == "failed" :
                        break
                
                print(f"Uploaded files to Vector Store {vector_store_id} with status: {file_batch.schema_json}\n{file_batch}")
                
                # 5. Update knowledge file
                if file_batch.status == "failed":
                    print(f"Failed to update files to Vector Store")
                else:                    
                    # To make the files accessible to your assistant, 
                    # update the assistant’s tool_resources with the new vector_store id.
                    assistant_name = f"Created_assistant_{self.botName}"
                    attached_assistant = self.client.beta.assistants.update(
                        name=assistant_name,
                        assistant_id=self.assistantID,
                        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
                        tools=[{"type": "file_search"}],
                    )
                    print(f"Update knowledge file success on Assistant: {attached_assistant.id}\n{attached_assistant}")
                
            except Exception as e:
                tb = traceback.format_exc()
                print(f"Fail to update knowledge file \n{tb}")

        self.sync = 1

    def process_files_upload(self):
        instruction = instruction_to_generate_qa_lists_from_text_vi

        for file_path in self.upload_file_paths:
            if self.genIntent:
                qa_df = process_input_text_file(file_path, 'pdf', instruction, 'vi', 1, PAGES_THRESHOLD_TO_BREAK, False)
                print(qa_df)
                self.questions.extend(qa_df['question'].to_list())
                self.answers.extend(qa_df['answer'].to_list())

            if self.feedIntent:
                text_page_list = extract_text_from_file(file_path, 'pdf')
                with open(self.intent_file, "a") as f:
                    for item in text_page_list:
                        f.write(str(item) + "\n")  # Convert each item to string and add newline

        if self.sync == 1:
            self.sync = 2
        else:
            self.publish_output()

    def process_crawler_results(self):
        instruction = instruction_to_generate_qa_lists_from_text_vi

        if self.genIntent:
            for file_path in self.crawl_result_files:
                qa_df = process_input_text_file(file_path, 'json', instruction, 'vi', 1, PAGES_THRESHOLD_TO_BREAK, False)
                print(qa_df)
                self.questions.extend(qa_df['question'].to_list())
                self.answers.extend(qa_df['answer'].to_list())

        if self.sync == 1:
            self.sync = 2
        else:
            self.publish_output()

    def callback_l2_app(self, body, sub_dir=None):
        '''
            Function: callback_l2_app
        '''
        print("Start callback l2_app consuming!")
        path_intent_file = self.intent_file
        path_sub = f"uploads/{self.requestID}"
        if not os.path.exists(path_sub):
            os.makedirs(path_sub)
        domain = urlparse(body).netloc
        output_file_name = path_sub + "/" + domain + "_output.json"
        while os.path.exists(output_file_name):
            domain += "_x"
            output_file_name = path_sub + "/" + domain + "_output.json"
        match = body
        if body.endswith('/'):
            match += '**'
        else:
            match += '/**'

        config = Config(
            url=body,
            match=match,
            selector="body",
            # selector="#SITE_PAGES",
            max_pages_to_crawl=10,
            output_file_name = output_file_name,
            path_intent_file = path_intent_file
        )
        asyncio.run(crawler(config))
        self.crawl_result_files.append(output_file_name)

        # self.reset_task_queue()

# Function to get page HTML
async def get_page_html(page, selector):
    await page.wait_for_selector(selector)
    element = await page.query_selector(selector)
    return await element.inner_text() if element else ""

# Crawl function
async def crawl(config):
    results = []
    queue = [config.url]
    # print(f"match : {config.match}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        if config.cookie:
            await page.context.add_cookies([{
                "name": config.cookie['name'], 
                "value": config.cookie['value'], "url": config.url}])

        try:
            count=1
            while queue and len(results) < config.max_pages_to_crawl:
                url = queue.pop(0)
                print(f"Crawler: {count}/{config.max_pages_to_crawl} Crawling {url}")
                try:
                    await page.goto(url, timeout = 0)
                    html = await get_page_html(page, config.selector)
                    results.append({'url': url, 'html': html})
                    with open(config.output_file_name, 'w') as f:
                        json.dump(results, f, indent=2)

                    with open(config.path_intent_file, "a") as f:
                        f.write(html + "\n")  # Add newline character after the text
                    # print(html)

                    # Extract and enqueue links
                    links = await page.query_selector_all("a")
                    for link in links:
                        href = await link.get_attribute("href")
                        if href and fnmatch.fnmatch(href, config.match):
                            # print(f" Add link to queue {href}")
                            queue.append(href)
                except Exception as e:
                    tb = traceback.format_exc()
                    print(f"[ERROR]Can't load the page! {url} \n{tb}")
                count+=1
        finally:
            await browser.close()

    return results

async def crawler(config):
    results = await crawl(config)
    with open(config.output_file_name, 'w') as f:
        json.dump(results, f, indent=2)
