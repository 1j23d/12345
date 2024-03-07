import random
from time import localtime
from requests import get, post

import datetime
import sys, json
import os
import requests



# 日志目录

log_home = '/home/xusl/log/wx'

# 日志 level

# 日志打印到控制台

log_to_console = True

# 每日一言

lines = [
"会好，迟早。",
"生命几许，遵从自己，别赶路，感受路。",
"去爱具体的生活。",
"拐个弯，与生活和解，得失都随意。",
"不要预知明天的烦恼。",
"后来重闻往事如耳旁过风，不慌不忙。",
"勇敢的人先享受世界。",
"玫瑰不用长高，晚霞自会俯腰，爱意随风奔跑，温柔漫过山腰。",
"春风得意马蹄疾，一日看尽长安花。",
"你若决定灿烂，山无遮，海无拦。",
"中途下车的人很多，你不必耿耿于怀。",
"内心丰盈者，独行也如众。",
"你记得花，花就不怕枯萎。",
"春日不迟，相逢终有时。",
"日升月落总有黎明。",
"有人等烟雨，有人怪雨急。",
"等风来，不如追风去。",
"真诚永远可贵。",
"喜乐有分享，共度日月长。",
"在过程中追逐意义。"
]

def get_color(): # 获取随机颜色
get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
color_list = get_colors(100)
return random.choice(color_list)

def get_access_token(config):

    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        sys.exit(1)
    return access_token

def get_now_datetime():
"""
获取当前日期
:return: datetime now
"""
return datetime.datetime.now()

def get_datetime_str(d_date=None, pattern='%Y-%m-%d'):
"""
获取指定日期 字符格式
:param d_date:
:param pattern:
:return:
"""
if not d_date:
d_date = get_now_datetime()
return datetime.datetime.strftime(d_date, pattern)

def parse_str2date(s_date, pattern='%Y-%m-%d'):
"""
将字符串转换为日期格式
:param s_date:
:param pattern:
:return:
"""
return datetime.datetime.strptime(s_date, pattern)

def get_weather_info(config, today_dt):
"""
获取城市当日天气
:return:
"""
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
city_id = config["city_id"]
region_url = "http://t.weather.sojson.com/api/weather/city/{}".format(city_id)
response = get(region_url, headers=headers).json()

    if response["status"] == 200:
        forecast = response["data"]["forecast"]
        for item in forecast:
            if item["ymd"] == today_dt:
                return True, item
    else:
        return False, response["status"]

def get_birthday(config, year, today_dt):
"""
获取距离下次生日的时间
:return:
"""

    birthday = config["birth_day"]  # 获取生日日期
    birthday_year = birthday.split("-")[0]  # 2023 or r2023
    # 将str日期转换为日期型
    # d_birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")

    # 判断是否为农历生日
    if birthday_year[0] == "r":
        # 获取农历生日的今年对应的月和日
        try:
            r_mouth = int(birthday.split("-")[1])
            r_day = int(birthday.split("-")[2])
            nl_birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        except TypeError:

            # 调用系统命令行执行 pause 命令，目的是在控制台窗口显示 "请按任意键继续. . ." 的提示信息，并等待用户按下任意键后继续执行程序
            # os.system("pause")
            sys.exit(1)     # 异常退出

        birthday_month = nl_birthday.month
        birthday_day = nl_birthday.day
        # 今年生日
        year_date = datetime.date(int(year), birthday_month, birthday_day)
    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 获取国历生日的今年对应月和日
        year_date = datetime.date(int(year), birthday_month, birthday_day)

    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    year_date = get_datetime_str(year_date)
    if today_dt > year_date:
        if birthday_year[0] == "r":
            r_mouth = int(birthday.split("-")[1])
            r_day = int(birthday.split("-")[2])
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((int(year) + 1), r_mouth, r_day).to_datetime().date()
            birth_date = datetime.date((int(year) + 1), r_last_birthday.month, r_last_birthday.day)
            print(type(birth_date))
        else:
            # 获取国历明年生日的月和日
            birth_date = datetime.date((int(year) + 1), birthday_month, birthday_day)

            str_birth_date = get_datetime_str(birth_date)
        birth_day = (datetime.datetime.strptime(str_birth_date, "%Y-%m-%d").date() - datetime.datetime.strptime(today_dt, "%Y-%m-%d").date()).days

    elif today_dt == year_date:
        birth_day = 0
    else:
        birth_day = (datetime.datetime.strptime(year_date, "%Y-%m-%d").date() - datetime.datetime.strptime(today_dt, "%Y-%m-%d").date()).days

    if birth_day == 0:
        birthday_data = "生日快乐，祝福你无事绊心弦，所念皆如愿。"
    else:
        birthday_data = "平安喜乐，得偿所愿。"

    return birth_day, birthday_data

def get_image_url():
url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
'Content-type': 'application/x-www-form-urlencoded'

    }
    r = requests.get(url, headers=headers, verify=False)
    r.encoding = 'UTF-8-sig'
    image_url = "https://cn.bing.com" + json.loads(r.text)["images"][0]["url"]

    return image_url

def send_message(to_user, access_token, template_id, result, city_nm, birth_day, birthday_data):
"""
发送微信通知
:param to_user:
:param access_token:
:param template_id:
:param result:
:param city_nm:
:param birth_day:
:param birthday_data:
:return:
"""
weather = result["type"] # 天气
max_temperature = result["high"] # 高温
min_temperature = result["low"] # 低温
glowing_terms = random.choice(lines) # 每日一言

    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year  # 年 2024
    month = localtime().tm_mon  # 月 1
    day = localtime().tm_mday  # 日 19

    today = datetime.date(year=year, month=month, day=day)
    week = week_list[today.isoweekday() % 7]

    data = {
        "touser": to_user,
        "template_id": template_id,
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "city_nm": {
                "value": city_nm,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "max_temperature": {
                "value": max_temperature,
                "color": get_color()
            },
            "min_temperature": {
                "value": min_temperature,
                "color": get_color()
            },
            "glowing_terms": {
                "value": glowing_terms,
                "color": get_color()
            },
            "birth_day": {
                "value": birth_day,
                "color": get_color()
            },
            "birthday_data": {
                "value": birthday_data,
                "color": get_color()
            }
        }
    }

    # 推送消息
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()

if **name** == '**main**':
today_dt = get_datetime_str() # 获取当日日期
t_year = today_dt.split("-")[0] # 当年

    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
            access_token = get_access_token(config)
            birth_day, birthday_data = get_birthday(config, t_year, today_dt)    # 生日祝福语
            city_nm = config["city_nm"]                 # 城市名
            # 获取城市当日天气
            flag, result = get_weather_info(config, today_dt)
            template_id = config["template_id"]         # 模板ID
            # 接收的用户
            to_user = config["user"]                    # 用户里诶奥

except FileNotFoundError:
