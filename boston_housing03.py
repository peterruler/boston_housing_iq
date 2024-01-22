# -*- coding: utf-8 -*-
"""boston_housing03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NNIhDpm2jH0FUKLeHencG-g2JirCTsiB

[ZHAW Exercise Week 4 Linear Regression with tensorflow](https://github.com/toelt-llc/COURSE-zhaw-dlcourse-spring2019/blob/master/Week%204%20-%20One%20Neuron/Week%204%20-%20Linear%20Regression%20with%20Tensor%20Flow.ipynb)
"""

def compare_mse(sess, y_, train_x, test_x, kp):
    if (kp < 1):
        pred_y = sess.run(y_, feed_dict = {X:test_x, keep_prob:kp})
        mse = tf.reduce_mean(tf.square(pred_y - test_y))
        print("MSE Test: %.4f" % sess.run(mse))

        pred_y = sess.run(y_, feed_dict = {X:train_x, keep_prob:kp})
        mse = tf.reduce_mean(tf.square(pred_y - train_y))
        print("MSE Train: %.4f" % sess.run(mse))
    else:
        pred_y = sess.run(y_, feed_dict = {X:test_x})
        mse = tf.reduce_mean(tf.square(pred_y - test_y))
        print("MSE Test: %.4f" % sess.run(mse))

        pred_y = sess.run(y_, feed_dict = {X:train_x})
        mse = tf.reduce_mean(tf.square(pred_y - train_y))
        print("MSE Train: %.4f" % sess.run(mse))

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from tensorflow import keras

import numpy as np

import sklearn.linear_model as sk

(train_data, train_targets), (test_data, test_targets) = keras.datasets.boston_housing.load_data()
features = np.array(train_data)
labels = np.array(train_targets)

train_data

def normalize(dataset):
    mu = np.mean(dataset, axis = 0)
    sigma = np.std(dataset, axis = 0)
    return (dataset-mu)/sigma

n_training_samples = features.shape[0]
n_dim = features.shape[1]

print('The dataset has',n_training_samples,'training samples.')
print('The dataset has',n_dim,'features.')

features_norm = normalize(features)

print(features_norm.shape)
print(labels.shape)

np.random.seed(42)
rnd = np.random.rand(len(features_norm)) < 0.8

train_x = np.transpose(features_norm[rnd])
train_y = np.transpose(labels[rnd])
test_x = np.transpose(features_norm[~rnd])
test_y = np.transpose(labels[~rnd])

print(train_x.shape)
print(train_y.shape)

np.random.seed(42)
rnd = np.random.rand(len(features_norm)) < 0.8

train_x = np.transpose(features_norm[rnd])
train_y = np.transpose(labels[rnd])
test_x = np.transpose(features_norm[~rnd])
test_y = np.transpose(labels[~rnd])

print(train_x.shape)
print(train_y.shape)

train_y = train_y.reshape(1,len(train_y))
test_y = test_y.reshape(1,len(test_y))

print(train_y.shape)
print(test_y.shape)

tf.reset_default_graph()

X = tf.placeholder(tf.float32, [n_dim, None])
Y = tf.placeholder(tf.float32, [1, None])
learning_rate = tf.placeholder(tf.float32, shape=())

W = tf.Variable(tf.ones([n_dim, 1]))
b = tf.Variable(tf.zeros(1))

init = tf.global_variables_initializer()

y_ = tf.matmul(tf.transpose(W),X)+b
cost = tf.reduce_mean(tf.square(y_-Y))
training_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

def run_linear_model(learning_r, training_epochs, train_obs, train_labels, debug = False):
    sess = tf.Session()
    sess.run(init)

    cost_history = np.empty(shape=[0], dtype = float)

    for epoch in range(training_epochs+1):
        sess.run(training_step, feed_dict = {X: train_obs, Y: train_labels, learning_rate: learning_r})
        cost_ = sess.run(cost, feed_dict={ X:train_obs, Y: train_labels, learning_rate: learning_r})
        cost_history = np.append(cost_history, cost_)

        if (epoch % 1000 == 0) & debug:
            print("Reached epoch",epoch,"cost J =", str.format('{0:.6f}', cost_))

    return sess, cost_history

sess, cost_history = run_linear_model(learning_r = 0.01,
                                training_epochs = 10000,
                                train_obs = train_x,
                                train_labels = train_y,
                                debug = True)

plt.rc('font', family='arial')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')

plt.tight_layout()

fig = plt.figure(figsize=(10, 7))

ax = fig.add_subplot(1, 1, 1)
ax.plot(cost_history, ls='solid', color = 'black')
ax.set_xlabel('epochs', fontsize = 16)
ax.set_ylabel('Cost function $J$ (MSE)', fontsize = 16)
plt.xlim(0,200)
plt.tick_params(labelsize=16)

pred_y = sess.run(y_, feed_dict = {X: test_x, Y: test_y})
mse = tf.reduce_mean(tf.square(pred_y - test_y))

plt.rc('font', family='arial')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')

plt.tight_layout()

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(1, 1, 1)
ax.scatter(test_y, pred_y, lw = 5)
ax.plot([test_y.min(), test_y.max()], [test_y.min(), test_y.max()], 'k--', lw = 5)
ax.set_xlabel('Measured Target Value', fontsize = 16)
ax.set_ylabel('Predicted Target Value', fontsize = 16)
plt.tick_params(labelsize=16)

compare_mse(sess, y_, train_x, test_x, 1)

sess.close()

print ('Starting first model')
sess1, cost_history1 = run_linear_model(learning_r = 0.1,
                                training_epochs = 10000,
                                train_obs = train_x,
                                train_labels = train_y,
                                debug = True)

print ('Starting second model')
sess2, cost_history2 = run_linear_model(learning_r = 0.01,
                                training_epochs = 10000,
                                train_obs = train_x,
                                train_labels = train_y,
                                debug = True)

print ('Starting third model')
sess3, cost_history3 = run_linear_model(learning_r = 0.001,
                                training_epochs = 10000,
                                train_obs = train_x,
                                train_labels = train_y,
                                debug = True)

plt.rc('font', family='arial')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')

plt.tight_layout()

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(1, 1, 1)
ax.plot(cost_history1, ls='solid', color = 'black', label='$\gamma=0.1$')
ax.plot(cost_history2, ls='dashed', color = 'black', label='$\gamma=0.01$')
ax.plot(cost_history3, ls='dotted', color = 'black', label='$\gamma=0.001$')
ax.set_xlabel('epochs', fontsize = 16)
ax.set_ylabel('Cost function $J$ (MSE)', fontsize = 16)
plt.xlim(0,300)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize = 16)
plt.tick_params(labelsize=16)

sess1.close()
sess2.close()
sess3.close()

lm = sk.LinearRegression()
lm.fit(np.transpose(train_x), np.transpose(train_y))
msetest = np.mean((np.transpose(test_y)-lm.predict(np.transpose(test_x)))**2)
msetrain = np.mean((np.transpose(train_y)-lm.predict(np.transpose(train_x)))**2)

print('Train MSE=',msetrain)
print('Test MSE=',msetest)