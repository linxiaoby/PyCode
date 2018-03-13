# -*- coding: UTF-8 -*-
import webbrowser
import requests
import time
import json
import ssl
import io

# IP 47.94.116.128

# webs = ['http://htpmsg.chongdingdahui.com/msg/current', 'http://htpmsg.jiecaojingxuan.com/msg/current']
# webs = ['http://htpmsg.chongdingdahui.com/msg/current']
# webs = ['http://chongdingdahui.com']
# webs = ['http://htpmsg.jiecaojingxuan.com/msg/current']

ssl._create_default_https_context = ssl._create_unverified_context

link = 'http://msg.api.chongdingdahui.com/msg/current'

headers={
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'User-Agent': 'Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; MI 6 Build/NMF26X) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
	'X-Live-App-Version': '1.0.7',
	'X-Live-Device-Type': 'android',
	'X-Live-Session-Token':'1.8732524.752912.uNA.4b0106f89dff47d413cec27498bc2636',
	'Host': 'msg.api.chongdingdahui.com',
	'Connection': 'Keep-Alive',
	'Accept-Encoding': 'gzip',
	'Cache-Control': 'no-cache'
}

preQuestion = ""

f = io.open('out.txt', 'a', encoding='utf8')
g = io.open('questions.txt', 'a', encoding='utf8')
while True:
	try:
		resptext = requests.get(link, timeout = 1, headers = headers).text
	except requests.exceptions.Timeout:
		continue;
	# print(resptext)
	if resptext[0] != '{':
		continue
	resptext = json.loads(resptext)
	# print(resptext)
	if resptext['msg'] != 'no data' and resptext['msg'] != 'no data ':
		curQuestion = resptext.get('data', {})
		curQuestion = curQuestion.get('event', {})
		curAnswer = curQuestion.get('options', "")
		curQuestion = curQuestion.get('desc', "no data")
		if curQuestion != "no data" :
			index = curQuestion.find(".")+1
			curQuestion = curQuestion[index:]
			index = curQuestion.find("?")
			if index == -1:
				index = curQuestion.find("？")
			if index != -1:
				curQuestion = curQuestion[:index]
		curAnswer = curAnswer[1:-1].split(",")
		# print(curQuestion)
		# if curQuestion != preQuestion:
		if  curQuestion != "no data" and curQuestion != preQuestion:
			# print(resptext)
			# 百度搜索
			# webbrowser.open("http://www.baidu.com/s?wd=" + curQuestion)
			# 将 json 数据写入文件
			json.dump(resptext, f, ensure_ascii=False)
			f.write('\n')
			# 将问题和答案写入文件
			print(curQuestion +'\n')
			g.write(curQuestion + '\n')
			kw = curQuestion
			for ans in curAnswer:
				ans = ans[1:-1]
				kw = kw + " "
				kw = kw + ans
				# webbrowser.open("http://www.baidu.com/s?wd=" + curQuestion + " " + ans)
				############ 比较搜索结果数目
				# res = requests.get(url='http://www.baidu.com/s', params={'wd': curQuestion + " " + ans})
				# content = res.text
				# index = content.find('百度为您找到相关结果约') + 11
				# content = content[index:]
				# index = content.find('个')
				# count = content[:index].replace(',', '')
				# print(ans + '   ' + count + '\n')
				############
				print(ans + '\n')
				g.write(ans + '\n')
			
			webbrowser.open("http://www.baidu.com/s?wd=" + curQuestion)
			webbrowser.open("http://www.baidu.com/s?wd=" + kw)
			preQuestion = curQuestion
		else:
			pass
	else:
		print('no data.\n')
	time.sleep(0.3)
f.close();
