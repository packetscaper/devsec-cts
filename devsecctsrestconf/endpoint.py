import json
import requests

class Endpoint():

    def __init__(self,mac):
      self.ip = None
      self.mac = mac
      self.vrf = None
      self.username = None
      self.ise_endpoint_policy = None
      self.ise_endpoint_identity_group = None
      self.auth_type = None
      self.auth_protocol = None
      self.sgt = None
      self.switch_interface = None

    def set_ip(self,ip):
      self.ip = ip

    def get_ip(self,mac):
      return self.ip

    def set_mac(self,mac):
      self.mac = mac

    def get_mac(self) :
      return self.mac

    def set_vrf(self,vrf):
      self.vrf = vrf

    def get_vrf(self):
      return self.vrf

    def set_sgt(self,sgt):
        self.sgt = sgt

    def get_sgt(self):
        return self.sgt

    def set_ise_info(self,ise_info):
        self.username = ise_info["user_name"]
        self.auth_type = ise_info["auth_method"]
        self.ise_endpoint_identity_group = ise_info["identity_group"]
        self.ise_endpoint_policy = ise_info["endpoint_policy"]
        self.switch_interface = ise_info["switch_interface"]
        self.auth_protocol = ise_info["auth_protocol"]