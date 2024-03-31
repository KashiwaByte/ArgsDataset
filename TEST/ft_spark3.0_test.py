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
domain = "patchv3"
# domain = "generalv3"

#云端环境的服务地址
Spark_url = "wss://spark-api-n.xf-yun.com/v3.1/chat"  # 微调v3.0环境的地址
# Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"   #通用v3.0地址


token = 0
AE = 0
SE = 0
LAE = 0
LSE = 0
LWrong = 0
wrong = 0
tiny_count =0
middle_count = 0
big_count = 0
swanlab.init(experiment_name="AQ_LCdev_Spark_FT2")

def quality_type(score):
    if float(score)<=0.3:
        return -1
    if 0.3<float(score)<=0.7:
        return 0
    if float(score)>0.7:
        return 1
    
def loss(label_score,score,i,wrong):
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
    MAE = AE/(i+1-wrong)
    MLAE = LAE/(i+1-wrong)
    swanlab.log({"MAE":MAE})
    swanlab.log({"MLAE":MLAE})
    MSE_loss = pow(float(label_score)-float(score),2)
    LSE_loss = pow(quality_type(label_score)-quality_type(score),2)
    SE += MSE_loss
    LSE += LSE_loss
    MSE = SE/(i+1-wrong)
    MLSE = LSE/(i+1-wrong)
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
            if quality_type(score)!=quality_type(label_score):
                LWrong+=1
       
            SparkApi.answer=""
            loss(label_score=label_score,score=score,i=i,wrong=wrong)
            swanlab.log({"wrong_time":wrong})
            swanlab.log({"Lwrong_time":LWrong})
            # time.sleep(1)
            


            
            
            
