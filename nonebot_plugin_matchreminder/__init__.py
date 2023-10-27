from nonebot import get_driver
from .config import *
from nonebot.permission import SUPERUSER
import datetime
from datetime import timedelta
from nonebot.plugin import on_fullmatch
from nonebot import require, get_bot
from nonebot.rule import to_me
from nonebot.log import logger
import asyncio
from .data_source import *
matchreminder_time=matchreminder_config.matchreminder_time
matchreminder_list=matchreminder_config.matchreminder_list


from nonebot.plugin import PluginMetadata
__plugin_meta__ = PluginMetadata(
    name="算法比赛查询和今日比赛自动提醒",
    description="可以查询牛客、atcoder、codeforces平台比赛信息并在今日比赛前进行提醒(请在.env.prod添加或修改超级用户，以免出现意料之外的错误)",
    usage=\
        "/cf->查询cf比赛\n"\
        "/nc->查询牛客比赛\n"\
        "/atc->查询atcoder比赛\n"\
        "/今日比赛->查询今天的比赛\n"\
        '/比赛提醒->手动设置定时提醒(仅超级用户,可以自己改)\n'
        '/开摆->删除所有提醒任务,注意是所有定时任务(不建议乱用)(仅超级用户，可以自己改)\n',
    type="application",
    homepage="https://github.com/zhuhiki/nonebot_plugin_matchreminder",
    config=Config,
    supported_adapters = {"nonebot.adapters.onebot.v11"},
)
try:
    scheduler = require("nonebot_plugin_apscheduler").scheduler
except BaseException:
    scheduler = None
logger.opt(colors=True).info(
    "已检测到软依赖<y>nonebot_plugin_apscheduler</y>, <g>开启定时任务功能</g>"
    if scheduler
    else "未检测到软依赖<y>nonebot_plugin_apscheduler</y>, <r>禁用定时任务功能</r>"
)

today_matcher = on_fullmatch('/今日比赛',priority=70,block=True)
@today_matcher.handle()
async def _():
    msg = await ans_today()
    await today_matcher.finish(msg)

#比赛闹钟的提示信息
async def noticemesage(msg):
    await asyncio.sleep(2)
    for id in matchreminder_list:
        await asyncio.sleep(1)
        await get_bot().send_group_msg(group_id=id,message=msg)

#设置提醒任务
async def auto_notice():
    global cf
    global nc
    global atc
    await ans_today()

    today = datetime.datetime.now().date()
    msg1=''
    msg2=''
    msg3=''
    n=0
    if(len(cf)>0):
        for cfn in cf:
            cur_time = datetime.datetime.strptime(str(cfn[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                date_object1 = datetime.datetime.strptime(cfn[1], '%Y-%m-%d %H:%M')+timedelta(minutes=-30)
               
                msg1='哇哇哇，马上要比赛喽，可别迟到了啊！'+'\n'
                if n==0:
                    msg1+='◉cf比赛：\n'
                    n=1
                msg1 += "比赛名称：" + cfn[0] + '\n'
                msg1 += "比赛时间：" + cfn[1] + '\n'
                msg1 += "比赛链接：" + cfn[2] + '\n'
                if scheduler:
                    scheduler.add_job(noticemesage,'date',run_date=date_object1,kwargs={"msg":msg1 })
                    logger.info('cf比赛提醒添加成功')
    n=0
    if(len(nc)>0):
        for ncn in nc:
            cur_time = datetime.datetime.strptime(str(ncn[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                date_object2 = datetime.datetime.strptime(ncn[1], '%Y-%m-%d %H:%M') + timedelta(minutes=-30)
                
                msg2 = '哇哇哇，马上要比赛喽，可别迟到了啊！' + '\n'
                if n==0:
                    msg2+='◉牛客比赛：\n'
                    n=1
                msg2 += "比赛名称：" + ncn[0] + '\n'
                msg2 += "比赛时间：" + ncn[1] + '\n'
                msg2 += "比赛链接：" + ncn[2] + '\n'
                if scheduler:
                    scheduler.add_job(noticemesage, 'date', run_date=date_object2, kwargs={"msg":msg2 })
                    logger.info('牛客比赛提醒添加成功')
    if(len(atc)>0):
        for atcn in atc:
            cur_time = datetime.datetime.strptime(str(atcn[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                date_object3 = datetime.datetime.strptime(atcn[1], '%Y-%m-%d %H:%M') + timedelta(minutes=-30)
                
                msg3 = '哇哇哇，马上要比赛喽，可别迟到了啊！' + '\n'
                if n==0:
                    msg3+='◉atc比赛：\n'
                    n=1
                msg3 += "比赛名称：" + atcn[0] + '\n'
                msg3 += "比赛时间：" + atcn[1] + '\n'
                msg3 += "比赛链接：" + atcn[2] + '\n'
                if scheduler:
                    scheduler.add_job(noticemesage, 'date', run_date=date_object3,kwargs={"msg":msg3 })
                    logger.info('atc比赛提醒添加成功')
    if(len(cf)==0 and len(nc)==0 and len(nc)==0):
        await noticemesage(msg='获取比赛异常，问问管理员吧！')
    if msg1 == '' and msg2 == '' and msg3 == '':
        await noticemesage(msg='今天没有比赛哦，我可以好好休息了，但是你们不能哦')
    else:
        await noticemesage(msg='今日比赛提醒装填完毕，我会提醒你们的！')
#定时启动设置比赛提醒任务
if scheduler:
    scheduler.add_job(auto_notice,
                      "cron", hour=matchreminder_time['hour'],minute=matchreminder_time['minute'],id="auto_notice"
                      )
###手动设置定时任务(我也不知道为什么要做手动的，不过感觉总会有点用处的)
notice=on_fullmatch('/提醒比赛',priority=70,block=True,permission=SUPERUSER)
@notice.handle()
async def noticehand():
    global cf
    global nc
    global atc
    await ans_today()
    today = datetime.datetime.now().date()
    msg1=''
    msg2=''
    msg3=''
    n=0
    if(len(cf)>0):
        for cfn in cf:
            cur_time = datetime.datetime.strptime(str(cfn[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                #在此处修改比赛提醒的时间,下面同理
                date_object1 = datetime.datetime.strptime(cfn[1], '%Y-%m-%d %H:%M')+timedelta(minutes=-30)
        
                msg1='哇哇哇，马上要比赛喽，可别迟到哇！'+'\n'
                if n==0:
                    msg1+='◉cf比赛：\n'
                    n=1
                msg1 += "比赛名称：" + cfn[0] + '\n'
                msg1 += "比赛时间：" + cfn[1] + '\n'
                msg1 += "比赛链接：" + cfn[2] + '\n'
                if scheduler:
                    scheduler.add_job(noticemesage,'date',run_date=date_object1,kwargs={"msg":msg1 })
                    logger.info('cf比赛提醒添加成功')
    n=0
    if(len(nc)>0):
        for ncn in nc:
            cur_time = datetime.datetime.strptime(str(ncn[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                date_object2 = datetime.datetime.strptime(ncn[1], '%Y-%m-%d %H:%M') + timedelta(minutes=-30)
                
                msg2 = '哇哇哇，马上要比赛喽，可别迟到哇！' + '\n'
                if n==0:
                    msg2+='◉牛客比赛：\n'
                    n=1
                msg2 += "比赛名称：" + ncn[0] + '\n'
                msg2 += "比赛时间：" + ncn[1] + '\n'
                msg2 += "比赛链接：" + ncn[2] + '\n'
                if scheduler:
                    scheduler.add_job(noticemesage, 'date', run_date=date_object2, kwargs={"msg":msg2 })

                    logger.info('牛客比赛提醒添加成功')
    if(len(atc)>0):
        for atcn in atc:
            cur_time = datetime.datetime.strptime(str(atcn[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                date_object3 = datetime.datetime.strptime(atcn[1], '%Y-%m-%d %H:%M') + timedelta(minutes=-30)
                
                msg3 = '哇哇哇，马上要比赛喽，可别迟到哇！' + '\n'
                if n==0:
                    msg3+='◉atc比赛：\n'
                    n=1
                msg3 += "比赛名称：" + atcn[0] + '\n'
                msg3 += "比赛时间：" + atcn[1] + '\n'
                msg3 += "比赛链接：" + atcn[2] + '\n'
                if scheduler:
                    scheduler.add_job(noticemesage, 'date', run_date=date_object3,kwargs={"msg":msg3 })
                    logger.info('atc比赛提醒添加成功')
    if(len(cf)==0 and len(nc)==0 and len(nc)==0):
        await notice.finish(message='获取比赛异常，问问管理员吧！')
    if msg1 == '' and msg2 == '' and msg3 == '':
        await notice.finish(message='今天没有比赛哦，我可以好好休息了，但是你们不能哦')
    else:
        await notice.finish(message='今日比赛提醒装填完毕，我会提醒你们的！')
#删除所有定时任务
dele=on_fullmatch('/开摆',permission=SUPERUSER)
@dele.handle()
async def delet():
    if scheduler:
        scheduler.remove_all_jobs()
        logger.info('已删除所有定时任务')
    await dele.finish(message='删除提醒成功！希望能度过一个快乐的假期呢!')
#查询今日比赛
async def ans_today():  # today
    global cf
    global atc
    global nc
    msg = ''
    n = 0
    today = datetime.datetime.now().date()
    if len(cf) == 0:
        await get_data_cf()
    if len(cf) > 0:
        for each in cf:
            cur_time = datetime.datetime.strptime(str(each[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                if n == 0:
                    msg += '◉cf比赛：\n'
                msg += '比赛名称：' + each[0] + '\n' \
                       + '比赛时间：' + each[1] + '\n' \
                                                 f'比赛链接：' + each[2] + '\n'
                n = 1
            else:
                break
    n = 0
    msg2 = ''
    if len(nc) == 0:
        await get_data_nc()
    if len(nc) > 0:
        # second = '{:.3f}'.format(time.time())
        # second2 = int(float(second)*1000)
        for data in nc:
            cur_time = datetime.datetime.strptime(str(data[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                if n == 0:
                    msg2 += '◉牛客比赛：\n'
                    n = 1
                msg2 += "比赛名称：" + data[0] + '\n'
                msg2 += "比赛时间：" + data[1] + '\n'
                msg2 += "比赛链接：" + data[2] + '\n'
    n = 0
    msg3 = ''
    if len(atc) == 0:
        await get_data_atc()

    if len(atc) > 0:
        for each in atc:
            cur_time = datetime.datetime.strptime(str(each[1]), "%Y-%m-%d %H:%M").date()
            if cur_time == today:
                if n == 0:
                    msg3 += '◉atc比赛：\n'
                msg3 += '比赛名称：' + each[0] + '\n' \
                        + '比赛时间：' + each[1] + '\n' \
                        + '比赛链接：' + each[2] + '\n'

    if len(cf) == 0 and len(nc) == 0 and len(atc) == 0:
        return f'查询出错了，稍后再尝试哦~'
    if msg == '' and msg2 == '' and msg3 == '':
        return '今天没有比赛，但也要好好做题哦~'
    return '找到今天的比赛如下：\n' + msg + msg2 + msg3

