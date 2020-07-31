import pymysql
import json
import time
Host = 
User = 
Password = 
Database = 


def dbQueryByBits(bit1=None, bit2=None, bit3=None, bits=None):
    """

    :param bits: 按.分割的bits串
    :param bit1: 望文生义
    :param bit2: 望文生义
    :param bit3: 望文生义
    :return: 元组(ID，LoginToken）
    """
    db = pymysql.connect(Host, User, Password, Database)
    cursor = db.cursor()
    if bits:
        try:
            cursor.execute("SELECT `id`, `LoginToken` FROM `ipRec` WHERE `bit1`=%d AND `bit2`=%d AND `bit3`=%d" %
                           (int(bits.split(".")[0]), int(bits.split(".")[1]), int(bits.split(".")[2])))
        except ValueError:
            return False
        except KeyError:
            return False
        except IndexError:
            return False
    else:
        try:
            cursor.execute("SELECT `id`, `LoginToken` FROM `ipRec` WHERE `bit1`=%d AND `bit2`=%d AND `bit3`=%d" %
                           (int(bit1), int(bit2), int(bit3)))
        except ValueError:
            return False
        except KeyError:
            return False
        except IndexError:
            return False

    data = cursor.fetchone()
    return data


def CheckLoginToken(LoginID, LoginToken, From):
    result = dbQueryByBits(bits=From)
    # print(result[0], result[1], LoginID, LoginToken)
    if result is None:
        return False
    if result is False:
        return False
    if LoginID != result[0] or LoginToken != result[1]:
        return False
    return result[0]


def GetTodoListByID(id, ipVersion):
    try:
        int(id)
        int(ipVersion)
    except ValueError:
        return False
    db = pymysql.connect(Host, User, Password, Database)
    cursor = db.cursor()
    cursor.execute("SELECT `v%dtodo` FROM `ddnsTodo` WHERE `id`=%d" % (ipVersion, id))
    return json.loads(cursor.fetchone()[0])


def AddDDnsHistory(LoginID, ip, ipVersion, ServiceReturn, Status):
    db = pymysql.connect(Host, User, Password, Database)
    cursor = db.cursor()
    sql = "INSERT INTO `History`(`CliId`, `ip`, `ipVersion`, `ServicerReturn`, `Time`, `Status`) VALUES (%s,' %s', %s,\"%s\",'%s', '%s')" % (LoginID, ip, ipVersion, ServiceReturn, (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), Status)
    cursor.execute(sql)
    db.commit()


if __name__ == "__main__":
    # print(dbQueryByBits(bits="0.0.0"))
    print(GetTodoListByID(1, 6))