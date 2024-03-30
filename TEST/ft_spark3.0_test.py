import swanlab
import csv
import time

csv_file = 'dev.csv'
        

import SparkApi
#以下密钥信息从控制台获取
appid = "51bb5f32"     #填写控制台中获取的 APPID 信息
api_secret = "ZDA5MDZjZWY0YzE5NmY3MWNjNTQ4YWMz"   #填写控制台中获取的 APISecret 信息
api_key ="bfd094c6b2feb6dbf9bfe3bba6954f76"    #填写控制台中获取的 APIKey 信息

#调用微调大模型时，设置为“patch”
# domain = "patchv3"
domain = "generalv3"

#云端环境的服务地址
# Spark_url = "wss://spark-api-n.xf-yun.com/v3.1/chat"  # 微调v3.0环境的地址
Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"   #通用v3.0地址


token = 0
AE = 0
SE = 0
wrong = 0
swanlab.init(experiment_name="AQ_dev_Spark")
def loss(label_score,score,i,wrong):
    global AE
    global SE
    swanlab.log({"lable_score":label_score,"score":score})
    MAE_loss = abs(float(label_score)-float(score))
    AE += MAE_loss
    MAE = AE/(i+1-wrong)
    swanlab.log({"MAE":MAE})
    MSE_loss = pow(float(label_score)-float(score),2)
    SE += MSE_loss
    MSE = SE/(i+1-wrong)
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
            
            
            text =[ {"role": "system",
                    "content": "请根据以下论述和主题,给出论证质量评分(只需要输出一个范围从0-1的分数,精确到小数点后9位),不要给出分析."},
                    { "role":"user",
                    "content":str({'sentence':sentence , 'topic': topic})          
                    }]
            

            SparkApi.main(appid,api_key,api_secret,Spark_url,domain,text)
            score = SparkApi.answer
            try:
                float(score)
            except ValueError:
                score = label_score
                wrong += 1
            SparkApi.answer=""
            loss(label_score=label_score,score=score,i=i,wrong=wrong)
            swanlab.log({"wrong_time":wrong})
            # time.sleep(1)
            


            
            
            
