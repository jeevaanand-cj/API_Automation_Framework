import os, sys

from PutRequests.getdocsperaunbundling.PUT_MakeEndpoint import makeEndpoint

current_path = os.path.abspath('.')
parent_path = os.path.dirname(current_path)
sys.path.append(parent_path)

from CommonClass.apirequests.RequestsLib import apiRequest


def putPatientAndAppointment(apiTestData, endpointkey, configLogger, readPayLoadJson=None, headers=None, env_instance=None):
    logger = configLogger
    try:
        logger.info('################# EHR_NEW PATIENT AND APPOINTMENT ######################')
        # get endpoint details
        endPoint, Token, ResponseCode, ResponseBodyVerification, ResponseBodyType = makeEndpoint(apiTestData["BaseUrl"].get("Put Valid Patient"), apiTestData, endpointkey, 'Valid Patient')
        # Get the endpoint
        endPointAfterReplacement = endPoint.replace('uuid', os.getenv('file_name')).replace('{', "").replace('}', "")
        logger.info("Given api endpoint is : " + endPointAfterReplacement)
        endPointAfterReplacement = endPointAfterReplacement + "?" + Token
        logger.info('################# Sample Data used for test ######################')
        logger.info('Transaction ID : '+os.getenv('file_name'))
        logger.info('Docspera ID : ' + os.getenv('docspera_id'))
        logger.info('Patient MRN : ' + os.getenv('mrn_number'))
        apiRequest("PUT", endPointAfterReplacement, ResponseCode, configLogger, readPayLoadJson, headers, ResponseBodyType=ResponseBodyType)

    except AssertionError as error:
        logger.error("Validation error in given api endpoint, exception is:" + str(error))
        assert False
