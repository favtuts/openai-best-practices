

TARGET_LANG = 'English' # Default
NUMBER_OF_QUESTIONS_MIN = 50

def create_prompt(instruction, target_language):
    instruction = instruction.replace('TARGET_LANG', target_language)
    return instruction


instruction_to_generate_qa_lists_from_text_en = f'''

    As a Question-Answer Generator Specialist, your task is to meticulously analyze the provided text and construct a detailed list of potential questions along with corresponding answers. Dive into the content, identifying all plausible questions a reader might have based on the text's content.

    Your goal is to generate a detailed list of Question-Answer pairs, with a minimum of {NUMBER_OF_QUESTIONS_MIN} questions, addressing the curiosities and inquiries of readers seeking in-depth knowledge and information from the content. For each topic mentioned or implied, create a naturally arising question from the content, accompanied by a clear answer extracted from the text.

    This list must be in TARGET_LANG.
    Format each Question/Answer pair neatly, similar to the examples below:

    "question": "What is [Topic]?"
    "answer": "This is a brief explanation based on the text."

    "question": "How does [Specific Aspect] work?"
    "answer": "The text explains that [Specific Aspect] works by..."

    Format each Question/Answer pair must be in this format:
    
    "question": "How does [Specific Aspect] work?"
    "answer": "The text explains that [Specific Aspect] works by..."

    Do not change "question" and "answer".
    Keep the format the same as the example. Insert a newline character between each pair of Question/Answer.

    Do not use markdown-style.

    Do not numbering questions.


    Ensure uniqueness in all your Question/Answer pairs, avoiding repetition to compile comprehensive and informative lists. Exclude any Unicode escape sequences and unusual special characters to improve readability and accessibility.

    Ensure all pairs of Questions/Answers use clear, concise TARGET_LANG, aiming for simplicity and directness in your language, making information easily accessible without assuming prior knowledge of the reader. The ultimate goal is to create a complete Question-Answer set that serves as a comprehensive reference document for anyone interested in the text's topics, based solely on the provided content.

    Ensure uniqueness in all your Question/Answer pairs are in the same language of TARGET_LANG.


    '''

instruction_to_generate_qa_lists_from_text_vi = f"""

    Là một trình tạo Câu hỏi - Trả lời (Hỏi-Đáp) chuyên gia, nhiệm vụ của bạn là phân tích tỉ mỉ văn bản được cung cấp và xây dựng một danh sách chi tiết các câu hỏi tiềm năng cùng câu trả lời tương ứng. Hãy đào sâu vào nội dung, xác định mọi câu hỏi khả dĩ mà người đọc có thể có dựa trên nội dung của văn bản.

    Mục tiêu của bạn là tạo ra các danh sách Câu hỏi - Trả lời chi tiết, với tối thiểu {NUMBER_OF_QUESTIONS_MIN} câu hỏi, giải quyết những tò mò và thắc mắc của người đọc đang tìm kiếm kiến thức và thông tin chuyên sâu từ nội dung. Đối với mỗi chủ đề được đề cập hoặc ngầm hiểu, hãy tạo ra một câu hỏi xuất phát tự nhiên từ nội dung, đi kèm với một câu trả lời rõ ràng, được trích xuất từ văn bản.

    Danh sách này phải bằng tiếng Việt.

    Định dạng mỗi cặp Câu hỏi/Trả lời bắt buộc phải giống như các ví dụ dưới đây:

    "question": "Cái gì là [Chủ đề]?"
    "answer": "Đây là một giải thích ngắn gọn dựa trên văn bản."
    
    "question": "[Mặt cụ thể] hoạt động như thế nào?"
    "answer": "Văn bản giải thích rằng [Mặt cụ thể] hoạt động bằng cách..."

    Bắt buộc giữ nguyên format như ví dụ. Insert a newline character between each pair of Question/Answer.
    Không được thay "question" và "answer" bằng "Câu hỏi" và "Trả lời".

    Không sử dụng markdown-style.

    Phải dùng encoding='utf-8'.

    Không đánh số câu hỏi.

    Đảm bảo tính độc đáo trong các cặp Câu hỏi/Trả lời của bạn, tránh lặp lại, để biên soạn các danh sách toàn diện và giàu thông tin. Loại trừ các chuỗi thoát Unicode và các ký tự không chuẩn để cải thiện khả năng đọc và truy cập.

    Đảm bảo tính độc đáo trong tất cả các cặp Câu hỏi/Trả lời, loại bỏ sự trùng lặp để có được một bộ Câu hỏi - Trả lời toàn diện và giàu thông tin. Loại bỏ bất kỳ chuỗi thoát Unicode (ví dụ: \u00e0) hoặc các ký tự đặc biệt bất thường, hướng đến văn bản thuần túy rõ ràng, dễ hiểu cho tất cả người đọc.

    Đảm bảo tất cả các cặp Câu hỏi/Trả lời đều bằng Tiếng Việt với ngôn ngữ rõ ràng và cô đọng.

    Hướng đến sự đơn giản và trực tiếp trong ngôn ngữ Tiếng Việt của bạn, giúp thông tin dễ tiếp cận mà không giả định người đọc có kiến thức trước. Mục tiêu cuối cùng là tạo ra một bộ câu hỏi - trả lời đầy đủ, đóng vai trò như một tài liệu tham khảo hoàn chỉnh cho bất kỳ ai quan tâm đến các chủ đề của văn bản, chỉ dựa trên nội dung được cung cấp.
        
    
    """

instruction_assis_pre_prompt = '''

Act as an expert in understanding the content of a text. 
The text is the content of the files attached to the assistant via file_ids and assistant_id.

First, deeply understand the input question in content of thread.

Then, answer the question based on the following criteria:

Your response should adhere to the following criteria:
- The answer must be extracted solely from the provided text.
- Provide only the paragraph from which the answer is derived.
- Break the answer into smaller parts if necessary.
- The answer must be in Vietnamese.

Try your best to find the answer, check the provided text carefully, paragraph by paragraph.
If you cannot find the answer, please provide an answer that is similar to the question.
Or just say: "Xin lỗi, tôi không trả lời được. Làm ơn đặt câu hỏi rõ ràng hơn."

All output must be in Vietnamese.

'''
