import base64,json
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

SEKIRO_URL = "https://${your_server_ip}/business-demo/invoke"

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


a = sekiro()
url = "/api.xiaolanben.com/xlb-gateway/blue-book/company/companyData?eid=qxca1785a9a97606cfa44545f33c576374&page=0&type=newMedias&pageSize=100"
sign = a.sign_by_get(url)
print(sign)

# 输出结果
# /api.xiaolanben.com/xlb-gateway/blue-book/company/companyData?eid=qxca1785a9a97606cfa44545f33c576374&page=0&type=newMedias&pageSize=100&h_t=1693280989495&h_v=h5_1129163840@0&h_sign=959c706c7098e2e1a9c099e094eda9c4
