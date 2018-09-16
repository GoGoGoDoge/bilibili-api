from GetAss import *
import hashlib
import os
import random
import time

def Top50FromTodo():
    urls = []
    with open('todo.list', 'r') as f:
        i = 0
        for url in f:
            urls.append(url.strip())
            i = i + 1
            if i > 50:
                break
    return urls

def GetHash(url):
    m = hashlib.md5()
    m.update(url)
    hashVal = m.hexdigest()
    return hashVal


def WriteToHashList(url):
    hashVal = GetHash(url)
    with open('done.hash', 'a') as f:
        f.write(hashVal)
        f.write('\n')

def CheckExist(doneUrls, url):
    hashVal = GetHash(url)
    return hashVal in doneUrls

def WriteToDoneList(url):
    with open('done.list', 'a') as f:
        f.write(url)
        f.write('\n')

def WriteToLowList(url):
    with open('low.list', 'a') as f:
        f.write(url)
        f.write('\n')

def RemoveTop50AndUpdateFromTodo():
    urls = []
    with open('todo.list', 'r') as f:
        i = 0
        for url in f:
            i = i + 1
            if i > 50:
                break
        for url in f:
            urls.append(url.strip())
    with open('todo.list', 'w') as f:
        for url in urls:
            f.write(url)
            f.write('\n')

def LoadHash():
    doneUrls = {}
    with open('done.hash', 'r') as f:
        for url in f:
            doneUrls[url.strip()] = True
    return doneUrls

def CreateAidDir(aid):
    path = os.path.join('jobs', str(aid))
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def CreateVideoInfoPath(aid, pid):
    path = CreateAidDir(aid)
    path = os.path.join(path, str(aid) + '-' + str(pid) + '.info')
    return path

def CreateDanmuPath(aid, pid):
    path = CreateAidDir(aid)
    path = os.path.join(path, str(aid) + '-' + str(pid) + '.raw')
    return path

def LetsRock():
    urls = Top50FromTodo()
    doneUrls = LoadHash()
    appkey = "03fc8eb101b091fb"
    for url in urls:
        print("searching:", url)
        if CheckExist(doneUrls, url):
            print("[INFO]", "Get info already:", url)
            continue

        aid, pid = ParseUrlInfo(url)
        if aid == "":
            continue

        video = GetVideoInfo(aid,appkey,AppSecret=None,page = pid)
        if video.danmu < 50:
            WriteToLowList(url)
        else:
            path = CreateVideoInfoPath(aid, pid)
            with open(path, 'w') as f:
                video.saveToFile(f)
            danmuPath = CreateDanmuPath(aid, pid)
            with open(danmuPath, 'w') as f:
                f.write(GetDanmuku(video.cid))
            WriteToHashList(url)
            WriteToDoneList(url)

    # RemoveTop50AndUpdateFromTodo()
def LetsRock2():
    urls = Top50FromTodo()
    doneUrls = LoadHash()
    appkey = "03fc8eb101b091fb"
    aid = 30122252
    pid = 1
    count = 0
    while count < 20000:
        count += 1
        if count % 3 == 0:
            time.sleep(random.randrange(1,5))
        aid = random.randrange(3012225, 30122252)
        url = 'https://www.bilibili.com/video/av%d/?p=1'%(aid)
        print(count, "searching:", url)
        if CheckExist(doneUrls, url):
            print("[INFO]", "Get info already:", url)
            continue

        aid, pid = ParseUrlInfo(url)
        if aid == "":
            continue

        video = GetVideoInfo(aid,appkey,AppSecret=None,page = pid)
        if video.danmu < 50:
            WriteToLowList(url)
        else:
            path = CreateVideoInfoPath(aid, pid)
            with open(path, 'w') as f:
                video.saveToFile(f)
            danmuPath = CreateDanmuPath(aid, pid)
            with open(danmuPath, 'w') as f:
                f.write(GetDanmuku(video.cid))
        WriteToHashList(url)
        WriteToDoneList(url)




def Example():
    url = sys.argv[1]
    aid, pid = ParseUrlInfo(url)
    appkey = "03fc8eb101b091fb"
    video = GetVideoInfo(aid,appkey,AppSecret=None,page = pid)
    with open('tmp.txt', 'w') as f:
        video.saveToFile(f)
    with open('danmu.raw', 'w') as f:
        f.write(GetDanmuku(video.cid))


if __name__ == '__main__':
    LetsRock2()
    # Example()
    # url = sys.argv[1]
    # aid, pid = ParseUrlInfo(url)
    # print(aid, pid)


