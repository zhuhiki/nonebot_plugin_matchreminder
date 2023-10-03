import time
from httpx import AsyncClient
from nonebot.plugin import on_fullmatch, on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent,GroupMessageEvent
import asyncio
from httpx import AsyncClient
import datetime
from bs4 import BeautifulSoup
from nonebot.plugin import on_fullmatch
from nonebot.log import logger
import re
import lxml
import datetime
import time
from nonebot.plugin import on_fullmatch
from fake_useragent import FakeUserAgent
###列表下标0为比赛名称、下标1为比赛时间、下标2为比赛链接
cf = []
async def get_data_cf() -> bool:
    global cf
    url = 'https://codeforces.com/api/contest.list?gym=false'
    num = 0 #尝试获取的次数，最多尝试三次
    while num < 3 :
        try:
            if(len(cf) > 0):
                cf.clear()
            async with AsyncClient() as client:
                r = await client.get(url, timeout=10)
            for each in r.json()['result'][0::]:
                if each['phase'] != "BEFORE":
                    break
                contest_name = each['name']
                contest_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(each['startTimeSeconds']))
                id = each['id']
                contest_url = f'https://codeforces.com/contest/{id}'
                cf.append([contest_name, contest_time, contest_url])  #从左到右分别为比赛名称、比赛时间、比赛链接
            cf.reverse()
            return True
        except:
            num += 1
            await asyncio.sleep(2)  #两秒后再次获取信息
    return False
async def ans_cf() -> str:
    global cf
    if len(cf) == 0:
        await get_data_cf()
    if len(cf) == 0:
        return f'突然出错了，稍后再试哦~'
    msg = ''
    tot = 0
    for each in cf:
        msg += '比赛名称：' + each[0] + '\n'\
            + '比赛时间：' + each[1] + '\n'\
            + '比赛链接' + each[2]
        tot += 1
        if (tot != 3):
            msg += '\n'
        else:
            break
    return f"找到最近的 {tot} 场cf比赛为：\n" + msg
cf_matcher = on_fullmatch('/cf',priority = 80,block=True)
@cf_matcher.handle()
async def reply_handle():
    msg = await ans_cf()
    await cf_matcher.finish(msg)
#atc比赛
###列表下标0为比赛名称、下标1为比赛时间、下标2为比赛链接
atc = []
async def get_data_atc() -> bool:  # 以元组形式插入列表中，从左到右分别为比赛名称、比赛时间、比赛链接
    global atc
    url = f'https://atcoder.jp/contests/?lang=en'
    num = 0  # 爬取次数，最多爬三次
    while num < 3:
        try:
            if len(atc) > 0:
                atc.clear()
            async with AsyncClient() as client:
                resp = await client.get(url=url, timeout=10.0)
            soup =BeautifulSoup(resp.text, 'lxml').find_all(name='div', attrs={'id': 'contest-table-upcoming'})[0].find_all('tbody')[0].find_all('td')
            ans1 = str(soup[1].contents[5].contents[0])
            url1 = 'https://atcoder.jp' + re.findall(r'<a href="(.+?)">', str(soup[1]))[0]
            ss = str(soup[0].contents[0].contents[0].contents[0]).replace('+0900', '')
            ans2 = str(datetime.datetime.strptime(ss, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=1))
            ans2 = ans2[0:-3]
            ans3 = str(soup[5].contents[5].contents[0])
            url2 = 'https://atcoder.jp' + re.findall(r'<a href="(.+?)">', str(soup[5]))[0]
            ss1 = str(soup[4].contents[0].contents[0].contents[0]).replace('+0900', '')
            ans4 = str(datetime.datetime.strptime(ss1, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=1))
            ans4 = ans4[0:-3]
            atc.append([ans1, ans2, url1])
            atc.append([ans3, ans4, url2])
            return True
        except Exception as e:
            logger.warning(str(e))
            num += 1
            await asyncio.sleep(2)
    return False


async def ans_atc() -> str:
    global atc
    try:
        if len(atc) == 0:
            await get_data_atc()
        if len(atc) == 0:
            return f'突然出错了，稍后再试哦~'
        return f"找到最近的 2 场atc比赛为：\n" \
               + '比赛名称：' + atc[0][0] + '\n' + '比赛时间：' + atc[0][1] + '\n' + '比赛链接：' + atc[0][2] + '\n' \
               + '比赛名称：' + atc[1][0] + '\n' + '比赛时间：' + atc[1][1] + '\n' + '比赛链接：' + atc[1][2]
    except:
        return f'突然出错了，稍后再试哦~'
atc_matcher = on_fullmatch('/atc', priority=80, block=True)
@atc_matcher.handle()
async def reply_handle():
    msg = await ans_atc()
    await atc_matcher.finish(msg)
#牛客比赛
headers = {
    'user-agent': FakeUserAgent().random
}
###列表下标0为比赛名称、下标1为比赛时间、下标2为比赛链接
nc = []
async def get_data_nc() -> bool:
    global nc
    url = 'https://ac.nowcoder.com/acm/calendar/contest'
    num = 0  # 爬取次数,最大为3
    while num < 3:
        try:
            date = str(datetime.datetime.now().year) + ' - ' + str(datetime.datetime.now().month)
            second = '{:.3f}'.format(time.time())
            params = {
                'token': '',
                'month': date,
                '_': second
            }
            if (len(nc) > 0):
                nc.clear()

            async with AsyncClient() as client:
                r = await client.get(url, headers=headers, params=params, timeout=20)

            r = r.json()
            second2 = int(float(second) * 1000)
            if r['msg'] == "OK" and r['code'] == 0:
                for data in r["data"]:
                    if data["startTime"] >= second2:
                        contest_name = data["contestName"]
                        contest_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(data['startTime'] / 1000))
                        contest_url = data["link"]
                        nc.append([contest_name, contest_time, contest_url])
                return True
            else:
                return False
        except:
            num += 1
            await asyncio.sleep(2)
    return False


async def ans_nc() -> str:
    global nc
    if len(nc) == 0:
        await get_data_nc()
    if len(nc) == 0:
        return f'突然出错了，稍后再试哦~'
    # second = '{:.3f}'.format(time.time())
    # second2 = int(float(second)*1000)
    msg = ''
    n = 0
    for data in nc:
        n += 1
        msg += "比赛名称：" + data[0] + '\n'
        msg += "比赛时间：" + data[1] + '\n'
        msg += "比赛链接：" + data[2] + '\n'
        if n == 3:
            break
    return f"找到最近的 {n} 场牛客比赛为：\n" + msg
nc_matcher = on_fullmatch(('/nc'), priority=70, block=True)
@nc_matcher.handle()
async def _():
    msg = await ans_nc()
    await nc_matcher.finish(msg)