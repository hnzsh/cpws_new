import json
from datetime import datetime
from or_sql import oracle_select_13,oracle_update_13
from redis_db import db_redis_task
from loguru import logger
import time


def task():
    try:
        push_sql = """SELECT x.公司名称,x.MD5 FROM SMC_USER.数盟查_批量查询采集任务交互表 x WHERE x.裁判文书=0"""

        se_13 = oracle_select_13(push_sql)
        for se in se_13:
            up_se0 = se[0]
            up_se1 = se[1]
            js = json.dumps({"md5":up_se1,"company":up_se0}, ensure_ascii=False)
            up_sql = f"""UPDATE SMC_USER.数盟查_批量查询采集任务交互表 SET 裁判文书 = 1,裁判文书开始时间 = TO_DATE('{datetime.now().now().strftime('%Y-%m-%d %H:%M:%S')}', 'YYYY-MM-DD HH24:MI:SS') WHERE SMC_USER.数盟查_批量查询采集任务交互表.MD5 = '{up_se1}'"""
            db_redis_task.lpush("cpws", js)
            logger.info(js)
            oracle_update_13(up_sql)
            time.sleep(1)
    except Exception as e:
        logger.error(e.args[0])
        time.sleep(120)


if __name__ == '__main__':
    while True:
        task()
        hour = datetime.now().hour
        t1 = 3 if 8 < hour < 19 else 10
        time.sleep(t1)

