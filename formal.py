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
    print ('dept:'+deptname.text)
    if not os.path.exists(Title):
        os.makedirs(Title)
    filename2 = Title  + "/" + deptname.text + ".csv"
    with codecs.open(filename2, 'a',encoding='utf8') as fo:
            fo.write(u'\ufeff')
            fo.write("准考証號,姓名,錄取別,錄取學校")
            fo.write("\n")
            count4 = 0
            for a in Info:
                    a = a.replace('\n','')
                    a = a.replace('】','】\n')
                    fo.write(a)
                    count4+=1
                    if (count4 % 4 == 0):
                        count4=0
                        fo.write("\n")
                    else: 
                        fo.write(",")