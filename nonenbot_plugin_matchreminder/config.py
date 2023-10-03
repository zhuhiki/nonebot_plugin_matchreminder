from pydantic import BaseModel, Extra
from typing import List, Dict
from pathlib import Path

from nonebot import get_driver

driver = get_driver()

class Config(BaseModel, extra=Extra.ignore):
    matchreminder_time: Dict[str, str] = {"hour": "8", "minute": "30"}
    #此处添加发送每日比赛提醒的群聊
    matchreminder_list: List[str] = []
    """Plugin Config Here"""

matchreminder_config = Config