import requests
from bs4 import BeautifulSoup as bs
import os , sys
import codecs

#建立資料夾建立csv檢視各系所資訊

url = "https://www.tkbgo.com.tw/mutualChabang/toSchoolDep.jsp?state=1&school_no=S1010"

res = requests.get(url)

soup = bs(res.text,"lxml")

deptInfo = soup.select("div.mSTb td")

SchName = soup.find("h2","mainTtl")
TaskName = soup.select("div.breadcrumbs span")
Title = SchName.text + TaskName[0].text + TaskName[1].text + TaskName[2].text.strip()

if not os.path.exists(Title):
        os.makedirs(Title)
filename = Title + '/DeptInfo.csv'
with codecs.open(filename, 'a',encoding='utf8') as f:
    f.write(u'\ufeff')
    f.write('校系名稱,href,\n')
    for info in deptInfo:
        f.write(info.text)
        f.write(",")
        f.write(info.find("a").get("href"))
        f.write("\n")

#建立陣列載入各連結
Depturl = []
for info in deptInfo:
    Depturl.append(info.find("a").get("href"))

#引用連結抓取各系所榜單
for url in Depturl:
    Info = []
    res = requests.get(url)
    soup = bs(res.text,"lxml")
    info = soup.select("div.mSTb td")
    for i in info:
            Info.append(i.text)
    deptname = soup.find("h2","mainTtl")
    print (deptname.text)
    if not os.path.exists(Title):
        os.makedirs(Title)
    filename2 = Title  + "/" + deptname.text + ".csv"
    with codecs.open(filename2, 'a',encoding='utf8') as fo:
            fo.write(u'\ufeff')
            fo.write("准考証號,姓名,錄取別,錄取學校")
            fo.write("\n")
            count = 0
            cunt2 = 0
            adm_no = '111'    #儲存准考證號
            name = '222'            #儲存姓名
            qual_order = '333'  #儲存錄取別
            for a in Info:
                    a = a.replace('\n','')    #去掉隱藏換行符號
                    if (len(a) == 9):
                        fo.write("\n")
                        fo.write(a)
                        fo.write(",")
                        adm_no = a
                        count = 0
                    elif (len(a) >= 2 and len(a) <= 5): #姓名
                        fo.write(a)
                        fo.write(",")
                        name = a
                    elif a.startswith('正') or a.startswith('備'): #錄取別
                        fo.write(a)
                        fo.write(",")
                        qual_order = a
                    elif (a.startswith('國立') and a.endswith('】')) or (a.startswith('私立') and a.endswith('】')): #偵測字首字尾進行換行
                        a = a.replace('】','】\n' + adm_no + ',' + name + ',' + qual_order + ',')    #在下一行插入准考證/姓名/錄取別
                        fo.write(a)
                        fo.write('國立中正大學')