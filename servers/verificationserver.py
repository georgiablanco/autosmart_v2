'''
not complete
VERIFICATION SERVER
AUTHOR: GEORGIA BLANCO-LITCHFIELD GBL06
'''

import traceback
from flask import Flask, request, jsonify
import autosmart_v2.function as cdb
from autosmart_v2.utils.utils import createFileLogger
from autosmart_v2.config.config import Config
from autosmart_v2.config.verification_config import verification_config

VERSION = 1.2
LOG_FILE = Config['verificationserverLog']
EXTRACTOR_REPORTS = Config['extractorReports']

logger = createFileLogger(LOG_FILE)
app = Flask(__name__)



@app.route('/verifyPara', methods=['GET'])
def verifyPara():
    slotId = request.args['slotId']
    attrib  = request.args['attribute']
    attribute = verification_config[attrib]
    exp_value = request.args['exp_value']

    logger.info("Verifying value from top paragraph for slot ID =" + slotId + " attribute =" + attribute + " expected value = " + exp_value)
    # response = {}

    print(EXTRACTOR_REPORTS + "cdb_report" + str(int(slotId)) + ".html")
    path = EXTRACTOR_REPORTS + "cdb_report" + str(int(slotId)) + ".html"
    value_to_be_verified = cdb.get_value_from_para(path, attribute)
    logger.info('%s', attribute)
    if exp_value != value_to_be_verified:
        logger.error("Teststep verification Failed")
        logger.info("Expecting: %s=%s, but, found %s=%s", attribute, exp_value,
                    attribute, value_to_be_verified)
            logger.info("Ending test")
            response = "incorrect"

        else:
            logger.info("Teststep verification passed")
            response = "correct"

    return response

    # try:
    #     print(EXTRACTOR_REPORTS + "cdb_report" + str(int(slotId)) + ".html")
    #     path = EXTRACTOR_REPORTS + "cdb_report" + str(int(slotId)) + ".html"
    #     value_to_be_verified = cdb.get_value_from_para(path,
    #                         attribute)
    #     logger.info('%s', attribute)
    #     if exp_value != value_to_be_verified:
    #         logger.error("Teststep verification Failed")
    #         logger.info("Expecting: %s=%s, but, found %s=%s", attribute, exp_value,
    #                          attribute, value_to_be_verified)
    #         logger.info("Ending test")
    #         response = "incorrect"
    #
    #     else:
    #         logger.info("Teststep verification passed")
    #         response = "correct"
    #
    # except Exception as exc:
    #     response["error"] = [
    #         str(exc),
    #         traceback.format_exc()
    #     ]
    #     return jsonify(response)
    # if DEBUG:
    # 	raise exc


@app.route('/verifyTable', methods=['GET'])
def verifyTable():
    slotId = request.args['slotId']
    header = request.args['header']
    unique_id = request.args['unique_id']
    column = request.args['column']
    exp_value = request.args['exp_value']

    logger.info("Verification of table values")
    response = {}
    try:
        value_to_be_verified = cdb.get_value_from_row(
            EXTRACTOR_REPORTS + "cdb_report" + str(int(slotId)) + ".html", header, unique_id,
            column)
        if exp_value != value_to_be_verified:
            logger.error("Teststep verification Failed")
            logger.info("Expecting: %s=%s, but, found %s=%s", column, exp_value,
                         column, value_to_be_verified)
            return False
        else:
            logger.info("Teststep verification passed")
            return True

    except Exception as exc:
        response["error"] = [
            str(exc),
            traceback.format_exc()
        ]
        return jsonify(response)


@app.route('/verifyUnderTable', methods=['GET'])
def verifyUnderTable():
    slotId = request.args['slotId']
    header = request.args['header']
    attribute = request.args['attribute']
    exp_value = request.args['exp_value']
    self.logger.info("Verification of value under table")
    response = {}

    try:
        value_to_be_verified = cdb.get_value_under_table(
                EXTRACTOR_REPORTS + "cdb_report" + str(int(slotId)) + ".html", header, attribute)
        if exp_value != value_to_be_verified:
            logger.error("Teststep verification Failed")
            logger.info("Expecting: %s %s=%s, but, found %s=%s", header, attribute, exp_value,
                             header, value_to_be_verified)
            logger.info("Ending test")
            response = "incorrect"

        else:
            logger.info("Teststep verification passed")
            response = "correct"

    except Exception as exc:
        response["error"] = [
            str(exc),
            traceback.format_exc()
        ]
        return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8989)


