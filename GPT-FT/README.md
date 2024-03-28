# GPT微调指南
以下是本人的GPT微调实操指南

### 1.提示词优化与确认
反复尝试获取最优场景提示词。

### 2.数据集生成
将原始数据集处理成jsonl格式。

### 3.检测与估算价格
通过官方提供的数据集格式检测代码与估算代码对数据集进行检测与微调价格评估。详见[format_val](format_val.ipynb)

### 4.上传微调数据集与验证集
上传数据集，并获取数据集ID用于微调使用。详见[upload_data](upload_data.py)


![image.png](https://kashiwa-pic.oss-cn-beijing.aliyuncs.com/20240328201720.png)

### 5.设置参数开始训练
设置好需要的参数，包括模型，训练轮次，数据集以及后缀，然后就开始训练。详见[gpt_finetune](gpt_finetune.py)


![image.png](https://kashiwa-pic.oss-cn-beijing.aliyuncs.com/20240328201118.png)

## File

gpt_dev  :file-tdT41CadgQ9veSIF9pkkki6I
gpt_test :file-5niQQTEeZA5Tp7eqeaAf3Xwe


## Job 
FineTuningJob(id='ftjob-1wNnwfLPPO7AhjPblH0F6d9l', created_at=1711627657, error=Error(code=None, message=None, param=None, error=None), fine_tuned_model=None, finished_at=None, hyperparameters=Hyperparameters(n_epochs=3, batch_size='auto', learning_rate_multiplier='auto'), model='gpt-3.5-turbo-0125', object='fine_tuning.job', organization_id='org-RpMnx6ZFiYCP2TvaCUkqoetz', result_files=[], status='validating_files', trained_tokens=None, training_file='file-tdT41CadgQ9veSIF9pkkki6I', validation_file='file-5niQQTEeZA5Tp7eqeaAf3Xwe', user_provided_suffix='arg_quality-0328')