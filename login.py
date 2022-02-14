import time
import requests
import json
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

session = requests.session()
token = ""
uid = ""
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.110 Safari/537.36"
    }


def get_reqtimestamp():
    """
    此函数用于返回一个当前时间的毫秒级时间戳13位
    :return:当前时间的一个13位时间戳
    """
    t = time.time()  # 获取当前时间
    return int(round(t * 1000))


def timestamp2time(timestamp):
    """
    将时间戳转化为时间格式
    :param timestamp: 需要转化的时间戳
    :return: 转换后的时间格式
    """
    timeStamp = int(timestamp)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def login(url):
    """
    处理登录流程
    :param url:登录的url
    :return:
    """
    # 1.准备登录所需的账号，密码，时间戳等信息
    user_id = "18374652055"     # 账号
    password = "Gyz13874774169."    # 密码
    reqtimestamp = get_reqtimestamp()     # 通过当前时间生成13位的时间戳
    data = {
        "code": "",
        "email": user_id,
        "mobile": "",
        "password": password,
        "remember": "0",
        "reqtimestamp": reqtimestamp,
        "type": "login"
    }
    # 2.登录，打印登录信息
    global headers
    try:
        response = session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            print("登录成功！")
            global token
            token = response.json()['data']['token']
            global uid
            uid = response.json()['data']['uid']
            # 登录后的操作需在headers中加入token信息，因此在此处更新token
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/96.0.4664.110 Safari/537.36",
                "token": token
            }
            response.close()
    except:
        print("登录失败，请重试！")
        response.close()


def get_userinfo(url):
    """
    获取当前登录的用户的信息
    :param url: 获取用户信息所需的url
    :return: 返回json格式的登录用户信息
    """
    # 1.准备获取用户信息所需的data
    reqtimestamp = get_reqtimestamp()
    data = {
        "reqtimestamp": reqtimestamp
    }
    try:
        response = session.post(url, data=data, headers=headers)
        response.raise_for_status()  # 如果状态不是200，引发HTTRError异常
        user_info = json.dumps(response.json()['data'], ensure_ascii=False)
        response.close()
        return json.loads(user_info)
    except requests.HTTPError:
        return "产生HTTP错误异常"
    except requests.ConnectTimeout:
        return "连接远程服务器超时"
    except requests.ConnectionError:
        return "网络连接错误异常"
    except requests.URLRequired:
        return "URL缺失异常"
    except requests.TooManyRedirects:
        return "超过最大奖重定向次数"
    except requests.Timeout:
        return "请求URL超时"
    else:
        return "出现其他异常"


def get_semester_list(url):
    """
    获取当前账号的学年列表
    :param url: 获取学期列表的url
    :return: 返回json格式的学期信息
    """
    # 1.准备获取学期列表所需的信息
    reqtimestamp = get_reqtimestamp()
    data = {
        "isstudy": "1",
        "reqtimestamp": reqtimestamp,
        "search": ""
    }
    try:
        response = session.post(url, data=data, headers=headers)
        response.raise_for_status()  # 如果状态不是200，引发HTTRError异常
        semester_list = json.dumps(response.json()['data'], ensure_ascii=False)
        response.close()
        return json.loads(semester_list)['semester']
    except requests.HTTPError:
        return "产生HTTP错误异常"
    except requests.ConnectTimeout:
        return "连接远程服务器超时"
    except requests.ConnectionError:
        return "网络连接错误异常"
    except requests.URLRequired:
        return "URL缺失异常"
    except requests.TooManyRedirects:
        return "超过最大奖重定向次数"
    except requests.Timeout:
        return "请求URL超时"
    else:
        return "出现其他异常"


def get_semester_course_list(semester, term):
    """
    获取当前学期的课程列表
    :param semester: 学年
    :param term: 学期
    :return: 字典格式的当前学期课程列表
    """
    url = "https://openapiv5.ketangpai.com//CourseApi/semesterCourseList"
    # 1.准备data
    data = {
        "isstudy": "1",
        "reqtimestamp": get_reqtimestamp(),
        "search": "",
        "semester": semester,
        "term": term
    }
    try:
        response = session.post(url, data=data, headers=headers)
        response.raise_for_status()  # 如果状态不是200，引发HTTRError异常
        semester_course_list = json.dumps(response.json()['data'], ensure_ascii=False)
        response.close()
        return json.loads(semester_course_list)
    except requests.HTTPError:
        return "产生HTTP错误异常"
    except requests.ConnectTimeout:
        return "连接远程服务器超时"
    except requests.ConnectionError:
        return "网络连接错误异常"
    except requests.URLRequired:
        return "URL缺失异常"
    except requests.TooManyRedirects:
        return "超过最大奖重定向次数"
    except requests.Timeout:
        return "请求URL超时"
    else:
        return "出现其他异常"


def get_course_homework(id):
    """
    获取当前课程的作业列表
    :param id: 需要获取作业的课程的id
    :return: 列表格式的作业列表
    """
    homework_url = "https://openapiv52.ketangpai.com//FutureV2/CourseMeans/getCourseContent"
    data = {
        "contenttype": "4",
        "courseid": id,
        "courserole": "0",
        "desc": "3",
        "dirid": "0",
        "lessonlink": "[]",
        "limit": "100",
        "page": "1",
        "reqtimestamp": get_reqtimestamp(),
        "sort": "[]",
        "vtr_type": ""
    }
    try:
        response = session.post(homework_url, data=data, headers=headers)
        response.raise_for_status()  # 如果状态不是200，引发HTTRError异常
        homework_list = json.dumps(response.json()['data'], ensure_ascii=False)
        response.close()
        return json.loads(homework_list)['list']
    except requests.HTTPError:
        return "产生HTTP错误异常"
    except requests.ConnectTimeout:
        return "连接远程服务器超时"
    except requests.ConnectionError:
        return "网络连接错误异常"
    except requests.URLRequired:
        return "URL缺失异常"
    except requests.TooManyRedirects:
        return "超过最大奖重定向次数"
    except requests.Timeout:
        return "请求URL超时"
    else:
        return "出现其他异常"


def homework_list2webpage(coursename, homework_list, web):
    """
    将作业信息填入到网页
    :param coursename:作业所属课程的名字
    :param homework_list: 作业列表
    :param web: 浏览器对象
    :return:
    """
    for each in homework_list:
        web.find_element(By.XPATH, '//*[@id="TextBox_coursename"]').send_keys(coursename)
        web.find_element(By.XPATH, '//*[@id="TextBox_homeworktitle"]').send_keys(each['title'])
        web.find_element(By.XPATH, '//*[@id="TextBox_createtime"]').send_keys(timestamp2time(each['createtime']))
        web.find_element(By.XPATH, '//*[@id="TextBox_publishtime"]').send_keys(timestamp2time(each['publish_time']))
        web.find_element(By.XPATH, '//*[@id="TextBox_endtime"]').send_keys(timestamp2time(each['endtime']))
        time.sleep(3)
        web.find_element(By.XPATH, '//*[@id="Button_submit"]').click()
        alert = web.switch_to.alert
        time.sleep(1)
        alert.accept()


if __name__ == '__main__':
    # 1.登录
    login_url = "https://openapiv53.ketangpai.com//UserApi/login"
    login(login_url)
    # 2.获取用户信息
    userinfo_url = "https://openapiv5.ketangpai.com//UserApi/getUserBasinInfo"
    user_info = get_userinfo(userinfo_url)
    # 3.获取学年学期列表
    semester_list_url = "https://openapiv5.ketangpai.com/CourseApi/semesterList"
    semester_list = get_semester_list(semester_list_url)
    # 基于测试需求，此代码暂时封存
    # course_list = []
    # 4.使用selenium启动浏览器并打开目标网页
    web = Chrome()
    web.get("http://192.168.31.27:82/selenium")
    # 5.获取每个学年学期的课程
    for each in semester_list:
        semester = each['semester']
        term = each['term']
        semester_course_list = get_semester_course_list(semester, term)
        # course_list.append(semester_course_list)
        # print(course_list)
        # 6.获取每个课程的作业列表
        for each_course in semester_course_list:
            print(each_course)
            course_id = each_course['id']
            course_name = each_course['coursename']
            homework_list = get_course_homework(course_id)
            # 7.将作业填入到指定网页
            homework_list2webpage(course_name, homework_list, web)
    # semester = semester_list[1]['semester']
    # term = semester_list[1]['term']
    # test_course_list = get_semester_course_list(semester, term)
    # print(test_course_list[2])




