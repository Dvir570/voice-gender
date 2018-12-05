import numpy as np
import pandas as pd
import tensorflow as tf


def read_data_set():
    print("start reading the data set")
    data_set = pd.read_csv('voice-gender dataset.csv')
    data_set.label = data_set.label.replace(to_replace=['male', 'female'], value=[0, 1])
    data_set = data_set.sample(frac=1).reset_index(drop=True)
    print("finish reading the data set")
    return data_set


def split_data_set():
    print("start split the data set to 70-30")
    index = int(len(voice.index) * 0.7)
    data_x = np.array(voice.drop(['label'], axis=1))
    data_y = np.array(voice.loc[:, ['label']])
    print("finish split the data set")
    print("in the train have:", index, "samples and in the test have:", len(voice.index)-index, "samples")
    return data_x[:index], data_y[:index], data_x[index:], data_y[index:]


def model_training():
    print("start training the model")
    for i in range(0, 10000):
        sess.run(train_op, feed_dict={x: train_data_x, y_: train_data_y})
        loss, _, acc = sess.run([loss_op, train_op, accuracy], feed_dict={
            x: train_data_x, y_: train_data_y})
        if i % 500 == 0:
            print("Step: {:5}\tLoss: {:.3f}\tAcc: {:.2%}".format(
                i, loss, acc))
    print("finish training the model")
    # print("w:", sess.run(W), " b:", sess.run(b), " loss:",
    #       loss_op.eval(session=sess, feed_dict={x: train_data_x, y_: train_data_y}))


def model_testing():
    print("start testing the model")
    print("accuracy: ", sess.run([accuracy, tf.round(logits)], feed_dict={x: test_data_x, y_: test_data_y})[0])


voice = read_data_set()
train_data_x, train_data_y, test_data_x, test_data_y = split_data_set()
features = len(voice.columns) - 1
x = tf.placeholder(tf.float32, [None, features])
y_ = tf.placeholder(tf.float32, [None, 1])

# Construct model
number_of_neurons_each_layer = [features, 20, 40, 40, 4, 1]
input_into_hidden_layers = [x]
for i, hidden_size in enumerate(number_of_neurons_each_layer):
        if i == len(number_of_neurons_each_layer):
            nn = tf.layers.dense(input_into_hidden_layers[i], hidden_size, activation=None)
        else:
            nn = tf.layers.dense(input_into_hidden_layers[i], hidden_size, activation=tf.nn.relu)
        input_into_hidden_layers.append(nn)
logits = input_into_hidden_layers[len(number_of_neurons_each_layer)]

# Define loss and optimizer
cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=y_)
loss_op = tf.reduce_mean(cross_entropy)
train_op = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(loss_op)

# Accuracy
predicted = tf.nn.sigmoid(logits)
correct_prediction = tf.equal(tf.round(predicted), y_)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Initializing the variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    model_training()
    model_testing()
