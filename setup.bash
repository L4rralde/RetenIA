export REPO_PATH=$(dirname $(readlink -f "${BASH_SOURCE:-$0}"))
source $REPO_PATH/ros/catkin_ws/devel/setup.bash
#export ROS_HOST_NAME=
#export ROS_MASTER_URI=http://localhost:11311
export ROS_MASTER_URI=http://$1:11311
#export ROS_IP=