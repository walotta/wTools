import os
import sys
import re
from pikepdf import Pdf

target_path=''
if len(sys.argv)>2:
    sys.stderr.write('has too many argv\n')
    exit()
elif len(sys.argv)==1:
    target_path=input('input your target path, "." for run path: \n')
else:
    target_path=sys.argv[1]

target_path=os.path.expanduser(target_path)
pdf_lst=[]
try:
   pdf_lst = [f for f in os.listdir(target_path) if f.endswith('.pdf')] 
except:
    sys.stderr.write('path error\n')
    exit()

if len(pdf_lst)==0:
    sys.stderr.write('find no pdf file\n')
    exit()

pdf_lst = [os.path.join(target_path, filename) for filename in pdf_lst]

def query_merge():
    print('\033[36m=============\033[0m')
    print('找到下列文件：')
    for i in range(len(pdf_lst)):
        print('\033[36m'+str(i)+'. \033[33m'+os.path.basename(pdf_lst[i])+'\033[0m')
    ans=input('输入要合并的pdf的编号(1, 2, 3-5, all)，或者使用正则表达式匹配文件名:\n')
    matchList=[]
    if ans.lower()=='all':
        matchList=pdf_lst
    elif '.pdf' in ans:
        for file in pdf_lst:
            try:
                if re.search(ans,os.path.basename(file)):
                    matchList.append(file)
            except:
                print('syntax error in regular expression')
                return query_merge()
    else:
        splitList=ans.split(',')
        for s in splitList:
            if '-' in s:
                if s.count('-')>1:
                    print('has too many "-"')
                    return query_merge()
                else:
                    sList=s.split('-')
                    numList=[]
                    for i in sList:
                        if i.isdecimal()!=True:
                            print('num match error')
                            return query_merge()
                        else:
                            numList.append(int(i))
                            if int(i) not in range(len(pdf_lst)):
                                print('num out of range')
                                return query_merge()
                    # numList.sort()
                    rangeTmp=0
                    if numList[0]<=numList[1]:
                        rangeTmp=range(numList[0],numList[1]+1)
                    else:
                        rangeTmp=range(numList[0],numList[1]-1,-1)
                    for i in rangeTmp:
                        matchList.append(pdf_lst[i])
            else:
                if s.isdecimal()!=True:
                    print('num out of range')
                    return query_merge()
                else:
                    if int(s) not in range(len(pdf_lst)):
                        print('num match error')
                        return query_merge()
                    matchList.append(pdf_lst[int(s)])
    print('you want to merge:')
    for i in range(len(matchList)):
        print('\033[33m'+os.path.basename(matchList[i])+'\033[0m')
    ans=input('confirm? [Y/n] ')
    if(ans.upper()=='Y'):
        return matchList
    else:
        return query_merge()


mergeList=query_merge()

ans=Pdf.new()
for pdf in mergeList:
    src=Pdf.open(pdf)
    ans.pages.extend(src.pages)

def outputFile(): 
    outFile=input('input your outfile name, begin with / means abspath: \n')
    try:
        if outFile[0]=='/':
            ans.save(outFile+'.pdf')
        else:
            ans.save(os.path.abspath(target_path+'/'+outFile+'.pdf'))
    except:
        print('\033[31mfail to create, retry...\033[0m')
        outputFile()
    else:
        print('finish!')

outputFile()
