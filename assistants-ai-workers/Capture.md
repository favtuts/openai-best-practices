# First run

```sh
Using env file: /home/tvt/techspace/openai/openai-best-practices/assistants-ai-workers/.env
Start with type :  l2_app
[INFO] Start thread!
[INFO] Start thread 0
Start thread : 0
[INFO] LISTENING......
[INFO] Waiting for msg at task_queue !
Initial Connection!!
Start listen!intent_crawler
Start consuming! intent_crawler

[INFO]Start callback! intent_crawler time = 2024-08-12 21:56:18.594565 
Start callback intent_crawler
Body : b'{"botName":"Calla test","assistantId":null,"requestId":"66a0a84f994cb30aa0b2b351.v1.6","apiKey":null,"urls":[],"fileUrls":["http://192.168.0.33:3307/va-admin/api/v1/file/66b987a55379df46a4d104d7"],"genIntent":true,"feedIntent":false}', ch: <BlockingChannel impl=<Channel number=1 OPEN conn=<SelectConnection OPEN transport=<pika.adapters.utils.io_services_utils._AsyncPlaintextTransport object at 0x7fda9d264280> params=<ConnectionParameters host=192.168.0.33 port=5672 virtual_host=/ ssl=False>>>>, method <Basic.Deliver(['consumer_tag=ctag1.2d4bbf0cc4124b2994312a6673fbf2d8', 'delivery_tag=1', 'exchange=', 'redelivered=False', 'routing_key=intent_crawler'])>, porperties : <BasicProperties(['content_type=application/json', 'delivery_mode=2', 'headers={}', 'priority=0'])> 
[INFO] Put Queue : intent_crawler 2024-08-12 21:56:18.594683 
*********************************************
[ERROR] Fail to put queue join() argument must be str, bytes, or os.PathLike object, not 'NoneType'
Continue...
Finish call back of listening
```