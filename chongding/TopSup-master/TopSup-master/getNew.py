# -*- coding: UTF-8 -*-
import webbrowser
import requests
import time
import json
import ssl
import io
import urllib.request
from common import methods
from threading import Thread

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
	#'X-Live-Session-Token':'1.8732524.752912.uNA.4b0106f89dff47d413cec27498bc2636',
    'X-Live-Session-Token':'1.15205828.1179814.ReI.54a72de6c353e87946117b9cb504e7a0', #wanglin的id
	'Host': 'msg.api.chongdingdahui.com',
	'Connection': 'Keep-Alive',
	'Accept-Encoding': 'gzip',
	'Cache-Control': 'no-cache'
}

preQuestion = ""

f = io.open('out.txt', 'a', encoding='utf8')
# g = io.open('questions.txt', 'a', encoding='utf8')
while True:
	# try:
	# 	resptext = requests.get(link, timeout = 1, headers = headers).text
	# except requests.exceptions.Timeout:
	# 	continue;
	# # print(resptext)
	# if resptext[0] != '{':
	# 	continue
	# resptext = json.loads(resptext)
	resptext={"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "11.以下哪个酒店是七星级？", "displayOrder": 10, "liveId": 117, "options": "[\"阿拉伯塔酒店\",\"酋长国宫殿酒店\",\"文莱帝国酒店\"]", "questionId": 1348, "showTime": 1516014767626, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
	resptext={"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "12.以下哪个不属于奇经八脉中的八脉之一？", "displayOrder": 11, "liveId": 117, "options": "[\"数脉 \",\"带脉\",\"任脉\"]", "questionId": 1349, "showTime": 1516014837005, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
	#resptext = {"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "1.标准的足球比赛中双方各派出多少人上场？", "displayOrder": 0, "liveId": 106, "options": "[\"9\",\"11\",\"13\"]", "questionId": 1210, "showTime": 1515762116727, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
	# resptext = {"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "3.中国的探月工程命名为？", "displayOrder": 2, "liveId": 106, "options": "[\"嫦娥工程\",\"后羿工程\",\"天宫工程\"]", "questionId": 1212, "showTime": 1515762220030, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
	# resptext = {"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "4.京剧中，饰演性格活泼，开朗的青年女性的是？", "displayOrder": 3, "liveId": 106, "options": "[\"花旦\",\"青衣\",\"刀马旦\"]", "questionId": 1213, "showTime": 1515762268031, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
	# resptext = {"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "5.电影《神偷奶爸》中的小黄人是格鲁的什么？", "displayOrder": 4, "liveId": 106, "options": "[\"亲戚\",\"宠物\",\"员工\"]", "questionId": 1214, "showTime": 1515762319326, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
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
			#print(curQuestion +'\n')
			#g.write(curQuestion + '\n')
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
				#print(ans + '\n')
				#g.write(ans + '\n')
			# kw = urllib.request.quote(kw)
			# webbrowser.open("http://www.baidu.com/s?wd=" + kw)
			#webbrowser.open("http://www.baidu.com/s?wd=" + curQuestion)
			preQuestion = curQuestion
			curQuestion=urllib.request.quote(curQuestion)
			curAnswer=urllib.request.quote(curAnswer)
			m1 = Thread(methods.run_algorithm(0, curQuestion, curAnswer))
			# m2 = Thread(methods.run_algorithm(1, question, choices))
			m3 = Thread(methods.run_algorithm(2, curQuestion, curAnswer))
			m1.start()
			# m2.start()
			m3.start()

		else:
			pass
	else:
		print('no data.\n')
	time.sleep(0.5)
f.close();
