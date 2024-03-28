import csv
import json

csv_file = 'set/train.csv'
jsonl_file = 'SPARK-FT/spark_train.jsonl'

# 生成JSONL文件
messages = []

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行

    for row in reader:
        if len(row) >= 4:
            sentence = row[0]
            topic = row[1]
            score = row[3]
            message={ "input": str({'sentence':{sentence},'topic': {topic}}),"target":score}
            messages.append(message)
# 保存为JSONL文件
with open(jsonl_file, 'w', encoding='utf-8') as file:
    for message in messages:
        file.write(json.dumps(message, ensure_ascii=False) + '\n')
        