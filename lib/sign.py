import sys
from ctypes import *

class Sign:
     def __init__(self) -> None:
          self.cur = None
          if sys.platform == "darwin":
                self.cur = cdll.LoadLibrary("./src/bestV8_mac_m.dylib")
          elif sys.platform == "linux":
                self.cur = cdll.LoadLibrary("./src/bestV8_x64.so")
          elif sys.platform == "win32":
                self.cur = cdll.LoadLibrary("./src/bestV8_win64.dll")
          else:
                raise Exception("unknown systerm!")
          self._jsfile = self._get_jsfile()

     def _get_encrypt_value(self,data):
          result = bytes(20000)
          self.cur.runJs.argtypes = (c_char_p, c_char_p)
          for x in range(1):
               self.cur.runJs(create_string_buffer(data.encode('utf8')), result)
               return result.rstrip(b"\x00").decode('utf-8')
     def _get_jsfile(self):
           try:
              data = open("./src/xlbsiren0906.js","r").read()
              return data
           except Exception as e:
                print(e)   
     def sign(self,url):
          jsfile = self._jsfile
          exec_jsfile = jsfile.replace("_kqsec_r1is_", url, 1)
          return self._get_encrypt_value(exec_jsfile)



if __name__ == "__main__":
     url = "/api.xiaolanben.com/xlb-gateway/blue-book/company/companyData?eid=q072badde03989d63245bcda8e97c0ad5&page=0&type=newMedias&pageSize=100"
     test = Sign()
     a = test.sign(url)
     print("===start===\n"+"sign: "+a+"\n====end====")

