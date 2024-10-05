import os
import pandas as pd
from Data_Generator import NiftiDataGenerator
file_names=[x for x in os.listdir("./New_Processed/New_Processed")]
labels=[]
df = pd.read_csv('./Phenotypic_file.csv')

for i in file_names:
    sub_id=int(i.split(".")[0])
    dxgrp=df[df['SUB_ID']==sub_id]['DX_GROUP'].iloc[0]
    if dxgrp==1:
        labels.append(1)
    elif dxgrp==2:
        labels.append(0)
    else:
        print("Error")

split_index = int(len(file_names) * 0.8)
train_generator=NiftiDataGenerator(file_paths=file_names,labels=labels)
print(len(train_generator))