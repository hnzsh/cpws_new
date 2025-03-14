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

# redis连接
def get_cpws():
    REDIS_HOST_TASK = ''
    REDIS_PORT_TASK = 
    REDIS_PW_TASK = ''
    REDIS_DB_TASK = 0
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
    lis = [("手机号", "密码")]# 可多个
    count += 1
    choose = count % len(lis)
    logger.info('count: %s, choose: %s' % (count,choose))
    user_name = lis[choose][0]
    user_pwd = lis[choose][1]
    logger.info("使用账号：%s" % user_name)
    session = get_session(user_name, user_pwd)

