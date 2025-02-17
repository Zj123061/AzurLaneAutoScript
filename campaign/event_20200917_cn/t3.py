from module.logger import logger
from module.map.map_base import CampaignMap
from module.map.map_grids import RoadGrids, SelectedGrids

from .campaign_base import CampaignBase
from .t1 import Config as ConfigBase

MAP = CampaignMap('T3')
MAP.shape = 'I9'
# MAP.camera_data = ['D2', 'D6', 'D7', 'F2', 'F6', 'F7']
# MAP.camera_data_spawn_point = ['D7', 'D6']
MAP.camera_data = ['D3', 'D5', 'D7', 'F3', 'F5', 'F7']
MAP.camera_data_spawn_point = ['D5']
MAP.portal_data = [('I2', 'A1'), ('A1', 'I2'), ('I9', 'H1'), ('H1', 'I9')]
MAP.map_data = """
    -- -- -- ++ ME -- ME -- ++
    -- -- MB ++ -- -- -- -- --
    ++ ++ ++ ++ -- ++ ++ -- ME
    -- MS -- Me -- Me ++ -- --
    ME -- ++ -- __ -- -- -- ME
    -- -- SP -- -- Me ++ ++ ++
    Me -- -- SP ++ -- ++ MB --
    -- MS -- -- -- MS ++ -- --
    ++ -- Me -- ME -- ++ -- --
"""
MAP.map_data_loop = """
    -- -- -- -- ME -- ME -- ++
    -- -- MB -- -- -- -- -- --
    ++ ++ ++ -- -- ++ ++ -- ME
    -- MS -- Me -- Me ++ -- --
    ME -- ++ -- __ -- -- -- ME
    -- -- SP -- -- Me -- -- --
    Me -- -- SP ++ -- ++ MB --
    -- MS -- -- -- MS ++ -- --
    ++ -- Me -- ME -- ++ -- --
"""
MAP.weight_data = """
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 2, 'siren': 1},
    {'battle': 1, 'enemy': 1},
    {'battle': 2, 'enemy': 1},
    {'battle': 3, 'enemy': 1},
    {'battle': 4, 'enemy': 1, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, G1, H1, I1, \
A2, B2, C2, D2, E2, F2, G2, H2, I2, \
A3, B3, C3, D3, E3, F3, G3, H3, I3, \
A4, B4, C4, D4, E4, F4, G4, H4, I4, \
A5, B5, C5, D5, E5, F5, G5, H5, I5, \
A6, B6, C6, D6, E6, F6, G6, H6, I6, \
A7, B7, C7, D7, E7, F7, G7, H7, I7, \
A8, B8, C8, D8, E8, F8, G8, H8, I8, \
A9, B9, C9, D9, E9, F9, G9, H9, I9, \
    = MAP.flatten()


class Config(ConfigBase):
    # ===== Start of generated config =====
    MAP_SIREN_TEMPLATE = ['CAred']
    MOVABLE_ENEMY_TURN = (2,)
    MAP_HAS_SIREN = True
    MAP_HAS_MOVABLE_ENEMY = True
    MAP_HAS_MAP_STORY = True
    MAP_HAS_FLEET_STEP = True
    MAP_HAS_AMBUSH = False
    MAP_HAS_PORTAL = True
    # ===== End of generated config =====


class Campaign(CampaignBase):
    MAP = MAP

    def battle_0(self):
        if self.clear_siren():
            return True

        return self.battle_default()

    def battle_4(self):
        return self.clear_boss()
