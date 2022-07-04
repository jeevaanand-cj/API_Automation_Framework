# pre-def library import
import ast
import os
import time
import allure
# custom-def library import
import pytest
from CommonClass.AuthToken import getCurrentSessionToken
from PutRequests.getdocsperaunbundling.PUT_CommonActions import putPatientAndAppointment
from GetRequests.getdocsperaunbundling.GET_CommonActions import getPatientAndAppointment, getPatientAndAppointmentDeltaChange


class TestOpenMasterListTestCases:

    @pytest.mark.parametrize('readPayLoadJsonWithUUID', ["Payload/Json/Base_Patient_Uuid_Payload.json"], indirect=['readPayLoadJsonWithUUID'])
    @allure.title("TC001 PUT - Patient And Appointment - Automation")
    def test_put_patient_and_appointment_automation_test(self, apiTestData, readPayLoadJsonWithUUID, configLogger):
        putPatientAndAppointment(apiTestData=apiTestData , endpointkey="Patient And Appointment", configLogger=configLogger, readPayLoadJson=readPayLoadJsonWithUUID, headers=ast.literal_eval(apiTestData['Headers']['ContentTypeWithJsonBlob']))

    @allure.title("TC002 GET - Patient And Appointment - Automation")
    def test_get_patient_and_appointment_automation_test(self, apiTestData, configLogger):
        time.sleep(5)
        getPatientAndAppointment(apiTestData=apiTestData, endpointkey="Patient And Appointment",configLogger=configLogger)

    @allure.title("TOKEN - GET - APIGEE-DEV - Automation")
    def test_token_generation_test(self, apiTestData, configLogger):
        credWithEnvName= apiTestData['Credentials']['docspera']
        getCurrentSessionToken(token_url= credWithEnvName['TokenUrl'], client_id=credWithEnvName['ClientId'], client_secret=credWithEnvName['ClientPassword'], logger=configLogger)
        configLogger.info(os.environ['jwt-token'])

    @pytest.mark.parametrize('readPayLoadJson', ["Payload/Json/Delta_Change.json"],indirect=['readPayLoadJson'])
    @allure.title("TC003 GET - Delta Change - Automation")
    def test_get_delta_change_automation_test(self, apiTestData,readPayLoadJson, configLogger):
        time.sleep(5)
        getPatientAndAppointmentDeltaChange(apiTestData=apiTestData, endpointkey="Delta Change",configLogger=configLogger, readPayLoadJson=readPayLoadJson, headers=ast.literal_eval(apiTestData['Headers']['DeltaChangeHeader']))