# coding=utf-8
import sys


cmd = 'wdiff.exe --start-delete={{{ --start-insert=[[[ --end-delete=}}} --end-insert=]]] contract1.txt contract2.txt > out.txt'
import subprocess
PIPE = subprocess.PIPE
p = subprocess.Popen(cmd, shell = True)
p.wait()

class Diff:
    def __init__(this, value, filename, line, linenum, index, coord, priority):
        this.value = value
        this.filename = filename
        this.line = line
        this.linenum = linenum
        this.index = index
        this.coord = coord
        this.priority = priority
        
    
fin = open('out.txt', 'rt', encoding='utf-8')
listdiff = []
linenum = 0;
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


for x in listdiff:
  print(x.value, x.filename, x.line, x.linenum, x.index, x.coord, x.priority)
	



