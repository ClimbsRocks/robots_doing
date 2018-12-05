#!/usr/bin/env python
import gym

from baselines import deepq
import rospy

import task_env_tbot2_speed_maze


def callback(lcl, _glb):
    # stop training if reward exceeds 199
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 1000
    return is_solved


def main():

    rospy.init_node('deep_turtle_gym', anonymous=True) #This is the line you have to add
    # rospy.init_node('deep_turtle_gym', anonymous=True, log_level=rospy.DEBUG) #This is the line you have to add

    raise(IntentionalStoppingError('init_node finished'))

    print('making env')
    env = gym.make('TurtleBot2SpeedMaze-v0')
    print('made env')

    # model = deepq.models.mlp([64])
    print('entering deepq.learn')
    act = deepq.learn(
        env,
        network='mlp',
        lr=1e-3,
        total_timesteps=100000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        print_freq=10,
        callback=callback
    )

    model_name = "deep_turtle1.pkl"
    print("Saving model to {}".format(model_name))
    act.save(model_name)


if __name__ == '__main__':
    main()