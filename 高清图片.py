# -- coding: utf-8 --
import urllib.request
import re
import time
import os
import datetime
import requests
import socket


def schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('进度：' + '%.2f%%' % per)


def getjpg(url, page):
    #headers = ("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    headers = {
        'Host':'pixabay.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    }

    html1 =requests.get(url,headers)
    time.sleep(3)
    html1 = html1.text
    pat1 = ' https://cdn.pixabay.com/photo/.*?\_480.jpg '
    result1 = re.compile(pat1).findall(str(html1))
    pat2 = 'https://cdn.pixabay.com/photo/.*?__480.jpg'
    imagelist = re.compile(pat2).findall(str(result1))

    x = y = z = 1
    for imageurl in imagelist:
        if len(imageurl) < 100:
            imagename = os.path.join(absfilepath, str(page)+str(x)+'.jpg')
            print()
            print('正在下载第', page, '页，第', x, '张图片', '保存路径为:', absfilepath)
            try:
                start = datetime.datetime.now()
                socket.setdefaulttimeout(10)
                urllib.request.urlretrieve(imageurl, filename=imagename, reporthook=schedule)
                end = datetime.datetime.now()
                a = (end - start).total_seconds()
                print('一共用时'+str(a)+'秒')

            except socket.timeout:
                count = 1
                while count <= 5:
                    try:
                        print('你这破网速不行啊！重新下载第', page, '页，第', x, '张图片')
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


def headers():
    print('****************************************************')
    print('********* 该程序会下载你指定主题的高清图片 *********')
    print('********* 图片网址：https://pixabay.com    *********')
    print('********* 制作时间：2018年3月18日          *********')
    print('********* 作    者：Jaydon                 *********')
    print('****************************************************')
    print()


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
    page1 = input('请输入一共要下载的页数：')
    filepath(keyword)
    
    for i in range(1, int(page1)+1):
        key = urllib.request.quote(keyword)
        url = "https://pixabay.com/zh/photos/?min_height=&image_type=photo&cat=&q=" + key + "&min_width=&order=&pagi=" + str(i)
        getjpg(url, i)
    print()
    print('数据下载完成')
    headers()
