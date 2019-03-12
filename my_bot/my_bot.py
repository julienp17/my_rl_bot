# -*- coding: utf-8 -*-

import math
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

class RoucoolBot(BaseAgent):

    def __init__(self, name, team, index):

        # Run BaseAgent's init
        super().__init__(name, team, index)
        self.controller = SimpleControllerState()

        # Game data
        self.bot_pos = None
        self.bot_rot = None

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        # Update bot current position & rotation
        self.bot_yaw = packet.game_cars[self.team].physics.rotation.yaw
        self.bot_pos = packet.game_cars[self.index].physics.location
        
        # Get ball position & aim at it
        ball_pos = packet.game_ball.physics.location
        self.aim(ball_pos.x, ball_pos.y)

        # Drive forward
        self.controller.throttle = 1

        return self.controller

    def aim(self, target_x, target_y):
        angle_between_bot_and_target = math.atan2(target_y - self.bot_pos.y,
                                                  target_x - self.bot_pos.x)
        angle_front_to_target = angle_between_bot_and_target - self.bot_yaw

        # Correct the values
        if angle_front_to_target < -math.pi:
            angle_front_to_target += 2 * math.pi
        if angle_front_to_target > math.pi:
            angle_front_to_target -= 2 * math.pi

        if angle_front_to_target < math.radians(-5):
            self.controller.steer = -1
        elif angle_front_to_target > math.radians(10):
            self.controller.steer = 1
        else:
            self.controller.steer = 0