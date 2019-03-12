# -*- coding: utf-8 -*-

"""The goal of this bot is to stay still."""

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

class StillBot(BaseAgent):

    def __init__(self):
        self.controller = SimpleControllerState()
    
    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        controller.throttle = 0
        return controller