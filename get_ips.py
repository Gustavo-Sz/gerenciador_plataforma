import subprocess, os, re

def get_ips(mac_addresses = list):
    
    def strToDic(str):
        out = {}
        auxs = str.split("\n")
        arp_out = []
        for i,line in enumerate(auxs):
            content = re.findall(r"[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+|[a-fA-F0-9]+-[a-fA-F0-9]+-[a-fA-F0-9]+-[a-fA-F0-9]+-[a-fA-F0-9]+-[a-fA-F0-9]+",line) # windows
            # content = re.findall(r"[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+|[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+",line); # linux
            if len(content) > 1:
                arp_out.append(content)
        arp_macs = [el[1] for el in arp_out]
        for mac in mac_addresses:
            if mac.lower() in arp_macs:
                i = arp_macs.index(mac.lower())
                out[mac] = arp_out[i][0]
            else:
                out[mac] = "não disponível"
        return out

    ips = {}
    cmd = ["arp","-a"] 
    st_cmd = subprocess.run(cmd, capture_output=True, encoding="utf-8")
    if st_cmd.returncode==0:
        ips = strToDic(st_cmd.stdout)


    return ips