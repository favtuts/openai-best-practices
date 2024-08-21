import os
import sys
import unicodedata
from unidecode import unidecode

from underthesea import word_tokenize

import pandas as pd
from langdetect import detect, LangDetectException
from thefuzz import fuzz

from gemini_engin import generate_text, extract_text_from_response

HIGH_CONFIDENCE_THRESHOLD = 75
MEDIUM_CONFIDENCE_THRESHOLD = 40
TOP_K = 2

# Read vietnamese stop words
def read_vietnamese_stopwords(vietnamese_stopwords_file_path):
    with open(vietnamese_stopwords_file_path, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
    return stopwords

def remove_vietnamese_stopwords(text, stopwords):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    filtered_text = ' '.join(filtered_words)
    return filtered_text
vietnamese_stopwords = read_vietnamese_stopwords('vietnamese_stopwords.txt')

def remove_vietnamese_accents(input_str):
    # Normalize the Unicode string to decompose characters with accents into character + accent combinations
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    
    # Filter out the accents and combine back to a single string without accents
    return "".join([c for c in nkfd_form if not unicodedata.combining(c)])

def detect_language(text, default_language='en'):
    """Detect the language of the given text."""
    try:
        detected_language_code = detect(text)
    except LangDetectException:
        detected_language_code = default_language
    return detected_language_code

def compute_similarity(sentence1, sentence2, target_language):
    if target_language == 'Vietnamese':
        # sentence1 = remove_vietnamese_accents(sentence1)
        #sentence2 = remove_vietnamese_accents(sentence2)

        sentence1 = word_tokenize(sentence1, format="text")
        sentence2 = word_tokenize(sentence2, format="text")
        
    # print(target_language, sentence1, sentence2)

    """Compute sentence similarity using TheFuzz."""
    similarity_score = fuzz.ratio(sentence1, sentence2) # token_sort_ratio, token_set_ratio, partial_ratio

    return similarity_score

def look_for_similarity_questions(user_input, qa_data, target_language):
    """Look for similar questions in the QA data."""
    # Calculate similarity scores, including the index of each question
    similarity_scores = [(compute_similarity(user_input.lower(), question.lower(), target_language), idx) 
                         for idx, question in enumerate(qa_data['question'])]
    similarity_scores.sort(reverse=True, key=lambda x: x[0])
    
    # Filter out questions below a certain similarity threshold or return the top K questions
    similar_questions_indices_high = [(score, idx) for score, idx in similarity_scores if score > HIGH_CONFIDENCE_THRESHOLD][:TOP_K]
    similar_questions_indices_medium = [(score, idx) for score, idx in similarity_scores if score > MEDIUM_CONFIDENCE_THRESHOLD][:TOP_K]
    
    # Print the similar questions
    print('\n\nSimilar questions identified:')
    for score, idx in similar_questions_indices_medium:
        question = qa_data.iloc[idx]['question']
        print(f'Question: {question} (Confidence: {score}%)')
    print('\n\n')

    return similar_questions_indices_high, similar_questions_indices_medium

def look_for_similarity_answers(user_input, qa_data, target_language):
    """Look for similar answers in the QA data."""
    # Calculate similarity scores, including the index of each question
    similarity_scores = [(compute_similarity(user_input.lower(), question.lower(), target_language), idx) 
                         for idx, question in enumerate(qa_data['answer'])]
    similarity_scores.sort(reverse=True, key=lambda x: x[0])
    
    # Filter out questions below a certain similarity threshold or return the top K questions
    similar_questions_indices = [(score, idx) for score, idx in similarity_scores if score > MEDIUM_CONFIDENCE_THRESHOLD][:TOP_K]

    # Print the similar questions
    print('\n\nSimilar answers identified:')
    for score, idx in similar_questions_indices:
        question = qa_data.iloc[idx]['answer']
        print(f'Answer: {question} (Confidence: {score}%)')
    print('\n\n')

    return similar_questions_indices

def find_questions_by_indices(question_indices, qa_data):
    """Retrieve questions for the given indices."""
    return [qa_data.iloc[idx]['question'] for score, idx in question_indices]

def look_for_answers(similar_questions_indices, qa_data):
    """Retrieve answers for the similar questions identified."""
    output_answers = []
    for score, idx in similar_questions_indices:
        label = 'Complementary' if MEDIUM_CONFIDENCE_THRESHOLD <= score <= HIGH_CONFIDENCE_THRESHOLD else ''
        answer = qa_data.iloc[idx]['answer']
        output_answers.append((answer, f'(Confidence: {score}%)'))
    return output_answers

def get_answer(user_input, qa_data, target_language):
    user_input = str(user_input)
    user_input = user_input.lower().strip()
    similar_questions_indices_high, similar_questions_indices_medium = look_for_similarity_questions(user_input, qa_data, target_language)

    if similar_questions_indices_high:
        output_answers = look_for_answers(similar_questions_indices_high, qa_data)
        if output_answers:
            return output_answers
    elif similar_questions_indices_medium and not similar_questions_indices_high:
        suggessted_similar_questions = find_questions_by_indices(similar_questions_indices_medium, qa_data)
        if suggessted_similar_questions:
            return [f'Sorry, I do not have an answer for that. Please try to ask more specifically. For example: {suggessted_similar_questions}']
    else:
        similar_answer_indices = look_for_similarity_answers(user_input, qa_data, target_language)
        output_answers = []
        if similar_answer_indices:
            for idx in range(len(similar_answer_indices)):
                output_answers.append(qa_data['answer'][similar_answer_indices[idx]])
                return output_answers
        else:
            return ['Sorry, I do not have an answer for that. Please try to ask more specifically.']
    
    # If no similar questions are found
    '''
    answer_list = qa_data["answer"].tolist()
    question_list = qa_data["question"].tolist()
    prompt = f'Given the concept of {user_input}, identify the list item that best matches this concept from the following options {question_list}'


    response_with_gemini = generate_text(prompt)
    # print(prompt)
    if response_with_gemini is not None:
        # answer = response_with_gemini.text
        answer = extract_text_from_response(response_with_gemini)
        print('\n\nGemini answer:', answer)
        answer = answer.strip().lower()
        similar_questions_indices = look_for_similarity_questions(answer, qa_data)
        
        if similar_questions_indices:
            output_answers = look_for_answers(similar_questions_indices, qa_data)
            if output_answers:
                return output_answers
        
        # return [f'I am not sure about the following answer. Please try to ask more specifically. {answer}.']
    '''

    return ['Sorry, I do not have an answer for that. Please try to ask more specifically.']

# Main function
if __name__ == '__main__':
    print('\n\nQ&A Chatbot\n\n')
    data_file_path = sys.argv[1]

    # Read Q&A data from Excel file
    qa_data = pd.read_excel(data_file_path)

    while True:
        user_input = input("\nEnter your question (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            break

        # Fetching answers based on the user input
        output_answers = get_answer(user_input, qa_data)
        
        if output_answers == ['Sorry, I do not have an answer for that. Please try to ask more specifically.']:
            print(output_answers[0])  # Print the message directly
        else:
            print('\nAnswers:\n')
            for answer in output_answers:
                print(f"{answer}")

