'''
RUN TEST LOCALLY
NOT USED IN AUTOMATION FRAMEWORK
AUTHOR: GEORGIA BLANCO-LITCHFIELD GBL06
'''

from automationframework.autotest.base.template import Template
from automationframework.autotest.base.decorators import step
import time
import importlib
import requests
import verify_function as cdb
from config import Config

SERVER_NAME = Config['serverName']
STB_SERVER_NAME = Config['STBserverName']
EXTRACTOR_REPORTS = Config['extractorReports']

class Test():
    def __init__(self, logger, ip, slotId):
        self.logger = createFileLogger(LOG_FILE + logger + '.log')
        self.ip = ip
        self.slotID = slotId

    def runtest(self, slotID, ip):
        '''
        '''

        self.logger.info("Test Begin")
        for testcase in self.test_tree.getroot():
            self.logger.info("Testcases:%s,%s", testcase.tag, testcase.text)

            for test in testcase:
                if test.tag == 'teststep':
                    self.logger.info("Teststep: %s", test.attrib)
                for teststeps in test:
                    if teststeps.tag == 'action':
                        if teststeps.text == 'PLAY_STREAM':
                            self.play_stream(test)
                        elif teststeps.text == 'WAIT':
                            self.wait(test)
                        elif teststeps.text == 'EXTRACT_STB':
                            self.extract_stb(test, ip, slotID)
                        elif teststeps.text == 'VERIFY':
                            self.verify(test, slotID)
                        elif teststeps.text == 'COMMAND':
                            self.command(test, slotID)

        requests.get(SERVER_NAME + 'stopstream', timeout=60)
        self.logger.info(threading.enumerate())

    def play_stream(self, _clients, stream_name):
        self.logger.info("Playing stream: " + stream_name + " for " + _clients + "clients")
        requests.get(SERVER_NAME + 'startstream?clients=' + _clients + '&stream=' + stream_name, timeout=60)

        resp = requests.get(SERVER_NAME + 'startstream?clients=' + _clients + '&stream=' + stream_name, timeout=60)

        self.logger.info("The content of the request is:" + resp.content)

        if resp.ok:
            self.logger.info("Play stream server worked")
            return True
        else:
            self.logger.error("Player stream server did not work")
            return False

    def wait(self, wait_time):
        self.logger.info("Wait for step to be completed")  # will be removed
        time.sleep(int(wait_time) * 60)
        return True

    def extract_stb(self):
        self.logger.info("Extracting STB")
        requests.get(STB_SERVER_NAME + 'stbExtract?ip=' + "192.168.0.106" + '&report_no=' + str(int(self.slotId)), timeout=60)

        resp = requests.get(STB_SERVER_NAME + 'stbExtract?ip=' + self.ip + '&report_no=' + str(int(self.slotId)), timeout=60)
        if resp.ok:
            self.logger.info("Extract STB complete")
            return True
        else:
            self.logger.error("Unable to extract STB")
            return False

    def verify_para(self, attribute, exp_value):
        self.logger.info("Verification of top paragraph value")
        print(EXTRACTOR_REPORTS + "cdb_report" + str(int(stb.slotId)) + ".html")
        value_to_be_verified = cdb.get_value_from_para(
                            EXTRACTOR_REPORTS + "cdb_report" + str(int(self.slotId)) + ".html",
                            attribute)
        self.logger.info('%s', attribute)
        if exp_value != value_to_be_verified:
            self.logger.error("Teststep verification Failed")
            self.logger.info("Expecting: %s=%s, but, found %s=%s", attribute, exp_value,
                             attribute, value_to_be_verified)
            self.logger.info("Ending test")
            #requests.get(SERVER_NAME + 'stopstream')

        else:
            self.logger.info("Teststep verification passed")
            return True

    def verify_table(self, header, unique_id, column, exp_value):
        self.logger.info("Verification of table values")

        value_to_be_verified = cdb.get_value_from_row(
                EXTRACTOR_REPORTS + "cdb_report" + str(int(stb.slotId)) + ".html", header, unique_id,
                column)
        if exp_value != value_to_be_verified:
            self.logger.error("Teststep verification Failed")
            self.logger.info("Expecting: %s=%s, but, found %s=%s", column, exp_value,
                                 column, value_to_be_verified)
                #requests.get(SERVER_NAME + 'stopstream')
        else:
            self.logger.info("Teststep verification passed")
            return True

    def verify_under_table(self, header, attribute, exp_value):
        self.logger.info("Verification of value under table")

        value_to_be_verified = cdb.get_value_under_table(
            EXTRACTOR_REPORTS + "cdb_report" + str(int(stb.slotId)) + ".html", header, attribute)
        if exp_value != value_to_be_verified:
            self.logger.error("Teststep verification Failed")
            self.logger.info("Expecting: %s %s=%s, but, found %s=%s", header, attribute, exp_value,
                            header, value_to_be_verified)
            self.logger.info("Ending test")
            #requests.get(SERVER_NAME + 'stopstream')

        else:
            self.logger.info("Teststep verification passed")
            return True


    def command(self, command_type, name_of_command):
        rcu = Remote(Config['ipRCU'], Config['portRCU'], self.logger)
        self.logger.info("Perform Command")

        if command_type == 'common':
            lib = importlib.import_module('autosmart.templates.common')
            step = lib.__dict__[name_of_command]
            instance = step(self.logger, stb.slotId)
            instance.execute(rcu)
            return True
        elif command_type == 'rcu':
            rcu.operate(name_of_command, stb.slotId, 2)
            return True
        else:
            self.logger.info("Incorrect parameter, must be either common or rcu")


class StopStream(Template):
    """
    Playout prerecorded stream
    """
    TAG = "play stream"

    def __init__(self):
        Template.__init__(self)

        self.addDescription(self.NAME_DESC,
                            'Stopping stream')

        self.addDescription(self.EXP_DESC,
                            'Stopping stream')

        self.addDescription(self.PASS_DESC,
                            'Stream successfully stopped')

        self.addDescription(self.FAIL_DESC,
                            'Stream did not stop')

    def executeCore(self, stb, status):

        self.logger.info('Stopping stream')
        requests.get(SERVER_NAME + 'stopstream')

        resp = requests.get(SERVER_NAME + 'stopstream')
        if resp.ok:
            self.logger.info("Stopping stream complete")
            return True
        else:
            self.logger.error("Unable to stop stream")
            return False



# import sys
# import getopt  # ????
# import time
# import logging
# import threading
# import importlib
# import requests
# import json
# import xml.etree.ElementTree as et
# from multiprocessing import Process
# from argparse import ArgumentParser
# from autosmart.utils.utils import createFileLogger
# import function as cdb
# from autosmart.config.config import Config
# from autosmart.rcu import Remote
# import autosmart.templates.common
#
# #from socketIO_client import SocketIO
#
#
# LOG_FILE = Config['runtestLog']
# TEST_FOLDER = Config['testFolder']
# BOX_FOLDER = Config['boxFolder']
# SERVER_NAME = Config['serverName']
# STB_SERVER_NAME = Config['STBserverName']
# RCU_LOG = Config['rcuLog']
# EXTRACTOR_REPORTS = Config['extractorReports']
#
# class Test():
#     def __init__(self, test_tree, logger):
#         self.logger = createFileLogger(LOG_FILE + logger + '.log')
#         self.test_tree = et.parse(TEST_FOLDER + test_tree + '.xml')
#
#     def runtest(self, slotID, ip):
#         '''
#         '''
#
#         self.logger.info("Test Begin")
#         for testcase in self.test_tree.getroot():
#             self.logger.info("Testcases:%s,%s", testcase.tag, testcase.text)
#
#             for test in testcase:
#                 if test.tag == 'teststep':
#                     self.logger.info("Teststep: %s", test.attrib)
#                 for teststeps in test:
#                     if teststeps.tag == 'action':
#                         if teststeps.text == 'PLAY_STREAM':
#                             self.play_stream(test)
#                         elif teststeps.text == 'WAIT':
#                             self.wait(test)
#                         elif teststeps.text == 'EXTRACT_STB':
#                             self.extract_stb(test, ip, slotID)
#                         elif teststeps.text == 'VERIFY':
#                             self.verify(test, slotID)
#                         elif teststeps.text == 'COMMAND':
#                             self.command(test, slotID)
#
#         requests.get(SERVER_NAME + 'stopstream', timeout=60)
#         self.logger.info(threading.enumerate())
#
#     def play_stream(self, test):
#         self.logger.info("Play Stream")
#         parameters = []
#         for teststeps in test:
#             # logger.info("Reading params: %s,%s,%s", teststeps.tag, teststeps.attrib, teststeps.text)
#             if teststeps.tag == 'parameter':
#                 parameters.append(teststeps.text)
#         self.logger.info(parameters[0] + " and " + parameters[1])
#
#         # with SocketIO('localhost', 5000) as socketIO:
#         #     socketIO.emit('Ready to play')
#
#         requests.get(SERVER_NAME + 'startstream?folder=' + parameters[0] + '&stream=' + parameters[1], timeout=60)
#         self.logger.info("server done")
#
#         return True
#
#     def wait(self, test):
#         self.logger.info("Wait for step to be completed")  # will be removed
#         for teststeps in test:
#             # logger.info("Reading params: %s,%s,%s", teststeps.tag, teststeps.attrib, teststeps.text)
#             if teststeps.tag == 'parameter':
#                 wait_time = teststeps.text
#                 time.sleep(int(wait_time) * 60)
#         return True
#
#     def extract_stb(self, test, ip, slotID):
#         self.logger.info("Extract STB")
#
#         requests.get(STB_SERVER_NAME + 'stbExtract?ip=' + ip + '&report_no=' + str(int(slotID)), timeout=60)
#         return True
#
#     def verify(self, test, slotID):
#         self.logger.info("Verify")
#         parameters = []
#         for teststeps in test:
#             # logger.info("Reading params: %s,%s,%s", teststeps.tag, teststeps.attrib, teststeps.text)
#             if teststeps.tag == 'parameter':
#                 parameters.append(teststeps.text)
#
#         if parameters[0] == 'para':
#             value_to_be_verified = cdb.get_value_from_para(
#                 EXTRACTOR_REPORTS + "cdb_report" + str(int(slotID)) + ".html",
#                 parameters[1])  # E:/GeorgiaAdSmart/AutoSmart/work/Python/autosmart/servers/stbreports/cdb_report1.html
#             self.logger.info('%s', parameters[1])
#             if parameters[2] != value_to_be_verified:
#                 self.logger.error("Teststep verification Failed !!!")
#                 self.logger.info("Expecting: %s=%s, but, found %s=%s", parameters[1], parameters[2],
#                                  parameters[1], value_to_be_verified)
#                 self.logger.info("Ending test")
#
#             else:
#                 self.logger.info("Teststep verification passed")
#
#         if parameters[0] == 'table':
#             value_to_be_verified = cdb.get_value_from_row(EXTRACTOR_REPORTS + "cdb_report" + str(int(slotID)) + ".html",
#                                                           parameters[1], parameters[2], parameters[3])
#             if parameters[4] != value_to_be_verified:
#                 self.logger.error("Teststep verification Failed !!!")
#                 self.logger.info("Expecting: %s=%s, but, found %s=%s", parameters[3], parameters[4],
#                                  parameters[3], value_to_be_verified)
#                 # stop test
#             else:
#                 self.logger.info("Teststep verification passed")
#
#         if parameters[0] == 'under table':
#             value_to_be_verified = cdb.get_value_under_table(
#                 EXTRACTOR_REPORTS + "cdb_report" + str(int(slotID)) + ".html", parameters[1], parameters[2])
#             if parameters[3] != value_to_be_verified:
#                 self.logger.error("Teststep verification Failed !!!")
#                 self.logger.info("Expecting: %s %s=%s, but, found %s=%s", parameters[1], parameters[2], parameters[3],
#                                  parameters[1], value_to_be_verified)
#                 self.logger.info("Ending test")
#
#             else:
#                 self.logger.info("Teststep verification passed")
#
#     def command(self, test, slotID):
#         parameters = []
#         rculog = createFileLogger(RCU_LOG)
#         rcu = Remote(Config['ipRCU'], Config['portRCU'], rculog)
#
#         for teststeps in test:
#             self.logger.info("Reading params: %s,%s,%s", teststeps.tag, teststeps.attrib, teststeps.text)
#             if teststeps.tag == 'parameter':
#                 parameters.append(teststeps.text)
#         if parameters[0] == 'common':
#             lib = importlib.import_module('autosmart.templates.common')
#             step = lib.__dict__[parameters[1]]
#             instance = step(self.logger, slotID)
#             instance.execute(rcu)
#             return True
#         elif parameters[0] == 'rcu':
#             rcu.operate(parameters[1], slotID, 2)
#             return True
#         else:
#             self.logger.info("Incorrect parameter, must be either common or rcu")
#
#
#
#
# class TestRunner():
#     def __init__(self):
#         None
#
#     @property
#     def build_parser(self):
#         parser = ArgumentParser()
#         parser.add_argument("-t", "--test", dest="testname",
#                             help="Test to be completed")
#         parser.add_argument("-o", "--output", dest="logstore",
#                             help="results and log store")
#         parser.add_argument("-b", "--box", dest="box_file",
#                             help="box ip and soltID/report number")
#         return parser
#
#     def run(self, slotID, ip, test, log):
#         t = Test(test, log + slotID)
#         t.runtest(slotID, ip)
#
#     def individualTests(self):
#         parser = self.build_parser
#         args = parser.parse_args()
#
#         # for proc in psutil.process_iter():
#         #     print proc
#
#         print("Get status")
#         resp = requests.get(SERVER_NAME + "status", timeout=60)
#         print resp.content
#         if resp.ok:
#             json_resp = resp.json()
#             json_resp["data"]
#             data = json_resp.get("data", None)
#             if data is None:
#                 print(json_resp.get("error"))
#
#             if resp.json()["data"]["status"] == "Playing":
#                 print('stopping streammmm')
#                 requests.get(SERVER_NAME + 'stopstream', timeout=60)
#
#         print("Load boxes info")
#         test_boxes = BOX_FOLDER + args.box_file + '.json'
#
#         with open(test_boxes) as test_file:
#             json_data = json.load(test_file)
#             for key, val in json_data.items():
#                 print("Stb details: {}:{}".format(key, val))
#                 proc = Process(target=self.run, args=(key, val, args.testname, args.logstore))
#                 print("starting proc:{}".format(proc))
#                 proc.start()
#
#             print("Wait for all of tests to finish")
#             proc.join()
#             print("Finished!")
#
#
# if __name__ == "__main__":
#     TestRunner().individualTests()
#
# # python runtest.py -t firstfeature -o autosmart -b boxips
#
#
# #        s = subprocess.check_output('tasklist', shell=True)
# #        for app_name in ("DtPlay.exe", "StreamXpress.exe"):
# #            if app_name in s:
# #                resp = requests.get(SERVER_NAME + 'stopstream', timeout=60)
# #                if res.ok:
# #                    break
#
#
# # class Test():
# #     def __init__(self, test_tree, logger):
# #         self.logger = createFileLogger(LOG_FILE + logger + '.log')
# #         self.test_tree = et.parse(TEST_FOLDER + test_tree + '.xml')
# #
# #     def runtest(self, slotID, ip):
# #         '''
# #         '''
# #
# #         self.logger.info("Test Begin")
# #         for testcase in self.test_tree.getroot():
# #             self.logger.info("Testcases:%s,%s", testcase.tag, testcase.text)
# #
# #             for test in testcase:
# #                 if test.tag == 'teststep':
# #                     self.logger.info("Teststep: %s", test.attrib)
# #                 for teststeps in test:
# #                     if teststeps.tag == 'action':
# #                         if teststeps.text == 'PLAY_STREAM':
# #                             self.play_stream(test)
# #                         elif teststeps.text == 'WAIT':
# #                             self.wait(test)
# #                         elif teststeps.text == 'EXTRACT_STB':
# #                             self.extract_stb(test, ip, slotID)
# #                         elif teststeps.text == 'VERIFY':
# #                             self.verify(test, slotID)
# #                         elif teststeps.text == 'COMMAND':
# #                             self.command(test, slotID)
# #
# #         requests.get(SERVER_NAME + 'stopstream', timeout=60)
# #         self.logger.info(threading.enumerate())
# #
# #     def play_stream(self, test):
# #         self.logger.info("Play Stream")
# #         parameters = []
# #         for teststeps in test:
# #             # logger.info("Reading params: %s,%s,%s", teststeps.tag, teststeps.attrib, teststeps.text)
# #             if teststeps.tag == 'parameter':
# #                 parameters.append(teststeps.text)
# #         self.logger.info(parameters[0] + " and " + parameters[1])
# #
# #         # with SocketIO('localhost', 5000) as socketIO:
# #         #     socketIO.emit('Ready to play')
# #
# #         requests.get(SERVER_NAME + 'startstream?folder=' + parameters[0] + '&stream=' + parameters[1], timeout=60)
# #         self.logger.info("server done")
# #
# #         return True
# #
# #     def wait(self, test):
# #         self.logger.info("Wait for step to be completed")  # will be removed
# #         for teststeps in test:
# #             # logger.info("Reading params: %s,%s,%s", teststeps.tag, teststeps.attrib, teststeps.text)
# #             if teststeps.tag == 'parameter':
# #                 wait_time = teststeps.text
# #                 time.sleep(int(wait_time) * 60)
# #         return True
# #
# #     def extract_stb(self, test, ip, slotID):
# #         self.logger.info("Extract STB")
# #
# #         requests.get(STB_SERVER_NAME + 'stbExtract?ip=' + ip + '&report_no=' + str(int(slotID)), timeout=60)
# #         return True
# #
# #     def verify(self, test, slotID):
# #         self.logger.info("Verify")
# #         parameters = []
# #         for teststeps in test:
# #             # logger.info("Reading params: %s,%s,%s", teststeps.tag, teststeps.attrib, teststeps.text)
# #             if teststeps.tag == 'parameter':
# #                 parameters.append(teststeps.text)
# #
# #         if parameters[0] == 'para':
# #             value_to_be_verified = cdb.get_value_from_para(
# #                 EXTRACTOR_REPORTS + "cdb_report" + str(int(slotID)) + ".html",
# #                 parameters[1])  # E:/GeorgiaAdSmart/AutoSmart/work/Python/autosmart/servers/stbreports/cdb_report1.html
# #             self.logger.info('%s', parameters[1])
# #             if parameters[2] != value_to_be_verified:
# #                 self.logger.error("Teststep verification Failed !!!")
# #                 self.logger.info("Expecting: %s=%s, but, found %s=%s", parameters[1], parameters[2],
# #                                  parameters[1], value_to_be_verified)
# #                 self.logger.info("Ending test")
# #
# #             else:
# #                 self.logger.info("Teststep verification passed")
# #
# #         if parameters[0] == 'table':
# #             value_to_be_verified = cdb.get_value_from_row(EXTRACTOR_REPORTS + "cdb_report" + str(int(slotID)) + ".html",
# #                                                           parameters[1], parameters[2], parameters[3])
# #             if parameters[4] != value_to_be_verified:
# #                 self.logger.error("Teststep verification Failed !!!")
# #                 self.logger.info("Expecting: %s=%s, but, found %s=%s", parameters[3], parameters[4],
# #                                  parameters[3], value_to_be_verified)
# #                 # stop test
# #             else:
# #                 self.logger.info("Teststep verification passed")
# #
# #         if parameters[0] == 'under table':
# #             value_to_be_verified = cdb.get_value_under_table(
# #                 EXTRACTOR_REPORTS + "cdb_report" + str(int(slotID)) + ".html", parameters[1], parameters[2])
# #             if parameters[3] != value_to_be_verified:
# #                 self.logger.error("Teststep verification Failed !!!")
# #                 self.logger.info("Expecting: %s %s=%s, but, found %s=%s", parameters[1], parameters[2], parameters[3],
# #                                  parameters[1], value_to_be_verified)
# #                 self.logger.info("Ending test")
# #
# #             else:
# #                 self.logger.info("Teststep verification passed")
# #
# #     def command(self, test, slotID):
# #         parameters = []
# #         rculog = createFileLogger(RCU_LOG)
# #         rcu = Remote(Config['ipRCU'], Config['portRCU'], rculog)
# #
# #         for teststeps in test:
# #             self.logger.info("Reading params: %s,%s,%s", teststeps.tag, teststeps.attrib, teststeps.text)
# #             if teststeps.tag == 'parameter':
# #                 parameters.append(teststeps.text)
# #         if parameters[0] == 'common':
# #             lib = importlib.import_module('autosmart.templates.common')
# #             step = lib.__dict__[parameters[1]]
# #             instance = step(self.logger, slotID)
# #             instance.execute(rcu)
# #             return True
# #         elif parameters[0] == 'rcu':
# #             rcu.operate(parameters[1], slotID, 2)
# #             return True
# #         else:
# #             self.logger.info("Incorrect parameter, must be either common or rcu")
