#尋找並切割字串的函數
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

str = "x國立台灣科技大學--化學工程系碩士班丙組甄試(一般生)  複試【備取8】x國立政治大學--資訊管理學系科技組甄試(一般生)  複試【備取1】x國立成功大學--化學系甄試(一般生)  複試【備取32】x私立中原大學--企業管理學系甄試(一般生)  複試【正取4】x";

temp = str.split("x")
str.join("x")
print (str.split("x"))

for a in range(0,len(temp)) :
	if temp[a].startswith("國"):
		print ("國" + find_between( temp[a], "國", "-" ))
	elif temp[a].startswith("私"):
		print ("私" + find_between( temp[a], "私", "-" ))
	else :
		continue;
		
	print (find_between( temp[a], "--", " " ))
	print (find_between( temp[a], "【", "】" ))
	#print ("\n")
	
	