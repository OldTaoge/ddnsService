import json
from aliyunsdkcore.client import AcsClient, ServerException, ClientException
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest


class AliAPI:
    def __init__(self, accessKeyId, accessSecret):
        self.accessKeyId = accessKeyId
        self.accessSecret = accessSecret
        self.LineToLine = {
            "cm": "mobile",
            "cu": "unicom",
            "ct": "tetecom",
            "ss": "search",
            "oc": "oversea",
            "main": "default",
        }

    def GetRec(self, DomainName, Type=None, Line=None):
        """
        :param DomainName:(必选）域名名称。
        :param Type:（非必选）解析记录类型A、MX、CNAME、TXT、REDIRECT_URL、FORWORD_URL、NS、AAAA、SRV
        :param Line:（非必选）解析线路 defaul默认 telecom电信 unicom联通 mobile移动 oversea海外 search 搜索引擎
        :return: Dirt
        """
        # print(DomainName)
        # print(Type)
        # print(Line)
        client = AcsClient(self.accessKeyId, self.accessSecret, 'cn-hangzhou')

        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_PageNumber(1)
        request.set_PageSize(500)
        request.set_DomainName(DomainName)
        if Type:
            request.set_Type(Type)  # A、MX、CNAME、TXT、REDIRECT_URL、FORWORD_URL、NS、AAAA、SRV
        if Type:
            request.set_Line(Line)  # defaul默认 telecom电信 unicom联通 mobile移动 oversea海外 search 搜索引擎
        response = json.loads(client.do_action_with_exception(request))
        Records = response["DomainRecords"]["Record"]
        if response["TotalCount"] > response["PageSize"]:
            Getd = response["PageSize"]
            PageNumber = 1
            while Getd < response["TotalCount"]:
                PageNumber = PageNumber + 1
                request.set_PageNumber(PageNumber)
                response = json.loads(client.do_action_with_exception(request))
                Getd += response["PageSize"]
                for Record in response["DomainRecords"]["Record"]:
                    Records.append(Record)
        return Records

    def UpdateRec(self, RecID, RR, Type, Value, Line):
        """
        :param RecID:解析记录的ID
        :param RR:主机记录
        :param Type:解析记录的类型
        :param Value:记录值
        :param Line:解析线路
        :return:
        """
        client = AcsClient(self.accessKeyId, self.accessSecret, 'cn-hangzhou')
        request = UpdateDomainRecordRequest()
        request.set_RecordId(RecID)
        request.set_RR(RR)
        request.set_Type(Type)
        request.set_Value(Value)
        if Line:
            request.set_Line(Line)
        try:
            response = json.loads(client.do_action_with_exception(request))
        except ServerException as e:
            return {
                "info": str(e),
                "status": 1
            }
        except ClientException as e:
            return {
                "info": str(e),
                "status": 1
            }
        return {
            "info": response,
            "status": 0
        }


if __name__ == "__main__":
    Alidns = AliAPI('LTAI4GHFLEJ6WVbf2AejQoT8', 'CwEMs9QFLnWeMRACxDrb80gOilI0BI')
    print(Alidns.GetRec("node.oldtaoge.space"))
    # print(Alidns.UpdateRec(19679127112464384, 'cn-qd-dx', 'AAAA', '::3', 'default'))
    # print(Alidns.LineToLine["cm"])
