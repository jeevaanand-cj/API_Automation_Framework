import json
import os, sys

from CommonClass.CommonApiActions import writeResponseBodyInJson

current_path = os.path.abspath('.')
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)
from GetRequests.getdocsperaunbundling.GET_MakeEndpoint import makeEndpoint
from CommonClass.apirequests.RequestsLib import apiRequest, renameJsonDir
from CommonClass.apirequests.RequestsLib import stringValidations


def getPatientAndAppointment(apiTestData, endpointkey, configLogger, readPayLoadJson=None, env_instance=None,headers=None):
    logger = configLogger
    try:
        # get endpoint details
        endPoint, Token, ResponseCode, ResponseBodyVerification, ResponseBodyType = makeEndpoint(apiTestData["BaseUrl"].get("Get Valid Patient"), apiTestData, endpointkey, 'Valid Patient')
        # Get the endpoint
        endPointAfterReplacement = endPoint.replace('uuid',os.getenv('file_name')).replace('{', "").replace('}', "")
        logger.info("Given api endpoint is : " + endPointAfterReplacement)
        endPointAfterReplacement = endPointAfterReplacement + "?" + Token
        responseBodyDict, reponseBody, Headers = apiRequest("GET", endPointAfterReplacement, ResponseCode, configLogger,ResponseBodyVerification=ResponseBodyVerification, ResponseBodyType=ResponseBodyType)

        filename = os.getcwd() + "/Payload/JsonList/" + str(os.getenv('docspera_id')) + "/Docspera/AckFileFromDocspera_" + str(os.getenv('file_name')) + ".json"
        writeResponseBodyInJson(filename, jsonData=json.loads(reponseBody))

        logger.info('##################### Test details comparison with Acknowledgement Json #########################')
        if 'plain' != ResponseBodyType.lower():
            stringValidations('Transaction ID', responseBodyDict.get('transaction_id'), 'file_name', logger)
            stringValidations('Docspera ID', responseBodyDict.get('Docspera_ID'), 'docspera_id', logger)
            os.environ['DSEP PatientID'] = responseBodyDict.get('DSEP PatientID')[0]
            os.environ['OID'] = responseBodyDict.get('OID')[0]
            renameJsonDir()
            logger.info('##################### Docspera Input and Acknowledgement File Generated with the following details #########################')
            logger.info('Acknowledgement file generated with the transaction id of: '+ os.getenv('file_name') )
            logger.info('DSEP ID retrieved from ack message is : ' + os.getenv('DSEP PatientID'))
            logger.info('OID retrieved from ack message is : ' + os.getenv('OID'))
    except AssertionError as error:
        logger.error("Validation error in given api endpoint, exception is:" + str(error))
        assert False


def getPatientAndAppointmentDeltaChange(apiTestData, endpointkey, configLogger, readPayLoadJson=None, env_instance=None, headers=None):
    logger = configLogger
    try:
        # get endpoint details
        endPoint, Token, ResponseCode, ResponseBodyVerification, ResponseBodyType = makeEndpoint(apiTestData["BaseUrl"].get("Apigee Dev"), apiTestData, endpointkey, 'Apigee Dev')
        # Get the endpoint
        endPointAfterReplacement = endPoint.replace('OID', os.getenv('OID')).replace('epoch_time_from', os.getenv('epoch_time_from')).replace('{', "").replace('}', "")
        logger.info("Given api endpoint is : " + endPointAfterReplacement)
        api_headers = headers
        api_headers['Authorization'] = 'Bearer '+os.environ['jwt-token']

        responseBodyDict, reponseBody, Headers = apiRequest("GET", endPointAfterReplacement, ResponseCode, configLogger,ResponseBodyVerification=ResponseBodyVerification,ResponseBodyType=ResponseBodyType,readPayLoadJson=readPayLoadJson, headers=api_headers)

        logger.info('##################### Test details comparison with delta change response json #########################')
        if 'plain' != ResponseBodyType.lower():
            if int(responseBodyDict.get('resource_count')[0]) > 0:
                logger.info('Total resource count for this delta change is : '+responseBodyDict.get('resource_count')[0]+ ', epoch from '+responseBodyDict.get('epoch_from')[0]+' epoch to '+responseBodyDict.get('epoch_to')[0])
                stringValidations('Patient ID', responseBodyDict.get('id'), 'DSEP PatientID', logger, True)
                stringValidations('Appointment ID', responseBodyDict.get('id'), 'appointment_value', logger)
                stringValidations('Organization ID', responseBodyDict.get('org_id'), 'OID', logger)
                stringValidations('Epoch From', responseBodyDict.get('epoch_from'), 'epoch_time_from', logger)
                logger.info('##################### Delta change response and url response comparison #########################')
                for apiUrls in responseBodyDict.get('url'):
                    logger.info("Api endpoint retrieved from delta change response is : " + apiUrls)
                    apiUrls = apiUrls+"?"+apiTestData["Credentials"].get("docspera").get('sas_token_velys_dsep')
                    responseBodyDict, reponseBody, Headers =  apiRequest("GET", apiUrls, "[200]", configLogger, ResponseBodyType="Json", ResponseBodyVerification=['id','value', 'resourceType'])
                    # stringValidations(responseBodyDict.get('resourceType')[0] +" ID", responseBodyDict.get('id'), 'DSEP PatientID', logger, True)
                    # stringValidations(responseBodyDict.get('resourceType')[0] + " ID", responseBodyDict.get('id'),'appointment_value', logger, True)
                    filename = os.getcwd() + "/Payload/JsonList/DSEP_"+str(os.getenv('DSEP PatientID')) + "/Velys/"+responseBodyDict.get('resourceType')[0]+"_"+responseBodyDict.get('id')[0]+".json"
                    writeResponseBodyInJson(filename, jsonData=json.loads(reponseBody))
            else:
                logger.info('No resource is available in the response body, and the resource count is: '+responseBodyDict.get('resource_count')[0])
    except AssertionError as error:
        logger.error("Validation error in given api endpoint, exception is:" + str(error))
        assert False
