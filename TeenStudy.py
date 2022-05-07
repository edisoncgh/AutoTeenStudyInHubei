import requests
import requests.utils
from urllib.parse import quote, unquote
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

# 用户识别码
# openid是一个长度为28个字符
# 由数字、大小写字母与符号组成的串
openid = ""

def show_exit(content):
    input(content)
    exit()

'''
获取课程识别码
:param info:
    s:Session
:return:
    课程识别码
'''
def get_code(s):
    url = "https://h5.cyol.com/special/weixin/sign.json"
    headers ={
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Origin": "http://h5.cyol.com",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    resp = s.get(url,headers=headers).json()
    return list(resp)[-1]

'''
获取用户信息
:param info:
    s:Session
:return:
    用户信息
'''
def get_user(s):
    headers = {
        "Host": "api.fjg360.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "*/*",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = "https://api.fjg360.cn/index.php?m=vote&c=index&a=get_members&openid="+ openid
    resp = s.get(url, headers=headers).json()
    if resp.get("code") == 1:
        return resp.get("h5_ask_member")
    else:
        show_exit("用户OPENID配置有误，请检查后重试")

'''
获取课程信息
:param info:
    s:Session
    code:团课识别码
:return:
    课程信息
'''
def get_course(s,code):
    headers = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = 'https://h5.cyol.com/special/daxuexi/'+ code +'/m.html'
    resp = s.get(url,headers=headers)
    soup = BeautifulSoup(resp.content.decode("utf8"),"lxml")
    course = soup.title.string[7:]
    return course

'''
提交用户进入页面信息至青春湖北数据库
:param info:
    info:用户信息
    course:课程信息
    s:Session
:return:
    保存情况
'''
def save_door(info, course, s):
    headers = {
        "Host": "cp.fjg360.cn",
        "Connection": "keep-alive",
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = "https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&sessionId=&imgTextId=&ip="
    url += "&username=" + info["name"]
    url += "&phone=" + "未知"
    url += "&city=" + info["danwei1"]
    url += "&danwei2=" + info["danwei3"]
    url += "&danwei=" + info["danwei2"]
    url += "&openid=" + openid
    url += "&num=10"
    url += "&lesson_name=" + course
    resp = s.get(url,headers=headers).json()
    if resp.get("code") == 1:
        return True
    else:
        show_exit("用户信息有误，请检查后重试")

'''
下载课程完成截图
:param info:
    code:课程识别码
:return:
    null
'''
def obtain_end_img(code):
    urlretrieve("https://h5.cyol.com/special/daxuexi/" + code + "/images/end.jpg", "C:\\Users\\Edisoncgh\\Desktop\\" + code + ".jpg")


def main():
    s = requests.session()
    code = get_code(s)
    user_info = get_user(s)
    course = get_course(s, code)
    save_door(user_info, course, s)
    obtain_end_img(code)


if __name__ == '__main__':
    main()
