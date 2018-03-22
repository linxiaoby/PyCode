import requests
import re
def open_webbrowser_count(question,choices):
    print('\n-- 方法2： 题目+选项搜索结果计数法 --\n')
    print('Question: ' + question)
    if '不是' in question:
        print('**请注意此题为否定题,选计数最少的**')

    counts = []
    for i in range(len(choices)):
        # 请求
        req = requests.get(url='http://www.baidu.com/s', params={'wd': question + choices[i]})
        content = req.text
        index = content.find('百度为您找到相关结果约') + 11
        content = content[index:]
        index = content.find('个')
        count = content[:index].replace(',', '')
        counts.append(count)
        #print(choices[i] + " : " + count)
    output(choices, counts)

if __name__ == "__main__":
    req = requests.get(url='https://www.google.com/search?q=Chinese')
    print (req)
    # str = req.text
    print (str)
    con = re.findall(r"About (.+?) results",str)
    # cnt = con[0].replace(',', '')
    print(con)


    # index = content.find('About % results') + 6
    #
    # content = content[index:]
    # index = content.find('results (% seconds)')
    # count = content[:index].replace(',', '')
    # print(count)
