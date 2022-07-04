import requests


class Validations():
    def __init__(self, logger):
        self.logger = logger

    def statusCodeValidation(self,statuscodes,responsestatuscode ):
        try:
            assert str(responsestatuscode) in statuscodes
            return True
        except AssertionError:
            return False

    def negativeStatusCodeValidation(self,negativeresponsestatuscode):
        try:
            assert negativeresponsestatuscode in self.negativestatuscodevalidation
            return True
        except AssertionError as err:
            return False

    def responseTimeValidation(self, reponsetime):
        try:
            if reponsetime<1:
                return 'Low response time'
            else:
                self.logger.warning('This endpoint took more than 1 sec for response !')
                return 'High response time'

        except requests.exceptions.Timeout as e:
            print('Timeout exception')
