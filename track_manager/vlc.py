import telnetlib
import popen2

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
        vlc_instance = telnetlib.Telnet('localhost', 4121)
        print 'handshake:', vlc_instance.read_until('>')
        vlc_instance.write('stop\n')
        print 'stop:', vlc_instance.read_until('>')
        vlc_instance.write('clear\n')
        print 'clear:', vlc_instance.read_until('>')
        vlc_instance.write("add file://{0}\n".format(playlist_path.replace(' ', '%20')))
        print "add:", vlc_instance.read_until('>')
        vlc_instance.write("play\n")
        print "play:", vlc_instance.read_until('>')

        vlc_instance.write("playlist\n")
        print "playlist:", vlc_instance.read_until('>')

        vlc_instance.write('logout\n')
        print "logout:", vlc_instance.read_until('>')
        vlc_instance.close()

    @classmethod
    def run(cls, playlist_file_path, run_parameters):
        popen2.popen2('nohup vlc {0} --loop "{1}" &'.format(run_parameters, playlist_file_path))

