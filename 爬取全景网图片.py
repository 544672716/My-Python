# -- coding: utf-8 --
import urllib.request
import re
import time
import os
import datetime
import requests
import socket
from urllib.parse import urlencode


def headers():
    print('*****************************************************')
    print('********* 该程序会下载你指定主题的高清图片  *********')
    print('********* 图片网址：http://www.quanjing.com *********')
    print('********* 制作时间：2018年3月18日           *********')
    print('********* 作    者：Jaydon                  *********')
    print('*****************************************************')
    print()


def schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('进度：' + '%.2f%%' % per)


def get_one_url(keyword, page):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    }
    paras = {
        'key': keyword,
        'pageSize': '200',
        'pageNum': page,
        'imageType': '2',
        'sortType': '1',
        #'imageSType': 'v',
        'callback': 'searchresult',
    }
    url = 'http://search.quanjing.com/search?' + urlencode(paras)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def downloadimg(img):
    x = y = z = 1
    pat1 = 'http://quanjing-photo.oss.aliyuncs.com/[a-z0-9/]+.jpg'
    imagelist = re.compile(pat1).findall(img)

    for imageurl in imagelist:
        imagename = os.path.join(absfilepath, str(i) + str(x) + '.jpg')
        print()
        print('正在下载第', i, '页第', x, '张图片', '保存路径为:', absfilepath)
        try:
            start = datetime.datetime.now()
            socket.setdefaulttimeout(10)
            urllib.request.urlretrieve(imageurl, filename=imagename, reporthook=schedule)
            end = datetime.datetime.now()
            a = (end - start).total_seconds()
            print('一共用时' + str(a) + '秒')

        except socket.timeout:
            count = 1
            while count <= 5:
                try:
                    print('你这破网速不行啊！重新下载第', i, '页第', x, '张图片')
                    urllib.request.urlretrieve(imageurl, filename=imagename, reporthook=schedule)
                    break

                except socket.timeout:
                    err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                    print(err_info)
                    count += 1

                except urllib.error.URLError as e:
                    if hasattr(e, 'code'):
                        print('code出现' + str(y) + '次问题')
                        print(e, "code")
                        x += 1
                        y += 1
                    if hasattr(e, 'reason'):
                        print('reason出现' + str(z) + '次问题')
                        print(e, 'reason')
                        x += 1
                        z += 1
                    time.sleep(5)

                except Exception as e:
                    print('exception:' + str(e))
                    time.sleep(5)
        x += 1


def filepath(keyword):
    global absfilepath
    filepath = os.makedirs(os.path.abspath('.') + "\\" + keyword)
    absfilepath = os.path.abspath(str(keyword))
    return absfilepath


def checkfile(keyword):
    while os.path.isdir(keyword):
        print()
        print("该主题文件夹已经存在！路径为:" + os.path.abspath(keyword))
        print()
        print('程序将在10秒之后关闭!!!!')
        time.sleep(10)
        return exit()


if __name__ == '__main__':
    headers()
    keyword = input('请输入你想要下载的主题：')
    checkfile(keyword)
    page = input('请输入一共要下载的页数：')
    filepath(keyword)

    for i in range(1, int(page) + 1):
        img = get_one_url(keyword, i)
        downloadimg(img)
    print()
    print('数据下载完成!按任意键退出!')
    input()

