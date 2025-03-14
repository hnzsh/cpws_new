# -*- coding: utf-8 -*-
import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from ip_get import get_ip
import math
import hashlib
from or_sql import mysql_insert,mysql_select,mysql_select_whjy
from redis_db import db_redis_task
import redis
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from or_sql import oracle_select_13,oracle_update_13
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


def is_night_or_early_morning():
    now = datetime.now()
    evening_7pm = now.replace(hour=19, minute=0, second=0, microsecond=0)
    morning_9am_next_day = (now + timedelta(days=1)).replace(hour=8, minute=30, second=0, microsecond=0)

    if now >= evening_7pm:
        now = now + timedelta(days=1)

    return evening_7pm <= now < morning_9am_next_day


sss = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
count = int(random.choice(sss))


def is_element_visible(driver, locator):
    try:
        element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(locator)
        )
        return element.is_displayed()
    except:
        return False


def get_cpws():
    REDIS_HOST_TASK = '192.168.0.89'
    REDIS_PORT_TASK = 16379
    REDIS_PW_TASK = '@XDOPyZ&mCTQKe$c'
    REDIS_DB_TASK = 1
    REDIS_ENCODING = 'utf-8'
    redis_client = redis.StrictRedis(
        host=REDIS_HOST_TASK,
        port=REDIS_PORT_TASK,
        password=REDIS_PW_TASK,
        db=REDIS_DB_TASK,
        decode_responses=True
    )
    while True:
        try:
            key = redis_client.lpop('cpws')
            if key:
                logger.info("拉取信息:%s" % key)
                break
            else:
                raise
        except:
            logger.info("暂无数据......")
            time.sleep(180)
    return key


def scroll_down_slowly(driver, duration, scroll_amount):
    last_y = driver.execute_script("return window.pageYOffset;")
    for _ in range(int(scroll_amount / 10)):
        driver.execute_script(f"window.scrollTo(0, {last_y + 10});")
        last_y += 10
        time.sleep(duration / scroll_amount * 10)


def scroll_up_slowly(driver, duration, scroll_amount):
    last_y = driver.execute_script("return window.pageYOffset;")
    step = scroll_amount // 10
    interval = duration / 10.0
    for _ in range(int(scroll_amount / step)):
        new_y = last_y - step
        driver.execute_script(f"window.scrollTo(0, {new_y});")
        last_y = new_y
        time.sleep(interval)


def create_driver(headless=True, stealth=False):
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")  # 更隐蔽的无头模式
        options.add_argument("--window-size=1280,720")  # 避免响应式布局错乱
        options.add_argument("--disable-gpu")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    options.add_argument(r"--user-data-dir=C:\Users\SMKJ\AppData\Local\Google\Chrome\User Data\Default")

    if stealth:
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-web-security")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
    service = Service(executable_path=ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)

# def drivers():
#     options = webdriver.ChromeOptions()
#     # options.add_argument(f'--proxy-server=http://{get_ip("ZGZX")}')
#     options.add_argument("--user-data-dir=" + r'C:\Users\SMKJ\AppData\Local\Google\Chrome\User Data\Default')  # 使用本地浏览器插件
#     options.add_experimental_option("excludeSwitches", ['enable-automation'])
#     prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片    2 不加载图片
#     options.add_experimental_option("prefs", prefs)
#     driver = webdriver.Chrome(options=options)
#     return driver

# def drivers():
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # 添加无头模式参数
#     chrome_options.add_argument("--disable-gpu")  # 如果需要，可以禁用 GPU 加速
#     chrome_options.add_argument("--window-size=920x108")  # 设置虚拟窗口大小（可选）
#     driver = webdriver.Chrome(options=chrome_options)
#     return driver


def test_exceptions(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except Exception as e:
        print("测试错误原因:%s" % e)
        return False


def login(driver,phone, pwd):
    window_handles_all = driver.window_handles
    len_handle = len(window_handles_all)
    for i in range(len_handle):
        _lastWindow = driver.window_handles[-1]
        driver.switch_to.window(_lastWindow)
        time.sleep(1)
        driver.close()
    try:
        # driver = drivers()
        driver = create_driver(headless=False, stealth=True)
        driver.get("https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html?")
        driver.set_page_load_timeout(120)
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="loginLi"]/a').click()
        time.sleep(10)
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[0]
        driver.switch_to.frame(iframe)
        element_user = driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[1]/div/div/div/input')
        element_user.send_keys(phone)
        logger.info("输入手机号......")
        time.sleep(2)
        element_pwd = driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[2]/div/div/div/input')
        element_pwd.send_keys(pwd)
        logger.info("输入密码......")
        time.sleep(2)
        element_click = driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[3]/span')
        element_click.click()
        logger.info("点击登陆......")
        driver.switch_to.default_content()
        time.sleep(20)  # //*[@id="logout"]/a
        _lastWindow = driver.window_handles[-1]
        driver.switch_to.window(_lastWindow)
        driver.refresh()
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="logout"]/a[contains(text(),"退出")]')))
    except:
        driver.refresh()
        login(driver, phone, pwd)


def verify(driver):
    pause_time = random.uniform(35, 55)
    try:
        WebDriverWait(driver, pause_time).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="contentIframe"]')))
        return True
    except:
        return False


def tiqus(elements):
    results = []
    try:
        for element in elements:
            result = getattr(element, 'text', "null")
            results.append(result)
        root = ''.join(results)
    except:
        root = "null"
    return root


def tiqu(text):
    try:
        if text:
            text = text[0].text
            logger.info(text)
        else:
            text = "null"
    except Exception as e:
        logger.error("提取出现问题:", e)
        text = "null"
    return text


def get_session(phone, pwd):
    # driver = drivers()
    logger.info("启动......")
    driver = create_driver(headless=False, stealth=True)
    try:
        driver.get("https://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html?")
        driver.set_page_load_timeout(120)
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="loginLi"]/a').click()
        locator = (By.XPATH, '//*[@id="logout"]/a[contains(text(),"退出")]')
        if is_element_visible(driver, locator):
            pass
        else:
            time.sleep(15)
            iframe = driver.find_elements(By.TAG_NAME, 'iframe')[0]
            driver.switch_to.frame(iframe)
            element_user = driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[1]/div/div/div/input')
            element_user.send_keys(phone)
            logger.info("输入手机号......")
            time.sleep(2)
            element_pwd = driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[2]/div/div/div/input')
            element_pwd.send_keys(pwd)
            logger.info("输入密码......")
            time.sleep(2)
            element_click = driver.find_element(By.XPATH, '//*[@id="root"]/div/form/div/div[3]/span')
            element_click.click()
            logger.info("点击登陆......")
            driver.switch_to.default_content()
            time.sleep(3)  # //*[@id="logout"]/a
            _lastWindow = driver.window_handles[-1]
            driver.switch_to.window(_lastWindow)
            driver.refresh()
            WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="logout"]/a[contains(text(),"退出")]')))
        list_md5_key = []
        mysql_md5_key = mysql_select()
        while True:
            pause_time10086 = random.uniform(2, 3)
            time.sleep(pause_time10086)

            # 高级检索
            try:
                # keyword = driver.find_element(By.XPATH, '//div[@class="search-middle"]/input')
                # keyword.clear()
                # md_com = json.loads(get_cpws())
                # name_need = md_com["company"]
                # up_se1 = md_com["md5"]
                # time.sleep(pause_time10086)
                # keyword.send_keys(name_need)
                # time.sleep(pause_time10086)
                # driver.find_element(By.XPATH, '//*[@id="_view_1540966814000"]/div/div[1]/div[3]').click()
                # 高级检索
                keyword = driver.find_element(By.XPATH, '//*[@id="qbValue"]')
                time.sleep(pause_time10086)
                driver.find_element(By.XPATH,'//*[@id="_view_1540966814000"]/div/div[1]/div[1]').click()  # 点击高级检索
                time.sleep(pause_time10086)
                # driver.find_element(By.XPATH,'//*[@id="qbType"]').click()  # 选择检索类型
                # time.sleep(pause_time10086)
                # driver.find_element(By.XPATH,'//*[@id="qwTypeUl"]/li[7]').click()  # 选择判决结果进行检索
                # time.sleep(pause_time10086)
                md_com = json.loads(get_cpws())
                name_need = md_com['company']
                up_se1 = md_com['md5']
                keyword.send_keys(name_need)
                time.sleep(pause_time10086)
                driver.find_element(By.XPATH, '//*[@id="searchBtn"]').click()  # 点击  检索
                time.sleep(pause_time10086)
            except Exception as e:
                logger.error(e)
            try:
                WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="_view_1545184311000"]/div[1]/div[2]')))
            except:
                ver2 = verify(driver)
                if ver2:
                    login(driver, phone, pwd)
                    # keyword = driver.find_element(By.XPATH, '//div[@class="search-middle"]/input')
                    # keyword.clear()
                    # pause_time1 = random.uniform(2, 3)
                    # time.sleep(pause_time1)
                    # md_com = json.loads(get_cpws())
                    # name_need = md_com["company"]
                    # up_se1 = md_com["md5"]
                    # keyword.send_keys(name_need)
                    # time.sleep(pause_time1)
                    # driver.find_element(By.XPATH, '//*[@id="_view_1540966814000"]/div/div[1]/div[3]').click()
                    # time.sleep(pause_time1)
                    # 高级检索
                    keyword = driver.find_element(By.XPATH, '//*[@id="qbValue"]')
                    time.sleep(pause_time10086)
                    driver.find_element(By.XPATH, '//*[@id="_view_1540966814000"]/div/div[1]/div[1]').click()  # 点击高级检索
                    time.sleep(pause_time10086)
                    # driver.find_element(By.XPATH, '//*[@id="qbType"]').click()  # 选择检索类型
                    # time.sleep(pause_time10086)
                    # driver.find_element(By.XPATH, '//*[@id="qwTypeUl"]/li[7]').click()  # 选择判决结果进行检索
                    # time.sleep(pause_time10086)
                    md_com = json.loads(get_cpws())
                    name_need = md_com['company']
                    up_se1 = md_com['md5']
                    keyword.send_keys(name_need)
                    time.sleep(pause_time10086)
                    driver.find_element(By.XPATH, '//*[@id="searchBtn"]').click()  # 点击  检索
                    time.sleep(pause_time10086)
                    WebDriverWait(driver, 320).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="_view_1545184311000"]/div[1]/div[2]')))
            time.sleep(pause_time10086)
            try:
                numbers = int(driver.find_element(By.XPATH, '//*[@id="_view_1545184311000"]/div[1]/div[2]/span').text)
            except Exception as e:
                numbers = 0
                logger.error(e)
            logger.info(f"一共有{numbers}条数据......")
            if numbers != 0:
                pause_scroll_duration = random.uniform(5, 9)
                pause_scroll_total = random.uniform(600, 1200)
                scroll_down_slowly(driver, pause_scroll_duration, pause_scroll_total)
                try:
                    page_size_box = Select(driver.find_element(By.XPATH, '//div[@class="WS_my_pages"]/select[@class="pageSizeSelect"]'))
                    page_size_box.select_by_visible_text('15')
                except Exception as e:
                    logger.error("不能把文件数量设置成15条......%s" % e)
                pause_scroll_duration = random.uniform(3, 7)
                pause_scroll_total = random.uniform(600, 1200)
                scroll_up_slowly(driver, pause_scroll_duration, pause_scroll_total)
                # //*[@id="_view_1545184311000"]/div[2]/div[2]/a
                driver.find_element(By.XPATH, '//*[@id="_view_1545184311000"]/div[2]/div[2]/a').click()
                logger.info("选择排序......")
                pause_time2 = random.uniform(3, 5)
                time.sleep(pause_time2)
                page = 1

                if numbers % 15 == 0:
                    pageNumber = numbers // 15
                else:
                    pageNumber = numbers // 15 + 1
                pageNumbers = pageNumber
                click_num = 0
                while pageNumber:
                    initial_handle = driver.current_window_handle
                    time.sleep(page / 10)
                    time.sleep(pause_time2)
                    ranges = 15
                    if numbers <= ranges:
                        ranges = numbers
                    if pageNumber == 1 and numbers % 15 != 0:
                        ranges = numbers % 15
                    for i in range(ranges):
                        logger.info(f"爬取第{pageNumbers - pageNumber + 1}页,第{i + 1}个案例......")
                        event_xpath = '//*[@id="_view_1545184311000"]/div[' + str(i + 3) + ']/div[2]/h4/a'
                        title = tiqu(driver.find_elements(By.XPATH, '//*[@id="_view_1545184311000"]/div[' + str(i + 3) + ']/div[2]/h4/a'))
                        try:
                            fayuan = driver.find_element(By.XPATH, '//*[@id="_view_1545184311000"]/div[' + str(i + 3) + ']/div[3]/span[1]').text
                        except:
                            fayuan = "null"
                        combined_string = str(title + fayuan)
                        md5_hash = hashlib.md5()
                        md5_hash.update(combined_string.encode('utf-8'))
                        md5_key = md5_hash.hexdigest()
                        if md5_key in mysql_md5_key or md5_key in list_md5_key:
                            logger.info("文书已存在")
                            continue
                        logger.info("爬取新增文书...")
                        if test_exceptions(driver, event_xpath):
                            logger.info("开始爬取文书详情...")
                            time.sleep(5 + i / 10)
                            driver.find_element(By.XPATH, event_xpath).click()
                            ver = verify(driver)
                            if ver:
                                login(driver, phone, pwd)
                                break
                            else:
                                logger.info("进入详情页......")
                                time.sleep(1)
                                last_window_handle = driver.window_handles[-1]
                                driver.switch_to.window(last_window_handle)
                                # article_detail = driver.find_element(By.XPATH, '//div[@class="PDF_box"]')
                                try:
                                    article_detail = WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="PDF_box"]')))
                                    logger.info("开始提取内容...")
                                    time.sleep(5)
                                    biaoti = tiqu(article_detail.find_elements(By.XPATH, './/div[1]'))  # 标题
                                    anyou = tiqu(article_detail.find_elements(By.XPATH, './/*[@id="iframedf"]/span[1]'))  # 案由
                                    anhao = tiqu(article_detail.find_elements(By.XPATH, './/*[@id="iframedfah"]/span[1]'))  # 案号
                                    text_times = tiqu(article_detail.find_elements(By.XPATH,'.//div[2]/div/table/tbody/tr[2]/td[2]'))  # 发布时间
                                    article_detail_pox = driver.find_element(By.XPATH,'//*[@id="_view_1541573883000"]/div/div[1]/div[@class="PDF_pox"]')  # 裁判内容
                                    divs = article_detail_pox.find_elements(By.XPATH, './/div')

                                    len_divs = len(divs)
                                    groups = len_divs // 6
                                    s22 = tiqus(divs[:groups])
                                    s23 = tiqus(divs[groups:groups * 2])
                                    s25 = tiqus(divs[groups * 2:groups * 3])
                                    s26 = tiqus(divs[groups * 3:groups * 4])
                                    s27 = tiqus(divs[groups * 4:groups * 5])
                                    s28 = tiqus(divs[groups * 5:]).replace('\u3000', ' ')
                                    data_to_insert = (
                                        str(md5_key),
                                        str(biaoti),
                                        str(anhao),
                                        str(anyou),
                                        str(text_times),
                                        str(s22),
                                        str(s23),
                                        str(s25),
                                        str(s26),
                                        str(s27),
                                        str(s28)
                                    )
                                    logger.info(data_to_insert)
                                    try:
                                        sql = """
                                                INSERT INTO `cpwsdata` (`md5_key`, `标题`, `案号`, `案由`, `发布时间`, `s22`, `s23`, `s25`, `s26`, `s27`, `s28`)
                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                                ON DUPLICATE KEY UPDATE
                                                    `标题` = VALUES(`标题`),
                                                    `案号` = VALUES(`案号`),
                                                    `案由` = VALUES(`案由`),
                                                    `发布时间` = VALUES(`发布时间`),
                                                    `s22` = VALUES(`s22`),
                                                    `s23` = VALUES(`s23`),
                                                    `s25` = VALUES(`s25`),
                                                    `s26` = VALUES(`s26`),
                                                    `s27` = VALUES(`s27`),
                                                    `s28` = VALUES(`s28`)
                                                """
                                        mysql_insert(sql, data_to_insert)
                                        list_md5_key.append(md5_key)
                                        logger.info("更新MD5...")
                                    except Exception as e:
                                        logger.error("存储main出错", e)
                                        time.sleep(120)
                                except Exception as e:
                                    logger.error("提取详情,存储出错:%s" % e)
                                    driver.close()
                                    driver.switch_to.window(initial_handle)
                                    continue
                                time.sleep(10)
                                try:
                                    driver.close()
                                    driver.switch_to.window(initial_handle)
                                except Exception as e:
                                    logger.error(e)
                                    time.sleep(120)
                                    driver.close()
                                    driver.switch_to.window(initial_handle)
                        else:
                            continue
                    time.sleep(5)
                    pageNumber -= 1
                    try:
                        if click_num > 0:
                            break
                        driver.find_element(By.LINK_TEXT, '下一页').click()
                        time.sleep(2)
                        ver2 = verify(driver)
                        if ver2:
                            login(driver, phone, pwd)
                            break
                        click_num += 1
                    except Exception as e:
                        logger.error('没有下一页了......%s' % e)
                        time.sleep(120)
                    driver.switch_to.default_content()
                    page += 1
            try:
                up_sql = f"""UPDATE SMC_USER.数盟查_批量查询采集任务交互表 SET 裁判文书 = 2,裁判文书完成时间 = TO_DATE('{datetime.now().now().strftime('%Y-%m-%d %H:%M:%S')}', 'YYYY-MM-DD HH24:MI:SS') WHERE SMC_USER.数盟查_批量查询采集任务交互表.MD5 = '{up_se1}'"""
                oracle_update_13(up_sql)
            except Exception as e:
                logger.error(e)
                up_sql = f"""UPDATE SMC_USER.数盟查_批量查询采集任务交互表 SET 裁判文书 = 2,裁判文书完成时间 = TO_DATE('{datetime.now().now().strftime('%Y-%m-%d %H:%M:%S')}', 'YYYY-MM-DD HH24:MI:SS') WHERE SMC_USER.数盟查_批量查询采集任务交互表.MD5 = '{up_se1}'"""
                oracle_update_13(up_sql)
                time.sleep(120)
            driver.back()
            time.sleep(15)
    except Exception as e:
        logger.error("错误原因: %s" % e)
        try:
            up_sql = f"""UPDATE SMC_USER.数盟查_批量查询采集任务交互表 SET 裁判文书 = 2,裁判文书完成时间 = TO_DATE('{datetime.now().now().strftime('%Y-%m-%d %H:%M:%S')}', 'YYYY-MM-DD HH24:MI:SS') WHERE SMC_USER.数盟查_批量查询采集任务交互表.MD5 = '{up_se1}'"""
            oracle_update_13(up_sql)
        except Exception as e:
            up_sql = f"""UPDATE SMC_USER.数盟查_批量查询采集任务交互表 SET 裁判文书 = 2,裁判文书完成时间 = TO_DATE('{datetime.now().now().strftime('%Y-%m-%d %H:%M:%S')}', 'YYYY-MM-DD HH24:MI:SS') WHERE SMC_USER.数盟查_批量查询采集任务交互表.MD5 = '{up_se1}'"""
            oracle_update_13(up_sql)
            time.sleep(120)
            logger.error(e)
        try:
            js = json.dumps({"md5": up_se1, "company": name_need}, ensure_ascii=False)
            db_redis_task.rpush("cpws",js)
        except Exception as e:
            logger.error(e)
        login(driver, phone, pwd)
        if is_night_or_early_morning():
            logger.info("休息一下......")
            time.sleep(2700)
        else:
            logger.info("休息一下......")
            time.sleep(1000)
        return "空"


while True:
    lis = [("15836248161", "Gunxcun63@"), ("18439470189", "Aa123456!")]
    count += 1
    choose = count % len(lis)
    logger.info('count: %s, choose: %s' % (count,choose))
    user_name = lis[choose][0]
    user_pwd = lis[choose][1]
    logger.info("使用账号：%s" % user_name)
    session = get_session(user_name, user_pwd)
    # session = get_session("18640832929", "Abc123456")
# cache_li = mysql_select_whjy()
# cache_li = ['东莞市帝格五金制品有限公司', '中企凯澳幕墙装饰工程有限公司江阴分公司', '漳平市宏闽投资有限责任公司', '漳州市品凯机械有限公司', '汉川市乐川新型建筑材料有限公司', '张家港市甲壹建筑设计有限公司', '苏州金融租赁股份有限公司', '上海科苑景观工程设计有限公司', '安庆市南宜房地产开发有限公司池州分公司', '昆山市蓝天绿地静电技术有限公司', '四川凯莱实业有限公司', '丹阳市成量机电设备有限公司', '温州市合跃企业管理咨询有限公司', '合昌国际贸易(深圳)有限公司', '上海厚沛贸易有限公司', '佛山市禅城区威龙阀门机电供应站', '重庆市九龙橡胶制品制造有限公司', '上海众誉纸业有限公司', '贵州黔策策划有限公司', '漳州哈中食品贸易有限公司', '成都今月古月文化传播有限公司', '苏州越合强工业设备有限公司', '昆山市利群固废处理有限公司', '中山市锦标混凝土有限公司', '瓜州县祁连街瓜州门窗厂', '广东旭升建筑安装工程有限公司', '佛山市南海区明晟机械制造有限公司', '中山市传美奇电器有限公司', '东台溱东镇德之仁建材经营部', '上海恩森照明设计工程有限公司', '丹阳宇辰(天津)光电科技有限公司', '相城阳澄湖度假区湖之韵饭店', '中建三局集团有限公司', '池州市南门门窗厂', '常泰建设集团有限公司', '嵊州市祥顺印务有限公司', '平昌县第二建筑工程公司', '杭州恒益轩投资合伙企业(有限合伙)', '东莞市冈吉电子科技有限公司', '南木林县联绿农投资发展有限公司', '宁波科发宝鼎创业投资合伙企业(有限合伙)', '东莞市思博实业投资有限公司', '衡水丰捷贸易有限公司', '苏州旭野机电设备有限公司', '江苏地基工程有限公司', '广东邦克厨卫有限公司', '福建龙岩永大工贸有限公司', '陈瑛陈群陈璟陈亮', '苏州奥多油品有限公司', '衡水同伟商贸有限公司', '湖南高城消防实业有限公司', '江苏常瑞汽车集团有限公司宿迁分公司(尹成家)', '南京恒实电子有限公司', '江苏科宇装饰工程有限公司', '江阴红生广告装饰有限公司', '成都同盟雅致服装有限公司', '宁波江北力劲玻璃有限公司', '重庆建设建筑工程有限公司', '江山市紫姣食品经营部', '泉州延陵信息技术有限公司', '株洲太平洋药业有限公司', '苏州市天盛人防工程设备有限公司', '中翔(十堰)检验检测有限公司', '安吉递铺江安钢塑制品厂', '宜兴祥瑞园艺科技有限公司', '西安微开智慧科技有限公司', '杭州立诚实业有限公司', '福建省南方联合置业有限公司', '上海中林纸业有限公司', '河南红革幕墙有限公司贵州分公司', '苏州旭东建设工程有限公司', '广西金洪混凝土有限公司', '株洲和顺医疗器械贸易有限公司', '上海联合电影院线有限责任公司', '昆山益强环保纸品有限公司', '上海颂吉贸易有限公司', '四川明辉建筑工程有限公司', '四川蓝景光电技术有限责任公司', '北京北医泰然医疗投资管理有限公司', '冀州强达机械租赁站', '太仆寺旗宏捷货物运输中心(史建民)', '深圳市鑫腾宇实业有限公司', '镇江兴兆房地产开发有限公司', '张家界凯发建材有限公司', '中联重科股份有限公司', '上海洁光工贸有限公司', '泉州恒众贸易有限公司', '福建省美杰新型材料有限公司', '昆山华林森通风设备有限公司', '苏州阔野建材有限公司', '温州万腾鞋材有限公司', '河南永易享电子商务有限公司', '上海奕茂环境科技有限公司', '上海瑞齐实业有限公司', '贵州誉通达建筑工程有限责任公司', '苏州丰硕洁净技术有限公司', '北京巨典投资有限公司', '东莞华辉数控机床有限公司', '池州市东和兴商贸有限公司', '国家税务局大厂回族自治县税务局法制股', '众方同裕信息技术(北京)有限公司', '浙江康泰管业科技有限公司', '丹阳市科祺达电镀设备有限公司', '宁德市精信环保科技股份有限公司', '衡水市顺安致达建筑装饰有限公司', '上海宏信设备工程有限公司', '南通蒂博电梯有限公司', '上海晓事贸易有限公司', '上海甲君广告工程有限公司', '益阳朝阳建融安装部', '贵州万博瑞景工程设计有限公司', '中山市汇尊电器有限公司', '阜城县皓通工程安装有限公司', '杭州龙山化工有限公司', '修文龙发建材有限公司', '铜陵市金诚融资担保有限公司', '长兴和平鑫兴家俱厂(普通合伙)', '长沙市天心区安雅医疗器械服务部', '铜山区瑞宏宾馆', '江西禅信新材料科技有限公司', '四川宏达(集团)有限公司', '沈阳中建防水工程有限公司', '成都建工第九建筑工程有限公司', '衡水尚泽电梯销售有限公司', '上海冉琪机电设备有限公司', '太仓市浩凯贸易有限公司', '南通隆都时装有限公司', '胜利油田渤海管具有限责任公司', '江苏金融租赁股份有限公司', '上海昀升建设集团股份有限公司', '上海多田美术设计有限公司', '江苏德恒物业管理有限公司', '上海创逸健身发展有限公司', '广东众志联城建材有限公司', '江苏易诺威建筑科技有限公司', '南通通安金属材料有限公司', '苏州弗诺欣五金机电有限公司', '广州市增城骏展盈钢材经营部', '中山市兴中集团有限公司', '安吉盛祥面料商行', '雅玛札崎(苏州)精密冲压有限公司', '昆山市涵奇精密机械有限公司', '苏州工业园区中小企业融资担保有限公司', '定南县国有资产经营有限责任公司', '宜兴天马消防门业有限公司', '东莞市优创超声波科技有限公司', '仲利国际贸易(上海)有限公司', '日喀则市高争商混有限责任公司', '金华蓬勃装饰装潢材料有限公司', '佛山市祺沃专用设备有限公司', '海门市三星镇百度家用纺织品厂', '德尔保定智能流体有限公司', '衡水云泓金系商贸有限公司', '东莞市美信达实业投资有限公司', '广东中明建筑装饰实业有限公司', '佛山市顺德区佳涂乐恒融建筑装饰有限公司', '济南中弘旅游开发有限公司(关联方往来款)', '成都市鼎阳环保科技有限责任公司', '中山银达融资担保投资有限公司', '上海凝瑞粘合剂科技发展有限公司', '源科弘森精密科技(昆山)有限公司', '衡水市恒烁建设工程检测有限责任公司', '南通旺合祥纺织科技有限公司', '衡水鑫泽通风环保设备有限公司', '衡水诚达工程项目管理有限公司', '杭州汉斯人工环境工程有限公司', '黑龙江省鑫正融资担保集团有限公司', '江苏鑫宏机电制造有限公司', '苏州兰生中创企业管理有限公司', '丽水市佳业革基布销售有限公司', '北京天润融通科技股份有限公司', '吴江市天成模具材料有限公司', '四川盾安机电科技有限公司', '昆山聚优鼎精密机械有限公司', '四川上知文化传媒有限公司', '中山市亨派厨卫电器有限公司', '衢州市信保融资担保有限公司', '衡水昌海达建筑装饰有限公司', '苏州勉博建筑装饰工程有限公司', '成都市和乐门业有限公司', '乌海市飞龙商贸有限责任公司', '中山市新顺意物流实业有限公司', '智译安科(北京)科技有限公司', '江苏昊泽瑞光电科技有限公司', '四川旭晨华宇消防工程有限公司', '河北富士达电梯有限公司', '上海钺源实业有限公司', '修文县龙场镇卓能科技服务中心', '衡水阜强房屋建筑工程有限公司', '中山市石岐区小额贷款股份有限公司', '苏州方圆仪器设备校准检测服务有限公司', '吴江市汾湖镇金家坝车友汽车服务部', '刘燕(继承人)', '上海岩琦供应链股份有限公司', '上海恒开通信技术有限公司', '池州市工业发展投资有限公司', '武汉兴达电子线缆有限公司', '海门市美加顺电器经营部', '南通润达特阔染整有限公司', '江西鼎耀仿古家具有限公司', '兴化市红阳玻璃制品有限公司', '衡水晟环建筑工程有限公司', '昆山鑫裕佳人力资源有限公司', '佛山市禅城区德俊五金机电经营部', '泉州市宝象日化有限公司', '上海划云城市建设发展有限公司', '江苏省广电有线信息网络股份有限公司连云港分公司', '东莞市得力包装制品有限公司', '温州煜闳信息咨询有限公司', '肇庆市鼎湖区凤凰恒发木器厂', '池州市华润天成商务酒店有限公司', '深圳市宝安区沙井国辉电子经销部', '吴江市汾湖镇黎里万善轴承经营部', '无锡通达金翔钢材剪切有限公司', '宁波市鄞州远景货架有限公司', '上海德隆胶业有限公司', '德阳赛尔奇五金工具有限公司', '佛山市三水大炜陶瓷辅料有限公司', '湖北佳源美新型建材有限公司', '苏州隆振鑫物业有限公司', '合肥颖宏食品有限公司', '苏州莱博真空技术有限公司', '昆山星之尚计算机系统工程有限公司', '佛山市俊辉鸿贸易有限公司', '中山市高端科技服务有限公司', '日立电梯(中国)有限公司', '江苏城房物业管理有限公司', '江苏明超国际贸易有限公司', '张家港市杨舍镇石匠建材经营部(个体工商户)', '金华欧配装饰材料有限公司', '临海市广华汽车服务中心', '江苏善行资产管理有限公司', '温州市鹿城区丰门陈庆克鞋料店', '金宝丽科技(苏州)有限公司', '宁波银衣织造有限公司', '昆山市周市镇新月达防水涂料批发部', '东莞市民悦传输技术有限公司', '恒诚巨创(北京)科技有限公司', '荣盛房地产发展股份有限公司', '安吉亿祥线带商行', '北京金丰环球建筑装饰有限公司', '贵州盛达欣工程服务有限公司', '海南保誉置业有限公司', '泉港阿洪小吃店', '中山利展小额贷款股份有限公司', '泉州市达发织造有限责任公司', '重庆立博机电有限公司', '巴中翡翠文化传媒有限公司', '青岛海知遇健康科技有限公司', '江苏春阳幕墙门窗股份有限公司', '广州鑫力印刷有限公司', '太仓市众德食品有限公司', '衡水腾翔清洁服务有限公司', '杭摩新材料集团股份有限公司', '苏州富润得机电设备有限公司', '成都亿年房地产开发有限公司', '苏州安民安全科技有限公司', '广州中和养猪设备有限公司', '佛山市南海西樵昇大保温材料厂', '苏州市大华钢构净化工程有限公司', '佛山市南海区翔鑫达不锈钢加工厂', '上海虎威印刷材料有限公司', '新余良山矿业有限责任公司', '安吉租赁有限公司', '北京美格菲健身有限公司', '上海益善堂装饰设计有限公司', '兴宁市光科电子有限公司', '福建佶龙机械科技股份有限公司', '益阳中燃城市燃气发展有限公司', '江苏中南建设装饰集团有限公司', '巨人通力电梯有限公司', '北京中京合创投资有限责任公司', '上海权浩实业有限公司', '南京市国有资产投资管理控股(集团)有限责任公司', '苏州市木渎金桥经济技术发展公司', '江苏仁合中惠工程咨询有限公司', '湘西靓宅门窗有限公司', '苏州华大智联企业管理有限公司', '佛山市恒毅机电贸易有限公司', '中星联丰建设集团有限公司', '四川同辉钢结构有限公司', '阜城县啸通水暖五金商城', '苏州科勒迪电子有限公司', '苏州锦帆建设工程检测有限公司', '福建省平潭全健生物科技有限公司', '江苏大千虎皇集团有限公司', '黄冈市黄州区飞鹏酒类商行', '昆山恒创人力资源有限公司', '浙江华晟纺织科技有限公司', '常熟市虞山镇卫仕装饰材料商行', '昆山锦宁泽贸易有限公司', '温州市瓯海瞿溪品一鞋材经营部', '上海帛喆窗帘布艺经营部', '巴中市市政广告有限公司', '苏州国发科技小额贷款有限公司', '江苏豪威堡服饰实业有限公司', '四川鑫框视界文化传播有限公司', '昆山亿塑通物业服务管理有限公司', '浙江美达皮具有限公司', '中山市永盛市政工程有限公司', '海门恒基文化传媒有限公司', '南通金鹤钢材有限公司', '江苏三江基础工程有限公司', '上海德惠特种风机有限公司', '四川瀚聪市场管理有限公司', '监利市昊明广告有限公司', '武汉工建彩钢工程有限公司', '广东恒屹科技有限公司', '江苏中南锦程工程咨询有限公司', '河北省金融租赁有限公司', '广东万联经济发展有限公司', '广州绿葆健康管理有限公司', '河北峰领顺达建筑装饰有限公司', '息烽永靖镇光祥砂厂', '宁波市日安电器有限公司', '苏州瑞驰机电科技有限公司', '上海喜洛玻璃制品有限公司', '深圳市水圣科技发展有限公司', '贵阳白云胜辉采石厂', '盐城兴冈建设投资有限公司', '上海平归物流有限公司', '江苏彤心不动产营销代理有限公司', '嵊州市瑞欣机械有限公司', '昆山盛驰捷精密模具有限公司', '苏州冠鼎物业管理有限公司', '苏州环优检测有限公司', '四川玮图消防工程有限公司', '扬州格瑞特电气技术有限公司', '德化县铭新保力绒加工店', '河北冠能石油机械制造有限公司', '铜陵天源股权投资集团有限公司', '佛山市旗开得胜建材有限公司', '麦田信诺装饰工程(北京)有限公司', '佛山市悦华兴业进出口有限公司', '贵州燃气集团股份有限公司贵阳凯翼云城文化旅游有限公司', '张家界宏泰时代汽车服务有限公司', '苏州吴中经济开发区益顺鑫模具配件经营部', '天津兴航建材销售有限公司', '佛山陶盟供应链管理有限公司', '佛山市利家福建材有限公司', '新世纪发展集团有限公司安徽第一分公司', '德清杜伟生竹制品厂', '昆山东野电子有限公司', '东莞市清溪龙腾百货店', '东莞致宏精密模具有限公司', '广州房屋开发公司', '嘉凯城集团商业资产管理有限公司苏州分公司', '山东欧泰轴承有限公司', '江苏省信用融资担保有限公司', '杭州剡东不锈钢有限公司', '东莞市隆兴纸业有限公司', '张家口市良晨工矿物资有限公司', '武汉凯乐宏图房地产有限公司', '南通猛劲精密科技有限公司', '广州广臻感光材料有限公司', '湖南达瑞商贸有限公司', '黄嘉辉(原债权人中山邦迪五金玻璃制品有限公司)', '雅安市雨城区兆庆五金经营部', '衡水旭柏建设工程有限公司', '管理人后续清算费用', '福建惠安县高远石艺有限公司', '上海阿道润滑科技有限公司', '常州市哈特工具有限公司', '杭州新联竹制品有限公司', '西安星河力得企业管理咨询有限公司', '扬州市江都区伟宏焊割器材有限公司', '浙江联通家具配件有限公司', '温州普典经贸有限公司', '苏州凡特真空溅镀科技有限公司', '福州高新区投资控股有限公司', '广东金马游乐股份有限公司', '浙江流欣装饰工程有限公司', '武汉市金马凯旋家具投资有限公司', '南通绿能新能源汽车有限公司', '衡水衡洋物业服务有限公司', '南通市中南建工设备安装有限公司', '巴中市经济开发区合兴办公家具二经营部', '苏州鑫业诚金属材料有限公司', '丹阳市和鑫源资产投资管理有限公司', '昆山蔚坤环境技术服务有限公司', '衡水京坤岩土工程有限公司', '佛冈县广和置业有限公司', '长兴金融服务中心有限公司', '广州酷旅旅行社有限公司', '周美英陈九洲', '广州市君燕服装有限公司', '昆山焱赋包装制品有限公司', '中国房地产开发集团南通有限公司', '常熟市支塘镇周氏汽车维护服务部', '兰溪进泰商贸有限公司', '溧阳市光明塑粉厂', '上杭佳和小额贷款服务有限公司', '泉州福泰皮革有限公司', '全南县民间融资登记服务有限公司', '十堰国厚工贸有限公司', '苏州廷力人力资源有限公司', '佛山市超钥陶瓷材料有限公司', '南京德力体育用品有限公司', '江山市艾特电脑商行', '铜陵市盛丰管理咨询有限责任公司', '河北联谊工程项目管理有限公司', '南通川海环境服务有限公司', '湖南汇丰医药有限公司', '安吉史博家具股份有限公司', '苏州仓庆金属制品有限公司', '无锡高威工程机械制造有限公司', '上海超舜纺织品有限公司', '金华市晨源办公家具有限公司', '中国大唐集团新能源股份有限公司', '合肥协创企业管理咨询服务有限公司', '扬州天辉实验室装备环保工程有限公司', '河北迈尔斯通电子材料有限公司', '国药控股医疗器械(北京)有限公司', '河北恒茂建筑工程有限公司', '伊宁县哈羊饲料有限责任公司', '安徽苏邦节能科技有限公司', '贵州众鹏建设有限公司', '北京君之源伟业商贸有限公司', '包钢集团机械设备制造有限公司', '嵊州市金诚电子有限公司', '厦门国贸集团股份有限公司', '北京市国通资产管理有限责任公司', '泉州市台商投资区自来水有限公司', '重庆唯沃商业管理有限公司', '佛山市顺德区揽旺五金制品有限公司', '湖北丽群巍泰建筑工程有限公司', '邛崃恒泰昌商砼有限公司', '民生金融租赁股份有限公司', '长沙美奥物业管理服务有限公司', '绍兴卓拉纺织品有限公司', '四川一电航空技术有限公司', '杨根玲(池州市贵池区成功名烟名酒店)', '赣州发展融通资产管理有限公司', '上海昕民精密机械有限公司', '上海洁的环保设备有限公司', '宁波科仕诚塑料制品有限公司', '江苏登壹建设工程有限公司', '佛山市禅城区得众劳保用品经营部', '溧阳市银泰农村小额贷款有限公司', '扬中市威柯特生物工程设备有限公司', '安吉鹏盛家具厂', '昆山豫东企业管理有限公司', '义乌市创凯包装材料有限公司', '江苏捷诚建设项目管理咨询有限公司', '宁波兴嘉旺机械有限公司', '惠州市凯迪亚建材有限公司', '房商汇(江苏)信息科技有限公司', '苏州市百通金属制品有限公司', '广东凯勒斯卫浴实业有限公司', '徐州聚慧汽车服务有限公司', '重庆伟丰机械制造有限公司', '泉州市泉港区益康豆腐加工店', '联合环境水务(苏州)有限公司', '江苏省嘉园建设工程有限公司', '福州市医疗保障基金中心马尾管理部', '上海和雅石材工程有限公司', '广东精英无机材料有限公司', '包头市长江物资有限责任公司', '成都天达装饰广告有限公司', '泗阳县三联融资担保有限公司', '福清市永春混凝土外加剂有限公司', '常熟市鸿雁电器经营部', '上海茗松电力工程设备有限公司', '广州期诺贸易有限公司', '丹阳市和鑫源资产管理有限公司', '陈绿茵陈陆毅陈山范塞金', '霸州市梅地亚酒店管理有限公司', '武义银晶玻璃有限公司', '嵊州市宏诺机电有限公司', '安吉立辉贸易有限公司', '梁山宏轩机械配件制造有限公司', '山东建业合和项目管理有限公司', '亚洲新能源科技工程有限公司', '徐州铭睿新能源汽车服务有限公司', '监利中凯装饰工程设计有限公司', '上海兰俊建材有限公司', '重庆派朗建筑装饰集团有限公司', '福建易德鑫投资有限公司', '龙岩市医疗保障基金中心新罗管理部', '张家界好人建筑安装有限责任公司', '苏州荣盾人防工程防护设备有限公司', '苏州市苏园融资担保有限公司', '苏州市相城区永隆农村小额贷款有限公司', '扬州市恒隆典当行有限公司', '贵州昌昊建设有限责任公司', '苏州瑞华投资合伙企业(有限合伙)', '重庆洋铭建筑劳务有限公司', '巴中市星拓传媒有限公司', '四川众雁电梯有限公司', '南京市江宁区联鹏热处理厂', '仲利国际融资租赁有限公司', '上海锢悦金属材料有限公司', '浙江嘉欣金三塔丝绸服饰有限公司', '徐州市三官庙农贸市场有限公司', '江苏久诺新材料科技股份有限公司', '福建龙州工业园建设发展有限公司', '扬州派斯特换热设备有限公司', '上海翼利玻璃制品有限公司', '贵州豫章机电工程有限公司', '上海侨居玻璃有限公司', '梁山李娟商贸有限公司', '徐州寓泊容通停车场服务有限公司', '江苏阿特斯装饰工程有限公司', '泉州双瑞机械有限公司', '安吉博创家具有限公司', '河北臻安达电梯配件有限公司', '张家港市华宏钢结构有限公司', '衡水市冀州区得胜装卸搬运服务有限公司', '苏州睿发塑料包装材料厂', '东莞美兴模具有限公司', '昆山腾利达五金制品有限公司', '苏州海戈诺机械科技有限公司', '深圳市乐有家房产交易有限公司', '南通兴业人防工程设计有限公司', '天茂置业(南京)有限公司', '上海潘升玻璃制品有限公司', '北京时代动力鸿宇科技发展有限公司', '广东建滔积层板销售有限公司', '山东崇德纺纱有限责任公司', '江苏恒达机械制造有限公司', '广东顺德瑞利洁环境科技有限公司', '肇庆市如一房地产经纪有限公司', '中山市小榄镇新民五金制品厂(普通合伙)', '河南景之瑞服饰有限公司', '上海润上照明科技有限公司', '衡水铉鑫建筑工程有限公司', '苏州高新区中小企业融资担保有限公司', '宁德市福宁投资有限公司', '嵊州市雪峰电线电器场', '贵州燃气集团股份有限公司', '乐山市快捷劳务有限公司', '晋江经济报社', '石狮市古加希制衣有限公司', '安吉元顺竹木制品厂', '包钢集团万开实业有限公司昆区白彦道分公司', '上海马热实业有限公司', '衡水德一通电气设备有限公司', '河北五洲正元新材料有限公司', '四川海盛德广告有限公司', '粤欣雅纺织科技南通有限公司', '成都新光晋一科技有限责任公司', '徐州经济技术开发区金瑞房地产经营有限公司', '张家港市杨舍镇花火广告设计工作室', '吴江市苏商农村小额贷款股份有限公司', '上海越源信息科技有限公司', '北海世茂商业服务有限公司南京雨花分公司', '苏州绿加然农业投资有限公司', '上海子实喷涂机械有限公司', '益阳市朝阳心林花卉超市', '兴化市星元能源有限公司', '昆山昊捷晟五金制品有限公司', '上海先拓精细化工有限公司', '江苏恒立弹簧有限公司', '衡水烨龙建筑装饰工程有限公司', '常州奥马稀贵模具技术有限公司', '中山市巨风生活电器有限公司', '无锡大盛基础工程有限公司', '包头市四通鼓风机制造有限公司', '厦门汇堃投资合伙企业(有限合伙)', '贵州健通管道有限公司', '亳州市风瑞网络科技有限公司', '张美英郑凌燕', '广东坚朗五金制品股份有限公司', '衡水鼎正商贸有限公司', '库尔勒晶渃涵商贸有限公司', '昆山国创投资集团有限公司', '上海尊翔文化传播有限公司', '无锡普丽涂装有限公司', '石狮市中联银小额贷款有限公司', '赵黎阳潘如樑杨茂地李再励胡冬妹严美华戴春芳尹金招', '苏州伟益数控科技有限公司', '山西水务集团建设投资有限公司', '江苏建业建设集团有限公司', '南通四建集团有限公司', '江苏优盛美装饰材料有限公司', '徐州盛泉物业服务有限公司', '佛山市苏盐电器科技有限公司', '扬州华浦包装制品有限公司', '江苏盛阳消防门业有限公司', '江西国盛钨业有限责任公司', '常德宝峰建材销售有限公司', '恩平市和盛印刷制品有限公司', '广东粤财资产管理有限公司', '昆山亿峰粮油有限公司', '广州资产管理有限公司', '四川省建强建筑工程有限责任公司', '盐城琦昊环保设备有限公司', '南阳欧进建筑工程有限公司', '广州市宏洋箱包有限公司', '湖南星欣贸易有限公司', '康铭泰克科技股份有限公司', '包头市浩轩物资有限公司', '高新区浒墅关镇俞伟建材经营部', '泉州工拓机械制造有限公司', '苏州厍洋气体有限公司', '乐山市中区城区全成建材经营部', '佛山市普德机电设备有限公司', '链金国际有限公司', '乐山市中区城区顶上建材经营部', '国家税务总局盐城市盐都区税务局(税款滞纳金)', '昆山市锦溪镇奔阳服装厂', '苏州兰生现代产业园管理有限公司', '徐州荣爵汽车销售服务有限公司', '苏州市隆隆模具钢材有限公司', '烟台新科钢结构有限公司', '张家界市永定区小兵汽车维修部', '南昌世祥资产管理有限公司', '杭州传新纸品有限公司', '中山中汇投资集团有限公司', '昆山水淼物资有限公司', '国家税务总局广州市天河区税务局石牌税务所', '衡水纳瑞建材商贸有限公司', '有棱有角(上海)数字技术有限公司', '德州联瑞人防设备有限公司', '上海紫墙企业营销策划有限公司', '永城市领航新材料科技有限公司', '徐州市停车科技有限公司', '英轩重工有限公司', '无锡世腾包装材料有限公司', '湖南康盾健康科技有限公司', '伊东新(德阳)线缆设备有限公司', '江苏尊邦汽车配件有限公司', '苏州北桥建筑安装有限公司', '广州市智强企业管理咨询有限公司', '武陟县中小企业融资担保有限公司', '华油飞达集团有限公司', '江苏民安消防安全工程有限公司', '苏州佳捷知识产权代理有限公司', '海门市振兰建材有限公司', '娄底科悦思医疗器械有限公司', '重庆尚润电子有限公司', '东莞市惠金精密数控刀具有限公司', '金华市布克文化传播有限公司', '昆山市中裕农村小额贷款股份有限公司', '南京市江宁区汶成粮店', '广州市启蒙投资有限公司', '衡水重工电梯起重设备有限公司', '湖北襄大实业集团有限公司', '苏州市农业融资担保有限公司', '海门市立威建筑劳务有限公司', '扬州市江都区沿江农村小额贷款有限公司', '深圳市金秋电子科技有限公司', '宁波市鄞州汇南五金厂', '上海九梧装饰工程有限公司', '昆山宏锦益包装材料有限公司', '溧阳市农业贷款信用担保中心', '第九地质矿业勘察有限公司', '张家港市力成建材有限公司', '广东凯利威机电设备有限公司', '霍林郭勒市海神煤炭运销有限公司', '深圳市麦凯莱科技有限公司', '泰州神舟传动科技有限公司', '江苏鼎拓电子科技有限公司', '昆山市千灯镇宏伟乐纯水经营部', '苏州铁风营造工程有限公司', '连云港欧曼帝复合材料有限公司', '贵州汇友源消防工程有限公司', '佛山市善居电子商务有限公司', '苏州水力士机电设备安装有限公司', '昆山市星晖汽修服务中心', '锦然(浙江)建筑工程有限公司', '温州市可爱鞋业有限公司', '铜陵市义安区融资担保中心有限公司', '巴中市中信文化传媒有限责任公司', '中联重科融资租赁(北京)有限公司', '泉山区食在锦绣酒店', '南京吒象科技有限公司', '东莞钲熙企业管理咨询有限公司', '中海海隆商业管理(苏州)有限公司', '上海赛霆装饰材料有限公司', '空气化工产品气体生产(上海)有限公司', '丹阳智达模型有限公司', '重庆蜀地建筑工程有限公司', '明光市国厚资产管理有限公司', '北京侨信装饰工程有限公司', '四川省清溪茶业有限公司', '北京永和兴通实业有限公司', '平阳如祥资产管理有限公司', '苏州市吴艺园林绿化建设工程有限公司', '成都东方伟业合金有限公司', '锡山区鸿槐环氧地坪工程队', '龙岩市永定区永鑫融资担保有限公司', '苏州骏丰精工机械设备制造有限公司', '中睿智慧融资租赁(深圳)有限公司', '明光市富民小额贷款有限责任公司', '诏安城投集团有限公司', '东莞市华发纸张有限公司', '上海净达环境卫生发展有限公司', '宜兴市南翔印铁包装有限公司', '上海塔星幕墙装饰工程有限公司', '成都伯永恩贸易有限公司', '福安市华屹投资有限公司', '中山佬何电器有限公司', '江山市金杭贸易有限公司', '连云港市新浦区向阳社区旺家乐防盗门销售服务部', '益阳市邓石桥建筑工程有限公司', '上海速尊木业有限公司', '南昌市残疾人联合会', '昆山昌豪达精密机械有限公司', '无锡得朗建材贸易有限公司', '中山市一品精工电器有限公司', '大连巨铭房地产开发有限公司', '江苏慧眼数据科技股份有限公司', '中保世纪资产管理(北京)有限公司', '苏州致途金属制品有限公司', '浙江科博电器有限公司', '盐城曙光机械制造有限公司', '宜昌市国防动员办公室', '广东南安机电消防工程有限公司中山市分公司', '张家港和升数控机床制造有限公司', '湖北佐威电子科技有限公司', '天盾人防防护设备有限公司', '南京冀源节能建材有限公司', '中国邮政速递物流股份有限公司漳州市东山营业部', '上汽安悦充电科技有限公司', '苏州市鸿光模具有限公司', '深圳市华科联众营销策划有限公司', '九江鼎新实业有限公司', '南通长城建设集团有限公司', '岳阳军汇实业有限公司', '金华市鑫灿建筑材料有限公司', '山东京威建设工程质量检测有限公司', '汕头市博承投资有限公司', '河北迎客隆建设工程集团有限公司', '平昌县新世纪电脑经营部', '浙江浙北资产管理有限公司', '江苏利众建设工程有限公司', '苏州佳人良无纺布制品有限公司', '青岛居斯漫装饰有限公司', '苏州市禾裕科技小额贷款有限公司', '北京鑫诺金电子科技发展有限公司', '苏州市恒信建设监理咨询有限公司', '德清丽诺新材料科技有限公司', '广州丰利不锈钢制品有限公司', '吴江市松陵镇顺昌筛网五金商行', '绍兴柯桥日茂纺织有限公司', '深圳市合纵共创电子有限公司', '深圳前海百益资产管理股份有限公司', '无锡市于兴恒五金交电有限公司', '广州蚂蚁跳动传媒有限公司', '上海越光照明电器有限公司', '上海无声机电设备有限公司', '常州新展康精密机械厂', '江苏海泰供应链管理有限公', '平安国际融资租赁有限公司', '太仓市信合商务咨询有限公司', '昆山森之合模具技术有限公司', '岍慧(上海)化工有限公司', '中山市浩帆电子电器有限公司', '上海屹标建筑装饰工程有限公司', '国家税务总局广州市白云区税务局黄石税务所', '阜城县春来彩钢厂', '扬州市连心气体有限公司', '永康市仙阁贸易有限公司', '国家税务总局盐城市盐都区税务局(补充申报税款)', '评估费(生产线等)', '内蒙古晟辰地质勘查设计有限公司', '张家港市杨舍镇嘉翼发建材经营部', '福州海天装璜装修有限公司', '绍兴欧能光电有限公司', '昆山莘莘科技发展有限公司', '广州大都市国际旅行社有限公司中山七营业部', '丹阳市天晟投资有限公司', '徐州东大钢结构有限公司', '上海大容包装材料有限公司', '佛山市南海区伟富鸿塑料包装制品有限公司', '四川岷之窗装饰工程有限公司', '青岛正沃实业有限公司', '扬州大上钢铁贸易有限公司', '江苏常瑞汽车集团有限公司扬州分公司(王海艳)', '乐东百顺典当有限责任公司', '宁波卓尔智能家居有限公司', '碧堂物业服务(上海)有限公司常州分公司', '明策伟华有限公司', '安吉圣和家具有限公司', '福州八扇堂贸易有限公司', '泉州华利塑胶有限公司', '贵州恒源达电力工程建设有限责任公司', '江苏宏佳华新材料科技有限公司', '无锡唯江展示设计有限公司', '佛山市茂万电器实业有限公司', '苏州新顶点装饰设计制作有限公司', '昆明钦贤石材有限公司', '山东胜油管具有限公司', '常州三勇模型有限公司', '浙江新涛智控科持股份有限公司', '徐州华翔供用电工程有限公司连云港分公司', '广东省粤新资产管理有限公司', '柳道万和(苏州)热流道系统有限公司', '中山市奥森电子有限公司', '丹阳市佳飞亚机械有限公司', '广东佳富机电工程有限公司', '温州鹿城第三建筑工程有限公司', '徐州丰华信息科技有限公司', '郑州市迈丰门窗有限公司', '南通乔晟商贸有限公司', '安吉浩宸家具有限公司', '湖南省苏敬健康产业有限公司', '昆山奥瑞航空包装材料有限公司', '广东惠洁宝电器有限公司', '苏州通鼎非融资担保发展有限公司', '南通勘察设计有限公司', '北京北医医药有限公司', '江山市九鑫瓷业商行', '广州市御水机电设备科技有限公司', '天津新和国际物流有限公司上海分公司', '云汉芯城(上海)电子科技有限公司', '深圳市勘察研究院有限公司贵州分公司', '衡水市建设投资集团有限公司', '南通勤奔纺织有限公司', '欧姆特智能装备(扬州)有限公司', '上海市地矿建设有限责任公司', '昆山华通装饰工程有限公司', '佛山市造益机械设备有限公司', '苏州致尧工业地产咨询有限公司', '江苏舜天盛泰工贸有限公司', '昆山雄程精密组件有限公司', '江苏港运机械有限公司', '从江县丰泰矿业有限公司', '扬州市江阳工业园开发建设有限公司', '新明珠集团股份有限公司', '福建蓝壹环保有限公司', '联想融资租赁有限公司', '北京中方永固科技有限公司', '安吉县融资担保有限公司', '浙江大川照明有限公司', '南通美地园林工程有限公司', '上海富逸建筑工程队', '衡水兴作物业服务有限公司', '石家庄安居乐科技有限公司', '四川泛亚艺标景观工程有限公司', '苏州市吴中今晖产业投资合伙企业(有限合伙)', '鹤城建设集团股份公司佛山市分公司', '安阳市船友机电有限公司', '苏州工业园区科特建筑装饰有限公司', '储藏室实测面积差', '苏州唯准金属制品有限公司', '福州市简维装饰有限公司', '江苏苏油建设有限公司', '上海冰杰工贸有限公司', '昆山博众包装材料有限公司', '河北成达玻璃钢有限公司', '崇义县三志物流有限公司', '苏州久禾纸业有限公司', '金华市海日家居用品有限公司', '上海锐铂拓科技有限公司', '佛山市三角洲电器科技有限公司', '四川美凌蓄电池有限公司', '天津稳中园林绿化工程有限公司', '贵阳凯翼云城文化旅游有限公司', '南京佳强科技有限公司', '重庆驰骋机械制造有限公司', '武汉和兴祥建筑工程有限公司', '昆山金诚宇塑胶五金有限公司', '广东涵臣管道科技有限公司', '江苏太湖地基工程有限公司', '中投融资担保海安有限公司', '福州永强彩色包装有限公司', '南通宏讯安防工程有限公司', '邗江区邵氏小吃店', '揭阳市国杰实业投资有限公司', '衡水丙峰地基加固工程有限公司', '太仆寺旗建民矿山机电商店', '徐州易图汽车服务有限公司', '安吉介美家具有限公司', '江苏昊雄智能装备股份有限公司', '王延昕何春华', '厦门程泰食品有限公司', '嵊州市东兴金属材料有限公司', '苏州飞凌电子科技有限公司', '苏州国融企业管理有限公司', '苏州文丰金属材料有限公司', '四川华诚忠信建', '昆山本原模具钢材有限公司', '苏州亿尔斯模具有限公司', '佳泰(福建)实业有限公司', '恩平市佛燃能源有限公司', '张家港市润创金属制品有限公司', '重庆广豪建材有限公司', '石狮市三联贸易有限公司', '永辉彩食鲜发展有限公司', '苏州易兰洋生物资贸易有限公司', '上海广域建筑装饰工程有限公司', '重庆富吉机械制造有限公司', '苏州卓智众创企业管理服务有限公司', '通州建总集团有限公司', '余姚市兰山电机企业有限公司', '昆山市振利莱精密工具有限公司', '杭州意能企业管理合伙企业(有限合伙)', '上海拓邦化工科技有限公司', '上海顺泰电子科技有限公司', '四川省通信产业服务有限公司巴中市分公司', '龙岩市向荣制冷有限公司', '珠海经济特区西海集团有限公司', '上海泉益塑料包装材料有限公司', '广东河源莲田建筑工业化股份有限公司', '苏州市相城区黄桥潘春龙彩钢瓦店', '中山市富华管桩有限公司', '中邮建技术有限公司', '苏州昇彧纺织有限公司', '江苏港盛纺织科技有限公司', '内蒙古淳点实业有限公司', '宁波市安邦管业有限公司', '陈晓红江建荣江超云江晓明', '上海汉司实业有限公司', '山东崇德置业有限公司', '吴江市永达机械配件制造有限公司', '深圳市陶氏水处理设备技术开发有限公司', '湖州万美进出口有限公司', '泉州嘉润摩擦材料有限公司', '南通坤力通讯科技有限公司', '湖南省国立投资(控股)有限公司', '重庆华焜科技有限公司', '包头市依耐贸易有限责任公司', '海勃湾区新北方电机变压器修理部', '娄星区应许图文广告经营部', '山东崇德投资有限公司', '宁波易厨电器有限公司', '四川邛崃建筑有限公司', '江苏统一安装集团有限公司', '武宁县天元金属材料有限公司', '河北丰安电梯销售服务有限公司', '霸州市梅地亚温泉酒店', '安庆市大观区诚佳门窗加工厂', '浙江金大门业有限公司', '万源市华艺广告有限公司', '安徽恒康气弹簧有限公司', '泉州洛兴机械有限公司', '桔子酒店(中国)有限责任公司', '无锡市厚德雄资数控机床厂', '太仓市创源五金制品有限公司', '惠州市楷医科技有限公司', '重庆和金汽车配件有限公司', '河北拓联消防设备有限公司', '石棉县宏发塑料五金杂品门市部', '江苏亿隆金属表面处理有限公司', '佛山市壮盈材料科技有限公司', '镇江世通电子实业有限公司', '南通神驰电气有限公司', '宁波国普电器有限公司', '启迪设计集团股份有限公司', '江苏汇晟供应链管理有限公司', '湖北鑫腾煦保温材料有限公司', '江山市元隆食品经营部', '南通艺路贸易有限公司', '深圳市弘嘉祥科技有限公司', '欧力士融资租赁(中国)有限公司', '噢牌能源(浙江自贸区)有限公司', '广东金刚新材料有限公司', '江苏历显新材料科技有限公司', '南通西奥电梯有限公司', '佛山市菁濠建材有限公司', '昆山市华家喜运营管理有限公司', '昆山模懋注塑科技有限公司', '徐州陕汽华山汽车销售服务有限公司', '常州市聚川金属制品有限公司', '龙岩怡家园南祥物业管理有限公司', '潍柴火炬科技股份有限公司', '上海都浩建筑工程有限公司', '江苏恒耐炉料集团有限公司', '中山市优尊电器有限公司', '天津市水利工程集团有限公司', '太仓市联励电子科技有限公司', '上海申苏环境科技有限公司', '南昌奕星文化传媒有限公司', '嘉善艺胜金属装饰工程有限公司', '南通利兴华建材有限公司', '北京中弘弘毅投资有限公司(关联方往来款)', '佛山市南海区广汇能五金机械厂', '湖南立介信商贸有限公司', '湖南康瑞成医疗科技有限公司', '佛山市顺德区官皇五金塑料有限公司', '武邑县农村信用联社股份有限公司', '浙江光峰新材料科技有限公司', '青岛特来电智能设备有限公司', '广东聪信智能家居股份有限公司', '宁波市海曙洞桥怡中炉具厂', '常州奥森莱精密机械有限公司', '上海嘉萱蔓腾实业有限公司', '浙江阔邦纺织有限公司', '广东省水电集团有限公司', '丹阳市天惠投资发展有限公司', '舒城云辉物业有限公司', '广东特地陶瓷有限公司', '佛山市帝沃力陶瓷材料有限公司', '苏州汪涂思睿创业投资合伙企业(有限合伙)', '苏州市华能发电机有限公司', '铜陵金诚资产运营有限公司', '门口一问(苏州)智能化科技有限公司', '上海明锐工具有限公司', '福州市医疗保障基金中心鼓楼管理部', '上海兆合包装材料有限公司', '贵州正业工程技术投资有限公司', '绍兴智岛电器有限公司', '成都福桂苑健康咨询服务有限公司', '中山市基础建筑工程有限公司', '杭州力马汽配有限公司', '深圳市百慧生活科技有限公司', '南城县创新融资担保有限公司', '苏州佰鸿宇金属制品有限公司', '嵊州市恒润电机制造有限公司', '扬州市江都区沪武金仝农村小额贷款有限公司', '衡水铭丰人防设备有限公司', '池州市金能供热有限公司', '国家税务总局广州市白云区税务局景泰税务所', '上海炜铭商贸有限公司', '中诚智信工程咨询集团股份有限公司', '上海神开石油科技有限公司', '杭州艾柯伦贸易有限公司', '东莞市化兴胶粘剂有限公司', '龙海市海澄新旺鑫纸制品加工场', '东莞市韩社服装有限公司', '苏州天阳新能源科技有限公司', '海口蓝海水族有限公司', '南京恒尔森节能科技有限公司', '镇江市京口区捷诚农村小额贷款有限公司', '龙岩市龙大食品有限公司', '龙岩龙兴公路港物流有限公司', '重庆市丽锦建筑劳务有限公司', '四川博瑞人防工程有限公司', '上海茂速新型建材有限公司', '石狮市纺织品专业市场宏源商店', '河北晨滔智能科技有限公司', '浙江省浙商资产管理股份有限公司', '石狮市雄进贸易有限责任公司', '中山市普臣电气科技实业有限公司', '上海顿高实业发展有限公司', '衡水嘉轩乾幸商贸有限公司', '扬州市江都区合利农村小额贷款有限公司', '泗阳百盛钢结构有限公司', '广州广信感光材料有限公司', '深圳市长江塑钢有限公司', '吴江市鲈乡农村小额贷款股份有限公司', '苏州天月德安全技术科技有限公司', '苏州张琪建筑工程有限公司', '快递费(送达第二次分配实施方案发生)', '友博融资租赁(上海)有限公司', '监利县幸福广告有限公司', '佛山市南海区玥荣机械厂', '江西省融资担保集团有限责任公司', '温州大阳科技有限公司', '衡水森益建筑装饰工程有限公司', '译翎国际贸易(上海)有限公司', '上海利隆印刷器材有限公司', '重庆恒富机电制造有限公司', '美辉科技大厂回族自治县有限责任公司', '瑞江包装材料(上海)有限公司', '丹阳鼎尊国盛资产管理有限责任公司', '泰州海田电气制造有限公司', '霸州市泽华贸易有限公司', '上海姐姐好飒电子商务有限公司', '江苏宝涵租赁有限公司', '贵池区新光华车饰店', '常州市喆昌气弹簧有限公司', '纳雍县市政工程建设有限责任公司', '青岛福斯特物业管理有限公司', '徐州市云龙区鑫兴世昌汽车维修服务中心', '溧阳市食锦居餐饮有限公司', '徐州上析电气设备有限公司', '苏州市邓尉工业设备安装有限公司', '广州风情大世界有限公司', '上海松盈国际贸易有限公司', '河南金声听力技术有限公司', '石狮市博纶纺织贸易有限公司', '安徽九天印务有限公司', '上海中远汇丽建筑装潢有限公司', '南通飞宇电器设备有限公司', '饶辉跃(原债权人郑良艳)', '永年县农村信用联社股份有限公司', '上海祥中珠宝首饰有限公司', '成都赛野模型有限公司', '厦门宇龙机械有限公司', '苏州通鼎非融资性担保发展有限公司', '中国电建集团江西装备有限公司', '江苏常瑞汽车集团有限公司常州分公司(陈国平)', '石桂林(张俊娥)', '中盈商业保理(深圳)有限公司', '奥的斯机电电梯有限公司长沙分公司', '连云港德晖工程项目管理咨询有限公司', '云南奥柏家具制造有限公司', '苏州市吴中区甪直农村小额贷款有限公司', '泉州泉港阿平冷冻品店', '中旅水印(杭州)康养服务有限公司', '常州颖新纺织服饰有限公司', '霸州市日升昌贸易有限公司', '阜城县浩宇公路工程有限公司', '国家税务总局广州市从化区税务局温泉税务所', '玉林市亿祥纺织有限公司', '江苏泰洁检测技术股份有限公司', '天津海鑫融资租赁有限公司', '惠山洛社镇尚志水泥制品加工厂', '绍兴奋钧电机科技有限公司', '上海怔缘企业管理咨询中心', '中山市铭庆数字科技有限公司', '陈勇陈玲陈瑛陈丽敏', '江苏恒高建设有限公司', '中山火炬开发区利通达空调机电工程部', '昆山新亮杰机械设备有限公司', '徐州鸿蚨祥物业管理有限公司', '广州大都市国际旅行社有限公司广州大道南营业部', '环球车享汽车租赁有限公司', '临泉县中小企业融资担保有限公司', '苏州昌盛建设有限公司', '浙江寅寅科技有限公司', '深圳拓邦股份有限公司', '珠海中影影视服务有限公司', '徐州铁路嘉利商业贸易有限公司', '快递费(预留后期送达终结程序相关文书的快递费)', '上海水香贸易有限公司', '重庆玉田花木有限公司', '中山火炬开发区自来水有限公司', '常熟市玉山镇安士通治具商行', '四川永盛基业建设工程有限公司', '上海瑞科厨具有限公司', '上海俊江保温材料有限公司', '正力海洋工程有限公司', '晋江经济报发展有限责任公司', '江西国资创业投资管理有限公司', '浙江中合工程管理有限公司张家港分公司', '上海奔跑贸易有限公司', '衡水万信招标代理有限公司', '苏州研妙自动化科技有限公司', '马鞍山国源节能科技服务有限公司', '昆山耀越塑胶有限公司', '成都恒驰源新蓄电池有限公司', '河北舜联能源科技有限公司', '闽侯闽兴小额贷款有限公司', '上海万全保安服务有限公司', '衡水鼎力土方工程有限公司', '扬州市新巨人房地产开发有限公司', '吴江市恒泰投资担保有限公司', '苏州优咖文化传媒有限公司', '吴江市菀坪旭日缝纫机零件厂', '上海怀鑫木业有限公司', '济南中弘弘丰房地产开发有限公司(关联方往来款)', '吴江市顺江纺织有限公司', '衡水市筑兴建筑安装有限公司', '衡水佳奇建设工程有限公司', '东莞市昭鼎环保科技有限公司', '天津永联音悦文化传播有限公司', '上海杉丽实业有限公司', '苏州市贝森金属制品有限公司', '湖南湘晨空调工程有限公司', '攀枝花市国有投资(集团)有限责任公司(土地担保)', '深圳市招平申城三号投资中心(有限合伙)', '安徽省农业信贷融资担保有限公司', '成都市海纳建筑装饰工程有限公司', '南京苏宁建设监理有限公司', '贵州花溪喀斯特夜郎生态有限公司', '义乌科发创业投资合伙企业(有限合伙)', '成都市三星金属装饰有限公司', '虞城县明强仓储设备有限公司', '昆山市张浦镇誉可信模具经营部', '乌海市金广工贸有限责任公司', '高唐县国有旧城林场', '河北永瑞建筑安装工程有限公司衡水第一分公司', '石家庄宝石门业有限公司', '万华节能(烟台)工程有限公司', '四川国溢鑫华能源科技有限公司', '徐州市火花农贸市场有限公司', '林玮琼姚坤和', '上海和畅磨具磨料有限公司', '常熟耀拓机械有限公司', '四川博能燃气股份有限公司', '浙江省新华书店集团有限公司', '武汉雅西龙建筑节能涂料有限公司', '评估费(叉车)', '肇庆市欧陶新型材料有限公司', '阜城县四联商砼有限公司', '南京市浦口区明宏市场调查服务中心', '武汉公专建设安装工程有限公司重庆分公司', '中泽控股集团股份有限公司', '日喀则卓正工程有有限公司', '广州市新洪源空气净化制品有限公司', '阜城县魏双建材经销处', '龙飞科技(广东)有限公司', '衡水万兴保温建材有限公司', '中国石化国际事业有限公司', '福建正德有机板材有限公司', '安吉佳顺家具有限公司', '泉州市博良鞋材有限公司', '重庆开力暖通工程有限公司', '江苏祺睿汽车服务有限公司徐州分公司(陈超)', '无锡兰生中成企业管理有限公司', '义乌市彭小盒包装有限公司', '龙岩市医疗保障基金中心', '乌海市祥源机械设备安装有限公司', '上海港裕企业发展有限公司', '晋江正南贸易有限公司', '余姚市佳永士电器有限公司', '衡水信誉达防水工程有限公司', '福建隆盛轻工有限公司', '北京中弘网络营销顾问有限公司(往来款)', '佛山市元林房地产代理有限公司', '广东天腾精密科技有限公司', '吴江市豪宇五金机电有限公司', '广州佛朗斯股份有限公司佛山市高明分公司', '苏州安辰精密机械有限公司', '浙江树新木业有限公司', '南通市金信融资担保有限公司', '安徽杏集劳务有限公司', '上海致增实业有限公司', '广州领江会物业管理有限公司', '广州市麦力声医疗器械有限公司', '衡水磐石土方工程有限公司', '昆山凯昊通企业管理有限公司', '昆山龙汇纸制品有限公司', '开化县水务有限公司', '海安市海陵融资担保有限公司', '上海正儒企业发展有限公司', '河北万诚建材有限公司', '东莞市格锐特电子新材料有限公司', '明光融资担保有限公司', '太仓市奥虹绣品有限公司', '太仓市保安服务有限公司', '浙江台信资产管理有限公司', '雅莹集团股份有限公司', '苏州佳宜贸易有限公司', '中山市实业集团有限公司', '贵州伯乐居装饰设计工程有限公司', '吴江新世纪工程项目管理咨询有限公司', '乐山市名佳世纪广告有限公司', '上海驭擎机电有限公司', '东坡区凯萨灯饰经营部', '安徽龙云建设投资(集团)有限公司', '湖南国信财富小额贷款有限公司', '徐州经济开发区祥达停车场', '广州新宝房地产开发有限公司', '昆山华恒建筑装饰工程有限公司', '任丘市鑫实门业有限公司', '武汉威耐尔建材科技有限公司', '龙岩恒悦酒店有限公司', '临清市迅飞轴承有限公司', '天津蓝汇科技发展有限公司', '南京朗驰集团机电有限公司', '国家税务总局岳阳城陵矶新港区税务局城陵矶税务所', '佛山市群益化工有限公司', '盐城市昶桦儿童用品有限公司', '绍兴市冠越针纺有限公司', '武定县大银坝钛选厂', '日照市海洋水产资源增殖有限公司', '宁德市久恒商贸有限公司', '河北集建保温材料科技有限公司', '高新区横塘宫琪石材经营部', '苏州兰城网络科技有限公司', '嵊州市千瑞电器配件有限公司', '江西弘旺医疗器械有限公司', '江苏扮美装饰工程有限公司', '佛山市禅城区毅旋五金配件经营部', '定南县住房保障安置服务中心', '阜城县禧龙断桥铝塑门市部', '东莞市仲盛光电实业有限公司', '无锡巨优不锈钢有限公司', '上海君鸿实业有限公司', '昆山市闽安机械工程有限公司', '石狮国际轻纺城发展有限公司', '(二)破产费用', '北京微客联盟信息科技有限公司', '常州梦欣数控工具厂', '徐州玥家酒店有限公司', '德利泰(苏州)机械有限公司', '上海安悦节能技术有限公司', '徐州市出租汽车集团有限公司', '青岛汇堡酿造酒业有限公司', '苏州远辉铜铝销售有限公司', '衢州火宏国际汽车城商业管理有限公司', '佛山市呈现电器有限公司', '上海超川电子科技有限公司', '南京海瑞沣运动科技有限公司', '债权审查结果', '福建省石狮市和兴塑胶有限公司', '海勃湾康茂五金电料经销部', '南通通大科技小额贷款有限公司', '日照市水产集团总公司', '上海禾宇家具有限公司', '广东圣和电气工程有限公司', '苏州鸿业基精密组件有限公司', '武汉东方鸿建筑安装工程有限公司', '上海贺鑫包装材料有限公司', '上海翱束照明科技有限公司', '昆山市玉山镇车翔副食品批发部', '嵊州市万宁电器有限公司', '徐州开元名都大酒店有限公司', '郑州真金耐火材料有限责任公司', '陕西秦东圣建设工程有限公司', '重庆西骏建筑工程有限公司', '湖南额艾塞斯餐饮管理有限公司', '扬州鑫联运输有限公司', '江苏扬州信用融资担保有限公司', '张家港市誉之景建材有限公司', '湖北松建建设集团有限公司', '瑞乘(上海)生物科技有限公司', '望江县雷阳建筑安装有限责任公司', '四川鹏鹞环保设备有限公司', '饶辉跃(原债权人陈小玲)', '武汉市戴氏粉业装饰材料有限公司', '江苏华旸电器有限公司', '太仓市泓隆化纤有限公司', '山东金铂力数控机床制造有限公司', '上海勋聚丝印器材有限公司', '无锡风尚园林绿化有限公司', '上海沐焱金属材料有限公司', '华光源海国际物流(苏州)有限公司', '江苏伟森家居有限公司', '苏州梓豪食品有限公司', '广州市景成陶瓷原料有限公司', '吴中区甪直威迪亚五金商行', '苏州欧一汽车科技有限公司', '许昌中联心传科技有限公司', '四川雅化实业集团运输有限公司', '攀枝花市国有投资(集团)有限责任公司', '法律顾问费用', '石狮市万隆贸易有限公司', '杭州御智汽车科技有限公司', '南通晟泓机电设备有限公司', '苏州雪雅尔丝绸服饰工贸有限公司', '昆山市米斯特润滑油有限公司', '佛山市旺恒机械设备有限公司', '苏州双越精密钣金有限公司', '衡水诚坤建设工程有限公司', '南京旅游集团有限责任公司', '贵州筑美贸易有限公司', '岳阳市云溪区雄胜商行', '苏州工业园区恒昌纺织有限公司', '常熟市禾野精密电子工业有限公司', '莱茵技术(上海)有限公司', '苏州市中信轿车维修有限公司', '中铁国新贵州建工集团有限公司', '昆山吉庆丰模架有限公司', '巴中日报智点传媒有限责任公司', '江苏中南建筑科技发展有限公司', '高唐县金盾保安服务有限公司', '南通鸿升达贸易有限公司', '广州新原网络科技有限公司', '太仓市浏河镇龙威酒业营业部', '上海高和美贸易有限公司', '鹤城区通达电动车车行', '江山市瓦伦亚楼梯商行', '高唐县合信新型建材厂', '宁波金融资产管理股份有限公司', '上海连成(集团)有限公司', '一汽财务有限公司', '贵州本元利科技有限公司', '昆山市恒安工业气体有限公司', '珠海市依澄星宸房地产咨询服务有限公司', '重庆成欧机械有限公司', '泉州市博凯生物技术有限公司', '扬州市罗艺涂装机械制造有', '常熟启航企业管理咨询有限公司', '宁波翔速供应链管理有限公司', '宿迁市佳鑫新型建筑材料有限公司', '苏州金美狐建筑装饰有限公司', '苏州越城建筑设计有限公司', '吴江市黎里镇小柴线切割加工场', '温州同安鞋材有限公司', '晋江纬宸日用品贸易有限公司', '济南百士岩土工程有限公司华东分公司', '中山市港口镇群乐股份合作经济联合社', '浙江联轩展示道具有限公司', '江西盐通科技有限公司', '信州区俊辉五金经营部', '湖南湘景工程有限公司', '铜陵市信用融资担保集团有限公司', '谢远华刘小华', '中山市祥鸿环保工程有限公司', '龙岩市兴翰土石方工程有限公司', '江苏智科交通工程咨询监理有限公司', '杭州新草科技有限公司', '北京雅格液压机电有限公司', '辉腾商业保理(上海)有限公司', '上海泉尔泵阀制造有限公司', '昆山开发区吾爱粮芯机面店', '嵊州市豪峰电容电器厂', '太原市杏花岭区康利源食品销售中心', '泉州福贸贸易有限公司', '益阳高新产业发展投资集团有限公司', '徐州华东纺织浆料有限公司', '京马电机有限公司', '肇庆市成达自动化技术有限公司', '国药控股青岛有限公司', '佛山市誉朗纸品有限公司', '扬州飞宏达物资有限公司', '河北中博汇筑建筑工程有限公司', '苏州工业园区黄兴轩建材经营部', '苏州市茂林纸业有限公司', '深圳市德夏生物医学工程有限公司', '佛山市锦桂模具有限公司', '敬运镀锡板(苏州)有限公司', '宁波宣德德邦供应链管理有限公司', '嵊州市科力电器有限公司', '张家港保税区噢牌化工品有限公司', '广州大都市国际旅行社有限公司艺洲分公司', '衢州市柯城澄香酒业商行', '吴江区黎里镇乐盛精密模具经营部', '上海浦秋粘合剂有限公司', '昆山琨要华餐饮服务有限公司', '昆山市玉山镇唯胜凯电气设备维修部', '昆山福特莱纸业有限公司上海分公司', '重庆丽海国际货运代理有限公司', '扬州市东方热处理有限公司', '武汉艺达鑫工艺装饰有限公司', '铜陵瑞通小额贷款股份有限公司', '张家港韩枫木业有限公司', '广东四季福燃气具有限公司', '苏州维宏准精工科技有限公司', '岳阳泳鸿体育健身有限公司', '成都合达联行物业服务有限公司巴中分公司', '佛山市南海宝力包装材料有限公司', '德阳杰创科技有限公司', '佛山市顺德区炜彦五金制品厂', '江苏盛高建材有限公司', '江苏兴顺消防门业有限公司', '国药控股青岛大药房连锁有限公司', '重庆中天工程造价咨询有限公司', '陈知书(陈袁)', '岳阳德鑫物业管理有限公司', '嵊州市金诚不锈钢有限公司', '沭阳县加志服饰整理厂', '上海盛学建材有限公司', '崇川区金福铁艺材料经营部', '重庆建兴智能仪表有限责任公司', '扬州康进船业有限公司', '张家港黄金灯饰照明有限公司', '深圳市恒浩建工程项目管理有限公司', '厦门太古可口可乐饮料有限公司', '佛山市南海区西樵宏润塑料厂', '江西元邦科技协同创新体有限公司', '武汉市鑫龙城建筑工程质量检测有限公司', '苏州宝龙房地产发展有限公司', '昆山市花桥镇文轩建筑装饰材料经营部', '东莞市铭升网络科技有限公司', '佛山市南海区鹏塑五金塑料科技有限公司', '中山瑞浩电器有限公司', '乌海市盛翔商贸有限公司', '南京创利达精密机械有限公司', '福建省和东新型建材有限公司', '济南弘骏房地产开发有限公司(关联方往来款)', '太仓市盛达电泳有限公司', '嵊州市金丰木业有限公司', '江苏常瑞汽车集团有限公司苏州分公司(宋素华)', '上海汽车工业活动中心有限公司', '衡水泰飞建材贸易有限公司', '安徽慈湖建设集团有限公司', '重庆骏升汽车摩托车配件有限公司', '贵州奥克新科技有限责任公司', '天津大港新泉海水淡化有限公司', '北京中弘弘烨房地产开发有限公司(关联方往来款)', '广东宝的电器有限公司', '张家港市后塍高登建材店', '武定永丰钛业有限责任公司', '中山市卓森电器有限公司', '东莞市天安数码城有限公司', '江苏双建新型建材科技有限公司', '国家税务总局广州市从化区税务局太平税务所', '上海双利建筑装饰有限公司', '益阳市佳印图文广告有限公司', '苏州宝德莱机械设备有限公司', '江苏金航电器科技有限公司', '重庆市南岸区医疗保障事务中心', '佛山市禅城区达盈陶瓷机械经营部', '苏州鑫地园林景观设计有限公司', '丹阳市天工惠农农村小额贷款有限公司', '新都区比澳王建材经营部', '中国石油集团渤海石油装备制造有限公司', '杭州中科极光科技有限公司', '浙江精谷电器有限公司', '南通昕典石业有限公司', '扬中市融资担保有限公司', '上海颐阳广告有限公司', '常山县中小企业融资担保有限公司', '苏州晨睿环保科技服务有限公司', '巴州区巨人广告传媒中心', '海安永明金属材料有限公司', '广州房友圈网络科技有限公司', '长城宏业酒店有限公司', '常州市添琦椅业有限公司', '宁波市易锻精密机械有限公司', '昆山银桥控股集团有限公司', '苏州冠洲模具科技有限公司', '海门市启荣家具厂', '王寒青(原中山市东区橙果艺术中心已注销)', '苏州八六一精密五金有限公司', '河北兴奥建筑安装工程有限公司', '河北金祥锦住宅产业科技有限公司', '国家税务总局苏州市吴中区税务', '黄冈市品味人生商贸有限公司', '晋江鹏展展示道具有限公司', '上海南杉化工有限公司', '苏州秉诚工程造价咨询有限公司', '中华人民共和国中山海关', '贵州建工第八建设集团有限公司幕墙装饰分公司', '江苏城置物业服务有限公司绿地世纪城分公司', '南京凡利模具材料有限公司', '绍兴总杰电器有限公司', '苏州耐尔金属制品有限公司', '中山兴中集团有限公司', '江苏亿邦融资担保有限公司', '洛宁县宏达木业有限公司', '上海宗扬实业有限公司', '吴江峰云装卸有限公司', '苏州福康源物业管理有限公司', '浙江迪辰环保科技有限公司', '梧州市元盛新材料有限公司', '扬州丰源博能电气有限公司', '安吉时新家具厂', '苏州铭诺机电设备有限公司', '江苏顺丰速运有限公司', '昆山市保时杰机械有限公司', '北京中亚泰恒投资有限公司', '阜城县恒发商砼有限公司', '广州广通五金机电有限公司', '浙江悠游商旅服务有限公司', '乌海市凯达门业有限责任公司', '福州君立视讯知识产权代理有限公司', '浙江省磐安县天普橡塑厂', '品恒丝印器材(上海)有限公司', '武定县六纪商贸有限公司', '浙江嵊州澳利亚电机有限公司', '金斯达建设有限公司', '中国音像著作权集体管理协会', '宜兴瑞峰新型材料有限公司', '贵阳神石钙业有限公司', '佛山市禅城区摩根港泰耐火材料经营部', '厦门象屿资产管理运营有限公司', '九易庄宸科技(集团)股份有限公司天津分公司', '昆山旺之辉物资有限公司', '苏州安美润滑科技有限公司', '苏州高新区君发敏建材经营部', '苏州捷航五金机电设备有限公司', '砀山县辉宏木业有限公司', '福州海峡水果批发市场精品水果商行', '佛山市南海区旺洋服装厂', '莆田市茂林快递有限公司', '海门耀协贸易有限公司', '上海明宏船舶电器厂(普通合伙)', '唐山正海机械设备制造有限公司', '东莞市畅科电机有限公司', '泰州市新纪元农资有限公司', '胜利油田奥凯龙石油工程有限公司', '常熟市支塘镇任阳稻香水磨米粉厂', '中山市东博装饰设计工程有限公司', '菏泽盛强建材有限公司', '无锡市鑫星塑料片材有限公司', '深圳天俊实业股份有限公司', '徐州澳都物业管理有限公司', '广东智爱硕品牌运营有限公司', '安徽健康源医药有限公司', '东莞康力讯电子科技有限公司', '监利县勇戈地产营销代理有限公司', '嘉兴市引能润滑油有限公司', '重庆市酷麒派对娱乐有限公司', '嵊州市电容器厂', '益阳市朝阳盛辉管道疏通服务有限公司', '扬州市英成科技小额贷款有限公司', '昆山金特金属材料有限公司', '南通通塑塑料制品有限公司', '宁波天娇木业有限公司', '佛山陶原素材料科技有限公司', '福建闽盈投资有限公司', '中建二局第二建筑工程有限公司', '张家港市民哥防水工程有限公司', '浙江泓影文化传播有限公司', '嘉兴市海利达物资有限公司', '广州大禹防漏技术开发有限公司', '浙江欧飞新材料集团有限公司', '重庆开元融创焊接技术有限公司', '东莞迅达电子有限公司', '深圳市金色木棉锦汇壹号投资企业(有限合伙)', '苏州大成实业集团有限公司', '惠科股份有限公司', '东台启程精密电子技术有限公司', '上海梦菲建筑材料有限公司', '张家港李记建材贸易有限公司', '徐州高新区安全科技产业投资发展有限公司', '江苏翔天自动化设备有限公司', '张家港市杨舍镇塘市宇凯建材经营部', '苏州盛家厍商业管理有限公司', '常熟市明瑞针纺织有限公司', '南通冠龙工程设备有限公司', '四川鸿进达卫生技术服务有限公司', '镇江文化旅游产业集团有限责任公司', '上海颢明包装材料有限公司', '衡水普尚商贸有限公司', '深圳医药保健品进出口有限公司', '无锡市玉净净化科技有限公司', '衡水林达电力工程有限公司', '浙江帅牧电器有限公司', '乐山市惠灵科技有限公司', '贵阳大宏汽车运输有限公司', '无锡市天隆筛网有限公司', '江苏常瑞汽车集团有限公司镇江分公司(解士鹏)', '佛山市釉艺坊陶瓷原料有限公司', '泉州市德元食品有限公司', '福州秀屹农业发展有限公司', '兴化市华东铸钢有限公司', '上海鲸山精密工具有限公司', '东莞市合将实业有限公司', '衡水义德配电开关设备有限公司', '成都市郫都区洪宇恺信商业管理服务有限公司', '昆山市玉山镇鑫味森商行', '福建工友机械有限公司', '泊头市泊鲁石油配件厂', '中山市恒纳包装制品有限公司', '南通王府物业发展有限责任公司', '徐州亿博实业发展有限公司', '合肥爱旅航空服务有限公司', '南通宁泰消防设备有限公司', '安庆市富中小额贷款有限责任公司', '昆山市张浦镇华洋电脑设计室', '洛阳矿山机械工程设计研究院有限责任公司', '连云港市方舟实业有限公司', '广东鸿扬实业科技有限公司', '苏州天翊诚塑胶科技有限公司', '徐州观音国际机场有限责任公司', '龙岩市景棋混凝土有限公司', '阜城信泰房地产经纪有限公司', '浙江中凌进出口有限公司', '嵊州乐众电器有限公司', '瓜州竞发农业科技有限公司', '苏州木风机电工程有限公司', '岳阳市华胜装饰设计工程有限公司', '泉州斯魁尔贸易有限公司', '江苏春华秋实网络科技有限公司', '南通苏通人防防护设备有限公司', '太仓宝华物业管理有限公司', '武汉市浩然基础工程有限责任公司', '衡水民德空调设备销售有限公司', '苏州辰牧纺织有限公司', '衡水淑芳建筑工程有限公司', '乐山市中区城区洪有灯饰经营部', '宁德市医疗保障基金中心柘荣管理部', '温州锦鹿电子商务有限公司', '相城区黄埭镇东桥王小妹建材经营部', '苏州山鹰健康器材有限公司', '太仆寺旗大众机电有限责任公司', '江苏创大电气有限公司', '阜城县荣达建筑工程有限公司', '苏州珩璟精密机械有限公司', '重庆运玺物资有限公司', '吴江市吴越农村小额贷款股份有限公司', '河北碧云天环保设备有限公司', '北京六合伟业科技股份有限公司', '安吉孝源储炯海绵经营部', '广东众友创业投资有限公司', '东风汽车财务有限公司', '苏州飘志华复合材料科技有限公司', '张家港红宇建材有限公司', '昆山开发区谢佳福五金商行', '陕西长石电子材料股份有限公司']
# info_len = len(cache_li)
# print(info_len)
# batch_size = 20000
# for i in range(0, len(cache_li), batch_size):
#     start = i
#     end = min(i + batch_size, len(cache_li))
#     batch_data = cache_li[start:end]
#     db_redis_task.lpush("zgzx_300", *batch_data)
#     print(batch_data)深圳
#
