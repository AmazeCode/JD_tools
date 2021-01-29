import jdCookie
import json
import requests
import time


"""
1、此脚本用于东东农场 【好友】邀请助力 添加好友
2、效果:新加好友时为对方增加10g水;对方执行此脚本同理
3、此助力独立于助力得水，目前助力上限未知
4、欢迎补充一个足够多的shareCodes列表,只能是非好友关系,才能为对方助力
5、cron 0 */3 * * *
"""
shareCodes = [
              "99efa1431bb54cd8a34aaa90717fa1d8", # Smile
              "e0f290656b634dbeab0a0da0747c8140", # Dong
              "76abf74ddbf5434ab107cd968e3a77f0", # Dong2
              "5ac72c51bec24628bdd88d514cd3df58", # 当小黑遇到小白
              "ab11c483a1c542c285fb95c4fe65b640", # 李幸福
              "60ce5d7215ed45a9a0fa763e67804a33", # 李源儿
              "fdc2685a72e54834886a1ac76d8fe407"  # 李幸福2
              ]  # 欢迎在此处填写

def postTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'JD4iPhone/167249 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', functionId),
    )
    data = {
        'body': json.dumps(body),
        "appid": "wh5",
        "clientVersion": "9.1.0"
    }
    response = requests.post(
        'https://api.m.jd.com/client.action', headers=headers, cookies=cookies, data=data, params=params)
    return response.json()


def help(cookies):
    print("\n")
    data = postTemplate(cookies, "friendListInitForFarm",
                        {})

    print("他人运行此脚本为我助力")
    print(f"""今日新增好友: {data["inviteFriendCount"]}/10""")
    if data["inviteFriendCount"] > 0 and data["inviteFriendCount"] > data["inviteFriendGotAwardCount"]:
        print("领取邀请奖励")
        print(postTemplate(cookies, "awardInviteFriendForFarm", {}))
    print("\n>>>开始为他人助力")
    myFriendCode = [i["shareCode"]
                    for i in data["friends"] if "shareCode" in i]
    countOfFriend = data["countOfFriend"]
    _friendsList = [i for i in data["friends"]]
    if not _friendsList:
        print("好友列表为空  跳出")
        print(data)
        return
    lastId = _friendsList[-1]["id"]
    print(f"""fullFriend:{data["fullFriend"]}""")  # 好友添加总数有上限
    if data["fullFriend"]:
        print("好友达到上限,退出")
        return
    for i in range(countOfFriend//20):
        result = postTemplate(cookies, "friendListInitForFarm",
                              {"lastId": lastId})
        pageFriend = [i["shareCode"] for i in result["friends"]]
        if not result["friends"]:
            break

        lastId = [i for i in result["friends"]][-1]["id"]
        myFriendCode += pageFriend
    myshareCode = postTemplate(cookies, 'initForFarm', {})[
        "farmUserPro"]["shareCode"]

    shareCodes_diff = list(
        set(shareCodes).difference([myshareCode]))  # 去掉自己shareCode 若要去掉自己和好友的使用后边写法 (myFriendCode, [myshareCode])
    print("准备助力的shareCodes:", shareCodes_diff)
    if not shareCodes_diff:
        print("脚本中的shareCodes暂时没发现新好友,退出助力")
    for i in shareCodes_diff:
        data = postTemplate(cookies, "initForFarm", {
            "shareCode": f"{i}-inviteFriend"})
        helpResult = data["helpResult"]
        print(helpResult)  # 目前code未知
        """-1 为自己   17 已经是好友   0 新增好友   猜测有每日上限"""
        if helpResult["code"] == "0":
            print(f"""成功添加好友 [{helpResult["masterUserInfo"]["nickName"]}]""")
        time.sleep(0.5)

def run():
    for cookies in jdCookie.get_cookies():
        print("######################################")
        print(f"""【 {cookies["pt_pin"]} 】""")
        help(cookies)
        print("\n\n######################################")

if __name__ == "__main__":
    run()
