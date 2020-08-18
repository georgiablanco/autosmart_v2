'''
STREAM PLAYER FUNCTION
AUTHOR: GEORGIA BLANCO-LITCHFIELD GBL06
'''


import psutil, os
from autosmart_v2.runner import Runner
from autosmart_v2.config.config import Config

APP_PATH = Config['exctractorappPath']
STREAM_SPECS = Config['streamSpecs']
STREAMS_LOC = Config['streamsLocation']


class StreamPlayer(Runner):

    def __init__(self, name, status, stream, logger, counter):
        super(StreamPlayer, self).__init__(logger=logger)
        self.name = name
        self._status = status
        self.stream = stream
        self.logger = logger
        self.counter = counter

    @property
    def status(self):
        """
        """
        if not self.proc:
            print("Player status")
            for proc in psutil.process_iter():
                if proc.name == 'StreamXpress.exe' or proc.name == 'DtPlay.exe':
                    self._status = "Playing"
                    self.logger.error("Already playing {}, stopping before start of test".format(proc.name))
                    proc.kill()
                # else:
                #     self.logger.info("Process is not already playing. Continue with test.")

        return self._status


    def start_run(self, stream_file, clients):
        """
        """
        if self.counter == clients:
            command = APP_PATH + ' ' + stream_file + ' ' + STREAM_SPECS
            print("yeeeeeeeee")
            super(StreamPlayer, self).start_run(command, False)

        for proc in psutil.process_iter():
            if proc.name == 'DtPlay.exe':
                self._status = "Playing"
                self.stream = stream_file
                self.logger.info('Command being run:' + command)
            else:
                if self.counter == clients:
                    super(StreamPlayer, self).start_run(command, False)



    def stop_run(self):
        if self.proc:
            super(StreamPlayer, self).stop_run()
            self._status = "Stopped"
            self.logger.info("Stream Stopped111")
        else:
            for proc in psutil.process_iter():
                if proc.name == 'StreamXpress.exe' or proc.name == 'DtPlay.exe':
                    self.logger.info("The process is:" + proc)
                    proc.kill()
                    self._status = "Stopped"
                    self.stream = "No stream selected"
                    self.counter = 0
                    self.logger.info("Stream Stopped")


    @property
    def streams(self):
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(STREAMS_LOC):
            for f_name in f:
                if f_name.endswith('.ts'):
                    files.append(f_name)

        # with os.scandir(STREAMS_LOC) as entries:
        #     for entry in entries:
        #         if entry.is_dir():
        #             files.append(entry.name)

        return files

        # for f in files:
        #     print(f)

        # elif self._status == "Playing":
        #     try:
        #         for proc in psutil.process_iter():
        #             if (proc.name() == 'StreamXpress.exe' or proc.name() == 'DtPlay.exe'):
        #                 print proc
        #                 proc.kill()
        #                 print stoppedd
        #                 self._status = "Stopped"
        #                 self.logger.info("Stream Stopped")
        #     except Exception as exc:
        #         self.logger.error("cannot stop {}".format(exc))
        #         traceback.format_exc()
        #         self.logger.error("Stream player couldn't be stopped")

# from win32com.client import GetObject
# WMI = GetObject('winmgmts:')
# processes = WMI.InstancesOf('Win32_Process')

# if "python.exe" in [process.Properties_('Name').Value for process in processes]:
#     #do the thing

# s = subprocess.check_output('tasklist', shell=True)
# if "cmd.exe" in s:
#     print s

# s = subprocess.check_output('tasklist', shell=True)
# for app_name in ("StreamXpress.exe *32"):
#     if app_name in s:
#         os.system("taskkill /f /im StreamXpress.exe")

# for proc in psutil.process_iter():
#     if proc.name() == "StreamXpress.exe"
#         self.logger.info("Killing StreamXpress as open on computer.")

# raise Exception("Streamplayer is not running so cant stop it")

# s = subprocess.check_output('tasklist', shell=True)
# if not (DtPlay.exe) in s:
