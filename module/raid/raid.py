import numpy as np

from module.campaign.run import OCR_OIL
from module.combat.assets import *
from module.combat.combat import Combat
from module.exception import ScriptError
from module.logger import logger
from module.map.map_operation import MapOperation
from module.ocr.ocr import DigitCounter
from module.raid.assets import *
from module.ui.assets import RAID_CHECK


class OilExhausted(Exception):
    pass


class RaidCounter(DigitCounter):
    def pre_process(self, image):
        image = super().pre_process(image)
        image = np.pad(image, ((2, 2), (0, 0)), mode='constant', constant_values=255)
        return image


def raid_name_shorten(name):
    """
    Args:
        name (str): Raid name, such as raid_20200624, raid_20210708.

    Returns:
        str: Prefix of button name, such as ESSEX, SURUGA.
    """
    if name == 'raid_20200624':
        return 'ESSEX'
    elif name == 'raid_20210708':
        return 'SURUGA'
    elif name == 'raid_20220127':
        return 'BRISTOL'
    else:
        raise ScriptError(f'Unknown raid name: {name}')


def raid_entrance(raid, mode):
    """
    Args:
        raid (str): Raid name, such as raid_20200624, raid_20210708.
        mode (str): easy, normal, hard

    Returns:
        Button:
    """
    key = f'{raid_name_shorten(raid)}_RAID_{mode.upper()}'
    try:
        return globals()[key]
    except KeyError:
        raise ScriptError(f'Raid entrance asset not exists: {key}')


def raid_ocr(raid, mode):
    """
    Args:
        raid (str): Raid name, such as raid_20200624, raid_20210708.
        mode (str): easy, normal, hard

    Returns:
        RaidCounter:
    """
    raid = raid_name_shorten(raid)
    key = f'{raid}_OCR_REMAIN_{mode.upper()}'
    try:
        button = globals()[key]
        if raid == 'ESSEX':
            return RaidCounter(button, letter=(57, 52, 255), threshold=128)
        elif raid == 'SURUGA':
            return RaidCounter(button, letter=(49, 48, 49), threshold=128)
        elif raid == 'BRISTOL':
            return RaidCounter(button, letter=(214, 231, 219), threshold=128)
    except KeyError:
        raise ScriptError(f'Raid entrance asset not exists: {key}')


class Raid(MapOperation, Combat):
    def combat_preparation(self, balance_hp=False, emotion_reduce=False, auto=True, fleet_index=1):
        """
        Args:
            balance_hp (bool):
            emotion_reduce (bool):
            auto (bool):
            fleet_index (int):
        """
        logger.info('Combat preparation.')
        oil_checked = False

        if emotion_reduce:
            self.emotion.wait(fleet_index)

        while 1:
            self.device.screenshot()

            if self.appear(BATTLE_PREPARATION):
                if self.handle_combat_automation_set(auto=auto == 'combat_auto'):
                    continue
                if not oil_checked and self.config.StopCondition_OilLimit:
                    self.ensure_combat_oil_loaded()
                    oil = OCR_OIL.ocr(self.device.image)
                    oil_checked = True
                    if oil < self.config.StopCondition_OilLimit:
                        logger.hr('Triggered oil limit')
                        raise OilExhausted
            if self.handle_raid_ticket_use():
                continue
            if self.handle_retirement():
                continue
            if self.handle_combat_low_emotion():
                continue
            if self.appear_then_click(BATTLE_PREPARATION, interval=2):
                continue
            if self.handle_combat_automation_confirm():
                continue
            if self.handle_story_skip():
                continue

            # End
            if self.is_combat_executing():
                if emotion_reduce:
                    self.emotion.reduce(fleet_index)
                break

    def handle_raid_ticket_use(self):
        """
        Returns:
            bool: If clicked.
        """
        if self.appear(TICKET_USE_CONFIRM, offset=(30, 30), interval=1):
            if self.config.Raid_UseTicket:
                self.device.click(TICKET_USE_CONFIRM)
            else:
                self.device.click(TICKET_USE_CANCEL)
            return True

        return False

    def raid_enter(self, mode, raid, skip_first_screenshot=True):
        """
        Args:
            mode:
            raid:
            skip_first_screenshot:

        Pages:
            in: page_raid
            out: BATTLE_PREPARATION
        """
        entrance = raid_entrance(raid=raid, mode=mode)
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.appear_then_click(entrance, offset=(10, 10), interval=5):
                continue
            if self.appear_then_click(RAID_FLEET_PREPARATION, interval=5):
                continue

            # End
            if self.combat_appear():
                break

    def raid_expected_end(self):
        return self.appear(RAID_CHECK, offset=(30, 30))

    def raid_execute_once(self, mode, raid):
        """
        Args:
            mode:
            raid:

        Returns:
            in: page_raid
            out: page_raid
        """
        logger.hr('Raid Execute')
        self.config.override(
            Campaign_Name=f'{raid}_{mode}',
            Campaign_UseAutoSearch=False,
            Fleet_FleetOrder='fleet1_all_fleet2_standby'
        )
        self.emotion.check_reduce(1)

        self.raid_enter(mode=mode, raid=raid)
        self.combat(balance_hp=False, expected_end=self.raid_expected_end)
        logger.hr('Raid End')
