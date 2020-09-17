In this project, 6 models (model 0, model 1, ..., model 5) have been tested. While model 0 is set to be the control, 
and the other models are tested with changing the Architecture of CNN model. 
Model 1 is modified from Model 0 by removing one convolution layer and one maximum pooling layer
Model 2 is modified from Model 0 by changing the size of filter from 3x3 to 7x7 in convolution layer
Model 3 is modified from Model 0 by changing the size of filter from 2x2 to 4x4 in max pooling layer
Model 4 is modified from Model 0 by adding one hidden fully connected layer
Model 5 is modified from Model 0 by removing the dropout in training status 

Results are summarized as follow:
model 0 - 333/333 - 1s - loss: 0.1924 - accuracy: 0.9485
model 1 - 333/333 - 2s - loss: 3.4987 - accuracy: 0.0554
model 2 - 333/333 - 4s - loss: 0.5043 - accuracy: 0.8397
model 3 - 333/333 - 1s - loss: 3.5016 - accuracy: 0.0552
model 4 - 333/333 - 1s - loss: 3.5062 - accuracy: 0.0539
model 5 - 333/333 - 1s - loss: 0.1804 - accuracy: 0.9615

Comparing with model 0, it is observed that when we reducing one convolution layer and one maximum pooling layer in 
model 1, the accuracy drops a lot to only 5.54%. This is because our model cannot capture the important feature from
image when we try to reduce a convolution layer and a maximum pooling layer.

Similar results of very low accuracy are observed in model 3 (when we increase the size of filter in maximum pooling 
layer) and model 4 (when we add one more hidden layer). Because when we use a bigger filter in maximum pooling, some 
'locally' important features will be filtered out by 'globally' important features which greatly reduce the ability in
recognizing features. 

It is observed that when increasing the filter size in convolution layer, accuracy drops. May be the extra information 
from the far apart neighbouring pixels create noise to the model. 
 
Last but not least, it is observed that when we do not use dropout technique, the accuracy increase a bit. However,
the accuracy of model 5 drops from training to testing which is due to over-training.



