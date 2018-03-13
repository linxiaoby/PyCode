# -*- coding: UTF-8 -*-
import webbrowser
import requests
import json
import io
import re

# IP 47.94.116.128

#webs = ['http://htpmsg.chongdingdahui.com/msg/current', 'http://htpmsg.jiecaojingxuan.com/msg/current']
# webs = ['http://htpmsg.chongdingdahui.com/msg/current']
# webs = ['http://chongdingdahui.com']
webs = ['http://htpmsg.jiecaojingxuan.com/msg/current']
preQuestion = ""

f = io.open('out.txt', 'a', encoding='utf8')
while True:
	for link in webs:
			try:
				resptext = requests.get(link, timeout = 1).text
			except requests.exceptions.Timeout:
				continue;
			# print(resptext)
			if resptext[0] != '{':
				continue
			resptext = json.loads(resptext)
			# resptext = {"code": 0, "msg": "成功", "data": {
			# 	"event": {"answerTime": 10, "desc": "9.目前亚洲迪士尼乐园中1占地面积最大的是？", "displayOrder": 9, "liveId": 106,
			# 			  "options": "[\"东京迪士尼乐园\",\"香港迪士尼乐园\",\"上海迪士尼乐园\"]", "questionId": 1219,
			# 			  "showTime": 1515762612476, "status": 0, "type": "showQuestion"}, "type": "showQuestion"}}
			if resptext['msg'] != 'no data ':
				curQuestion = resptext.get('data', {})
				curQuestion = curQuestion.get('event', {})
				curOptions = curQuestion.get('options', [])
				curQuestion = curQuestion.get('desc', "no data")

				curOptions = curOptions[1:-1].split(",") #去掉中括号后切分 added by wl
				options=""
				for i in range(len(curOptions)):
					opt=curOptions[i][1:-1]
					if i==0:
						options = opt  #去掉引号
					else:
						options = options + " " +opt  # 去掉引号

				m=re.match(r"(\d+)\.",curQuestion)
				i=len(m.group(0))
				curQuestion=curQuestion[i:]
				# print(curQuestion)
				# if curQuestion != preQuestion:
				if  curQuestion != "no data" and curQuestion != preQuestion:
					print(resptext)

					# 百度搜索
					keywords = "{} {}".format(curQuestion,options)  #题目加选项一起作为关键词 added by wl
					webbrowser.open("http://www.baidu.com/s?wd=" + keywords)
					
					# 将 json 数据写入文件
					json.dump(resptext, f, ensure_ascii=False)
					f.write('\n')

					# 将问题和选项写入文件
					# qf.write(curQuestion)
					# qf.write('\n');
					# for opt in curOptions:
					# 	qf.write(opt)
					# 	qf.write('\n')
					#
					preQuestion = curQuestion
				else:
					pass
			else:
				print('no data.\n')
	for i in range(1, 5000000):
		pass;
f.close();
