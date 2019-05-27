import requests

import json
import urllib3
import xmltodict
class ISE:
 
 def __init__(self,adminip,mntip,username,password):
   self.ise = {
       'adminip' :adminip,
       'username':username,
       'password':password,
       'mntip'   :mntip  
       }
   self.headers = {"Accept":"application/json","Content-Type":"application/json"}
   self.sgts = {}
   self.adminurl = "https://{}:9060/ers/config".format(self.ise["adminip"])
   self.mnturl   = "https://{}/admin/API/mnt/Session/".format(self.ise["mntip"])


 def get_all_sgts_url(self):
    urllib3.disable_warnings()
    url = "https://{}:9060/ers/config/sgt?size=100"
    url = url.format(self.ise["adminip"]) 
    headers = {"Accept":"application/json", "Content-Type":"application/json"}
    r = requests.get(url,
                 headers = headers,
                 auth = (self.ise["username"], self.ise["password"]),
                 verify = False)
    json_resp =  r.json()
    return json_resp


 def get_sgts(self):
    json_resp = self.get_all_sgts_url()
    for j in json_resp["SearchResult"]["resources"]:
      urllib3.disable_warnings()
      resp = requests.get(j["link"]["href"],
                      auth = (self.ise["username"],self.ise["password"]),
                      headers = self.headers,
                      verify = False)
 
      r =resp.json()
      self.sgts[r["Sgt"]["value"]]= r["Sgt"]["name"]

 def get_userinfo(self,mac):
   if mac == "1111.1111.1111":
    return "user not found"
   else :
    url = "https://{}/admin/API/mnt/Session/MACAddress/{}".format(self.ise["mntip"],mac) 
    resp = requests.get(url,auth=(self.ise["username"],self.ise["password"]),verify=False)
    xml_dict = xmltodict.parse(resp.text)
    attr= xml_dict["sessionParameters"]
    return {"user_name":attr["user_name"], "endpoint_policy" : attr["endpoint_policy"],
            "switch_interface" : attr["nas_port_id"], "identity_group":attr["identity_group"],
            "auth_method": attr["authentication_method"],"auth_protocol":attr["authentication_protocol"]}


 
     
 def get_all_sgacls(self):
    urllib3.disable_warnings()
    url = "https://{}:9060/ers/config/sgacl?size=100"
    url = url.format(self.ise["adminip"])
    headers = {"Accept":"application/json", "Content-Type":"application/json"}
    r = requests.get(url,
                 headers = headers,
                 auth = (self.ise["username"], self.ise["password"]),
                 verify = False)
    json_resp =  r.json()
    return json_resp

 def get_sgaclcontent(self,sgacl):
  sgac = sgacl 
  json_resp= self.get_all_sgacls()
  sgacls = json_resp["SearchResult"]["resources"]
  for sgacl in sgacls:
   if sgacl["name"].encode('UTF-8') == sgac: 
    sgacllink = sgacl["link"]["href"]
  resp = requests.get(sgacllink,
                      auth = (self.ise["username"],self.ise["password"]),
                      headers = self.headers,
                      verify = False)

  r =resp.json()
  return r["Sgacl"]["aclcontent"]



  



 
 
