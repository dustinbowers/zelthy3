import json
import phonenumbers
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View

from zelthy.core.api import get_api_response

@method_decorator(csrf_exempt, name='dispatch')
class SMSSendView(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        config = data.get("config", {})
        extra_data = data.get("extra_data", {})
        pn = phonenumbers.parse(data['destination'])
        send_sms_uri = '/sms/2/text/advanced'
        params = {
                    "messages":[{
                    "from": config["src"],
                    "destinations": [{"to": str(pn.national_number)}],
                    "text": data["msg"]
                    }]
                    }
        headers = {"Authorization": config["api_key"]}
        url = config["base_url"] + send_sms_uri
        response = requests.request("POST", url, params=params, headers=headers, data=json.dumps(params), verify=False)
        if response.status_code == 200:
            return get_api_response(True, {"response": response.json()}, 200)
        else:
            return get_api_response(False, {"response": response.text}, response.status_code)

class SMSUpdateStatusView(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        record = data["record"]
        config = data["config"]
        try:
            msg_id = json.loads(record["response_text"])['messages'][0]['messageId']
            uri = f'/sms/1/reports?messageId={msg_id}&limit=3'
            url = config["base_url"] + uri
            response = requests.request(
                        "GET", url=url, 
                        headers={'Authorization':config["api_key"]},
                        verify=False)
            res_text = json.loads(response.text)
            delivery_status = res_text['results'][0]['status']['name']
            return get_api_response(True, {"delivery_status": delivery_status, "response": res_text}, 200)
        except Exception as e:
            return get_api_response(False, {"delivery_status": "failed", "response": res_text}, 500)

