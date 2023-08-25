#!/usr/bin/env python
# coding: utf-8

# # Convolutional Neural Network

# ### Importing the libraries

# In[1]:


import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator


# In[2]:


tf.__version__


# ## Part 1 - Data Preprocessing

# ### Preprocessing the Training set

# In[3]:


train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
training_set = train_datagen.flow_from_directory('dataset/train_note',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')


# ### Preprocessing the Test set

# In[4]:


test_datagen = ImageDataGenerator(rescale = 1./255)
test_set = test_datagen.flow_from_directory('dataset/test_note',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'categorical')


# ## Part 2 - Building the CNN

# ### Initialising the CNN

# In[5]:


cnn = tf.keras.models.Sequential()


# ### Step 1 - Convolution

# In[6]:


cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[64, 64, 3]))


# ### Step 2 - Pooling

# In[7]:


cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))


# ### Adding a second convolutional layer

# In[8]:


cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))


# ### Step 3 - Flattening

# In[9]:


cnn.add(tf.keras.layers.Flatten())


# ### Step 4 - Full Connection

# In[10]:


cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))


# ### Step 5 - Output Layer

# In[11]:


cnn.add(tf.keras.layers.Dense(9, activation='softmax'))


# ## Part 3 - Training the CNN

# ### Compiling the CNN

# In[12]:


cnn.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])


# ### Training the CNN on the Training set and evaluating it on the Test set

# In[13]:


cnn.fit(x = training_set, validation_data = test_set, epochs = 25)#epochs=훈련횟수, 결과 값 안나오면 숫자 늘려가기


# ## Part 4 - Making a single prediction

# In[16]:


import numpy as np
from keras.preprocessing import image
test_image = image.load_img('dataset/single_prediction/4.jpg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)

result = cnn.predict(test_image)

# 클래스 인덱스와 클래스 이름 매핑
class_indices = training_set.class_indices
class_names = {v: k for k, v in class_indices.items()}

# 예측 결과 확인
predicted_class_index = np.argmax(result)  # 가장 높은 확률을 가진 클래스 인덱스
predicted_class_name = class_names[predicted_class_index]  # 인덱스를 클래스 이름으로 변환


# In[17]:


print("Predicted Class :", predicted_class_name)


# In[ ]:




