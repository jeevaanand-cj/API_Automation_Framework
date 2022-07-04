import json
import logging
import os
from builtins import list
from collections import OrderedDict
import xmltodict


# from CommonClass.AuthToken import Tokengeneration

# Tokengeneration = Tokengeneration()


def find_values(jsonKey, jsonStr):
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(str(a_dict[jsonKey]))
        except KeyError:
            pass
        return a_dict

    json.loads(jsonStr, object_hook=_decode_dict)  # Return value ignored.
    return results

def writeResponseBodyInJson(file_name, jsonData):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as jsonfile:
        json.dump(jsonData, jsonfile, sort_keys=False, indent=2, ensure_ascii=False)
    jsonfile.close()

class ApiActions:

    def __init__(self, readEnvData):
        self.readEnvData = readEnvData

    def readJsonToDict(self, jsonfilename):
        try:
            with open(os.getcwd() + '/EnvDatas/Configuration/' + jsonfilename + '.json', 'r') as js:
                configData = json.load(js)
            js.close()
            return configData
        except Exception as e:
            print("Json path/file is invalid !!!")

    def replace_all(self, envname, text):
        dic = self.readJsonToDict("TestDataConfig").get(envname + "_EndPointParams")
        dic = OrderedDict(dic)
        for i, j in dic.items():
            text = text.replace(i, j).replace('{', "").replace('}', "")
        return text

    def getCurrentUrl(self, ServicenameBaseUrl, MethodName, Servicename, Endpointname):
        try:
            url = self.readEnvData["BaseUrl"][0].get(ServicenameBaseUrl) + self.readEnvData[MethodName][0].get(
                Servicename).get(Endpointname)
            return url
        except Exception as e:
            print("Unable to get endpoint url: " + str(e))
            return None

    def endPointParameters(self, url):
        try:
            endpoint_parameter_data = self.readEnvData["EndPointParameters"]
            url = url.replace("{", "").replace("}", "")
            url = '/'.join([endpoint_parameter_data.get(i, i) for i in url.split("/")])
            return url
        except Exception as e:
            print("Unable to read endpoint parameters: " + str(e))
            return None

    # def authTokenGeneration(self, logger):
    #     try:
    #         cred = self.readEnvData["Credentials"][0]
    #         Auth_token = Tokengeneration.getCurrentSessionToken(
    #             cred.get("TokenUrl"),
    #             cred.get("ClientID"),
    #             cred.get("ClientPass"),
    #             cred.get("Auth_audience"),
    #             logger=logger
    #         )
    #         return Auth_token
    #     except Exception as e:
    #         print("Unable get auth token: " + str(e))
    #         return None

    def endpointHeaders(self, OrgId, Auth_token):
        try:
            headerdict = self.readEnvData["Headers"][0]
            headers = {
                "x-organizationid": headerdict.get(OrgId),
                "Authorization": Auth_token
            }
            return headers
        except Exception as e:
            print("Unable get endpoint headers: " + str(e))
            return None

    def readPayLoadJson(self, jsonFileName):
        filepath = os.getcwd() + "/" + str(jsonFileName)
        with open(filepath, 'r') as js:
            jsondata = json.load(js)
        js.close()
        return jsondata

    def getSlotJsonForCreateAppointment(self, CreateAppointmentJson, AppointmentSlotJson):
        start = AppointmentSlotJson["entry"][0]["resource"]["start"]
        end = AppointmentSlotJson["entry"][0]["resource"]["end"]
        dict = {
            "start": start,
            "end": end
        }
        for key, val in CreateAppointmentJson.items():
            for sec_key, sec_val in dict.items():
                if key == sec_key:
                    replacedval = {key: sec_val}
                    CreateAppointmentJson.update(replacedval)
        return CreateAppointmentJson

    def xmlToJson(self, xmldata):
        data_dict = xmltodict.parse(xmldata)
        json_data = json.dumps(data_dict, indent=4)
        json_data = json.loads(json_data)
        return json_data

    def find_key_value_pairs(self, q, keys, dicts=None):
        dictFromList = {}
        if not dicts:
            dicts = [q]
            q = [q]
        data = q.pop(0)
        if isinstance(data, dict):
            data = data.values()
        for d in data:
            dtype = type(d)
            if dtype is dict or dtype is list:
                q.append(d)
                if dtype is dict:
                    dicts.append(d)
        if q:
            return self.find_key_value_pairs(q, keys, dicts)

        return [(k, v) for d in dicts for k, v in d.items() if k in keys]

    def responseBodyVerification(self, jsonverify, verifyval, logger):
        passdict = {}
        for key, val in jsonverify.items():
            for tupval in verifyval:
                if tupval[0] == key:
                    # String type verification
                    if isinstance(tupval[1], str):
                        try:
                            if str(val.lower()) == str(tupval[1].lower()):
                                # pass# print(val)
                                passdict[key] = val
                        except:
                            pass
                    # boolean type verification
                    if isinstance(tupval[1], bool):
                        try:
                            if bool(val.title()) == tupval[1]:
                                # pass# print(val)
                                passdict[key] = val
                        except:
                            pass
                    # List type verification
                    if isinstance(tupval[1], list):
                        for lstval in tupval[1]:
                            if isinstance(lstval, int):
                                # print(str(val) +" " +str(lstval))
                                try:
                                    if int(val) == int(lstval):
                                        passdict[key] = val
                                        # print("lst"+val)
                                except:
                                    pass
                            if isinstance(lstval, str):
                                try:
                                    if str(val.lower()) == str(lstval.lower()):
                                        passdict[key] = val
                                        # print("lst"+val)
                                except:
                                    pass
                            if isinstance(lstval, bool):
                                try:
                                    if bool(val.title()) == lstval:
                                        passdict[key] = val
                                except:
                                    pass
                    # Dict type verification
                    if isinstance(tupval[1], dict):
                        for key1, val1 in tupval[1].items():

                            if isinstance(val1, str):
                                try:
                                    if str(val.lower()) == str(val1.lower()):
                                        passdict[key] = val
                                except:
                                    pass
                            if isinstance(val1, bool):
                                try:
                                    if bool(val.title()) == val1:
                                        passdict[key] = val
                                except:
                                    pass
                            if isinstance(val1, list):
                                for lstval in val1:
                                    if isinstance(lstval, int):
                                        try:
                                            if int(val) == int(lstval):
                                                passdict[key] = val
                                        except:
                                            pass
                                    if isinstance(lstval, str):
                                        try:
                                            if str(val.lower()) == str(lstval.lower()):
                                                passdict[key] = val
                                                # print("lst"+val)
                                        except:
                                            pass
                                    if isinstance(lstval, bool):
                                        try:
                                            if bool(val.title()) == lstval:
                                                passdict[key] = val
                                        except:
                                            pass
        return passdict

    def responseBodyVerificationList(self, list_response, list_verify, contains=None):
        if contains:
            count = 0
            for listString1 in list_response:
                for listString2 in list_verify:
                    if listString2 in listString1:
                        count += 1
            if count > 0:
                return True, list_verify
            else:
                return False, None
        check = all(item in list_response for item in list_verify)
        if check is True:
            return True, list_verify
        else:
            return False, None

    def responseBodyHtmlValidation(self, data, listdata):
        passlist = []
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(data, "html.parser")
        for lisval in listdata:
            val = soup.find(text=lisval)
            if val is not None:
                passlist.append(val)
                passlist.append(soup.find(text=lisval).findParent())
            else:
                passlist.append(val)
        if None in passlist:
            return False, None
        else:
            return True, passlist

    def listToDict(self, listVal, methodName, serviceName):

        for dictVal in listVal[methodName]:
            try:
                return dictVal[serviceName]
            except:
                pass

    def get_all(self, myjson, key):
        # key = key.get()
        if type(myjson) == str:
            myjson = json.loads(myjson)
        if type(myjson) is dict:
            for jsonkey in myjson:
                if type(myjson[jsonkey]) in (list, dict):
                    self.get_all(myjson[jsonkey], key)
                elif jsonkey == key:
                    logger = logging.getLogger()
                    logger.setLevel(logging.INFO)
                    logger.info(myjson[jsonkey])
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    self.get_all(item, key)

    def verifyJsonKeyValues(self, jsonDict, vDict):
        verification = True
        # logging.info(jsonStr)
        json_repr = json.dumps(jsonDict)
        for key, value in vDict.items():
            if not ApiActions.find_values(self, key, value, json_repr):
                verification = False
        return verification
# lst = ['transaction_id']#, 'status', 'DSEP PatientID', 'Docspera_ID', 'OID']
# for i in range(len(lst)):
#     print(find_values(lst[i],'{"transaction_id": "f92655e1-5a35-4275-95a5-047c2bd48c60","Docspera_ID": "28553","status": 200,"acknowledgement": {"DSEP PatientID": "69fe7f44-7a32-468d-b865-a7a32b7523ff","OID": "2.16.840.1.119358475923.1","Docspera_ID": "28552"}}'))
