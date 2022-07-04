import calendar
import os
import random
import uuid
from datetime import datetime


class Constants:
    def __init__(self):
        self.patientParams = {}
        # set docspera id
        if os.getenv('docspera_id') is None:
            os.environ['docspera_id'] = "Docs_" + str(random.randint(11111, 99999))
            self.patientParams['docspera_id'] = os.getenv('docspera_id')
        else:
            self.patientParams['docspera_id'] = os.getenv('docspera_id')

        # set epochfrom id
        if os.getenv('epoch_time_from') is None:
            os.environ['epoch_time_from'] = str(calendar.timegm(datetime.utcnow().utctimetuple()))
            self.patientParams['epoch_time_from'] = os.getenv('epoch_time_from')
        else:
            self.patientParams['epoch_time_from'] = os.getenv('epoch_time_from')

    def patientParameters(self, uuidval):
        # set env variables
        os.environ['file_name'] = uuidval
        os.environ['patient_value'] = str(uuid.uuid4())
        os.environ['appointment_value'] = str(uuid.uuid4())
        os.environ['cal_id'] = str(random.randint(11111, 99999))
        os.environ['mrn_number'] = str(random.randint(11111, 99999))
        os.environ['medication_id'] = str(random.randint(11111, 99999))
        os.environ['medicationreq_id'] = str(random.randint(11111, 99999))
        os.environ['medication_statement_id'] = str(random.randint(11111, 99999))
        os.environ['medication_ad_id'] = str(random.randint(11111, 99999))
        os.environ['aller_id'] = str(random.randint(11111, 99999))
        os.environ['diag_id'] = str(random.randint(11111, 99999))
        os.environ['prac_id'] = str(random.randint(11111, 99999))
        os.environ['coverage_value'] = str(random.randint(11111, 99999))
        # store it in dict
        self.patientParams['file_name'] = os.getenv('file_name')
        self.patientParams['patient_value'] = os.getenv('patient_value')
        self.patientParams['appointment_value'] = os.getenv('appointment_value')
        self.patientParams['cal_id'] = os.getenv('cal_id')
        self.patientParams['mrn_number'] = os.getenv('mrn_number')
        self.patientParams['medication_id'] = os.getenv('medication_id')
        self.patientParams['medicationreq_id'] = os.getenv('medicationreq_id')
        self.patientParams['medicationreq_id'] = os.getenv('medicationreq_id')
        self.patientParams['medication_statement_id'] = os.getenv('medication_statement_id')
        self.patientParams['medication_ad_id'] = os.getenv('medication_ad_id')
        self.patientParams['aller_id'] = os.getenv('aller_id')
        self.patientParams['diag_id'] = os.getenv('diag_id')
        self.patientParams['prac_id'] = os.getenv('prac_id')
        self.patientParams['coverage_value'] = os.getenv('coverage_value')

        return self.patientParams
