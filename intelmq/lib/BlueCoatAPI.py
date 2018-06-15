# -*- coding: utf-8 -*-
"""
    BlueCoatAPI.py provides the ability to submit URLs for (re-)categorization using an API access 
    to BlueCoats SiteReview service. 
    
    Right now (2017-01) we are not aware of any possibility to register that account directly over the internet.
    Please check it with your contact at BlueCoat.
"""
import requests
import xmltodict
from intelmq.lib.baseLib import baseLib

__author__ = 'Christoph Giese <cgi1> <C.Giese@telekom.de>'


class BlueCoatAPI(baseLib):
    def __init__(self, logger=None, user=None, password=None):
        className = self.__class__.__name__
        super().__init__(className, logger)

        if self.config:
            self.user = self.config['credentials']['user']
            self.password = self.config['credentials']['password']
            self.report_threat_url = self.config['main']['report_threat_url']
            self.submission_check_url = self.config['main']['submission_check_url']
            self.category_list_url = self.config['main']['category_list_url']
            self.xsd_url = self.config['main']['xsd_url']

        if user:
            self.user = user

        if password:
            self.password = password

    def get_category_list(self):
        '''

        :return: List of BlueCoat categories as JSON dict
        '''

        payload = {
            'userID': self.user
        }

        headers = {
            "None": "None"
        }

        try:
            response = requests.get(self.category_list_url, headers=headers, params=payload, verify=False)

            if response.status_code == 200:
                parsed_response = xmltodict.parse(response._content)
                self.logger.debug("Successfully parsed get_category_list()-response from BC-API.")

                if 'Categories' in parsed_response:
                    if 'Category' in parsed_response['Categories']:
                        return parsed_response['Categories']['Category']

            else:
                self.logger.error("Error in response from bluecoat API!.")
                return -1

        except Exception as e:
            self.logger.exception(e)
            return -1

        return parsed_response

    def submit_url(self, url, submit_comment, cat1, cat2, email, customTrackingID, confidence):

        '''
        Submit an url to bluecoat for the given categories (cat1, cat2) and returns the submissionId for further usage
        :param url: URL to submit
        :param submit_comment: Comment for submission
        :param cat1: One of the predefined categories
        :param cat2: (Optional) One of the predefined categories
        :param email: Email address which receives the outcome of the url review
        :param customTrackingID: custom tracking ID (maximum 32 characters)
        :param confidence: integer value between 0-100 --> 0=no confidence; 100=compete confidence

        :return: uniq submissionId provided by BlueCoat API (7 characters, numbers only)
        '''

        payload = {
            'userID': self.user,
            'url': url,
            'comments': submit_comment,
            'cat1': cat1,
            'cat2': cat2,  # Optional
            'email': email,  # Optional
            'customTrackingID': customTrackingID  # Optional
        }

        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        try:
            parsed_response = None
            response = requests.post(self.report_threat_url, data=payload, headers=headers, verify=False)
            if response.status_code == 200:
                parsed_response = xmltodict.parse(response._content)
                self.logger.debug("Successfully parsed response from BlueCoat-Submit for URL [" + str(url) + "]:" + str(
                    parsed_response))
            else:
                self.logger.error("Error in response from BlueCoat API")

        except Exception as e:
            self.logger.exception(e)
            return None

        if parsed_response and len(parsed_response) > 0:

            good_case = False

            if "Accepted" in parsed_response or "Accepted" in parsed_response['SubmissionResult']:
                self.logger.debug("Accepted response for url'" + url + "' Response:" + str(parsed_response))

                if 'SubmissionResult' in parsed_response and 'Accepted' in parsed_response['SubmissionResult']:
                    self.logger.info(
                        "BlueCoat Accepted response for url'" + url + "' SubmissionResult (uniq id)=" + str(
                            parsed_response['SubmissionResult']['Accepted']['SubmissionId']))
                    return str(parsed_response['SubmissionResult']['Accepted']['SubmissionId'])
                if 'SubmissionResult' in parsed_response:
                    self.logger.info(
                        "BlueCoat Accepted response for url'" + url + "' SubmissionResult (uniq id)=" + str(
                            parsed_response['SubmissionResult']))
                    return str(parsed_response['SubmissionResult'])

                good_case = True

            if "Error" in parsed_response or "Error" in parsed_response['SubmissionResult'] and \
                    parsed_response['Error']['Code'] and parsed_response['Error']['Explanation']:
                self.logger.info(
                    "'" + url + "'response with Code=" + str(parsed_response['Error']['Code']) + " which means: " +
                    parsed_response['Error']['Explanation'])
                good_case = True
                return str(parsed_response['Error']['Code'])

            if "Rejected" in parsed_response or "Rejected" in parsed_response['SubmissionResult']:
                self.logger.info("Rejected response")
                good_case = True

            if not good_case:
                self.logger.error("Invalid response type..")

        else:
            self.logger.error("Error parsing response (its None!)")

    def check_submissions(self, submissionIDs):

        '''

        :param submissionIDs: <list> of submissionIDs to check
        :return: bluecoat rating (contains original categories, review information, submission information ...) Needs to be evaluated in further steps
        '''

        if submissionIDs is None or len(submissionIDs) < 1:
            self.logger.error("No submissionIDs provided")
            return None

        payload = {
            'userID': self.user,
            'submissionIDs': submissionIDs
        }

        headers = {
            "None": "None"
        }

        try:
            parsed_response = None
            response = requests.get(self.submission_check_url, data=payload, headers=headers, verify=False)

            if response.status_code == 200:
                parsed_response = xmltodict.parse(response._content)
                self.logger.debug("Successfully parsed response from BlueCoat to dict: " + str(parsed_response))
            else:
                self.logger.error("Error in response from bluecoat API")

        except Exception as e:
            self.logger.exception(e)
            return None

        if parsed_response is not None and len(parsed_response) > 0:
            self.logger.debug("ToDo: " + str(parsed_response))
