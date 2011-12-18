import telnetlib
import popen2
import os

class VLCController:
    def __init__(self):
        self.__socket = None

    def handshake(self):
        self.__socket = telnetlib.Telnet('localhost', 4121)
        return self.__socket.read_until('>')

    def command(self, c):
        self.__socket.write(c+"\n")
        return self.__socket.read_until('>')

    def close(self):
        self.command('logout')
        self.__socket.close()

    @classmethod
    def update_and_play(cls, playlist_path):
        vlc_instance = VLCController()

        vlc_instance.handshake()
        vlc_instance.command("stop")
        vlc_instance.command("clear")
        vlc_instance.command("add file://{0}".format(playlist_path.replace(' ', '%20')))
        vlc_instance.command("play")
        vlc_instance.close()

