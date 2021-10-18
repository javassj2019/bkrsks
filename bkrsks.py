import json
import time
from PIL import Image
from pytesseract import *
from selenium import webdriver
import requests
import re
import collections
import pymysql
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

code = 'utf8'
###正文开始
##网站访问的基本信息
http = 'http://'
https = 'https://'
host = 'm.bk.lxsk.com'
loginurl = '/WebAppLogin/Index'
userinfo = '/UserInfo/Index'
desktop = '/MobileDesktop/Index'
saveurl = '/WebAppUser_Subject_Relation/SaveStudyRecord'

###网站访问的基本header

header1 = collections.OrderedDict()
header1['Host'] = host
header1['Connection'] = 'keep-alive'
header1['Cache-Control'] = 'max-age=0'
header1['Origin'] = https + host
header1['Upgrade-Insecure-Requests'] = '1'
header1[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header1['Content-Type'] = 'application/x-www-form-urlencoded'
header1['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
header1['Referer'] = https + host + loginurl
header1['Accept-Encoding'] = 'gzip, deflate'
header1['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'
header1['Cookie'] = 'ASP.NET_SessionId=dskyxykydaqfboxcxzhzsm4r'
# 连接数据库并获取账户密码信息
conn = pymysql.connect(host='cdb-kce5k8kq.bj.tencentcdb.com', user='root', passwd='a159753A!', port=10264,
                       charset='utf8', db='rsks')
cur = conn.cursor(pymysql.cursors.DictCursor)  # 生成游标
def huoqushijuanbianhao ():
    #一、模拟登录
    base_url = 'https://bk.lxsk.com/'
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.implicitly_wait(10)
    oldhandle = browser.current_window_handle
    browser.get(base_url)
    # (1)登录页面截图
    browser.save_screenshot("D:/pic.png")  # 可以修改保存地址
    # (2)基操
    browser.find_element(by='id', value='ctl00_txtUserName').send_keys(username)
    browser.find_element(by='id', value='ctl00_txtPassWord').send_keys(passwd)
    time.sleep(2)
    # (3)获取图片验证码坐标+
    xpathstr = '/html/body/form/div[5]/table/tbody/tr/td[6]/table/tbody/tr/td[2]/img'
    code_ele = browser.find_element(by='xpath', value=xpathstr)
    print("验证码的坐标为：", code_ele.location)  # 控制台查看{'x': 1086, 'y': 368}
    print("验证码的大小为：", code_ele.size)  # 图片大小{'height': 40, 'width': 110}
    # (4)图片4个点的坐标位置
    left = code_ele.location['x']  # x点的坐标
    top = code_ele.location['y']  # y点的坐标
    right = code_ele.size['width'] + left  # 上面右边点的坐标
    height = code_ele.size['height'] + top  # 下面右边点的坐标
    PIC = Image.open('D:/pic.png')
    # (4)将图片验证码截取
    code_image = PIC.crop((left, top, right, height))
    code_image.save('D:/pic1.png')  # 截取的验证码图片保存为新的文件
    time.sleep(3)
    im = Image.open('D:/pic1.png')
    # 图片的处理过程
    im = im.convert('RGBA')
    pixdata = im.load()
    # 非字符区域刷白
    for y in range(24):
        for x in range(0, 7, 1):
            pixdata[x, y] = (0, 0, 0, 0)
    for y in range(24):
        for x in range(14, 16, 1):
            pixdata[x, y] = (0, 0, 0, 0)
    for y in range(24):
        for x in range(24, 25, 1):
            pixdata[x, y] = (0, 0, 0, 0)
    for y in range(24):
        for x in range(33, 34, 1):
            pixdata[x, y] = (0, 0, 0, 0)
    for y in range(24):
        for x in range(42, 48, 1):
            pixdata[x, y] = (0, 0, 0, 0)
    for y in range(0, 5, 1):
        for x in range(48):
            pixdata[x, y] = (0, 0, 0, 0)
    for y in range(18, 24, 1):
        for x in range(48):
            pixdata[x, y] = (0, 0, 0, 0)
    for y in range(24):
        for x in range(48):
            if pixdata[x, y][0] > 120:
                if pixdata[x, y][1] > 150:
                    pixdata[x, y] = (0, 0, 0, 0)

    im.save('D:/pic2.png', 'PNG')
    # im.show()
    aa = pytesseract.image_to_string(im, config='outputbase digits')
    checkcode = (aa.strip())
    print(checkcode)
    browser.find_element(by='id', value='ctl00_txtCheckCode').send_keys(checkcode)
    loginbtn = browser.find_element(by='id', value='ctl00_BtnLogin')
    loginbtn.click()
    time.sleep(3)
    alertcode = browser.switch_to.alert.text
    r = '验证码'
    err = re.findall(r, alertcode)
    print(err)
    if err:
        print('验证码错了，重来')
        browser.switch_to.alert.accept()
        browser.close()
        time.sleep(3)
        kaoshi()
        return
    else:
        print('验证码对了，继续')
    browser.switch_to.alert.accept()
    #点击到考试页面
    exambtn = browser.find_element(by='xpath',value='//*[@id="top-nav"]/li[4]/a')
    exambtn.click()
    time.sleep(3)
    browser.switch_to.alert.accept()
    browser.find_element(by='xpath',value='//*[@id="ctl00_ContentPlaceHolder1_dg"]/tbody/tr[2]/td[9]/a').click()
    time.sleep(2)
    allhandle = browser.window_handles
    for handle in allhandle:
        if handle != oldhandle:
            newhandle = handle
    browser.switch_to.window(newhandle)
    time.sleep(1)
    browser.find_element(by='xpath',value='//*[@id="BtnClickLogin"]').click()
    time.sleep(2)
    # urlstring = browser.current_url
    # r = 'ApplyDetailID=(.*)&SubjectId'
    # sjid = re.findall(r,urlstring)
    browser.close()
    return

# # 录入新用户
def Typeuserid():
    print('请输入用户名：')
    userAccount = input()
    print('请输入密码：')
    userPassword = input()
    # 用户查重
    checkuid = cur.execute('select UserID from User where UserID = (%s)', (userAccount))
    #print(checkuid)
    if (checkuid == 0):
        cur.execute('insert into User(UserID,UserPassword,Study) VALUES (%s,%s,%s)', (userAccount, userPassword, 0))
        conn.commit()
        print('用户添加完成')
    else:
        print('用户已存在，无需再次添加')
# 考试答案与提交
def kaoshi ():
    #使用模拟方法登录并获取试卷编号
    huoqushijuanbianhao()
    # 获取考试必要信息
    tt = requests.get(https + host + '/WebAppUser_Subject_Relation/ExamIndex', headers=header2, verify=False)
    r = 'id="hid_KeyId" value="(.*)"/>'
    Keyid = re.findall(r, tt.text)
    apiurl = 'bkpxkswebapi.lxsk.com'
    tokenurl = '/api/token'
    tokendata = 'grant_type=password&username=' + username + '&password=' + userpasswd
    tt = requests.post(http + apiurl + tokenurl, data=tokendata)
    dd = json.loads(tt.text)
    access_token = dd['access_token']
    examurl = '/api/User_Subject_Relation/GetExamList?PageIndex=1&PageSize=100&User_ID=' + userid
    headertoken = {}
    headertoken['Authorization'] = 'bearer ' + access_token
    tt = requests.get(http + apiurl + examurl, headers=headertoken)
    print(tt.request.headers)
    print(tt.text)
    dd = json.loads(tt.text)
    Subject_ID = dd['rows'][0]['cell'][1]
    PaperID = dd['rows'][0]['cell'][3]
    NumberNO = dd['rows'][0]['cell'][4]
    qsjurl = '/api/Examing/PrepareTest?vSubjectId=' + Subject_ID + '&vNumberNO=' + NumberNO + '&vPaperID=' + PaperID + '&vUser_ID=' + userid
    # qsjurl ='/User_Subject/EntryExamRoom.aspx?PaperID=' + PaperID + '&NumberNO=' + NumberNO + '&SubjectId=' + Subject_ID + '&KeyId=' + Keyid[0]
    tt = requests.post(http + apiurl + tokenurl, data=tokendata)
    dd = json.loads(tt.text)
    access_token = dd['access_token']
    headertoken['Authorization'] = 'bearer ' + access_token
    tt = requests.get(http + apiurl + qsjurl, headers=headertoken)

    r = '"(.*)"'
    sjid = re.findall(r, tt.text)[0]

    sjurl = '/api/PaperData/GetPaperData?_ApplyDetailID=' + sjid
    tt = requests.get(http + apiurl + sjurl, headers=headertoken)
    date = tt.text
    dd = json.loads(date)
    for i in range(20):
        UUIDS = dd['Rubric_S_Info'][i]['ID']
        TITLES = dd['Rubric_S_Info'][i]['RubricTitle']
        ANSWERS = dd['Rubric_S_Info'][i]['OptionAnswer'].split('#', -1)
        TYPES = dd['Rubric_S_Info'][i]['RubricType']
        point = cur.execute('select uuid from bk where uuid =' + UUIDS)  # 查询UUID
        if point == 0:
            if len(ANSWERS) < 4:
                cur.execute("insert into bk(uuid,timu,A,B,C,type) VALUES (%s,%s,%s,%s,%s,%s)",(UUIDS, TITLES, ANSWERS[0], ANSWERS[1], ANSWERS[2], TYPES))
            else:
                cur.execute("insert into bk(uuid,timu,A,B,C,D,type) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (UUIDS, TITLES, ANSWERS[0], ANSWERS[1], ANSWERS[2], ANSWERS[3], TYPES))
            print('有一道单选题不存在，试题编号为' + UUIDS)
    for i in range(10):
        UUIDD = dd['Rubric_D_Info'][i]['ID']
        TITLED = dd['Rubric_D_Info'][i]['RubricTitle']
        ANSWERD = dd['Rubric_D_Info'][i]['OptionAnswer'].split('#', -1)
        TYPED = dd['Rubric_D_Info'][i]['RubricType']
        point = cur.execute('select uuid from bk where uuid =' + UUIDD)  # 查询UUID
        # print(UUIDD, TITLED, ANSWERD[0], ANSWERD[1], ANSWERD[2], ANSWERD[3], TYPED)
        if point == 0:
            if len(ANSWERD) < 4:
                cur.execute("insert into bk(uuid,timu,A,B,C,type) VALUES (%s,%s,%s,%s,%s,%s)",
                            (UUIDD, TITLED, ANSWERD[0], ANSWERD[1], ANSWERD[2], TYPED))
            else:
                cur.execute("insert into bk(uuid,timu,A,B,C,D,type) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                            (UUIDD, TITLED, ANSWERD[0], ANSWERD[1], ANSWERD[2], ANSWERD[3], TYPED))
            print('有一道多选题不存在，试题编号为' + UUIDD)
    for i in range(20):
        UUIDB = dd['Rubric_B_Info'][i]['ID']
        TITLEB = dd['Rubric_B_Info'][i]['RubricTitle']
        ANSWERB = dd['Rubric_B_Info'][i]['OptionAnswer'].split('#', -1)
        TYPEB = dd['Rubric_B_Info'][i]['RubricType']
        point = cur.execute('select uuid from bk where uuid =' + UUIDB)  # 查询UUID
        if point == 0:
            cur.execute("insert into bk(uuid,timu,A,B,type) VALUES (%s,%s,%s,%s,%s)",
                        (UUIDB, TITLEB, ANSWERB[0], ANSWERB[1], TYPEB))
            print('有一道判断题不存在，试题编号为' + UUIDB)
    conn.commit()

    begintesturl = '/api/Examing/BeginTest?vApplyDetailID=' + sjid
    tt = requests.get(http + apiurl + begintesturl, headers=headertoken)
    print('开始考试卷'+ tt.text )
    tt = requests.post(http + apiurl + tokenurl, data=tokendata)
    print('得到秘钥' + tt.text)
    kk = json.loads(tt.text)
    access_token = kk['access_token']
    headertoken['Authorization'] = 'bearer ' + access_token
    savepaperurl = '/api/CheckPaper/SavePaper'
    danalistS = []
    for i in range(20):
        TITLES = dd['Rubric_S_Info'][i]['RubricTitle']
        TITLES = pymysql.escape_string(TITLES)
        UUIDS = dd['Rubric_S_Info'][i]['ID']
        point = cur.execute('select uuid from rsks.bk where timu = ' + '"' + TITLES + '"' + 'and type = "A"')
        if point == 0:
            print('有一道单选题答案不存在，试题编号为' + UUIDS)
        else:
            cur.execute('select answer from rsks.bk where timu = ' + '"' + TITLES + '"' + 'and type = "A"')
            daan = cur.fetchone()
            danalistS.insert(i, daan['answer'][0])
            # print(danalistS)
    danalistD = []
    for i in range(10):
        TITLED = dd['Rubric_D_Info'][i]['RubricTitle']
        TITLED = pymysql.escape_string(TITLED)
        UUIDD = dd['Rubric_D_Info'][i]['ID']
        point = cur.execute('select uuid from rsks.bk where timu = ' + '"' + TITLED + '"' + 'and type = "B"')
        if point == 0:
            print('有一道多选题答案不存在，试题编号为' + UUIDD)
        else:
            cur.execute('select answer from rsks.bk where timu = ' + '"' + TITLED + '"' + 'and type = "B"')
            daan = cur.fetchone()
            danalistD.insert(i, daan['answer'])
            #print(UUIDD,type(daan),danalistD)
    danalistB = []
    for i in range(20):
        TITLEB = dd['Rubric_B_Info'][i]['RubricTitle']
        TITLEB = pymysql.escape_string(TITLEB)
        UUIDB = dd['Rubric_B_Info'][i]['ID']
        point = cur.execute('select uuid from rsks.bk where timu = ' + '"' + TITLEB + '"' + 'and type = "C"')
        if point == 0:
            print('有一道判断题答案不存在，试题编号为' + UUIDB)
        else:
            cur.execute('select answer from rsks.bk where timu = ' + '"' + TITLEB + '"' + 'and type = "C"')
            daan = cur.fetchone()
            danalistB.insert(i, daan['answer'][0])
            # print(danalistB)
    applyid = 'ApplyDetailID=' + sjid
    danxuan = '&RubricSWrite='
    duoxuan = '&RubricDWrite='
    panduan = '&RubricBWrite='
    for i in range(20):
        danxuan = danxuan + danalistS[i] + '%7C'
    for i in range(10):
        dx = danalistD[i]
        dx = dx.replace('#', '%23')
        duoxuan = duoxuan + dx + '%7C'
    for i in range(20):
        panduan = panduan + danalistB[i] + '%7C'
    header3 = {}
    header3['Host'] = apiurl
    header3['Connection'] = 'keep - alive'
    header3['Accept'] = '* / *'
    header3['Origin'] = https + host
    header3['User - Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    header3['DNT'] = '1'
    header3['Content - Type'] = 'application / x - www - form - urlencoded;charset = UTF - 8'
    header3['Accept - Encoding'] = 'gzip, deflate'
    header3['Accept - Language'] = 'zh - CN, zh;q = 0.9'

    tt = requests.post(http+apiurl+tokenurl,headers=header3 ,data = tokendata)
    kk = json.loads(tt.text)
    access_token = kk['access_token']
    headertoken['Authorization'] = 'bearer ' + access_token
    header4 = {}
    header4['Host'] = apiurl
    header4['Connection'] = 'keep - alive'
    header4['Access-Control-Request-Method'] = 'POST'
    header4['Accept'] = '* / *'
    header4['Origin'] = https + host
    header4['User - Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    header4['DNT'] = '1'
    header4['Accept - Encoding'] = 'gzip, deflate'
    header4['Accept - Language'] = 'zh - CN, zh;q = 0.9'
    header4['Access-Control-Request-Headers'] = 'authorization'
    requests.options(http + apiurl + savepaperurl,headers=header4)
    header5 = header4
    header5['Authorization'] = 'bearer ' + access_token
    header5['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
    tt = requests.post(http + apiurl + savepaperurl, headers=header5, data=applyid + danxuan + duoxuan + panduan)
    print(tt.text)
    #提交考试答案，提交即交卷
    finshurl = '/api/CheckPaper/FinishedTest?vApplyDetailID=' + sjid
    requests.options(http + apiurl + finshurl,headers=header4)
    tt = requests.get(http + apiurl + finshurl, headers=header5)
    fenshu = tt.text
    cur.execute('UPDATE User SET Exem = (%s) WHERE UserID = (%s)', (fenshu,username))
    cur.execute('UPDATE User SET Study = 2 WHERE UserID = (%s)', (username))
    conn.commit()
    print('考试结束，分数已录入',fenshu)
    return





print('需要添加新用户吗？Yes')
checktype = input()
if (checktype == 'Y'):
    i = 0
    while (i <= 100):
        Typeuserid()
        i = i + 1
s = 0
l = cur.execute('select UserID,UserPassword from User where Study = 0')
while (s < l):
    ###开始登陆过程
    print(s,l)
    k = cur.execute('select UserID,UserPassword from User where Study = 0')
    if l >= 1:
        cur.execute('select UserID,UserPassword from User where Study = 0')
        tt1 = cur.fetchone()
        username = tt1['UserID']
        passwd = tt1['UserPassword']
        logindata = 'UserName=' + username + '&Password=' + passwd + '&txtCheckCode=6455'
        print('开始访问')
        tt1 = requests.get(https + host + loginurl, headers=header1, verify=False)
        # print(tt1.text)
        tt2 = requests.post(https + host + loginurl, headers=header1, data=logindata, verify=False)
        # print(tt2.text)
        tt = requests.get(https + host + userinfo, headers=header1, verify=False)
        # print(tt.text)
        uid = '<input type="hidden" id="hid_User_ID"  value="(.*)"/>'
        upsw = '<input type="hidden" id="hid_Password" value="(.*)" />'
        userid = re.findall(uid, tt.text)[0]
        userpasswd = re.findall(upsw, tt.text)[0]
        tt = requests.get(https + host + desktop, headers=header1, verify=False)
        # print(tt.text)
        name = '<font color="yellow">(.*)</font>'
        hyname = re.findall(name, tt.text)[0]
        print(hyname)

        # ##开始学习过程(刷课时）
        header2 = collections.OrderedDict()
        header2['Host'] = host
        header2['Connection'] = 'keep-alive'
        header2['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        header2['Origin'] = https + host
        header2['X-Requested-With'] = 'XMLHttpRequest'
        header2[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat'
        header2['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        header2['Accept-Encoding'] = 'gzip, deflate'
        header2['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'
        header2['Cookie'] = 'ASP.NET_SessionId=dskyxykydaqfboxcxzhzsm4r'
        sid = 4029
        while (sid <= 4054):
            savedata = 'vUserInfo_ID=' + str(userid) + '&vRefParentId=' + str(
                sid) + '&vCurrentPos=5000&myCurrentsession_time=01:01:45&random=99.7548329067212136'
            tt = requests.post(https + host + saveurl, headers=header2, data=savedata, verify=False)
            print(tt.text)
            sid = sid + 1

        cur.execute('UPDATE User SET Name = (%s) WHERE UserID = (%s)', (hyname, username))
        cur.execute('UPDATE User SET Study = 0 WHERE UserID = (%s)', (username))
        conn.commit()
        kaoshi()
        l = k - 1
print('库存学习人数已清零，请核查分数为零的问题考号')

cur.close()
conn.close()


