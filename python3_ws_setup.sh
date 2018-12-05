# Setup ~/python3_ws
cd
source /opt/ros/kinetic/setup.bash
mkdir -p ~/python3_ws/src
cd ~/python3_ws/
catkin_make

cd ~/python3_ws/src
git clone https://github.com/openai/baselines.git
cd baselines
virtualenv venv --python=python3
rm -rf .git

source venv/bin/activate

pip install tensorflow
pip install -e .
pip install pyyaml rospkg catkin_pkg exception defusedxml mpi4py

cd ~/python3_ws/src; cd baselines
source venv/bin/activate

pip install catkin_pkg pyyaml empy rospkg numpy
cd ~/python3_ws/src
git clone https://github.com/ros/geometry
git clone https://github.com/ros/geometry2
git clone https://bitbucket.org/theconstructcore/openai_ros.git
git clone https://bitbucket.org/theconstructcore/theconstruct_msgs.git
git clone https://github.com/erlerobot/gym-gazebo.git
rm -rf geometry/.git
rm -rf geometry2/.git
rm -rf openai_ros/.git
rm -rf theconstruct_msgs/.git
rm -rf gym-gazebo/.git
cd gym-gazebo
pip install -e .

cd ~/python3_ws/src
git init
git remote add origin https://github.com/ClimbsRocks/robots_doing.git
mv CMakeLists.txt CMakeLists.txt_backup
git fetch
git pull origin master

git config --global user.email "ClimbsBytes@gmail.com"
git config --global user.name "ClimbsRocks"

cd ~/python3_ws
rm -rf build devel
catkin_make --force-cmake
source devel/setup.bash

cd ~/python3_ws/src/baselines
source venv/bin/activate
cd ~/python3_ws
source devel/setup.bash
cd ~/python3_ws/src
git checkout deepq
git pull origin deepq && roslaunch tbot2_speed_maze start_training.launch

# rosservice call gazebo/get_world_properties
# rosservice call gazebo/delete_model "mobile_base"

# rosrun gazebo_ros spawn_model -file `rospack find rrbot_description`/urdf/rrbot.xml -urdf -y 1 -model rrbot1 -robot_namespace rrbot1
# rosrun gazebo_ros spawn_model -file /home/simulations/public_sim_ws/src/all/turtlebot3/turtlebot3/turtlebot3_description/urdf/turtlebot3_burger.urdf.xacro -urdf -y 1 -model burgerbot1 -robot_namespace burgerbot1




