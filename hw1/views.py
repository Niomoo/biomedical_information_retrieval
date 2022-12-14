from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import os
import xml.etree.ElementTree as ET
import json
from string import *
from wordcloud import WordCloud
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

# Create your views here.

def index(request):
    return render(request, 'index.html', {
        'uploaded': False,
    })

class Upload:
	# 驗證檔案大小、副檔名、是不是日期資料夾
    def __init__(self, path, ext):
        self.path = path
        self.ext = ext

    def load(self, f_obj):
        # 獲取檔案上傳物件
        if f_obj:
            self.f_obj = f_obj
        else:
            return '錯誤的上傳物件'

        # 檢測檔案型別，必須是指定的幾種副檔名對應的檔案型別
        errors = {
            -1: '沒有副檔名',
            -2: '無效的副檔名',
            -3: '未識別的副檔名',
            1: '有效的副檔名'
        }
        res = self.check_type()
        if res < 0:
            return errors[res]

        # 獲取檔案路徑
        file_path = self.get_path()

        # 上傳檔案
        if not self.write_file(file_path):
            return "檔案讀寫錯誤"

	# 之前所有的檢測都透過，才能返回True，否則返回對應的錯誤提示
        return f_obj

    def check_type(self):
        ext = os.path.splitext(self.f_obj.name)

        if len(ext) <= 1:
            return -1

        ext = ext[1].lstrip('.')
        if isinstance(self.ext, str):
            if ext != self.ext:
                return -2
        elif isinstance(self.ext, (tuple, list)):
            if ext not in self.ext:
                return -2
        else:
            return -3
        return 1

    def get_path(self):
        file_path = os.path.join(self.path, self.f_obj.name)
        return file_path

    def write_file(self, file_path):
        try:
            with open(file_path, 'wb') as fp:
                if self.f_obj.multiple_chunks():
                    for chip in self.f_obj.chunks():
                        fp.write(chip)
                else:
                    fp.write(self.f_obj.read())
            return True
        except:
            return False

def file_upload(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('files')
        f_upload = Upload("media/upload", ext=['xml', 'json'])
        res = f_upload.load(file_obj)
        path = f_upload.get_path()
        name, extension = os.path.splitext(file_obj.name)
        # 檔案上傳失敗，返回對應的提示資訊
        if isinstance(res, str):
            messages.error(request, res)
            return redirect('index')
        # 檔案成功上傳
        else:
            if extension == '.xml':
                content = XMLparser(path)
                return render(request, 'index.html', {
                    "uploaded": True,
                    "content": content,
                })
            elif extension == '.json':
                content = jsonParser(path)
                return render(request, 'index.html', {
                    "uploaded": True,
                    "content": content,
                })


def XMLparser(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    content = ''
    for info in root.iter('AbstractText'):
        node = info.text
        content += node
    words = countWords(content)
    char = countChar(content)
    sent = countSent(content)
    word_list = getWordList(content)
    drawWordCloud(content)
    return {
        "text": content,
        "words": words,
        "chars": char,
        "sentences": sent,
        "word_list": word_list,
    }

def jsonParser(jsonfile):
    with open(jsonfile) as file:
        data = json.loads(file.read())
    content = ''
    for text in data:
        content += text['Text']
    words = countWords(content)
    char = countChar(content)
    sent = countSent(content)
    word_list = getWordList(content)
    drawWordCloud(content)
    return {
        "text": content,
        "words": words,
        "chars": char,
        "sentences": sent,
        "word_list": word_list,
    }

def countWords(s):
    words = s.split()
    return len(words)

def countChar(s):
    charNum = 0
    words = s.split()
    for c in words:
        charNum += len(c)
    return charNum

def countSent(s):
    sentenceNum = sent_tokenize(s)
    return len(sentenceNum)

def getWordList(s):
    words_count = {}
    word_list = s.split()
    for word in word_list:
        if(words_count.get(word) == None):
            words_count[word] = 1
        else:
            words_count[word] += 1
    common_word = sorted(words_count.items(), key=lambda x: x[1], reverse=True)[:5]
    common_list = []
    for key, value in common_word:
        common_list.append({"key": key, "value": value})
    return common_list

def drawWordCloud(content):
    wordCloud = WordCloud(width=1600, height=800, background_color=None, mode="RGBA").generate(content)
    wordCloud.to_file("static/img/wordCloud.png")