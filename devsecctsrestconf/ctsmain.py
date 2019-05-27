from switch import Switch
from ise import ISE
from prettytable import PrettyTable

ise = ISE("10.10.10.20","10.10.10.20","admin","credentials")
switch = Switch("10.10.10.20","admin","credentials",ise)

def print_endpoints():
    endpoints = switch.get_endpoints()
    t = PrettyTable(['Mac Address','IP Address','VRF','SGT','Username','Profiling Policy','Identity Group','Auth Info'])
    for endpoint in endpoints:
        obj = endpoints[endpoint]
        t.add_row([obj.mac,obj.ip,obj.vrf,obj.sgt,obj.username,obj.ise_endpoint_policy,obj.ise_endpoint_identity_group,
                (obj.auth_type+" - "+obj.auth_protocol)])
    print t


def print_permissions():
    permissions = switch.get_permissions()
    t = PrettyTable(['src-sgt','dst-sgt','sgacl','rules','software-permit','software-denied','hardware-permit','hardware-denied'])
    for permission in permissions:
        obj = permissions[permission]
        t.add_row([obj.srcsgt,obj.dstsgt,obj.sgacl_name,obj.sgaclcontent,obj.sw_permit,obj.sw_denied,obj.hw_permit,obj.hw_denied])
    print t


if __name__ == "__main__":
 print_endpoints()
 print_permissions()

