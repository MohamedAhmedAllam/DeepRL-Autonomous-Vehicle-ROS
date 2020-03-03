# use relu instead of elu
# padding is SAME not VALID
# Change Cost function
#%%
with open('train1.txt') as f:
    #w, h = [int(x) for x in next(f).split()] # read first line
    array = []
    for line in f: # read rest of lines
        array.append([float(x) for x in line.split(',')])
print(array[0][5])
#%% Make data looks as images
import numpy as np
import pylab as plt
h=len(array)
x=np.zeros((h,200,200,1))
y=np.zeros((h,1))
for i in range(0,h):
    a=array[i][0:200*200]
    x[i,:,:,0]=np.reshape(a,(200,200))
    y[i][0]=array[i][(200*200)]
#%% Checking the images
im = plt.imshow(x[800,:,:,0], cmap='gray')
plt.colorbar(im, orientation='horizontal')
plt.show()
#%% CNN Model
import math
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy
from scipy import ndimage
import tensorflow as tf
from tensorflow.python.framework import ops
#%%
def create_placeholders(n_H0, n_W0, n_C0, n_y):
    X = tf.placeholder(tf.float32, [None, n_H0, n_W0, n_C0])
    Y = tf.placeholder(tf.float32, [None, n_y])
    return X, Y
#%%
def initialize_parameters():
    W1 = tf.get_variable("W1", [5, 5, 1, 24], initializer=tf.contrib.layers.xavier_initializer())
    W2 = tf.get_variable("W2", [5, 5, 24, 36], initializer=tf.contrib.layers.xavier_initializer())
    W3 = tf.get_variable("W3", [5, 5, 36, 48], initializer=tf.contrib.layers.xavier_initializer())
    W4 = tf.get_variable("W4", [3, 3, 48, 64], initializer=tf.contrib.layers.xavier_initializer())
    W5 = tf.get_variable("W5", [3, 3, 64, 76], initializer=tf.contrib.layers.xavier_initializer())
    
    W6 = tf.get_variable("W6", [100, 47500], initializer = tf.contrib.layers.xavier_initializer())
    b6 = tf.get_variable("b6", [100, 1], initializer = tf.zeros_initializer())
    W7 = tf.get_variable("W7", [50, 100], initializer = tf.contrib.layers.xavier_initializer())
    b7 = tf.get_variable("b7", [50, 1], initializer = tf.zeros_initializer())
    W8 = tf.get_variable("W8", [10, 50], initializer = tf.contrib.layers.xavier_initializer())
    b8 = tf.get_variable("b8", [10, 1], initializer = tf.zeros_initializer())
    W9 = tf.get_variable("W9", [1, 10], initializer = tf.contrib.layers.xavier_initializer())
    b9 = tf.get_variable("b9", [1, 1], initializer = tf.zeros_initializer())
    parameters = {"W1":W1,"W2":W2,"W3":W3,"W4":W4,"W5":W5,"W6":W6,"W7":W7,"W8":W8,"W9":W9,"b6":b6,"b7":b7,"b8":b8,"b9":b9}
    return parameters
#%%
def forward_propagation(X, parameters):
    W1 = parameters['W1']
    W2 = parameters['W2']
    W3 = parameters['W3']
    W4 = parameters['W4']
    W5 = parameters['W5']
    W6 = parameters['W6']
    W7 = parameters['W7']
    W8 = parameters['W8']
    W9 = parameters['W9']
    b6 = parameters['b6']
    b7 = parameters['b7']
    b8 = parameters['b8']
    b9 = parameters['b9']
    
    print(X.shape)
    Z1 = tf.nn.conv2d(X, W1, strides=[1, 2, 2, 1], padding='SAME')
    A1 = tf.nn.relu(Z1)
    print(A1.shape)
    Z2 = tf.nn.conv2d(A1, W2, strides=[1, 2, 2, 1], padding='SAME')
    A2 = tf.nn.relu(Z2)
    print(A2.shape)
    Z3 = tf.nn.conv2d(A2, W3, strides=[1, 2, 2, 1], padding='SAME')
    A3 = tf.nn.relu(Z3)
    print(A3.shape)
    Z4 = tf.nn.conv2d(A3, W4, strides=[1, 1, 1, 1], padding='SAME')
    A4 = tf.nn.relu(Z4)
    print(A4.shape)
    Z5 = tf.nn.conv2d(A4, W5, strides=[1, 1, 1, 1], padding='SAME')
    A5 = tf.nn.relu(Z5)
    print(A5.shape)
    
    P = tf.transpose(tf.contrib.layers.flatten(A5))
    print(P.shape)
    print(W6.shape)
    
    Z6 = tf.add(tf.matmul(W6, P), b6)
    A6 = tf.nn.relu(Z6)
    print(A6.shape)
    Z7 = tf.add(tf.matmul(W7, A6), b7)
    A7 = tf.nn.relu(Z7)
    print(A7.shape)
    Z8 = tf.add(tf.matmul(W8, A7), b8) 
    A8 = tf.nn.relu(Z8)
    print(A8.shape)
    Z9 = tf.add(tf.matmul(W9, A8), b9)
    print(Z9.shape)
    return Z9
#%%
def compute_cost(Z3, Y):
    cost=tf.reduce_sum(tf.losses.absolute_difference(labels=Y,predictions=Z3))
    #cost=tf.reduce_sum(tf.multiply(Y, tf.log(Z3)) + tf.multiply(1 - Y, tf.log(1 - Z3)))
    
    return cost
#%%
def random_mini_batches(X, Y, mini_batch_size = 64):
    m = X.shape[0]                  # number of training examples
    mini_batches = []

    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation,:]
    shuffled_Y = Y[permutation,:].reshape((m,1))

    num_complete_minibatches = int(math.floor(m/mini_batch_size)) 
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size:(k + 1) * mini_batch_size,:,:,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size:(k + 1) * mini_batch_size,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    if m % mini_batch_size != 0:
        end = m - mini_batch_size * math.floor(m / mini_batch_size)
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size:,:,:,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size:,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
        
    return mini_batches
#%%
def model(X_train, Y_train, learning_rate=0.009,num_epochs=100, minibatch_size=64, print_cost=True):
    ops.reset_default_graph()                 # to be able to rerun the model without overwriting tf variables
    (m, n_H0, n_W0, n_C0) = X_train.shape             
    n_y = Y_train.shape[1]                            
    costs = []
    
    X, Y = create_placeholders(n_H0, n_W0, n_C0, n_y)
    print("create_placeholders done")
    parameters = initialize_parameters()
    print("initialize_parameters done")
    Z3 = forward_propagation(X, parameters)
    print("forward_propagation done")
    cost = compute_cost(Z3, Y)
    print("compute_cost done")
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
    print("AdamOptimizer done")
    
    init = tf.global_variables_initializer()
    print("init done")
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(num_epochs):
            minibatch_cost = 0.
            num_minibatches = int(m / minibatch_size)
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size)
            for minibatch in minibatches:
                (minibatch_X, minibatch_Y) = minibatch
                _ , temp_cost = sess.run([optimizer, cost], feed_dict={X:minibatch_X, Y:minibatch_Y})
                minibatch_cost += temp_cost / num_minibatches
                
            if print_cost == True and epoch % 5 == 0:
                print ("Cost after epoch %i: %f" % (epoch, minibatch_cost))
            if print_cost == True and epoch % 1 == 0:
                costs.append(minibatch_cost)
        
        # plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()
        
        # Calculate accuracy on the test set
        accuracy = compute_cost(Z3, Y)
        print(accuracy)
        train_accuracy = accuracy.eval({X: X_train, Y: Y_train})
        print("Train Accuracy:", train_accuracy)
        
        return train_accuracy, parameters
#%%
_, parameters = model(x, y)
































