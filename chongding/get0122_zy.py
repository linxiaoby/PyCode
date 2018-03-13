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
	# resptext={"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "12. 2016年G20峰会在杭州举办，那么上一届在哪举办？", "displayOrder": 11, "liveId": 145, "options": "[\"安塔利亚\",\"匹兹堡\",\"首尔\"]", "questionId": 1689, "showTime": 1516540636993, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
	# resptext={"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "11. 以下哪款粉底液最适合油性皮肤使用？", "displayOrder": 10, "liveId": 145, "options": "[\"YSL逆龄粉底液\",\"阿玛尼滴管粉底液\",\"YSL羽毛粉底液\"]", "questionId": 1688, "showTime": 1516540539504, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
	# print(resptext)
	if resptext['msg'] != 'no data' and resptext['msg'] != 'no data ':
		curQuestion = resptext.get('data', {})
		curQuestion = curQuestion.get('event', {})
		curAnswer = curQuestion.get('options', "")
		curQuestion = curQuestion.get('desc', "no data")
		if curQuestion != "no data" :
			# if curQuestion[0] == ' ' or curQuestion[0] == ' ':
			# 	curQuestion = curQuestion[1:]
			# 	print(curQuestion)
			index = curQuestion.find(".")+1
			curQuestion = curQuestion[index:]
			index = curQuestion.find("?")
			if index == -1:
				index = curQuestion.find("？")
			if index != -1:
				curQuestion = curQuestion[:index]
		if curQuestion[0] == ' ' or curQuestion[0] == ' ':
			curQuestion = curQuestion[1:]
			
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
			kw1 = curQuestion + " " + curAnswer[0][1:-1]
			kw3 = ""
			for ans in curAnswer:
				ans = ans[1:-1]
				kw3 = kw3 + ans
				kw3 = kw3 + " "
				webbrowser.open('https://www.baidu.com/s?wd=' + curQuestion + ' ""' + ans+'""')
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
			kw3 = kw3 + curQuestion;
			# webbrowser.open("http://www.baidu.com/s?wd=" + kw1)
			# webbrowser.open("http://www.baidu.com/s?wd=" + kw3)
			# webbrowser.open("https://www.google.com.hk/search?q=" + curQuestion)
			webbrowser.open("http://www.baidu.com/s?wd=" + curQuestion)
			preQuestion = curQuestion
		else:
			pass
	else:
		print('no data.\n')
	time.sleep(0.3)
f.close()
g.close()
