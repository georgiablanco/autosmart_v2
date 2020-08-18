'''
STREAM EXPRESS SERVER
AUTHOR: GEORGIA BLANCO-LITCHFIELD GBL06
'''


from flask import Flask, request, jsonify
import traceback, os
from autosmart_v2.utils.utils import createFileLogger
from autosmart_v2.streamplayer import StreamPlayer
from autosmart_v2.config.config import Config

VERSION = 1.5
LOG_FILE = Config['streamserverLog']
STREAMS_LOC = Config['streamsLocation']
# DEBUG = os.getenviron("FLASK_DEBUG")
logger = createFileLogger(LOG_FILE)
app = Flask(__name__)


class Controller():
    def __init__(self):
        logger.info("creating")
        self.player = StreamPlayer(
                        name="player1",
                        status="Created",
                        stream="No stream selected",
                        logger=logger,
                        counter = 0
                        )


controller = Controller()


@app.route('/status', methods=['GET'])
def status():
    print("status")
    response = {}

    try:
        controller.player.status()

        response["data"] = {
            "name": controller.player.name,
            "status": controller.player.status,
            "stream": controller.player.stream,
            "clients": controller.player.counter

        }
    except Exception as exc:
        response["error"] = [
            str(exc),
            traceback.format_exc()
        ]

    return jsonify(response)


@app.route('/startstream', methods=['GET'])
def startstream():
    clients = request.args['clients']
    stream_name = request.args['stream'] + '.ts'
    # controller.counter += 1
    logger.info("Starting Stream")
    response = {}
    try:
        for path, dirs, files in os.walk(STREAMS_LOC):
            check_stream = 0
            if stream_name in files:
                check_stream += 1
                stream_path = os.path.join(path, stream_name)
                logger.info('Stream path found:' + stream_name)
                controller.player.counter += 1

                if controller.player.status != "Playing" and controller.player.counter == int(clients):
                    controller.player.start_run(stream_path, int(clients))

                else:
                    logger.info("Stream player is already playing. Attempting to stop the stream and restart")
                    controller.player.stop_run()
                    logger.info("we are here")
                    controller.player.start_run(stream_path, controller.player.counter)
                    response["data"] = {
                        "name": controller.player.name,
                        "status": controller.player.status,
                        "stream path": stream_path,
                        "stream": controller.player.stream,
                        "clients": controller.player.counter
                         }
            elif check_stream == 0:
                logger.info('No stream found in stream directory.')

    except Exception as exc:
        response["error"] = [
            str(exc),
            traceback.format_exc()
        ]
    # if DEBUG:
    #	raise exc

    return jsonify(response)


@app.route('/stopstream', methods=['GET'])
def stopstream():
    response = {}

    try:
        controller.player.stop_run()
        controller.counter = 0
        response["data"] = {
            "name": controller.player.name,
            "status": controller.player.status,
            "stream": controller.player.stream,
            "clients": controller.player.counter
        }
    except Exception as exc:
        response["error"] = [
            str(exc),
            traceback.format_exc()
        ]
    # if DEBUG:
    #	raise exc

    return jsonify(response)


@app.route('/streams', methods=['GET'])
def streams():
    response = {"data": controller.player.streams}

    return jsonify(response)

@app.route('/system_information')
def server_information():
    response = {
        "System": "StreamXpress Server",
        "Version": VERSION,
        "Uptime": " "
    }

    return jsonify(response)



if __name__ == '__main__':
    #    socket_io.run(app, debug=True, port=5000)
    app.run(debug=True, host='0.0.0.0', port=5000)

# http://localhost:5000/streamexp?folder=L2&stream=V2-AdSmart-Multiple-TPT
