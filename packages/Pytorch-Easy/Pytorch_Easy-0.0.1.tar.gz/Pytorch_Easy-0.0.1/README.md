# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 02:38:37 2021

@author: Dhusor
"""

Example Code: 

Run Model Pytorch Model From Zero Epoch:

y:start from zero epoch n:after previous epoch y
Enter Number Of Epoch: 1
Enter path to save the model: /content/drive/MyDrive/Data/


Again Train After Some Epochs.We need to load previous model info.

run_model(inception_v3,train_loader,validation_loader,optimizer,criterion)

y:start from zero n:train after previous epoch: n
Enter Previous Trained Path: /content/drive/MyDrive/Data/trained.pt  
Enter End 2
------------------------------------------------------------
Epoch 1/1
----------------------------Tranning Summary----------------------
training Tranning Avg. Loss: 1.6109 Tranning Avg. Acc: 0.2000
----------------------------Validation Summary-----------------
validation Validation Avg. Loss: 1.6110 Validation Avg. Acc: 0.2000