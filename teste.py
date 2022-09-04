import re,subprocess
#cmd = "arp -a | grep "
cmd = ["arp","-a"] 
st_cmd = subprocess.run(cmd, capture_output=True, encoding="utf-8")

aux = st_cmd.stdout.split("\n")
for i,line in enumerate(aux):
    #aux[i] = re.split('[\s]+',aux[i])[1:-2]
    # r"([0-9]+.[0-9]+.[0-9]+.[0-9])|([a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+)"
    aux[i] = re.findall(r"[0-9]+[.][0-9]+[.][0-9]+[.][0-9]|[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+:[a-fA-F0-9]+",line);
    # if aux[i][1] in mac_addresses:

print([aux[i][1] for i in range(0,len(aux)-1)])