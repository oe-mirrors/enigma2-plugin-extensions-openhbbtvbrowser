from __future__ import absolute_import
from enigma import eConsoleAppContainer
from . import datasocket
try:
    from Components.SystemInfo import BoxInfo
    BRAND = BoxInfo.getItem("brand")
except:
    from boxbranding import getBrandOEM
    BRAND = getBrandOEM()

class Browser:
    def __init__(self, urlcallback=None):
        if BRAND == "vuplus":
            vmode = open("/proc/stb/video/videomode_50hz", "r").read()
            self.resolution="1920x1080"
            if vmode[0:3] == "480":
                self.resolution="720x480"
            elif vmode[0:3] == "576":
                self.resolution="720x576"
            elif vmode[0:3] == "720":
                self.resolution="1280x720"
            elif vmode[0:3] == "216":
                self.resolution="3840x2160"
        self.onBroadcastPlay = []
        self.onBroadcastStop = []
        self.onExit = []
        self.commandserver = None

    def connectedClients(self):
        return self.commandserver.connectedClients()

    def start(self, url, onid, tsid, sid):
        if not self.commandserver:
            self.commandserver = datasocket.CommandServer()
            datasocket.onCommandReceived.append(self.onCommandReceived)
            datasocket.onBrowserClosed.append(self.onBrowserClosed)
            container = eConsoleAppContainer()
            if BRAND == "vuplus":
                container.execute("export EGLFS_LIBVUPL_SIZE=%s /usr/bin/openhbbtvbrowser %s --onid %d --tsid %d --sid %d" % (self.resolution, url, onid, tsid, sid))
            else:
                container.execute("/usr/bin/openhbbtvbrowser %s --onid %d --tsid %d --sid %d" % (url, onid, tsid, sid))
 
    def stop(self):
        if self.commandserver:
            self.commandserver = None

    def onCommandReceived(self, cmd, data):
        if cmd == 1:
            for x in self.onBroadcastPlay:
                x()
        elif cmd == 2:
            for x in self.onBroadcastStop:
                x()
        elif cmd == 6:
            for x in self.onExit:
                x()

    def onBrowserClosed(self):
        self.commandserver = None
        for x in self.onExit:
            x()
