import gym
import rospy
import roslaunch
import time
import numpy as np

from gym import utils, spaces
from gym_gazebo.envs import gazebo_env
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

from sensor_msgs.msg import LaserScan

from gym.utils import seeding
from gym.envs.registration import register

reg = register(
    id='MyCustomEnvSpeed-v0',
    entry_point='my_custom_env:MyCustomEnv',
    timestep_limit=100,
    )

class MyCustomEnv(gazebo_env.GazeboEnv):

    def __init__(self):
        print('starting init')
        # Launch the simulation with the given launchfile name
        # gazebo_env.GazeboEnv.__init__(self, "GazeboCircuitTurtlebotLidar_v0.launch")
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)

        self.action_space = spaces.Discrete(4) #F,L,R,Faster
        self.observation_space = spaces.Discrete(5)
        self.reward_range = (-np.inf, np.inf)

        self._seed()
        print('ended init')

    def discretize_observation(self,data,new_ranges):
        print('starting discretize_observation')
        discretized_ranges = []
        min_range = 0.2
        done = False
        mod = len(data.ranges) / new_ranges
        for i, item in enumerate(data.ranges):
            if (i%mod==0):
                if data.ranges[i] == float ('Inf'):
                    discretized_ranges.append(6)
                elif np.isnan(data.ranges[i]):
                    discretized_ranges.append(0)
                else:
                    discretized_ranges.append(int(data.ranges[i]))
            if (min_range > data.ranges[i] > 0):
                done = True

        print('ending discretize_observation')
        return discretized_ranges, done

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        print('starting _step')
        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause()
        except rospy.ServiceException as e:
            print(("/gazebo/unpause_physics service call failed"))
        if action == 0: #FORWARD
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.3
            vel_cmd.angular.z = 0.0
            self.vel_pub.publish(vel_cmd)
        elif action == 1: #LEFT
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.05
            vel_cmd.angular.z = 0.3
            self.vel_pub.publish(vel_cmd)
        elif action == 2: #RIGHT
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.05
            vel_cmd.angular.z = -0.3
            self.vel_pub.publish(vel_cmd)
        elif action == 3: #FASTER!
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.7
            vel_cmd.angular.z = 0.0
            self.vel_pub.publish(vel_cmd)

        print('made it through choosing and publishing action')
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/kobuki/laser/scan', LaserScan, timeout=5)
            except KeyboardInterrupt as e:
                data = 'hi'
            except:
                print("Time out /kobuki/laser/scan")
                pass
        print('got data')
        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            #resp_pause = pause.call()
            self.pause()
        except rospy.ServiceException as e:
            print(("/gazebo/pause_physics service call failed"))

        print('starting discretize_observation')
        state,done = self.discretize_observation(data,5)
        print('done with discretize_observation')

        if not done:
            if action == 0:
                reward = 5
            elif action == 3:
                reward = 10
            else:
                reward = 1
        else:
            reward = -200

        print('returning state, reward, done, {}')
        return state, reward, done, {}

    def _reset(self):

        # Resets the state of the environment and returns an initial observation.
        rospy.wait_for_service('/gazebo/reset_simulation')
        try:
            #reset_proxy.call()
            self.reset_proxy()
        except rospy.ServiceException as e:
            print(("/gazebo/reset_simulation service call failed"))

        # Unpause simulation to make observation
        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            #resp_pause = pause.call()
            self.unpause()
        except rospy.ServiceException as e:
            print(("/gazebo/unpause_physics service call failed"))

        #read laser data
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/kobuki/laser/scan', LaserScan, timeout=5)
            except:
                print("Something went wrong reading /kobuki/laser/scan")
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            #resp_pause = pause.call()
            self.pause()
        except rospy.ServiceException as e:
            print(("/gazebo/pause_physics service call failed"))

        state = self.discretize_observation(data,5)

        return state
