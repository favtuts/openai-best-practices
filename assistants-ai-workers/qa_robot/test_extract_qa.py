import re

import pandas as pd


def convert_text_to_faq_dataframe(text):
    # Initialize an empty DataFrame with columns for questions and answers
    faq_df = pd.DataFrame(columns=['question', 'answer'])
    faq_df_1 = pd.DataFrame(columns=['question', 'answer'])
    faq_df_2 = pd.DataFrame(columns=['question', 'answer'])

    # Adjusting the pattern for correct question-answer extraction
    pattern_1 = r'"question": "(.*?)"\s*?"answer": "(.*?)"'
    matches_1 = re.findall(pattern_1, text, re.DOTALL)
    if matches_1:
        # Create a list of dictionaries from matches, ensuring whitespace is stripped
        faq_list_1 = [{'question': match[0].strip(), 'answer': match[1].strip()} for match in matches_1]
        # Convert the list of dictionaries to a DataFrame
        faq_df_1 = pd.DataFrame(faq_list_1)
    
    # pattern_2 = r'Câu hỏi \d+: (.*?)\nTrả lời: (.*?)(?=\nCâu hỏi \d+|\Z)'
    pattern_2 = r'Câu hỏi(?: \d+)?:\s*(.*?)\nTrả lời:\s*(.*?)(?=\nCâu hỏi(?: \d+)?:|\Z)'



    matches_2 = re.findall(pattern_2, text, re.DOTALL)
    if matches_2:
        # Create a list of dictionaries from matches, ensuring whitespace is stripped
        faq_list_2 = [{'question': match[0].strip(), 'answer': match[1].strip()} for match in matches_2]
        # Convert the list of dictionaries to a DataFrame
        faq_df_2 = pd.DataFrame(faq_list_2)

    print('\n\n =========== faq_df_1 ==========')
    print(faq_df_1)

    print('\n\n ===========')
    print(faq_df_2)

    # Concatenate the two DataFrames
    faq_df = pd.concat([faq_df_1, faq_df_2], ignore_index=True)

    if not faq_df.empty:
        # Removing rows where the combination of all column values is duplicated
        faq_df = faq_df.drop_duplicates(subset=['question'], keep='first')

        # Reset the index of the DataFrame and drop the old index
        faq_df = faq_df.reset_index(drop=True)

    return faq_df

text = """
Câu hỏi 5: Người thụ hưởng có thể được chỉ định lại không?
Trả lời: Có, Bên mua bảo hiểm có thể gửi yêu cầu thay đổi (những) Người thụ hưởng hoặc tỉ lệ thụ hưởng của mỗi Người thụ hưởng của Hợp đồng bảo hiểm cho BIDV MetLife trong thời gian Hợp đồng bảo hiểm có hiệu lực và Người được bảo hiểm còn sống, nếu được Người được bảo hiểm đồng ý bằng văn bản.

Câu hỏi 6: Trong trường hợp Bên mua bảo hiểm là cá nhân bị tử vong, ai sẽ thừa kế quyền lợi và nghĩa vụ phát sinh từ Hợp đồng bảo hiểm?
Trả lời: Người thừa kế hợp pháp của Bên mua bảo hiểm sẽ thừa kế toàn bộ quyền lợi và nghĩa vụ phát sinh từ Hợp đồng bảo hiểm theo quy định của pháp luật về thừa kế.

Câu hỏi 7: Thời hạn yêu cầu giải quyết Quyền lợi bảo hiểm là bao lâu?
Trả lời: Trong vòng 12 tháng kể từ ngày Người được bảo hiểm tử vong hoặc Thương tật toàn bộ vĩnh viễn.

Câu hỏi 8: BIDV MetLife có trách nhiệm giải quyết Quyền lợi bảo hiểm trong bao lâu?
Trả lời: Trong vòng 30 ngày kể từ ngày nhận được đầy đủ hồ sơ yêu cầu giải Quyết quyền lợi bảo hiểm hợp lệ.

Câu hỏi 9: BIDV MetLife có được chuyển giao thông tin cá nhân của Bên mua bảo hiểm/Người được bảo hiểm cho bên thứ ba không?
Trả lời: Không, BIDV MetLife không được chuyển giao thông tin cá nhân do Bên mua bảo hiểm/Người được bảo hiểm cung cấp tại Hợp đồng bảo hiểm cho bất kỳ bên thứ ba nào khác, trừ các trường hợp theo quy định của pháp luật.

Câu hỏi 10: Khi nào BIDV MetLife sẽ miễn truy xét các nội dung kê khai không chính xác trong Hồ sơ yêu cầu bảo hiểm?
Trả lời: Khi Người được bảo hiểm còn sống, các nội dung kê khai không chính xác trong Hồ sơ yêu cầu bảo hiểm và các giấy tờ có liên quan sẽ được BIDV MetLife miễn truy xét sau 24 tháng kể từ Ngày hiệu lực của Hợp đồng bảo hiểm..

"question": "Quyền lợi bảo hiểm tử vong là gì?"
"answer": "BIDV MetLife sẽ chi trả 100% Số tiền bảo hiểm tương ứng quyền lợi tử vong được quy định tại Giấy chứng nhận bảo hiểm."

"question": "Quyền lợi bảo hiểm thương tật toàn bộ vĩnh viễn là gì?"
"answer": "BIDV MetLife sẽ chi trả 100% Số tiền bảo hiểm tương ứng quyền lợi Thương tật toàn bộ vĩnh viễn được quy định tại Giấy chứng nhận bảo hiểm."

"question": "Ngày hiệu lực của Hợp đồng là khi nào?"
"answer": "Là ngày Bên mua bảo hiểm hoàn tất Hồ sơ yêu cầu bảo hiểm và đóng đầy đủ Phí bảo hiểm tạm tính."
"question": "Ngày kỷ niệm hợp đồng là gì?"
"answer": "Là ngày tương ứng hàng năm của Ngày hiệu lực của Hợp đồng."

Câu hỏi: Loại trừ đối với sự kiện tử vong là gì?
Trả lời: BIDV MetLife sẽ không chi trả các quyền lợi bảo hiểm nếu Người được bảo hiểm tử vong do một trong các nguyên nhân sau: tự tử, cố ý phạm tội, thi hành án tử hình, nhiễm HIV/AIDS, sử dụng trái phép vũ khí quân dụng, các Bệnh có sẵn, Bệnh bẩm sinh, tâm thần.

Câu hỏi: Loại trừ đối với sự kiện Thương tật toàn bộ vĩnh viễn là gì?
Trả lời: BIDV MetLife sẽ không chi trả quyền lợi bảo hiểm nếu Người được bảo hiểm bị Thương tật toàn bộ vĩnh viễn do một trong các nguyên nhân sau: các trường hợp quy định tại Khoản 6.1 (Loại trừ áp dụng cho sự kiện tử vong), tham gia đánh nhau, tham gia các môn thể thao hoặc hoạt động nguy hiểm, lên, xuống, vận hành, phục vụ, hoặc đang được chở trên các thiết bị hoặc phương tiện vận chuyển hàng không, thực hiện phẫu thuật, khám chữa bệnh tại các cơ sở y tế không được thành lập và hoạt động hợp pháp, động đất, núi lửa, nổ bom hạt nhân, chiến tranh..Câu hỏi: Hợp đồng bảo hiểm tử kỳ là gì?
Trả lời: Hợp đồng bảo hiểm tử kỳ là thỏa thuận bằng văn bản giữa Bên mua bảo hiểm và Công ty bảo hiểm, trong đó ghi nhận quyền và nghĩa vụ của các bên trong quá trình thực hiện Hợp đồng.

Câu hỏi: Thời hạn bảo hiểm tạm thời bắt đầu từ khi nào?
Trả lời: Thời hạn bảo hiểm tạm thời bắt đầu từ khi Bên mua bảo hiểm hoàn tất Hồ sơ yêu cầu bảo hiểm và đóng đủ Phí bảo hiểm tạm tính.

Câu hỏi: Trường hợp nào BIDV MetLife sẽ không chi trả Quyền lợi bảo hiểm tạm thời?
Trả lời: BIDV MetLife sẽ không chi trả Quyền lợi bảo hiểm tạm thời và hoàn lại toàn bộ Phí bảo hiểm đã đóng sau khi trừ đi chi phí khám sức khỏe (nếu có), nếu Người được bảo hiểm tử vong trực tiếp do một trong các nguyên nhân sau:
- Không phải tai nạn;
- Tự tử, tự gây thương tích hoặc tự gây tai nạn, dù trong trạng thái tinh thần bình thường hay mất trí;
- Do hành vi cố ý của Bên mua bảo hiểm, Người thụ hưởng đối với Người được bảo hiểm;
- Sử dụng trái phép vũ khí quân dụng, sử dụng ma túy hoặc các chất kích thích, rượu, bia, vượt mức quy định của pháp luật.

Câu hỏi 6: Nếu Người được bảo hiểm ra khỏi phạm vi lãnh thổ Việt Nam trong thời gian từ 90 ngày trở lên, Bên mua bảo hiểm phải thông báo cho BIDV MetLife tối thiểu bao nhiêu ngày trước ngày Người được bảo hiểm xuất cảnh?
Trả lời: 30 ngày.

Câu hỏi 7: Trong vòng bao nhiêu tháng kể từ ngày Người được bảo hiểm tử vong hoặc Thương tật toàn bộ vĩnh viễn, Người yêu cầu giải quyết Quyền lợi bảo hiểm phải lập hồ sơ yêu cầu giải quyết quyền lợi bảo hiểm và gửi tới BIDV MetLife?
Trả lời: 12 tháng.

Câu hỏi 10: Trong trường hợp Bên mua bảo hiểm và/hoặc Người được bảo hiểm vi phạm nghĩa vụ kê khai thông tin, BIDV MetLife có thể đơn phương chấm dứt Hợp đồng bảo hiểm không?
Trả lời: Có, BIDV MetLife có quyền đơn phương chấm dứt Hợp đồng bảo hiểm ngay sau khi phát hiện ra hành vi vi phạm..


"""


convert_text_to_faq_dataframe(text)