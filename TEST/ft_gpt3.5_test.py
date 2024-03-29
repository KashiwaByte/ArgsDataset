import swanlab
import csv
import time
import cmath
from debater_python_api.api.debater_api import DebaterApi

csv_file = 'dev.csv'
        
from openai import OpenAI
client = OpenAI()





token = 0
AE = 0
SE = 0

swanlab.init(experiment_name="AQ_Dev_T0_GPT")
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
            label_score = row[3]
            response = client.chat.completions.create(
                # model="ft:gpt-3.5-turbo-0125:personal:arg-quality-0328:97kBFgug",
                model="gpt-3.5-turbo-0125",
                temperature=0,
                messages=[
                    {"role": "system", "content": "请根据以下论述和主题,给出论证质量评分(只需要输出一个范围从0-1的分数,精确到小数点后9位),不要给出分析."},
                    {"role": "user", "content": str({'sentence':sentence , 'topic': topic})}
                ]
                )
            score = response.choices[0].message.content
            token += response.usage.total_tokens
            swanlab.log({"token":token})
            loss(label_score=label_score,score=score,i=i)
            time.sleep(1)
            


            
            
            


