import swanlab
import csv
import time
import cmath
from debater_python_api.api.debater_api import DebaterApi

csv_file = 'en_test.csv'
        

debater_api = DebaterApi('58196082476caf02520157c9d8f4feefL05')
argument_quality_client = debater_api.get_argument_quality_client()


AE = 0
SE = 0
LAE = 0
LSE = 0
tiny_count =0
middle_count = 0
big_count = 0
LWrong = 0

swanlab.init(experiment_name="AQ_en_LCtest_PD")

def quality_type(score):
    if float(score)<=0.3:
        return -1
    if 0.3<float(score)<=0.7:
        return 0
    if float(score)>0.7:
        return 1

def loss(label_score,score,i):
    global AE
    global SE
    global LAE
    global LSE
    global tiny_count
    global middle_count
    global big_count
    swanlab.log({"lable_score":label_score,"score":score})
    MAE_loss = abs(float(label_score)-float(score))
    if MAE_loss<=0.1:
        tiny_count+=1
    elif  0.1<MAE_loss<=0.2:
        middle_count+=1
    else :
        big_count+=1
    LAE_loss =abs(quality_type(label_score)-quality_type(score))
    AE += MAE_loss
    LAE += LAE_loss
    MAE = AE/(i+1)
    MLAE = LAE/(i+1)
    swanlab.log({"MAE":MAE})
    swanlab.log({"MLAE":MLAE})
    MSE_loss = pow(float(label_score)-float(score),2)
    LSE_loss = pow(quality_type(label_score)-quality_type(score),2)
    SE += MSE_loss
    LSE += LSE_loss
    MSE = SE/(i+1)
    MLSE = LSE/(i+1)
    RMSE = MSE**0.5
    RMLSE = MLSE**0.5
    swanlab.log({"tiny_count":tiny_count,"middle_count":middle_count,"big_count":big_count})
    swanlab.log({"MSE":MSE})
    swanlab.log({"MLSE":MLSE})
    swanlab.log({"RMSE":RMSE})
    swanlab.log({"RMLSE":RMLSE})
    

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行

    for i, row in enumerate(reader):
        if i>=1000:
            break
        if len(row) >= 4:
            sentence = row[0]
            topic = row[1]
            label_score = row[3]
            sentence_topic_dict =[{'sentence': sentence, 'topic': topic}] 
            score = argument_quality_client.run(sentence_topic_dict)[0]
            if quality_type(score)!=quality_type(label_score):
                LWrong+=1
            swanlab.log({"Lwrong_time":LWrong})
            
            loss(label_score=label_score,score=score,i=i)
            time.sleep(2)
            


            
            
            




