import utils.Config as c
import requests
import http
import json
from urllib.parse import urlparse


class PublisherHandler(object):
    """This class takes a dataframe of payloads and posts them to the claim entry publisher api"""
    def __init__(self):
        self.bearer_token = self.get_bearer_token()

    def get_bearer_token(self):
        print("getting bearer token")
        headers = {}

        body = {'grant_type':'client_credentials',
                'client_id': c.client_id,
                'client_secret':c.client_secret,
                'scope':'rca_ce_access'}

        response = requests.post(c.token_url, data = body)
        token_data = response.json()
        response.close()

        bearer_token = token_data["access_token"]
        return bearer_token

    def post_data_frame(self,data_frame):
        payload_body = self.cast_df_to_payload_body(data_frame)
        response = self.post_claim_submission(payload_body)
        return response

    def cast_df_to_payload_body(self, data_frame):
        data_frame['payload'] = data_frame['payload'].apply(json.loads)
        payload_list = data_frame['payload'].tolist()
        combined_json = json.dumps(payload_list)
        return str(combined_json)

    def post_data_frame_test(self, data_frame):
        payload_body = self.cast_df_to_payload_body(data_frame)
        with open("sample.json","w") as file:
            file.write(payload_body)

    def post_claim_submission(self, payload_body):
        headers = {"Authorization": f"Bearer {self.bearer_token}",
                "User-Agent": "PostmanRuntime/7.28.4",
                "Content-Type": "application/json",
                "Accept":"*/*"} 
        parsed_url = urlparse(c.publisher_url)
        domain = parsed_url.netloc
        path = parsed_url.path
        
        conn = http.client.HTTPSConnection(domain)
        conn.request("POST", path, payload_body, headers)
        res = conn.getresponse()
        data = res.read()
        text = data.decode("utf-8")
        output = json.loads(text)
        conn.close()
        
        return output