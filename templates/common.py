'''
COMMON COMMANDS - NOT USED IN AUTOMATION FRAMEWORK
AUTHOR: GEORGIA BLANCO-LITCHFIELD GBL06
'''

from autosmart.rcu import Remote
from autosmart_v2.utils.utils import createFileLogger
from autosmart_v2.config.config import Config
import automationframework.sut.stb.base.actionnames as ACTIONS
from automationframework.autotest.base.template import Template

RCU_LOG = Config['rcuLog']
logger = createFileLogger(RCU_LOG)


'''
Check tune HD for correct way of formatting each template!!!!!!!!!
'''


# class Template():
#     """
#     Base class for steps
#     """
#
#     def __init__(self):
#         None
#
#     def execute(self, stb):
#         """
#         """
#         status = self.executeCore(stb)
#         return status
#
#     def executeCore(self, stb):
#         raise NotImplmentedError("Template::execute")


class FSR(Template):
    """
    Perform FSR for stb
    """
    TAG = "fsr"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('FSR being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate(ACTIONS.HOME, {"delay": 2})
        stb.operate(ACTIONS.HOME, {"delay": 1})
        for x in range(12):
            stb.operate(ACTIONS.DOWN, {"delay": 1})
        stb.operate(ACTIONS.NUM_0, {"delay": 1})
        stb.operate(ACTIONS.NUM_0, {"delay": 1})
        stb.operate(ACTIONS.NUM_1, {"delay": 1})
        stb.operate(ACTIONS.SELECT, {"delay": 1})
        for x in range(2):
            stb.operate(ACTIONS.DOWN, {"delay": 1})
        stb.operate(ACTIONS.RIGHT, {"delay": 1})
        stb.operate(ACTIONS.DOWN, {"delay": 1})
        stb.operate(ACTIONS.SELECT, {"delay": 1})
        stb.operate(ACTIONS.LEFT, {"delay": 1})
        stb.operate(ACTIONS.SELECT, {"delay": 1})

        return True


class PowerUp(Template):
    """
    Perform Power up for stb
    """
    TAG = "powerUp"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('Power up from standby exccuted')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Home', self.slotID, 2)
        stb.operate('Back', self.slotID, 1)

        return True


class TuneHD(Template):
    """
    Perform tunig to HD AdSmrt channel 561 for stb
    """
    TAG = "hd"

    def __init__(self):
        Template.__init__(self)
        logger.info('Tune to channel 561 HD being executed')

    def executeCore(self, stb, status):
        stb.operate(ACTIONS.HOME, timeParams={"delay": 2})
        stb.operate(ACTIONS.BACK, timeParams={"delay": 1})
        stb.operate(ACTIONS.NUM_5, timeParams={"delay": 1})
        stb.operate(ACTIONS.NUM_6, timeParams={"delay": 1})
        stb.operate(ACTIONS.NUM_1, timeParams={"delay": 1})
        return True


class TuneSD(Template):
    """
    Perform tunig to SD AdSmrt channel 531 for stb
    """
    TAG = "fsr"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('Tune to channel 531 SD being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Home', self.slotID, 5)
        stb.operate('Back', self.slotID, 1)
        stb.operate('5', self.slotID, 1)
        stb.operate('3', self.slotID, 1)
        stb.operate('1', self.slotID, 1)

        return True


class PlayRec(Template):
    """
    Perform Play out a recording for stb
    """
    TAG = "playRec"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('Play out recording being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Sky', self.slotID, 1)
        stb.operate('Right', self.slotID, 1)
        stb.operate('Select', self.slotID, 1)
        stb.operate('Select', self.slotID, 1)

        return True


class StopRec(Template):
    """
    Perform Play out a recording for stb
    """
    TAG = "stopRec"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('Stop recording being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Back', self.slotID, 1)
        stb.operate('Back', self.slotID, 1)

        return True


class DeleteRec(Template):
    """
    Perform delete a recording for stb
    """
    TAG = "deleteRec"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('Delete recording being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Sky', self.slotID, 3)
        stb.operate('Right', self.slotID, 1)
        stb.operate('Select', self.slotID, 1)
        stb.operate('Right', self.slotID, 1)
        stb.operate('Down', self.slotID, 1)
        stb.operate('Select', self.slotID, 1)
        for x in range(6):
            stb.operate('Down', self.slotID, 1)
        stb.operate('Right', self.slotID, 1)
        for x in range(2):
            stb.operate('Down', self.slotID, 1)
        for x in range(2):
            stb.operate('Right', self.slotID, 1)
        stb.operate('Down', self.slotID, 1)
        stb.operate('Select', self.slotID, 1)
        stb.operate('Home', self.slotID, 1)
        stb.operate('Back', self.slotID, 1)

        return True


class FFx2(Template):
    """
    Perform FFX2 for stb
    """
    TAG = "FFx2"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('FFx2 being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Forward', self.slotID, 1)

        return True


class FFx6(Template):
    """
    Perform FFX6 for stb
    """
    TAG = "FFx6"

    def __init__(self, logger):
        Template.__init__(self, logger, slotID)
        self.logger.info('FFx6 being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Forward', self.slotID, 1)
        stb.operate('Forward', self.slotID, 1)

        return True


class FFx12(Template):
    """
    Perform FFX12 for stb
    """
    TAG = "FFx12"

    def __init__(self, logger):
        Template.__init__(self, logger, slotID)
        self.logger.info('FFx12 being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Forward', self.slotID, 1)
        stb.operate('Forward', self.slotID, 1)
        stb.operate('Forward', self.slotID, 1)
        return True


class FFx30(Template):
    """
    Perform FFX30 for stb
    """
    TAG = "FFx30"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('FFx30 being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Forward', self.slotID, 1)
        stb.operate('Forward', self.slotID, 1)
        stb.operate('Forward', self.slotID, 1)
        stb.operate('Forward', self.slotID, 1)

        return True


class RWx2(Template):
    """
    Perform RWX2 for stb
    """
    TAG = "RWx2"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('RWx2 being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Rewind', self.slotID, 1)

        return True


class RWx6(Template):
    """
    Perform RWX6 for stb
    """
    TAG = "RWx6"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('RWx6 being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Rewind', self.slotID, 1)
        stb.operate('Rewind', self.slotID, 1)

        return True


class RWx12(Template):
    """
    Perform RWX12 for stb
    """
    TAG = "RWx12"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('RWx12 being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Rewind', self.slotID, 1)
        stb.operate('Rewind', self.slotID, 1)
        stb.operate('Rewind', self.slotID, 1)

        return True


class RWx30(Template):
    """
    Perform RWX30 for stb
    """
    TAG = "RWx30"

    def __init__(self, logger, slotID):
        Template.__init__(self, logger)
        self.logger.info('RWx30 being executed')
        self.slotID = slotID

    def executeCore(self, stb):
        stb.operate('Rewind', self.slotID, 1)
        stb.operate('Rewind', self.slotID, 1)
        stb.operate('Rewind', self.slotID, 1)
        stb.operate('Rewind', self.slotID, 1)

        return True


'''
if __name__ == "__main__":

    rcu = Remote(Config['ipRCU'], Config['portRCU'], '03', rculog)

    step = TuneSD(rculog)

    step.execute(rcu)
'''

# step = FSR()
# step.execute(rcu)


# rcu = Remote(Config['ipRCU'], Config['portRCU'], '03')
# rcu.operate('Sky', 2)
# rcu.operate('Back', 0.5)
