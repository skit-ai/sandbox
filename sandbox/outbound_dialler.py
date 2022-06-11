import os
import json
import requests
from typing import Dict, Tuple


LOGIN_URL = "{}/oauth/"
TOKEN_REFRESH_URL = "{}/oauth/refresh-token/"
CREATE_CALLS_URL = "{}/campaign_manager/outbound/calls/"
RETRIEVE_CALL_URL = "{}/campaign_manager/outbound/calls/{}/"


class OutboundDiallerClient():
    """ Instantiates a client object to handle interactions with the Outcound Calls API."""

    def __init__(self, email=None, password=None, api_basepath=None):

        self._access_token = self._refresh_token = None

        self._api_basepath = os.getenv("API_BASEPATH", api_basepath)
        self._email = os.getenv("OUTBOUND_DIALLER_EMAIL", email)
        self._password = os.getenv("OUTBOUND_DIALLER_PASSWORD", password)

        if self._email and self._password:
            self._access_token, self._refresh_token = self.get_tokens(self._email, self._password)
        else:
            raise Exception("Either email or password is not provided")


    ####
    ## methods to get access tokens

    def get_tokens(self, email, password) -> Tuple[str, str]:
        response = self.__login_api(email, password)
        self.check_access_token(response)
        return response.get("access_token"), response.get("refresh_token")

    def refresh_tokens(self, refresh_token=None):
        if not refresh_token:
            refresh_token = self._refresh_token

        if refresh_token:
            response = self.__refresh_token_api(refresh_token)
            self.check_access_token(response)
            return response.get("access_token"), response.get("refresh_token")
        else:
            raise Exception("No refresh token available. Try logging in again.")


    ####
    ## methods to create and retrieve calls

    def create_call(self, campaign_uuid: str, caller_number: str, metadata: Dict, tag="sandbox") -> Tuple[str, bool]:
        response = self.__create_calls_api(campaign_uuid, [caller_number], [metadata], tag)
        self.check_call_task_uuids(response)

        placed = None
        if response.get("call_task_uuids"):
            placed = True
            return response.get("call_task_uuids")[0], placed
        else:
            placed = False
            return response.get("failed")[0].get("ErrorString"), placed

    def retrieve_call(self, call_task_uuid: str,) -> Tuple[Dict, str]:
        response = self.__retrieve_call_api(call_task_uuid)

        status = None
        if response.get("status") == "COMPLETED":
            if response.get("answered_count") == 1:
                if "call_ended" in response.get("metadata"):
                    status = "SUCCESS"
                else:
                    status = "NOT ENDED"
            else:
                status = "NOT ANSWERED"
        else:
            status = "NOT COMPLETED"

        return response, status


    ####
    ## check responses for errors

    def check_call_task_uuids(self, response):
        if "call_task_uuids" not in response:
            raise Exception(response)

    def check_access_token(self, response: Dict):
        if "access_token" not in response:
            raise Exception(response)

    def check_json(self, response):
        return json.loads(response)


    ####
    ## Outbound Dialler APIs

    def __login_api(self, email, password) -> Dict:

        payload = json.dumps({
            "email": email,
            "password": password,
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        url = LOGIN_URL.format(self._api_basepath)

        response = requests.request("POST", url, headers=headers, data=payload)
        return self.check_json(response.text)

    def __refresh_token_api(self, refresh_token) -> Dict:

        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(refresh_token)
        }

        url = TOKEN_REFRESH_URL.format(self._api_basepath)

        response = requests.request("GET", url, headers=headers, data=payload)
        return self.check_json(response.text)

    def __create_calls_api(self, campaign_uuid, caller_number_list, metadata_list, tag) -> Dict:

        payload = json.dumps({
            "tag": tag,
            "campaign_uuid": campaign_uuid,
            "calls": [
                {
                    "caller_number": caller_number,
                    "metadata": metadata
                }
                for caller_number, metadata in zip(caller_number_list, metadata_list)
            ]
        })
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self._access_token),
            'Content-Type': 'application/json'
        }

        url = CREATE_CALLS_URL.format(self._api_basepath)

        response = requests.request("POST", url, headers=headers, data=payload)
        return self.check_json(response.text)

    def __retrieve_call_api(self, call_task_uuid):

        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(self._access_token)
        }

        url = RETRIEVE_CALL_URL.format(self._api_basepath, call_task_uuid)

        response = requests.request("GET", url, headers=headers, data=payload)
        return self.check_json(response.text)

