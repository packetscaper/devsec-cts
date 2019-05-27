#!usr/bin/python

from netmiko import ConnectHandler
import requests
from pprint import pprint
import json
from endpoint import Endpoint
import textfsm
import os,sys
from netaddr import EUI
class Switch:

        def __init__(self,ip,username,password,ise):
          self.cisco_switch = {
               'device_type': 'cisco_ios',
               'ip' : ip,
               'username' : username,
               'password' : password,
               }
          self.sgts = {}
          self.vrfs = []
          self.endpoints = {}
          self.arp = {}
          self.permissions = {}
          self.ise = ise


        def get_show_device_tracking_database(self):
          net_connect = ConnectHandler(**self.cisco_switch)
          device_tracking_output= net_connect.send_command('show device-tracking database') 
          f = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'templates/device_tracking_database.templ'),'r')
          template = textfsm.TextFSM(f)
          output = template.ParseText(device_tracking_output)
          for o in output:
             self.arp[o[0]] = o[1]

 
        def get_show_vrf(self):
          net_connect = ConnectHandler(**self.cisco_switch)
          vrf_output = net_connect.send_command('show vrf')
          f = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'templates/vrf.templ'),'r')
          template = textfsm.TextFSM(f)
          output = template.ParseText(vrf_output)
          for o in output:
            self.vrfs.append(o[0])

        def get_show_cts_role_based_sgtmaps_all(self):
            self.ise.get_sgts()
            self.sgts = self.ise.sgts
            net_connect = ConnectHandler(**self.cisco_switch)
            for vrf in self.vrfs:
                command = 'show cts role-based sgt-map vrf ' + vrf + ' all'
                cts_sgt_maps_output = net_connect.send_command(command)
                f = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'templates/cts_role_based_sgt_map_all.templ'), 'r')
                template = textfsm.TextFSM(f)
                output = template.ParseText(cts_sgt_maps_output)
                for o in output:
                    e = Endpoint(self.arp[o[0]])
                    e.set_ip(o[0])
                    e.set_vrf(vrf)
                    e.set_sgt(self.sgts[int(o[1])])
                    self.endpoints[self.arp[o[0]]] = e

                    # self.sgtmaps.append({'IP':o[0], 'SGT' : o[1], 'VRF' : vrf)i

        def get_show_cts_role_based_permissions(self):
            net_connect = ConnectHandler(**self.cisco_switch)
            cts_permissions_output = net_connect.send_command('show cts role-based permissions')
            f = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates/cts_role_based_permissions.templ'), 'r')
            template = textfsm.TextFSM(f)
            output = template.ParseText(cts_permissions_output)
            for o in output:
                p = Permission(o[0], o[1])
                self.permissions[(p.dstsgt, p.srcsgt)] = p
                p.set_sgacl(o[2], self.ise.get_sgaclcontent(o[2]))

        def get_show_cts_role_based_counters(self):
          net_connect = ConnectHandler(**self.cisco_switch)
          cts_counter_output = net_connect.send_command('show cts role-based counters')
          f  = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'templates/cts_role_based_counters.templ'),'r')
          template = textfsm.TextFSM(f)
          output = template.ParseText(cts_counter_output)
          for o in output:
             p = self.permissions[(self.sgts[int(o[1])],self.sgts[int(o[0])])]
             p.set_sw_denied(o[2])
             p.set_hw_denied(o[3])
             p.set_sw_permit(o[4])
             p.set_hw_permit(o[5])
             #self.cts_role_based_counters.append({'src-sgt':o[0],'dst-sgt':o[1],'sw-denied':o[2],'hw-denied':o[3],'sw-permit': o[4], 'hw-permit':o[5]})




             #self.cts_role_based_permissions.append({'src-sgt':o[0],'dst-sgt':o[1],'sgacl':o[2]})

           


        def get_ise_endpoint_info(self):
            for e in self.endpoints:
                mac = EUI(e)
                ise_info = self.ise.get_userinfo(mac)
                self.endpoints[e].set_ise_info(ise_info)


        def get_endpoints(self):
            self.get_show_vrf()
            self.get_show_device_tracking_database()
            self.get_show_cts_role_based_sgtmaps_all()
            self.get_ise_endpoint_info()
            return self.endpoints

        def get_permissions(self):
            self.get_show_cts_role_based_permissions()
            self.get_show_cts_role_based_counters()
            return self.permissions




class Permission:

    def __init__(self,srcsgt,dstsgt):
        self.dstsgt = dstsgt
        self.srcsgt = srcsgt
        self.sgacl_name = None
        self.sgaclcontent = None
        self.sw_permit = None
        self.hw_permit = None
        self.sw_denied = None
        self.hw_denied = None
        self.sw_monitor = None
        self.hw_monitor = None

    def set_sgacl(self,sgacl,sgaclcontent):
        self.sgacl_name = sgacl
        self.sgaclcontent = sgaclcontent

    def set_sw_permit(self,counter):
        self.sw_permit = counter


    def set_hw_permit(self,counter):
        self.hw_permit = counter

    def set_sw_denied(self,counter):
        self.sw_denied = counter

    def set_hw_denied(self,counter):
        self.hw_denied = counter





