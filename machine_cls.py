
class machine():
    def __init__(self,mac,ip,status, frame, canvas):
        self.mac = mac
        self.ip = ip
        self.status = status
        self.frame = frame
        self.canvas = canvas

    def set_ip(self, ip):
        self.ip.set(ip)


    def set_status(self, st):
        self.status.set(st)

    def create_canvas(self, cv):      
        self.canvas = cv