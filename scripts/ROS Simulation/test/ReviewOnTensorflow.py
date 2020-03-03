import math
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.framework import ops
#%%
y_hat = tf.constant(36, name='y_hat')            # Define y_hat constant. Set to 36.
y = tf.constant(39, name='y')                    # Define y. Set to 39
loss = tf.Variable((y - y_hat)**2, name='loss')  # Create a variable for the loss
init = tf.global_variables_initializer()         # When init is run later (session.run(init)),                                                 # the loss variable will be initialized and ready to be computed
with tf.Session() as session:                    # Create a session and print the output
    session.run(init)                            # Initializes the variables
    print(session.run(loss))                     # Prints the loss
#%%
a = tf.constant(2)
b = tf.constant(10)
c = tf.multiply(a,b)
init = tf.global_variables_initializer()
sess = tf.Session()
print(sess.run(c))
#%%
x = tf.placeholder(tf.int64, name = 'x')
print(sess.run(2 * x, feed_dict = {x: 3}))
sess.close()
#%%
Y = tf.add(tf.matmul(W, X), b)
X = tf.placeholder(tf.float32, [n_x, None], name="X")
cost = tf.nn.sigmoid_cross_entropy_with_logits(logits=z, labels=y)
one_hot_matrix = tf.one_hot(indices=labels, depth=C, axis=0)
W1 = tf.get_variable("W1", [25, 12288], initializer = tf.contrib.layers.xavier_initializer(seed=1))
b1 = tf.get_variable("b1", [25, 1], initializer = tf.zeros_initializer())
A1 = tf.nn.relu(Z1)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels))
#%%
