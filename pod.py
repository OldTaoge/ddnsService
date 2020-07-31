import requests
import json


class DnsPodAPI:
    """
    -1 登陆失败
    -2 API使用超出限制
    -3 不是合法代理 (仅用于代理接口)
    -4 不在代理名下 (仅用于代理接口)
    -7 无权使用此接口
    -8 登录失败次数过多，帐号被暂时封禁
    85 帐号异地登录，请求被拒绝
    -99 此功能暂停开放，请稍候重试
    1 操作成功
    2 只允许POST方法
    3 未知错误
    6 用户ID错误 (仅用于代理接口)
    7 用户不在您名下 (仅用于代理接口)
    83 该帐户已经被锁定，无法进行任何操作
    85 该帐户开启了登录区域保护，当前IP不在允许的区域内
    """

    def __init__(self, ID, Token):
        self.apiID = ID
        self.Token = Token
        self.PublicData = {
            'login_token': str(self.apiID) + ',' + str(self.Token),
            'format': 'json'
        }
        self.UA = 'OldTaogeRequest/Alpha0.0.1 (admin@oldtaoge.space)'
        self.LineToLine = {
            "cm": "移动",
            "cu": "联通",
            "ct": "电信",
            "ss": "搜索引擎",
            "oc": "境外",
            "main": "默认",
        }
        if not self.UserDetail():
            return

    def ResToJson(self, res):
        resJson = json.loads(res.text)
        if resJson["status"]['code'] == '1':
            return resJson
        else:
            print(resJson, "来自pod.DnsPodAPI.ResToJson")
            return resJson

    def UserDetail(self):
        res = requests.post('https://dnsapi.cn/User.Detail', self.PublicData,
                            headers={'User-Agent': self.UA})
        return self.ResToJson(res)

    def GetDomainList(self):
        res = requests.post('https://dnsapi.cn/Domain.List', self.PublicData,
                            headers={'User-Agent': self.UA})
        return self.ResToJson(res)

    def RecordList(self, domain, sub_domain=None, record_type=None, record_line=None):
        FormData = self.PublicData
        FormData['domain'] = domain
        FormData["offset"] = 0
        Getd = 100

        if sub_domain:
            FormData["sub_domain"] = sub_domain
        if record_type:
            FormData["record_type"] = record_type
        if record_line:
            FormData["record_line"] = record_line

        res = requests.post('https://dnsapi.cn/Record.List', FormData,
                            headers={'User-Agent': self.UA})
        res = self.ResToJson(res)
        Record = res["records"]
        if int(res["info"]["record_total"]) > 100:
            while Getd < int(res["info"]["record_total"]):
                FormData["offset"] += 100
                FormData["length"] = 100
                res = requests.post('https://dnsapi.cn/Record.List', FormData,
                                    headers={'User-Agent': self.UA})
                res = self.ResToJson(res)
                Getd += res["info"]["records_num"]
                for record in res["records"]:
                    Record.append(record)
        return Record

    def UpdateRecord(self, Domain, recordId, subDomain, recordLine, value):
        FormData = self.PublicData
        FormData['domain'] = Domain
        FormData['record_id'] = recordId
        FormData['sub_domain'] = subDomain
        FormData['record_line'] = recordLine
        FormData['value'] = value
        res = requests.post("https://dnsapi.cn/Record.Modify", FormData,
                            headers={'User-Agent': self.UA})
        res = self.ResToJson(res)
        if int(res["status"]["code"]) == 1:
            status = 0
        else:
            status = 1
        return {
            "info": res,
            "status": status
        }
