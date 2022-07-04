import pytest
import os, re
import json
import logging
import allure
import mysql.connector
import uuid
from CommonClass.FrameworkConstants import Constants
import command
import subprocess

############################# Allure config #######################################
class AllureLoggingHandler(logging.Handler):
    def log(self, message):
        with allure.step('Log {}'.format(message)):
            pass

    def emit(self, record):
        self.log("({}) {}".format(record.levelname, record.getMessage()))


class AllureCatchLogs:
    def __init__(self):
        self.rootlogger = logging.getLogger()
        self.allurehandler = AllureLoggingHandler()

    def __enter__(self):
        if self.allurehandler not in self.rootlogger.handlers:
            self.rootlogger.addHandler(self.allurehandler)

    def __exit__(self, exc_type, exc_value, traceback):
        self.rootlogger.removeHandler(self.allurehandler)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup():
    with AllureCatchLogs():
        yield

def pytest_configure(config):
    config._metadata = None

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call():
    with AllureCatchLogs():
        yield

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown():
    with AllureCatchLogs():
        yield


############################# custom fixtures ######################################

# get env name for test
@pytest.fixture(scope="class")
def readPayLoadJsonWithUUID(request):
    active_uuid = uuid.uuid4()
    filepath = os.getcwd() + "/" + str(request.param)
    with open(filepath, 'r') as js:
        base_jsondata = json.load(js)
    js.close()
    base_jsonStr = json.dumps(base_jsondata)
    jsonDataModify = Constants().patientParameters(str(active_uuid))
    for keys, value in jsonDataModify.items():
        if keys in base_jsonStr:
            base_jsonStr = base_jsonStr.replace("{{" + keys + "}}", value)
    jsonData = json.loads(base_jsonStr)

    file_name = os.getcwd() + "/Payload/JsonList/"+str(os.getenv('docspera_id'))+"/Docspera/InputPayLoadForDocspera_"+str(active_uuid)+".json"
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as jsonfile:
        json.dump(jsonData, jsonfile, sort_keys=False, indent=2, ensure_ascii=False)
    jsonfile.close()

    return jsonData


@pytest.fixture(scope="class")
def readPayLoadJson(request):
    filepath = os.getcwd() + "/" + str(request.param)
    with open(filepath, 'r') as js:
        jsondata = json.load(js)
    js.close()
    return jsondata


@pytest.fixture(scope="class")
def readPayLoadXml(request):
    filepath = os.getcwd() + "/" + str(request.param)
    xmldata = open(filepath, 'rb')

    return xmldata


@pytest.fixture(scope="class")
def readPayLoadTextFile(request):
    with open(os.getcwd() + "/" + str(request.param), 'r') as file:
        data = file.read().replace('\r', '')
    return data


@pytest.fixture(scope="class")
def readUploadFilePath(request):
    filepath = os.getcwd() + "/" + str(request.param)
    return filepath


@pytest.fixture(scope="class")
def apiTestData():
    # get env name
    env_name = "DEV" if os.getenv("EnvironmentName") is None else os.getenv("EnvironmentName").upper()
    # read json for access the env data
    path = os.getcwd()
    # filepath = os.path.join(path, "EnvDatas/TestData/", env_name + '_ApiTestData.json')
    #filepath =os.path.expanduser('./EnvDatas/TestData/'+env_name+'_ApiTestData.json')
    subprocess.run(["ls", "-l"])
    subprocess.run(["cd ~"])
    # with open(filepath,  'r') as js: Dry_Run_-_Automation_DAA/dsp_daa_fhir_layering/TestCases/apirequesttest/
    with open(r'/home/agentadmin/workspace/Test_Dry_Run_Automation_DAA/dsp_daa_fhir_layering/EnvDatas/TestData/DEV_ApiTestData.json') as js:
    #with open(os.getcwd() + '/EnvDatas/TestData/' + env_name + '_ApiTestData.json', 'r') as js:
        apiEndpointData = json.load(js)
    js.close()
    # return the dict for test data
    return apiEndpointData


@pytest.fixture(scope="class")
def readEnvDataFromDB():
    # get env name
    env_name = "Dev" if os.getenv("EnvironmentName") is None else os.getenv("EnvironmentName").title()
    # sqlquery = 'SELECT * FROM api_automation.post_openjobs_endpoints;'
    method_lst = ['get', 'post', 'put', 'delete', 'head', 'patch']
    # read json for access the env data
    with open(os.getcwd() + '/EnvDatas/Configuration/DbConfigData.json', 'r') as js:
        dbjsondata = json.load(js)
    js.close()
    # store the retrived data to variable
    endpoint_sqlquerylst = dbjsondata['SqlQuery']['Enpoint_Query']
    endpoint_baseurl_query = dbjsondata['SqlQuery']['BaseUrlQuery'][0].replace('$env', env_name)
    endpoint_headers_query = dbjsondata['SqlQuery']['HeadersQuery'][0]
    endpoint_auth_query = dbjsondata['SqlQuery']['AuthQuery'][0]
    password = os.getenv("dbUserPassword")
    # DB Connection
    db = mysql.connector.connect(host=dbjsondata['DbCredentials']['HostName'],
                                 user=dbjsondata['DbCredentials']['DbUsername'], passwd=password)
    cursor = db.cursor()
    # Final dict for env data
    finalendpointdict = {}
    for sqlquery in endpoint_sqlquerylst:
        sqlquery = sqlquery.replace('$env', env_name)
        ServiceName, MethodName = (re.split('[_,.]', sqlquery)[-2].title()), (re.split('[_,.]', sqlquery)[2].title())
        if MethodName.lower() in method_lst:
            MethodName = MethodName.title() + "MethodUrls"
        # fetch db data
        cursor.execute(sqlquery)
        columns = cursor.description
        # dict for store the db data
        finalendpointdict_temp1 = {}
        finalendpointdict_temp2 = {}
        client_secdict = {}
        for value in cursor.fetchall():
            tmp = {}
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            finalendpointdict_temp1[tmp['EndPointName']] = tmp
        finalendpointdict_temp2[ServiceName] = finalendpointdict_temp1
        finalendpointdict.setdefault(MethodName, [])
        finalendpointdict[MethodName].append(finalendpointdict_temp2)
    # base url dict
    BaseUrlDict = {}
    cursor.execute(endpoint_baseurl_query)
    for value in cursor.fetchall():
        BaseUrlDict[value[2]] = value[3]
    finalendpointdict["BaseUrl"] = BaseUrlDict
    # Herders read
    HeadersDict = {}
    cursor.execute(endpoint_headers_query)
    for value in cursor.fetchall():
        HeadersDict[value[1]] = value[2]
    finalendpointdict["Headers"] = HeadersDict
    # Client read
    ClientDict = {}
    cursor.execute(endpoint_auth_query)
    cli_columns = cursor.description
    for value in cursor.fetchall():
        cli_tmp = {}
        for (index, column) in enumerate(value):
            cli_tmp[cli_columns[index][0]] = column
        ClientDict[cli_tmp['Id']] = cli_tmp
    finalendpointdict["Credentials"] = ClientDict
    with open(os.getcwd() + '/EnvDatas/DEV_ApiTestData.json', 'w') as jsonfile:
        json.dump(finalendpointdict, jsonfile, sort_keys=True, indent=8, ensure_ascii=False)
    jsonfile.close()
    # return the dict for test data
    return finalendpointdict


@pytest.fixture(scope="class")
def configLogger():
    logger = logging.getLogger()
    allure_handler = AllureLoggingHandler()
    logger.setLevel(logging.INFO)
    allure_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    allure_handler.setFormatter(formatter)
    logger.addHandler(allure_handler)
    return logger
