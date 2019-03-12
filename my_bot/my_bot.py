# -*- coding: utf-8 -*-

import math
import time
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 -y1)**2)

class RoucoolBot(BaseAgent):

    def __init__(self, name, team, index):

        # Run BaseAgent's init
        super().__init__(name, team, index)
        self.controller = SimpleControllerState()

        # Constants 
        self.DISTANCE_DODGE = 500
        self.DODGE_TIME = 0.5

        # Game data
        self.bot_pos = None
        self.bot_rot = None

        # Dodging 
        self.should_dodge = False
        self.on_second_jump = False 
        self.next_dodge_time = 0
        
        self.dodge_interval = 0 # <-- Deprecated

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        # Update current game data values
        self.bot_yaw = packet.game_cars[self.team].physics.rotation.yaw
        self.bot_pos = packet.game_cars[self.index].physics.location
        ball_pos = packet.game_ball.physics.location
        
        # Get ball position & aim at it
        self.aim(ball_pos.x, ball_pos.y)

        if (self.index == 0 and self.bot_pos.y < ball_pos.y) or (self.index == 1 and self.bot_pos.y > ball_pos.y):
            self.aim(ball_pos.x, ball_pos.y)
            if calculate_distance(self.bot_pos.x, self.bot_pos.y, ball_pos.x, ball_pos.y) < self.DISTANCE_DODGE:
                self.should_dodge = True
        else:
            self.controller.boost = True
            if self.team == 0:
                self.aim(0, -5000)
            else:
                self.aim(0, 5000)

        ## Demo enemy
        # if self.team == 0:
        #     enemy_team = 1
        # else:
        #     enemy_team = 0
        # enemy_pos = packet.game_cars[enemy_team].physics.location
        # self.aim(enemy_pos.x, enemy_pos.y)
        # self.controller.boost = True

        self.controller.boost = False
        self.controller.jump = 0
        self.controller.throttle = 1
        self.check_dodge()

        return self.controller

    def calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 -y1)**2)

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

    def check_dodge(self):
        if self.should_dodge and time.time() > self.next_dodge_time:
            self.controller.jump = True
            self.controller.pitch = -1

            if self.on_second_jump:
                self.on_second_jump = False
                self.should_dodge = False
            else:
                self.on_second_jump = True
                self.next_dodge_time = time.time() + self.DODGE_TIME