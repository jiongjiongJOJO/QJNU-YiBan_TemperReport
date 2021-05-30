import json
import requests
import random
from yiban import YiBan
import util
import os
import re

def send(token,message):
    title = '曲靖师范学院 - 体温填报'  # 改成你要的标题内容
    content = message  # 改成你要的正文内容
    url = 'http://pushplus.hxtrip.com/send'
    data = {
        "token": token,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)

#user = os.getenv("USER")
#password = os.getenv("PASSWORD")
#token = os.getenv("TOKEN")
users_info = os.getenv("USERS")
for user_info in users_info.split():
    user,password,token = map(str, user_info.split('----'))
    try:
        yb = YiBan(user, password)
        yb.login()
        yb.getHome()
        print("登录成功 %s" % yb.name)
        yb.auth()
        all_task = yb.getUncompletedList()["data"]
        all_task = list(filter(lambda x: "体温报备" in x["Title"], all_task))
        if len(all_task) == 0:
            print("没找到今天体温上报的任务，可能是你已经上报，如果不是请手动上报。")
            send(token,"没找到今天体温上报的任务，可能是你已经上报，如果不是请手动上报。")
        else:
            all_task_sort = util.desc_sort(all_task, "StartTime")  # 按开始时间排序
            new_task = all_task_sort[0]  # 只取一个最新的
            print("找到未上报的任务：", new_task)
            task_detail = yb.getTaskDetail(new_task["TaskId"])["data"]
            FormList = eval(yb.getFormId(task_detail["WFId"])["data"]["FormJson"].replace("true", "True"))
            ids = {}
            for i in FormList:
                if ('体温' in i['props'].values()):
                    ids['体温'] = i['id']
                elif ('个人健康是否异常' in i['props'].values()):
                    ids['个人健康是否异常'] = i['id']
                elif('获取定位' in i['props'].values()):
                    ids['获取定位'] = i['id']
            if('晨检' in task_detail["Title"]):
                dict_form = {ids['体温']: ["36.2", "36.3", "36.4", "36.5", "36.6", "36.7", "36.8"][random.randint(0, 6)],  # 随机体温
                             ids['个人健康是否异常']: "正常",
                             ids['获取定位'] : {
                                 "time": util.get_time_no_second(),
                                 "longitude": 103.752319,
                                 "latitude": 25.525995,
                                 "address": "云南省曲靖市麒麟区紫薇路161号靠近曲靖师范学院樱苑3栋"}
                             }
            else:
                #ids = re.compile("\"id\":\"(.*?)\"").findall(yb.getFormId(task_detail["WFId"])["data"]["FormJson"])
                dict_form = {ids['体温']: ["36.2", "36.3", "36.4", "36.5", "36.6", "36.7", "36.8"][random.randint(0, 6)],# 随机体温
                             ids['个人健康是否异常']: ["正常"],
                             ids['获取定位'] : {
                                 "time": util.get_time_no_second(),
                                 "longitude": 103.752319,
                                 "latitude": 25.525995,
                                 "address": "云南省曲靖市麒麟区紫薇路161号靠近曲靖师范学院樱苑3栋"}
                             }

            ex = {"TaskId": task_detail["Id"],
                  "title": "任务信息",
                  "content": [{"label": "任务名称", "value": task_detail["Title"]},
                              {"label": "发布机构", "value": task_detail["PubOrgName"]}]}

            submit_result = yb.submit(json.dumps(dict_form, ensure_ascii=False), json.dumps(
                ex, ensure_ascii=False), task_detail["WFId"])
            if submit_result["code"] == 0:
                share_url = yb.getShareUrl(submit_result["data"])["data"]["uri"]
                print("已完成一次体温上报[%s]" % task_detail["Title"])
                print("访问此网址查看详情：%s" % share_url)
                #send(token,"已完成一次体温上报["+task_detail["Title"]+"]<br>访问此网址查看详情："+share_url)
            else:
                print("[%s]遇到了一些错误:%s" % (task_detail["Title"], submit_result["msg"]))
                send(token,task_detail["Title"]+"遇到了一些错误:"+submit_result["msg"])
    except Exception as e:
        print("出错啦")
        print(e)
        send(token,"出错了" + e)
