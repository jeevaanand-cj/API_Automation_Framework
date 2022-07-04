import json
import os
import time

import requests
from CommonClass.CommonApiActions import find_values
from CommonClass.RequestValidations import Validations


def apiRequest(requestType, endPoint, ResponseCode, logger, readPayLoadJson=None, headers=None,ResponseBodyVerification=None, ResponseBodyType=None, env_instance=None):
    ValidationsObj = Validations(logger)
    count = 0
    try:
        while True:
            if readPayLoadJson is None:
                readPayLoadJson = {}
                headers = {}
            if 'PUT' == requestType.upper():
                response = requests.put(endPoint, data=json.dumps(readPayLoadJson), headers=headers)
            if 'GET' == requestType.upper():
                response = requests.get(endPoint, data=json.dumps(readPayLoadJson), headers=headers)
            if 'POST' == requestType.upper():
                response = requests.post(endPoint, data=json.dumps(readPayLoadJson), headers=headers)
            if 'DELETE' == requestType.upper():
                response = requests.delete(endPoint, data=json.dumps(readPayLoadJson), headers=headers)
            statusCodeValidation = ValidationsObj.statusCodeValidation(ResponseCode, response.status_code)
            # status code - verification
            if statusCodeValidation:
                logger.info("Current api endpoint response code is:  " + str(response.status_code))
                break
            if count >= 36:
                break
            else:
                time.sleep(5)
                count += 1

        if not statusCodeValidation:
            logger.error('Expected response code [' + str(
                ResponseCode) + '] not matched with the actual response code [' + str(
                response.status_code) + ']')
            raise AssertionError
        else:
            if ResponseBodyType is not None or ResponseBodyType.lower() != 'plain':
                if 'json' == ResponseBodyType.lower():
                    responseBody = jsonValidation(response, ResponseBodyVerification, logger)
                    logger.info('Response validation values from given api response: ' + str(responseBody))
                    return responseBody, response.text, response.headers
            else:
                return None

    except requests.exceptions.RequestException as e:
        logger.info(e)


def jsonValidation(response, ResponseBodyVerification, logger):
    responseText = response.text
    DataFromAckJson = {}
    try:
        for i in range(len(ResponseBodyVerification)):
            DataFromAckJson[ResponseBodyVerification[i]] = []
            DataFromAckJson[ResponseBodyVerification[i]] = find_values(ResponseBodyVerification[i], responseText)
        return DataFromAckJson
    except Exception as e:
        logger.info(e)
        return None


def renameJsonDir():
    try:
        # make ack json file
        source = os.getcwd() + "/Payload/JsonList/" + str(os.getenv('docspera_id'))
        des = os.getcwd() + "/Payload/JsonList/DSEP_" + str(os.getenv('DSEP PatientID'))
        os.rename(source, des)
    except FileNotFoundError as e:
        print(e)


def stringValidations(keyName, listValue, envValue, logger, contains=None):
    for stringValue in listValue:
        if contains is True:
            if os.getenv(envValue) in stringValue:
                logger.info(keyName + ' is present in the response body with the value of: ' + stringValue)

        if os.getenv(envValue) == stringValue:
            logger.info(keyName + ' is present in the response body with the value of: ' + stringValue)
        else:
            continue
