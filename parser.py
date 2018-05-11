import io
import chardet
import os
import codecs
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.snowball import RussianStemmer

class Parser:
    badwords = ['я', 'а', 'да', 'но', 'тебе', 'мне', 'ты', 'и', 'у', 'на', 'ща', 'ага',
                'так', 'там', 'какие', 'который', 'какая', 'туда', 'давай', 'короче', 'кажется', 'вообще',
                'ну', 'не', 'чет', 'неа', 'свои', 'наше', 'хотя', 'такое', 'например', 'кароч', 'как-то',
                'нам', 'хм', 'всем', 'нет', 'да', 'оно', 'своем', 'про', 'вы', 'м', 'тд',
                'вся', 'кто-то', 'что-то', 'вам', 'это', u'эта', 'эти', 'этот', 'прям', 'либо', 'как', 'мы',
                'просто', 'блин', 'очень', 'самые', 'твоем', 'ваша', 'кстати', 'вроде', 'типа', 'пока', 'ок', 
                'т', 'д', 'р'
    ]       
    
    def __init():
        return
    
    def get_data_from_file(self, address_of_text):
        bytes = min(32, os.path.getsize(address_of_text))
        raw = open(address_of_text, 'rb').read(bytes)
        
        if raw.startswith(codecs.BOM_UTF8):
            encoding = 'utf-8-sig'
        else:
            result = chardet.detect(raw)
            encoding = result['encoding']
        
        infile = io.open(address_of_text, 'r', encoding=encoding)
        data = infile.read()
        infile.close()
        
        return data
    
    def parse_text(self, text):
        text = list(text)
        
        for i in range(len(text)):
            is_cyrillic_symbol = False
            if text[i] >= 'А' and text[i] <= 'Я':
                is_cyrillic_symbol = True
            if text[i] >= 'а' and text[i] <= 'я':
                is_cyrillic_symbol = True
                
            if is_cyrillic_symbol == False:
                text[i] = ' '
                
        text = ''.join(text)
        text = text.split()
        filtered_words = [word for word in text if word not in stopwords.words('russian') and word not in self.badwords]
        
        stemmer = RussianStemmer()
        
        for i in range(len(filtered_words)):
            filtered_words[i] = stemmer.stem(filtered_words[i])
            
        return filtered_words
                    
    def exclusion_signle_copy(self, word_list):
        cnt = Counter(word_list)
        words = [word for word in word_list if cnt[word] > 1]
        return words
            
    
    def text_preprocessing(self, file_name):
        data = self.get_data_from_file(file_name)
        words = self.parse_text(data)
        words = self.exclusion_signle_copy(words)
        for i in range(len(words)):
            words[i] = words[i] + ' '
        text = ''.join(words)
        return text

