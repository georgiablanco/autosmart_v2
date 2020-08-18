'''
STB EXTRACTOR SERVER
CREATOR: GBL06
'''

import psutil
import os
from flask import Flask, request, jsonify
from autosmart_v2.runner import Runner
from autosmart_v2.utils.utils import createFileLogger
from autosmart_v2.config.config import Config

VERSION = 1.2
LOG_FILE = Config['stbserverLog']
APP_PATH = Config['stbappPath']
REPORT_PATH = Config['extractorReports']

logger = createFileLogger(LOG_FILE)
app = Flask(__name__)

IP_CHANGE = {
    "10.184.130.78": "192.168.0.100", #TITAN
    "10.184.130.81": "192.168.1.102", #XWING
    "10.184.130.13": "192.168.2.102", #FALCONV2
    "10.184.130.12": "192.168.3.100" #FALCOND1
}


@app.route('/stbExtract', methods=['GET'])
def stbExtract():
    # ip = IP_CHANGE[str(request.args['ip'])]
    ip_recieved = request.args['ip']
    ip = str(ip_recieved)
    report_no = request.args['report_no']
    dos_command = APP_PATH + " get_report " + IP_CHANGE[ip] + " stbreports " + report_no
    response = {}
    print("Stb extract")
    try:
        for proc in psutil.process_iter():
            if proc.name == 'STB_Extractor.exe':
                logger.error('STB Extractor Application running. Ending process')
                proc.kill()

        logger.info('Command being run:' + dos_command)
        extractor_runner = Runner(logger)
        extractor_runner.start_run(dos_command, False)
        logger.info('Command successful')
        response["data"] = {
            "name": ip,
            "status": "Report Extracted"
        }
    except Exception as exc:
        logger.error('Command failed')
        response["error"] = {
            "name": ip,
            "status": "Report unable to extract"
        }

    return jsonify(response)


@app.route('/extractorFiles')
def extractor_files():
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(REPORT_PATH):
        for f_name in f:
            if f_name.endswith('.html'):

                files.append(f_name)

    # with os.scandir(STREAMS_LOC) as entries:
    #     for entry in entries:
    #         if entry.is_dir():
    #             files.append(entry.name)

    return files

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9898)

# http://localhost:5000/stbExtract?ip=192.168.3.101&report_no=1
