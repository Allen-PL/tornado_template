# __*__coding:utf-8__*__
# @ModuleName: 
# @Function: 
# @Author: pl
# @Time: 2021/11/23 14:15
import datetime

from apscheduler.schedulers.tornado import TornadoScheduler

from libs.aliyun_sms import sms


class InitFuncStore():

    async def create_task(self):
        scheduler = TornadoScheduler()
        now = datetime.datetime.now()
        task_instance = AssemblyOutTask()
        scheduler.add_job(task_instance.run, 'interval', seconds=3,
                          next_run_time=now + datetime.timedelta(seconds=10))
        scheduler.start()


async def send_sms_code(phone: str, code: str):
    response = await sms(phone, code, )
    # 记录日志


