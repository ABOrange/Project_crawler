import requests
from bs4 import BeautifulSoup as bs
import os , sys
import codecs

#--提取字串中間值函數--#
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
#--提取字串中間值函數--#
        
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
            fo.write("准考証號,姓名,錄取別,錄取學校,錄取學系")
            adm_no = '111'    #儲存准考證號
            name = '222'            #儲存姓名
            qual_order = '333'    #儲存錄取別
            school = '444'        #儲存學校
            dept = '555'        #儲存系所
            for i in range(0, len(Info)):
                Info[i] = Info[i].replace('\n','x')    #替換換行字元
                Info[i] = Info[i].replace('\xa0','y')    #替換空白字元

                if (len(Info[i]) == 9):    #辨識准考證 #(1st row)
                    fo.write("\n")
                    fo.write(Info[i])
                    fo.write(",")
                    adm_no = Info[i]
                    
                elif (len(Info[i]) >= 2 and len(Info[i]) <= 5): #辨識姓名 #(1st row)
                    fo.write(Info[i])
                    fo.write(",")
                    name = Info[i]
                    
                elif Info[i].startswith('正') or Info[i].startswith('備'): #辨識每位第一個錄取別欄位 #(1st row)
                    fo.write(Info[i] + ",")
                    fo.write(SchName.text + ",")    #所在頁面之學校
                    fo.write(deptname.text + "\n")    #所在頁面之系所

                elif ((Info[i].startswith('x國') and Info[i].endswith('x')) or (Info[i].startswith('x私立') and Info[i].endswith('x'))): #偵測字首
                    temp = Info[i].split("x")    #以x切割並暫存split後的array -> ['', '國立成功大學--工程科學系甲組甄試(一般生)yy複試【備取26】', '']
                    for a in range(0,len(temp)) :    #走訪temp每個array
                        if temp[a].startswith("國"):
                            school = ("國" + find_between( temp[a], "國", "-" ))    #提取字串後儲存國立學校
                        elif temp[a].startswith("私"):
                            school = ("私" + find_between( temp[a], "私", "-" ))    #提取字串後儲存私立學校
                        else :
                            continue;
                        dept = find_between( temp[a], "--", "y" )    #提取字串後儲存系所
                        qual_order = find_between( temp[a], "【", "】" )    #提取字串後儲存錄取別
                    
                        fo.write(adm_no + "," + name + "," + qual_order + "," + school + "," + dept + "\n")    #每位第二行開始寫入 #(2nd to last row)