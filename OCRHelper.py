# coding=utf-8
import subprocess
import codecs
import os
import csv
import re
import sys

dir_path = os.path.dirname(os.path.realpath('__file__'))

class OptionWord:
  def __init__(self, 
               level,
               page_num,
               block_num,
               par_num,
               line_num,
               word_num,
               left,
               top,
               width,
               height,
               conf,
               text,
               priority):
    self.level = level
    self.page_num = page_num
    self.block_num = block_num
    self.par_num = par_num
    self.line_num = line_num
    self.word_num = word_num
    self.left = left
    self.top = top
    self.width = width
    self.height = height
    self.conf = conf
    self.text = text
    self.priority = priority

class Diff:
    def __init__(this, value, filename, line, linenum, index, strarr, priority):
        this.value = value
        this.filename = filename
        this.line = line
        this.linenum = linenum
        this.index = index
        this.strarr = strarr
        this.priority = priority

def tesseract_run(image_path, file_name, oem, psm, tsv = False):
#
    output_path = os.path.join(dir_path, file_name)
    cmd = dir_path + '/Tesseract/tesseract.exe --tessdata-dir ' + dir_path + '/Tesseract/tessdata ' + image_path + ' ' + output_path + ' --oem '+ oem + ' --psm ' + psm + ' -l rus'

    if tsv:
        cmd = cmd + " tsv"

    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, shell = True)
    p.wait()
#

def update_txt(file_name):
#
    file_read = open(file_name, encoding='utf-8')
    text = file_read.read()
    file_read.close()
    text = text.replace("\\", " ").replace(u"╚", " ").replace(u"╩", " ").replace("  "," ")
    text = text.lower()
    #text = re.sub('\-\s\r\n\s{1,}|\-\s\r\n|\r\n', '', text) #deleting newlines and line-breaks
    text = re.sub('[_%©?*,!@#$%^&()\d]|[+=]|[[]|[]]|[/]|"|\s{2,}|-', ' ', text) #deleting symbols

    file_write = open(file_name, 'w')
    file_write.write(text)
    file_write.close()
#

def get_coordinates(file_name, words, search_word, priority):
#
    if (len(words) != 0):
        file_name = file_name + '.tsv'
        file_path = os.path.join(dir_path, file_name)

        all_lines = []

        with open(file_path, encoding="utf-8") as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\n")
            for line in tsvreader:
                items = line[0].split('\t')
                option_word = OptionWord(items[0], items[1], items[2], items[3], items[4], items[5], items[6], items[7], items[8], items[9], items[10], items[11], priority)
                all_lines.append(option_word)

        block = ' '
        line_num = ' '
        index = 0
        for line in all_lines:
            if words[index] in line.text and len(words) > index:
                index = index + 1
                block = line.block_num
                line_num = line.line_num

                if index == len(words) - 1:
                    break
            else:
                index = 0

        for line in all_lines:
            if line.block_num == block and line.line_num == line_num and search_word in line.text:
                line.page_num = line.page_num + '_' + file_name + '.jpeg'
                return line

    return None
#

def call_wdiff(item1, item2):
#
    cmd = 'wdiff.exe --start-delete={{{ --start-insert=[[[ --end-delete=}}} --end-insert=]]] ' + item1 + ' ' + item2 + ' > out.txt'
    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, shell = True)
    p.wait()

    fin = open('out.txt')
    listdiff = []
    linenum = 0
    for line in fin:
        count = 0
        beginword = -1
        while beginword > -2:
            beginword = line.find('[[[', beginword+1, len(line))
            if beginword != -1:
                endword = line.find(']]]', beginword+3, len(line))
                if endword != -1:
                    value = line[beginword+3:endword]
                    diff = Diff(value, 'contract2', line, linenum, str(beginword - count*6), None, -1)
                    listdiff.append(diff)
                    count += 1
            else:
                    beginword = -2


        beginword = -1
        while beginword > -2:
            beginword = line.find('{{{', beginword+1, len(line))
            if beginword != -1:
                endword = line.find('}}}', beginword+3, len(line))
                if endword != -1:
                    value = line[beginword+3:endword]
                    diff = Diff(value, 'contract1', line, linenum, str(beginword - count*6), None, -1)
                    listdiff.append(diff)
                    count += 1
            else:
                beginword = -2
        linenum += 1
    fin.close()

    #dd.MM.yyyy \ dd.MM.YY
    standartDate = '(\d{1,2})\.(\d{1,2})\.(\d\d{1,2})'
    #1 февраля 2018
    textDate = '(\d{1,2})\s((февра|апре)ля|ма(рта|я)|ию(н|л)я|августа|(((сент|окт|но)я|дека)б|янва)ря)\s(\d\d{1,2})'

    #12.13
    sumWithDot = '(\d+)\.(\d+)'
    #12,13
    sumWithComma = '(\d+),(\d+)'
    #12 рублей 00 копеек
    textSum = '(\d+)\s(рублей|руб(\.?))\s(\d+)\s(копеек|коп(\.?))'
    #12 руб
    shortTextSum = '(\d+)\s(рублей|руб(\.?))'

    #текст
    text = '[а-я](\s|(.+)|)([а-я]|)'

    # И.И. Иванов
    initialsBeforeName = '[А-Я](\.?)(\s?)[А-Я](\.?)(\s)[А-Я]([а-я]+)'
    # Иванов И.И.
    initialsAfterName = '[А-Я]([а-я]+)(\s)[А-Я](\.?)(\s?)[А-Я](\.?)'
    # Иванов Иван Иванович
    fullName = '[А-Я]([а-я]+)\s[А-Я]([а-я]+)\s[А-Я]([а-я]+)'

    #не буквы\цифры
    symbols = '[^А-Яа-я0-9]+'

    for x in listdiff:
        if re.match(standartDate+'|'+textDate+'|'+sumWithDot+'|'+sumWithComma+'|'+textSum+'|'+shortTextSum+'|' + text, x.value):
            x.priority = 1
        if re.match(initialsBeforeName+'|'+initialsAfterName+'|'+fullName, x.value):
            x.priority = 2
        if re.match(symbols, x.value):
            x.priority = 3
        if (x.priority == -1):
            x.priority = 1
      
    for x in listdiff:
        correctstr = x.line
        if x.filename != "contract2":
            correctstr = correctstr.replace('[[[', '')
            correctstr = correctstr.replace(']]]', '')
            tmp = re.split(r'\{\{\{.+\}\}\}', str(correctstr))
            newstr = ''
            for tmpitem in tmp:
                newstr += tmpitem
            correctstr = newstr
        else:
            correctstr = correctstr.replace('{{{', '')
            correctstr = correctstr.replace('}}}', '')
            tmp = re.split(r'\[\[\[.+\]\]\]', str(correctstr))
            newstr = ''
            for tmpitem in tmp:
                newstr += tmpitem
            correctstr = newstr
        x.strarr = correctstr.split()

    arr_coord = []
    for x in listdiff:
        words = x.value.split()
        for word in words:
            arr_coord.append(get_coordinates(x.filename, x.strarr, word, x.priority))   

    return arr_coord
#

def recognition_run(image_path_original, image_path_changed, oem, psm):
#
    file_name_original = os.path.basename(image_path_original)
    file_name_original = os.path.splitext(file_name_original)[0]

    tesseract_run(image_path_original, file_name_original, oem, psm, False)
    tesseract_run(image_path_original, file_name_original, oem, psm, True)

    file_name_original = file_name_original + '.txt'
    file_path_original = os.path.join(dir_path, file_name_original)
    update_txt(file_path_original)

    file_name_changed = os.path.basename(image_path_changed)
    file_name_changed = os.path.splitext(file_name_changed)[0]

    tesseract_run(image_path_changed, file_name_changed, oem, psm, False)
    tesseract_run(image_path_changed, file_name_changed, oem, psm, True)

    file_name_changed = file_name_changed + '.txt'
    file_path_changed = os.path.join(dir_path, file_name_changed)
    update_txt(file_path_changed)

    return call_wdiff(file_name_original, file_name_changed)
#

def recognition(image_path_original, image_path_changed):
#
    return recognition_run(image_path_original, image_path_changed, '1', '6')
#

