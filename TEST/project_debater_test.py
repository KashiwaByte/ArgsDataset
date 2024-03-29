import swanlab
import csv
import time
import cmath
from debater_python_api.api.debater_api import DebaterApi

csv_file = 'test.csv'
        

debater_api = DebaterApi('58196082476caf02520157c9d8f4feefL05')
argument_quality_client = debater_api.get_argument_quality_client()

AE = 0
SE = 0

swanlab.init(experiment_name="ArgQuality_PD")
def loss(label_score,score,i):
    global AE
    global SE
    swanlab.log({"lable_score":label_score,"score":score})
    MAE_loss = abs(float(label_score)-float(score))
    AE += MAE_loss
    MAE = AE/(i+1)
    swanlab.log({"MAE":MAE})
    MSE_loss = pow(float(label_score)-float(score),2)
    SE += MSE_loss
    MSE = SE/(i+1)
    RMSE = MSE**0.5
    swanlab.log({"MSE":MSE})
    swanlab.log({"RMSE":RMSE})
    

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行

    for i, row in enumerate(reader):
        if i>=1000:
            break
        if len(row) >= 4:
            sentence = row[0]
            topic = row[1]
            label_scores = row[3]
            sentence_topic_dict =[{'sentence': sentence, 'topic': topic}] 
            scores = argument_quality_client.run(sentence_topic_dict)[0]
            loss(label_score=label_scores,score=scores,i=i)
            time.sleep(10)
            


            
            
            




