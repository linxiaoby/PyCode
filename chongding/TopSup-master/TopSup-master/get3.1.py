# -*- coding: UTF-8 -*-
import webbrowser
import requests
import json
import io

# IP 47.94.116.128

# webs = ['http://htpmsg.chongdingdahui.com/msg/current', 'http://htpmsg.jiecaojingxuan.com/msg/current']
# webs = ['http://htpmsg.chongdingdahui.com/msg/current']
# webs = ['http://chongdingdahui.com']
webs = ['http://htpmsg.jiecaojingxuan.com/msg/current']
preQuestion = ""

f = io.open('out.txt', 'a', encoding='utf8')
g = io.open('questions.txt', 'a', encoding='utf8')
while True:
	for link in webs:
			try:
				resptext = requests.get(link, timeout = 1).text
			except requests.exceptions.Timeout:
				continue;
			if resptext[0] != '{':
				continue
			resptext = json.loads(resptext)
			resptext = {"code": 0, "msg": "成功", "data": {"event": {"answerTime": 10, "desc": "1.标准的足球比赛中双方各派出多少人上场？", "displayOrder": 0, "liveId": 106, "options": "[\"9\",\"11\",\"13\"]", "questionId": 1210, "showTime": 1515762116727, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
			# print(resptext)
			if resptext['msg'] != 'no data':
				curQuestion = resptext.get('data', {})
				curQuestion = curQuestion.get('event', {})
				curAnswer = curQuestion.get('options', "")
				curQuestion = curQuestion.get('desc', "no data")

				if curQuestion != "no data" :
					index = curQuestion.find(".")+1
					curQuestion = curQuestion[index:]
				
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
					for ans in curAnswer:
						ans = ans[1:-1]
						# webbrowser.open("http://www.baidu.com/s?wd=" + curQuestion + " " + ans)
						############ 比较搜索结果数目
						res = requests.get(url='http://www.baidu.com/s', params={'wd': curQuestion + " " + ans})
						content = res.text
						index = content.find('百度为您找到相关结果约') + 11
						content = content[index:]
						index = content.find('个')
						count = content[:index].replace(',', '')
						print(ans + '   ' + count + '\n')
						############
						g.write(ans + '   ' + count + '\n')
					
					preQuestion = curQuestion
				else:
					pass
			else:
				print('no data.\n')
	for i in range(1, 5000000):
		pass;
f.close();
