import subprocess

def pingMachines(ips):

    cmd= "ping"
    sts = {}

    for machine in ips:
        st_cmd = subprocess.run([cmd, f"{machine}","-n", "1","-w","500"], capture_output=True, encoding="utf-8") # windows
        # st_cmd = subprocess.run([cmd, f"{machine}","-c", "1","-w","1"], capture_output=True, encoding="utf-8") # linux
        if "Received = 1" in st_cmd.stdout: # windows
        # if "1 received" in st_cmd.stdout: # linux
            sts[f"{machine}"] = 1
        else:
            sts[f"{machine}"] = 0
        
    return sts
