from flask import Flask
from flask import request

import json
import re

from ali import AliAPI
from pod import DnsPodAPI
from db import GetTodoListByID, CheckLoginToken, AddDDnsHistory

app = Flask(__name__)
Alidns = AliAPI('<AccessKey ID>', '<AccessKey Secret>')
dnspod = DnsPodAPI('<ID>', '<Token>')


@app.route("/GetAli/")
def GetAli():
    return json.dumps(Alidns.GetRec("node.oldtaoge.space"))


@app.route("/GetPod/")
def GetPod():
    return json.dumps(dnspod.RecordList("oldtaoge.space"))


@app.route("/GetIpv4Addr/<str>/")
def GetIpv4Addr(str, num=1):
    pattern = re.compile(
        r'/\d{3}(\.\d{3}){3}/'
    )
    ip = []
    for ips in pattern.findall(str):
        print(ips)
        if num < 1:
            return json.dumps(ip)
        else:
            ip.append(ips[0])
            num -= 1
    return json.dumps(pattern.findall(str))


@app.route("/GetIpv6Addr/<str>/")
def GetIpv6Addr(str, num=1, firstBit=None):
    pattern = re.compile(
        r'\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*'
    )
    ip = []
    for ips in pattern.findall(str):
        if firstBit and firstBit == ips[0].split(":", 1)[0]:
            return ips[0]
        if not firstBit:
            if num < 1:
                return json.dumps(ip)
            else:
                ip.append(ips[0])
                num -= 1
    return json.dumps(pattern.findall(str))


@app.route("/ddns/Set", methods=['POST'])
def Set():
    try:
        LoginID = int(request.form["LoginID"])
        LoginToken = request.form["LoginToken"]
        From = request.form["From"]
        ipVersion = int(request.form["ipVersion"])
        if ipVersion == 4:
            ip4 = request.form["ip4"].replace(" ", "")
            if ip4 == '':
                return "请检查IPv4 addr"
        else:
            ip6 = request.form["ip6"].replace(" ", "")
            if ip6 == '':
                return "请检查IPv6 addr"
    except KeyError:
        return "请检查参数"
    except ValueError:
        return "请检查参数"
    sqlID = CheckLoginToken(LoginID, LoginToken, From)
    if not sqlID:
        return "鉴权失败"
    for todo in GetTodoListByID(LoginID, ipVersion):
        if todo["service"] == "ali":
            if ipVersion == 4:
                result = Alidns.GetRec(todo["domain"], "A", Alidns.LineToLine[todo["line"]])
                ip = ip4
            else:
                result = Alidns.GetRec(todo["domain"], "AAAA", Alidns.LineToLine[todo["line"]])
                ip = ip6
            for rec in result:
                if rec["RR"] == todo["sub_domain"]:
                    if rec["Value"] != ip:
                        print(rec["Value"], ip)
                        res = Alidns.UpdateRec(rec["RecordId"], rec["RR"], rec["Type"], ip, Alidns.LineToLine[todo["line"]])
                        # print(res)
                        AddDDnsHistory(LoginID, ip, ipVersion, res["info"], res["status"])
                    else:
                        AddDDnsHistory(LoginID, ip, ipVersion, "IP Addr Not Change", 0)
        if todo["service"] == "pod":
            if ipVersion == 4:
                result = dnspod.RecordList(todo["domain"], todo["sub_domain"], "A", dnspod.LineToLine[todo["line"]])
                ip = ip4
            else:
                result = dnspod.RecordList(todo["domain"], todo["sub_domain"], "AAAA", dnspod.LineToLine[todo["line"]])
                ip = ip6
            for rec in result:
                if rec["value"] != ip:
                    print(rec["value"], ip)
                    res = dnspod.UpdateRecord(todo["domain"], rec["id"], todo["sub_domain"],
                                              dnspod.LineToLine[todo["line"]], ip)
                    # print(res)
                    AddDDnsHistory(LoginID, ip, ipVersion, res["info"], res["status"])
                else:
                    AddDDnsHistory(LoginID, ip, ipVersion, "IP Addr Not Change", 0)
    return "Every Things Has Been Done"


if __name__ == '__main__':
    app.run("0.0.0.0")
