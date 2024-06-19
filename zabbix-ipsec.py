#!/usr/local/bin/python3.8

import itertools
import re
import sys
import xml.etree.cElementTree as ET

IPSEC_CONF = '/var/etc/ipsec/swanctl.conf'
rtt_time_warn = 200
rtt_time_error = 300

def parseConf():
    reg_conn = re.compile(r'con\d+')
    reg_local = re.compile(r'local_addrs\s*=\s*(.*)')
    reg_remote = re.compile(r'remote_addrs\s*=\s*(.*)')
    reg_descr = re.compile(r'# P1 \(ikeid \d+\):\s*(.*)')
    
    data = {}
    
    with open(IPSEC_CONF, 'r') as f:
        soubor = f.read()
        # Capture the full con section
        groups = re.findall(r'(con\d+.*?\n\s*})', soubor, flags=re.DOTALL)
        
        for g in groups:
            conn_tmp = []
            m = re.search(reg_conn, g)
            if m:
                conn_tmp.append(m.group(0))
            
            local_tmp = []
            m1 = re.search(reg_local, g)
            if m1:
                local_tmp.append(m1.group(1))
            
            remote_tmp = []
            m2 = re.search(reg_remote, g)
            if m2:
                remote_tmp.append(m2.group(1))
            
            descr_tmp = []
            m3 = re.search(reg_descr, g)
            if m3:
                descr_tmp.append(m3.group(1))
            
            if conn_tmp and local_tmp and remote_tmp and descr_tmp:
                data[conn_tmp[0]] = [local_tmp[0], remote_tmp[0], descr_tmp[0]]
    
    return data

def getTemplate():
    template = """
        {{ "{{#TUNNEL}}":"{0}","{{#TARGETIP}}":"{1}","{{#SOURCEIP}}":"{2}","{{#DESCRIPTION}}":"{3}" }}"""

    return template

def getPayload():
    final_conf = """{{
    "data":[{0}
    ]
}}"""

    conf = ''
    data = parseConf().items()
    for key,value in data:
        tmp_conf = getTemplate().format(
            key,
            value[1],
            value[0],
            value[2],
            rtt_time_warn,
            rtt_time_error
        )
        if len(data) > 1:
            conf += '%s,' % (tmp_conf)
        else:
            conf = tmp_conf
    if conf[-1] == ',':
        conf=conf[:-1]
    return final_conf.format(conf)

if __name__ == "__main__":
    ret = getPayload()
    sys.exit(ret)
