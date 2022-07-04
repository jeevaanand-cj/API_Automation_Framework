import os

from CommonClass.CommonApiActions import ApiActions


def makeEndpoint(baseUrl, apiTestData, endpointkey, serviceName):
    ApiActionsObj = ApiActions(apiTestData)
    # POST_CommonActions
    BaseUrl = baseUrl
    env_name = "DEV" if os.getenv("EnvironmentName") is None else os.getenv("EnvironmentName").upper()
    BaseUrl = ApiActionsObj.replace_all(env_name, BaseUrl)
    # Get the current dict
    currentDict = ApiActionsObj.listToDict(listVal=apiTestData, methodName='PutMethodUrls', serviceName=serviceName)
    endPointWithoutBaseUrl = currentDict.get(endpointkey).get("EndPoint")
    # Get the endpoint
    ResponseBodyType = currentDict.get(endpointkey).get("ResponseType")
    ResponseBodyVerification = currentDict.get(endpointkey).get("ResponseValidation")
    ResponseCode = currentDict.get(endpointkey).get("ResponseCode")
    Token = apiTestData["Credentials"].get("docspera").get('sas_token_adls')
    endPoint = BaseUrl + endPointWithoutBaseUrl

    return endPoint, Token, ResponseCode, ResponseBodyVerification, ResponseBodyType
