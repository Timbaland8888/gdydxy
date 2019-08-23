#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#fucntion: change vm vdi size
#Arthour:Timbaland
#DATE:20190821
import  vm_tool
import time
# CREARTE VM LIST
vm_list = []
for vm in range(1,260):
    vm_list.append('YD02-%03d-V'%(vm))
# print(vm_list)


cn = vm_tool.connect('172.21.0.17')

#模板vdi 的vdi uuid
result_mb_vdi  = vm_tool.exec_commands(cn,'xe vm-disk-list  vm=YD02-001-V')
print(result_mb_vdi)
mb_vdi_uuid = result_mb_vdi[1].split(':')[6].split('\n')[0].strip()
# print(mb_vdi_uuid)
for vmid in range(1,259):
        #查询当前虚拟机vdi命令
        cn1 = vm_tool.connect('172.21.0.17')
        vdi_cd = """xe vm-disk-list  vm={0}""".format(vm_list[vmid])
        result_vdi_vbd = vm_tool.exec_commands(cn1,vdi_cd)
        #获取vdi uuid

        vdi_uuid = result_vdi_vbd[1].split(':')[6].split('\n')[0].strip()

        # time.sleep(5)
        #查询vm uuid 命令
        cn2 = vm_tool.connect('172.21.0.17')
        vm_name_lable_cd = """ xe vm-list name-label={0}""".format(vm_list[vmid])
        result_name_lable =  vm_tool.exec_commands(cn2,vm_name_lable_cd)
        vm_lanble_uuid = result_name_lable[1].split(':')[1].split('\n')[0].strip()
        # time.sleep(5)
        #删除虚拟机vdi命令
        cn3 = vm_tool.connect('172.21.0.17')
        vdi_destroy_cd = """ xe vdi-destroy uuid={0}""".format(vdi_uuid)
        result_vdi_destroy = vm_tool.exec_commands(cn3,vdi_destroy_cd)
        # time.sleep(5)
        #从模板YD02-001-V克隆一份VDI并获取新的uuid
        cn4 = vm_tool.connect('172.21.0.17')
        vdi_clone_cd = """xe vdi-clone new-name-label={0} uuid={1}""".format(vm_list[vmid],mb_vdi_uuid)
        # print(vdi_clone_cd)vdi_clone_cd
        result_vdi_clone = vm_tool.exec_commands(cn4,vdi_clone_cd)
        clone_vdi_uuid = result_vdi_clone[1].strip()
        print(clone_vdi_uuid)

        # #创建连接的vbd使VDI连接到虚拟机
        cn5 = vm_tool.connect('172.21.0.17')
        vdi_vbd_cd = """xe vbd-create vdi-uuid={0} vm-uuid={1} device=0 type=disk mode=RW""".format(clone_vdi_uuid,vm_lanble_uuid)
        print(vdi_vbd_cd)
        vm_tool.exec_commands(cn5,vdi_vbd_cd)

