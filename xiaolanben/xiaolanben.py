from utils.sign import sekiro
from urllib.parse import quote
import base64,json
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

proxy = {"http":"127.0.0.1:8080","https":"127.0.0.1:8080"}

class xiaolanben:
    def __init__(self) -> None:
        self.host = "https://www.xiaolanben.com"
        self.sekiro = sekiro()
        self.headers = {
            # Authorization userId 应该是必填字段，登录小蓝本后从浏览器或burp中获取
            "Authorization": "encrypt MjU3MTc5Mjk2LXYx.s3Bbu25WYqxM8dIxx0FbVAbS67uGmad_zv38t7sZ_T8lRmF0doUSfgrvTemaIMfO8S3Xqst0LMgalprTlZxaSA",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Referer": "https://www.xiaolanben.com/pc",
            "Accept": "application/json, text/plain, */*",
            "userId": "257179296",
            #"Cookie": "Hm_lvt_0a634afd1a81851812167241458087f8=1693227184; _gid=GA1.2.1444048971.1693227184; cna=cTxzHTS36WkCAa8N4onnx0+D; wtf=PtB79QQCADHPmtoxz5raMc-a2jHPmtoxz5ra; _medusa_token=247815164; login-id=73240417f17b473fb5a74ed3b1b56182BE3A; user-id=257179296; token=MjU3MTc5Mjk2LXYx.s3Bbu25WYqxM8dIxx0FbVAbS67uGmad_zv38t7sZ_T8lRmF0doUSfgrvTemaIMfOAJExScx3rRy4orPcRJ73hg; userId=257179296; _gat_gtag_UA_145833505_1=1; Hm_lpvt_0a634afd1a81851812167241458087f8=1693229312; _ga=GA1.1.751358039.1693227184; _ga_SJLX84YVYQ=GS1.1.1693227183.4.1.1693229327.0.0.0",
            "Connection": "close"
        }

    def get_sign(self,_url) ->str:
        return self.sekiro.sign_by_get(_url)
    
    def search_queryByKeyword(self,keyword) -> list: #按关键字查询
        keyword = quote(keyword)
        _url = f"""/api.xiaolanben.com/bluebook/api/v1/es/queryByKeyword?keyword={keyword}&pageId=1&pageSize=100"""
        signed_url = self.get_sign(_url)
        # print(signed_url)
        url = self.host + signed_url
        try:
            req = requests.get(url=url,headers=self.headers,proxies=proxy,verify=False)
            jsonData = req.json()
            companyArry = jsonData['companys']['companys']
            # 所有跟关键词相关的公司（组织）的集合
            eids = []
            for i in companyArry:
                eids.append(i['eid'])
            eids = sorted(list(set(eids)))    
            print(eids)    
            return eids
        except Exception as e:
            print(e)
            return []
        
    def find_newMedias(self,eid):
        _url = f"""/api.xiaolanben.com/xlb-gateway/blue-book/company/companyData?eid={eid}&page=0&type=newMedias&pageSize=400"""
        signed_url = self.get_sign(_url)
        url = self.host + signed_url
        xcx_accountName_list = []

        try:
            req = requests.get(url=url,headers=self.headers,proxies=proxy,verify=False)
            jsonData = req.json()
            # print(jsonData)
            if jsonData:
                for data in jsonData:
                    if 'typeName' in data.keys() and data['typeName'] == "xcx":
                        xcx_accountName_list.append(data['accountName']) 
            return xcx_accountName_list
        except Exception as e:
            print(e)
            return xcx_accountName_list
           
        
if __name__ == "__main__":
    test = xiaolanben()
    # a = test.search_queryByKeyword("北京大学")
    b = test.find_newMedias("q9fff123b21985b911b7db7abb68310a6")
    print(b)
