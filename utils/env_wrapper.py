'''
  We wrapper "RoboCup 2D Half Field Offense" from "https://github.com/LARG/HFO" into gym-style env.
  @python version : 3.6.4
  @author : pangjc
  @time : 2020/8/4
'''

import os
import hfo
from hfo import *
import time

hfo_root = "/home/pangjc/code/HFO"

class hfo_env():

    def __init__(self, port):

        game_cmd = "{}/bin/HFO --offense-agents=1" \
                   " --defense-npcs=1 --port={} --trials 200 --headless &".format(hfo_root, port)
        os.system(game_cmd)
        time.sleep(2)
        self.env = hfo.HFOEnvironment()
        self.env.connectToServer(HIGH_LEVEL_FEATURE_SET,
                            '{}/bin/teams/base/config/formations-dt'.format(hfo_root),
                            port,
                            'localhost',
                            'base_left',
                            False)

        self.avaliable_actions = {
            0:MOVE,
            1:SHOOT,
            2:DRIBBLE,
            3:GO_TO_BALL,
            4:NOOP
        }

        self.action_space = len(self.avaliable_actions)
        self.state_space = self.env.getStateSize()

    def reset(self):
        self.done = False
        state = self.env.getState()

        return state


    def step(self, action):
        self.env.act(self.avaliable_actions[action])
        status = self.env.step()
        next_state = self.env.getState()
        reward = self.getReward(status)
        done = False if status == IN_GAME else True

        return next_state, reward, done, {}

    def close(self):
        self.env.act(QUIT)
        self.env.step()


    def getReward(self, s):
        reward = 0
        # ---------------------------
        if s == GOAL:
            reward = 20
        # ---------------------------
        elif s == CAPTURED_BY_DEFENSE:
            reward = -10
        # ---------------------------
        elif s == OUT_OF_BOUNDS:
            reward = -10
        # ---------------------------
        # Cause Unknown Do Nothing
        elif s == OUT_OF_TIME:
            reward = -10
        # ---------------------------
        elif s == IN_GAME:
            reward = 0.01
        # ---------------------------
        elif s == SERVER_DOWN:
            reward = 0
        # ---------------------------
        else:
            print("Error: Unknown GameState", s)
        return reward


if __name__ == '__main__':

    import  argparse

    parser = argparse.ArgumentParser(description="Running time configurations")

    parser.add_argument('--port', default=6000, type=int)

    args = parser.parse_args()

    env = hfo_env(args.port)

    print(env.env.getStateSize())

    for _ in range(2000):
        s = env.reset()
        done = False
        while not done:
            a = 0 if s[5] != 1 else 2
            s, r, done, _ = env.step(a)

