# Abstract
In this project we use several algorithms to tackle the problem of controlling an
autonomous vehicle in the tasks of lane keeping and crash avoidance. The main
simulation environment is ROS where we implemented a vehicle model equipped
with a realistic laser sensor and a camera. Two separate simulation scenarios are
designed for each task, one scenario is for training the algorithms and the other is
to test the performance of the trained models. Three main learning algorithms are
used. A discrete reinforcement learning algorithm called Q-learning, A continuous
reinforcement learning algorithm called DDPG. The previous algorithms used laser
sensor readings as input. The final algorithm, which is a supervised deep learning
algorithm that uses an architecture of a Convolutional Neural Network, relied on
images fed from the camera as input. A comparative study of the results is done
based on specific evaluation criteria.

Read the report (graduation-design-project.pdf) for detailed description of the work.
