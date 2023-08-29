import base64,json
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

SEKIRO_URL = "https://124.221.135.47/business-demo/invoke"

# proxy = {"http":"127.0.0.1:8080","https":"127.0.0.1:8080"}

class sekiro:
    def __init__(self,group="xiaolanben"):
        self.sekiro_url = SEKIRO_URL
        self.data = {
            "group":group,
            "action":"",
            "url":"",
            "method":""
        }

    def sign_by_get(self,url,method="Get"):
        self.data['action'] = "sign"
        self.data['method'] = method
        self.data['url'] = base64.urlsafe_b64encode(url.encode('utf-8')).decode('utf-8')
        # self.data['url'] = url

        header = {'Content-Type': 'application/json'}
        json_data = json.dumps(self.data)
        try:
            req = requests.post(url=self.sekiro_url,data=json_data,headers=header,verify=False)
            # print(req.json())
            return req.json()['data']
        except Exception as e:
            print(e)
            return

if __name__ == "__main__":
    test = sekiro()
    url = "/api.xiaolanben.com/xlb-gateway/blue-book/company/companyData?eid=qxb10abf321eaffae4e6949b4fe38b7092&page=0&type=newMedias&pageSize=400"
    sign = test.sign_by_get(url)
    print(sign)