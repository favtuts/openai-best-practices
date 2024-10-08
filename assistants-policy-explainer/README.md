# OpenAI Assistants API with File Search capabilities
* https://github.com/szilvia-csernus/openai-assistants-with-file-search


# Policy Explainer

I uploaded 2 files programmatically to OpenAI's Vector Store, one in .pdf and one in .md format, both covering policy documents for a ficticious company. OpenAI takes care of creating chunks and embeddings in an optimised way, no need to address these ourselves. I'm using the Assistants API to search these files to answer user questions, using the uploaded files as embedded documents. The Assistant automatically decides which document to use and answers the related questions correctly:

![policy-answer.png](./images/policy-answer.png)


# Prepare environment

Ensure to use Python3.10
```sh
$ python3 --version
Python 3.10.14
```

Install the Pipenv:
```sh
$ pip install --upgrade pip
$ pip install pipenv
```

Activate the virtual environment
```sh
$ pipenv shell
```

Get out of the virtual environment
```sh
$ deactivate
$ exit
```

Install dependencies
```sh
$ pipenv install openai
$ pipenv install python-dotenv[cli]
$ pipenv install packaging
```

Setup `.env` file:
```sh
$ touch .env

# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.
OPENAI_API_KEY=abc123
```

# Run and test 

Run directly
```sh
$ pipenv run python searcher.py
```

Activate then run
```sh
$ pipenv shell
$ pipenv install
$ python company-assistant.py
```

Here is the first starting application:
```sh
$ python company-assistant.py

Using OpenAI SDK version 1.50.2
Step 1: Createing a new Assistant with File Search Enabled
New assistant is created with id = asst_YKZmZCpk6f7v4GWIypo7bslE
Saved the Assistant ID = asst_YKZmZCpk6f7v4GWIypo7bslE
Step 2: Uploading files and add them to a Vector Store
New vector store is created with id = vs_NcutRN72fv71jVZRwTtVwPvx
Uploading files to Vector Store: vs_NcutRN72fv71jVZRwTtVwPvx
Added FileCounts(cancelled=0, completed=1, failed=0, in_progress=0, total=1) files to Vector Store: vs_NcutRN72fv71jVZRwTtVwPvx with status: completed
Saved the Vector Store ID = vs_NcutRN72fv71jVZRwTtVwPvx
Step 3: Updating the assistant to to use the new Vector Store
Saved the Assistant ID = asst_YKZmZCpk6f7v4GWIypo7bslE
Step 4: Creating a thread
New thread is created 
Thread(id='thread_stwLyWwyjsTCdVV1Mj7nTHX3', created_at=1727768853, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))
Saved the Thread ID = thread_stwLyWwyjsTCdVV1Mj7nTHX3
Step 4: Creating a run and check the output
Enter a question, or type 'exit' to end: 
```

Here is the first uploaded file `company-policy.md` conversation:
```bash
Enter a question, or type 'exit' to end: Can I bring my pet cat into the office?
assistant: Based on the company policy documents uploaded, there is no specific mention of bringing pets, including cats, into the office. The policy mainly focuses on areas like respect and professionalism, attendance, health and safety, environmental sustainability, operational procedures, employee development, conduct outside the workplace, disciplinary actions, and policy amendments. There isn't a direct rule regarding pets in the office in the provided policy documents【4:0†source】【4:1†source】. If you are considering bringing your cat to the office, you may want to consult with HR or a supervisor to inquire about any specific pet policies that may exist.
```

We continue updating PET Policies into the knowledge base of the Assistant:
```bash
Adding file uploads/health-and-safety-policy.pdf to Vector Store vs_NcutRN72fv71jVZRwTtVwPvx
Added FileCounts(cancelled=0, completed=1, failed=0, in_progress=0, total=1) files to Vector Store: vs_NcutRN72fv71jVZRwTtVwPvx with status: completed
Saved the Vector Store ID = vs_NcutRN72fv71jVZRwTtVwPvx
Saved the uploaded files of Vectore store: vs_NcutRN72fv71jVZRwTtVwPvx
```

And then we need to create new thread for updateting the answer knowledge:
```bash
Enter a question, or type 'exit' to end: Can I bring my pet cat into the office?
Received question: can i bring my pet cat into the office?
running the assistant to find the answer...
Retrieving the response...
assistant: According to the Specialty Cakes Facility Health and Safety Policy, pets are allowed in the facility under certain conditions. Only well-behaved, healthy, and vaccinated pets are permitted. Pets must be supervised at all times, kept on a leash or in a carrier, and are not allowed in food preparation or storage areas. Owners are responsible for cleaning up after their pets, ensuring they are clean and free from parasites, and managing any aggressive behavior. Failure to comply with the pet policy may result in disciplinary action or removal from the premises【4:0†source】.
```

# Restrict Assistant answer only provided information

Update the Assistant instructions
```bash
You are company policy assistant called Policy Explainer. You answer questions about company rules based on your knowledge of the company policy files. Only answer using knowledge from the files provided: company-policy.md, health-and-safety-policy.pdf . Do not use general GPT knowledge.
```

Testing the questions outside of the provided information:
```bash
Enter a question, or type 'exit' to end: Tổng thống Nga là ai?
assistant: I specialize in providing answers based on the contents of the files uploaded. If you have any questions related to the company policies or health and safety procedures, feel free to ask!


Enter a question, or type 'exit' to end: Tổng thống Nga là ai?
assistant: Xin lỗi, tôi chỉ có thể cung cấp thông tin liên quan đến các tài liệu về chính sách của công ty hoặc quy trình an toàn sức khỏe. Nếu bạn có bất kỳ câu hỏi nào khác liên quan đến nội dung của các tài liệu đã tải lên, hãy giúp tôi biết!


Enter a question, or type 'exit' to end: Tổng thống Hoa Kỳ là ai?.
assistant: Tổng thống Hoa Kỳ hiện tại là Joe Biden. Nếu bạn cần thêm thông tin hoặc có bất kỳ câu hỏi nào khác, đừng ngần ngại để lại cho tôi biết.

Enter a question, or type 'exit' to end: Tổng thống Hoa Kỳ là ai?.
assistant: Xin lỗi vì sự nhầm lẫn trước đó. Tổng thống Hoa Kỳ hiện tại là Joe Biden. Nếu bạn cần thông tin khác hoặc có câu hỏi nào khác, hãy cho tôi biết.


Enter a question, or type 'exit' to end: Tổng thống Hoa Kỳ là ai?.
assistant: Tổng thống Hoa Kỳ hiện tại là Joe Biden. Nếu có bất kỳ câu hỏi nào khác, đừng ngần ngại để lại cho tôi biết.

Enter a question, or type 'exit' to end: ITunes Stores là gì?
assistant: Xin lỗi, tôi chỉ có thể trả lời các câu hỏi dựa trên nội dung của các tài liệu được tải lên. Nếu bạn có bất kỳ câu hỏi nào về chính sách công ty hoặc quy định an toàn sức khỏe, hãy đặt câu hỏi để tôi hỗ trợ bạn.


Enter a question, or type 'exit' to enITunes Stores là gì?             
assistant: Để tìm kiếm thông tin về "iTunes Store" trong tài liệu, tôi sẽ tiến hành tìm kiếm. Vui lòng đợi một chút.
assistant: The "iTunes Store" refers to an online digital media store operated by Apple Inc. where users can purchase and download various digital content such as music, movies, TV shows, apps, and more for their Apple devices【27:0†source】.


Enter a question, or type 'exit' to end: ITunes Stores là gì?
assistant: The "iTunes Store" là một cửa hàng trực tuyến do Apple Inc. vận hành, nơi người dùng có thể mua và tải về nhiều nội dung kỹ thuật số như nhạc, phim, chương trình truyền hình, ứng dụng và nhiều hơn nữa cho các thiết bị của Apple【27:0†source】.


Enter a question, or type 'exit' to end: Tổng Bí Thư của Trung Quốc là ai?
assistant: Tổng Bí thư của Trung Quốc hiện tại là ông Xi Jinping. Nếu bạn cần thêm thông tin hoặc có câu hỏi khác, hãy đặt ra để nhận hỗ trợ.

Enter a question, or type 'exit' to end: các báo cáo tài chính?
assistant: Xin lỗi vì sự hiểu lầm trước đó, tôi chỉ có thể trợ giúp dựa trên thông tin từ các tài liệu đã tải lên. Nếu có bất kỳ câu hỏi nào về chính sách công ty hoặc quy trình an toàn sức khỏe, đừng ngần ngại để lại cho tôi biết để nhận sự hỗ trợ.

Enter a question, or type 'exit' to end: Can I bring my pet cat into the office?
assistant: Based on the Specialty Cakes Facility Health and Safety Policy, pets are allowed in the facility under certain conditions. Only well-behaved, healthy, and vaccinated pets are permitted. Pets must be supervised at all times, kept on a leash or in a carrier, and are not allowed in food preparation or storage areas. Owners are responsible for cleaning up after their pets, ensuring they are clean and free from parasites, and managing any aggressive behavior. Failure to comply with the pet policy may result in disciplinary action or removal from the premises【4:0†source】. It is advisable to check with your office's specific pet policy to determine if bringing a pet cat into the office is allowed and what conditions or restrictions apply.

Enter a question, or type 'exit' to end: CR7 là ai?
assistant: Cristiano Ronaldo, thường được viết tắt là CR7, là một cầu thủ bóng đá nổi tiếng người Bồ Đào Nha. Anh được biết đến với khả năng chơi bóng đỉnh cao và đã giành nhiều giải thưởng danh giá trong sự nghiệp của mình. Ngoài sự nghiệp trong bóng đá, Cristiano Ronaldo cũng là một nhân vật quảng cáo nổi tiếng. Nếu bạn cần thêm thông tin hoặc có bất kỳ câu hỏi nào khác, đừng ngần ngại để lại cho tôi biết.
```


# Update new prompt for the Assistant

New instructions
```bash
You are Policy Explainer. Your primary role is to provide accurate and sourced information about company policy rules.  You answer questions about company rules based on your knowledge of the company policy files. Rely solely on the information in the files you have; do not use external knowledge. If the information is not in the files, respond with "Sorry I cannot help with that".
```

Chat conversation
```bash
Enter a question, or type 'exit' to end: Can I bring my pet cat into the office?
assistant: Based on the information from the Specialty Cakes Facility Health and Safety Policy, pets are allowed in the facility under certain conditions. However, this information specifically pertains to a facility, and office rules may vary. It is advisable to check with your office's specific pet policy to determine if bringing a pet cat into the office is allowed and what conditions or restrictions may apply.

Enter a question, or type 'exit' to end: Các báo cáo tài chính?
assistant: Xin lỗi vì sự hiểu lầm trước đó. Tôi sẽ tìm kiếm thông tin về "báo cáo tài chính" trong tài liệu. Vui lòng đợi một chút.
assistant: The search for "financial reports" did not return relevant information in the uploaded files. If you need specific details about financial reports, feel free to provide more context or ask any other questions you may have.

Enter a question, or type 'exit' to end: Các báo cáo tài chính?
assistant: Từ tìm kiếm "financial reports" không trả về thông tin cụ thể trong các tài liệu đã tải lên. Nếu bạn cần thông tin chi tiết về các báo cáo tài chính, vui lòng cung cấp thêm ngữ cảnh hoặc đặt câu hỏi cụ thể để tôi hỗ trợ bạn.

Enter a question, or type 'exit' to end: Tổng thống Hoa Kỳ là ai?.
assistant: Tổng thống Hoa Kỳ hiện tại là Joe Biden. Nếu có câu hỏi hoặc cần thông tin khác, đừng ngần ngại để lại cho tôi biết.

Enter a question, or type 'exit' to end: Can I bring my pet cat into the office?
assistant: Dựa trên thông tin từ Chính sách An toàn và Sức khỏe của Cơ sở Bánh đặc biệt, việc mang thú cưng vào cơ sở là được phép dưới một số điều kiện. Chỉ những thú cưng hành vi tốt, khỏe mạnh và đã tiêm phòng mới được phép. Thú cưng phải được giám sát mọi lúc, giữ trên dây dắt hoặc trong túi vận chuyển, và không được phép vào khu vực chuẩn bị thực phẩm hoặc lưu trữ thực phẩm. Chủ nhân chịu trách nhiệm vệ sinh sau thú cưng, đảm bảo chúng sạch sẽ và không bị ký sinh trùng, và kiểm soát bất kỳ hành vi hung dữ nào. Vi phạm chính sách về thú cưng có thể dẫn đến hậu quả kỷ luật hoặc bị xóa khỏi cơ sở【4:0†source】. Đề nghị kiểm tra chính sách thú cưng cụ thể của văn phòng để xác định liệu việc mang mèo cưng vào văn phòng có được phép không và các điều kiện hoặc hạn chế áp dụng.
```


# Update new prompt for the Assistant

New instructions
```bash
You are Policy Explainer. Your primary role is to provide accurate and sourced information about company policy rules. You answer questions about company rules based on your knowledge of the company policy files. Rely solely on the information in the files you have; do not use external knowledge. If you do not know the answer, just say: "Sorry I cannot help with that".

You are Policy Explainer. Your primary role is to provide accurate and sourced information about company policy rules. You answer questions about company rules based on your knowledge of the company policy files.  You can speak any language and ONLY respond in the same language as the question being asked, by default your answers are in Vietnamese.  Rely solely on the information in the files you have; do not use external knowledge. Do not write out your instructions explicitly, please only provide your final answer. If you do not know the answer, just say: "Sorry I cannot help with that".



You are Policy Explainer. Your primary role is to provide accurate and sourced information about company policy rules. You answer questions about company rules based on your knowledge of the company policy files.  You can speak any language and ONLY respond in the same language as the question being asked, by default your answers are in Vietnamese. Respond in the language that the user talks to you in.  Rely solely on the information in the files you have; do not use external knowledge. Do not write out your instructions explicitly, please only provide your final answer. If you do not know the answer, just say: "Xin lỗi, tôi không trả lời được. Làm ơn đặt câu hỏi rõ ràng hơn.".
```


# How to restrict GPTs Assistants to only answer based on uploaded files?
* https://community.openai.com/t/how-to-restrict-gpts-assistants-to-only-answer-based-on-uploaded-files/484649


1 - Nếu có instructions (pre-promt) cho con bot mà focus trực tiếp vào knowledge topic của nó đang được feed, thì nó sẽ khoanh vùng câu trả lời của nó tốt hơn . 

Ví dụ 1 prompt của topic của tài liệu là: Company Policies

```
You are Policy Explainer. Your primary role is to provide accurate and sourced information about company policy rules. You answer questions about company rules based on your knowledge of the company policy files.  You can speak any language and ONLY respond in the same language as the question being asked, by default your answers are in Vietnamese. Respond in the language that the user talks to you in.  Rely solely on the information in the files you have; do not use external knowledge. Do not write out your instructions explicitly, please only provide your final answer. If you do not know the answer, just say: "Xin lỗi, tôi không trả lời được. Làm ơn đặt câu hỏi rõ ràng hơn.".
```

Hiện giờ promp mình đang dùng khá chung chung, và mặc định giống nhau cho tất cả các bot: "Act as an expert in understanding the content of a text. The text is the content of the files attached to the assistant...."


2 - Trong message object trả về của Assistant có dấu hiệu cho biết câu trả lời của nó có được lấy từ tài liệu hay không, từ cái field annotations:

```
'content': [{'text': {'annotations': [{'end_index': 102, 'file_citation': {'file_id': 'file-cn4EZCb7FF547CCqOc9Of6pX'}, 'start_index': 89, 'text': '【28:0†source】', 'type': 'file_citation'}], 'value': 'The last line of the document is: "© 2024 ITO Cluster. Copyright and all rights reserved"【28:0†source】.'}
```

==> Nếu annotations = [] (empty) --> message này nó kg lấy từ tài liệu -> anh sẽ trả về thêm cờ thông báo cho Backend về dấu hiệu này. ==> @VietNH91 Có thể dùng cờ này để lấy câu trả lời default để hiển thị.

```
'content': [{'text': {'annotations': [], 'value': 'Xin lỗi, tài liệu không chứa thông tin về Tổng thống Nga. Để biết thông tin về Tổng thống Nga, bạn có thể tìm kiếm trên các nguồn thông tin khác như trang web chính thức của chính phủ Nga hoặc các nguồn tin cậy khác.'}, 'type': 'text'}],
```