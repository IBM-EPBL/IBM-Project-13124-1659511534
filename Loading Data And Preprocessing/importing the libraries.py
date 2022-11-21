import numpy as  np 

import tensorflow as tf 
import keras 
import keras.backend as k

from keras.optimizers import SGD,Adam,Adagrad,RMSprop 
from keras.application import * 
from keras.preprocessing import * 
from keras.preprocessing.image import  ImageDataGenerator,array_to_img,img_to_array,load_img 
from keras.callbacks import EarlyStopping, ModelCheckpoint 
from keras.models import Sequential 
from keras.layers import Dense,Conv2D, MaxPool2D, Flatten, Activation, BatchNormalization,Dropout 
from keras.utils.np_utils import to_categorical 
from sklearn.model_selection import train_test_split 

import matplotlib.pyplot as plt 

import glob 
from PIL import Image 
import os 
from os import listdir
