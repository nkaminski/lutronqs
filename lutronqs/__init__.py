import threading
import telnetlib
import re

class ConnectionError(Exception):
        pass

class ProcessorError(Exception):
        pass

class LutronQS:
    def _rxData(self):
        msgre = re.compile("\~(\S+?),(\S+)\r\n$")
        while(self.run):
            try:
                data = self._tc.read_until(b"\r\n",1)
            except telnetlib.NotConnectedError:
                self._return_data = None
                self._wait_v = ""
                self.run = False
                self._wait_e.set()
                return

            mobj = msgre.search(data.decode('ascii'))
            if not mobj:
                continue
            #Unblock anyone waiting on a get* call
            if(mobj.group(1) == self._wait_v or mobj.group(1) == "ERROR"):
                self._return_data = []
                self._return_data.append(mobj.group(1))
                self._return_data.append(mobj.group(2).split(","))
                self._wait_v = ""
                self._wait_e.set()
            #print("QS Processor said: " + mobj.group(1) + " " + mobj.group(2))
            if(self.onReceive):
                self.onReceive(mobj.group(1), mobj.group(2))
 
    def __init__(self,host,user,pwd):
        self._tc=None
        self._rxthread = threading.Thread(target=self._rxData)
        self.run=True
        self.onReceive=None
        self._wait_e=threading.Event()
        self._wait_v=""
        self._return_data=None

        #Init done, implementation starts here
        self._tc = telnetlib.Telnet(host)
        msg = b"login: "
        resp = self._tc.read_until(msg, 5)
        if(msg != resp.strip(b"\r\n")):
            raise ProcessorError("Unexpected data from QS processor: " + resp.decode('ascii'))
        self._tc.write(user.encode('ascii') + b"\r\n")
        msg = b"password: "
        resp = self._tc.read_until(msg, 5)
        if(msg != resp.strip(b"\r\n")):
            raise ProcessorError("Unexpected data from QS processor: " + resp.decode('ascii'))
        self._tc.write(pwd.encode('ascii') + b"\r\n")
        msg = b"QNET> "
        resp = self._tc.read_until(msg, 5)
        if(msg != resp.strip(b"\r\n")):
            raise ProcessorError("Login to processor failed!")
        self._rxthread.start()

    def close(self):
        self.run = False
        if(self._rxthread):
            try:
                self._rxthread.join()
            except:
                pass
        if(self._tc):
            self._tc.close()
 
    def __del__(self):
        self.close()

    def _write(self,data):
        if not self.run:
            raise ConnectionError("Not connected to QS processor!")
        try:
            self._tc.write(data.encode('ascii') + b"\r\n")
        except telnetlib.NotConnectedError:
            raise ConnectionError("Connection lost while sending command!")
    
    def _write_req(self,wverb,data):
        if not self.run:
            raise ConnectionError("Not connected to QS processor!")
        self._wait_v = wverb
        self._wait_e.clear()
        try: 
            self._tc.write(data.encode('ascii') + b"\r\n")
        except telnetlib.NotConnectedError:
            raise ConnectionError("Connection lost while sending command!")

        if self._wait_e.wait(5):
            return self._return_data
        else:
            raise ProcessorError("No response received from QS Processor in response to request!")

    def setAreaLevel(self,iid,level):
        cmdstr = "#AREA,%d,1,%d" % (iid, level)
        self._write(cmdstr)

    def setAreaScene(self,iid,scene):
        cmdstr = "#AREA,%d,6,%d" % (iid, scene)
        self._write(cmdstr)

    def getAreaScene(self,iid):
        cmdstr = "?AREA,%d,6" % (iid)
        return self._write_req("AREA",cmdstr)

