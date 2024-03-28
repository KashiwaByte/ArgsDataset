import csv
import json

csv_file = 'set/test.csv'
jsonl_file = 'LLAMA-FT/llama_test.jsonl'

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
            message={ "instruction":"请根据以下论述和主题,给出论证质量评分(只需要输出一个范围从0-1的分数,精确到小数点后9位).","input": str({'sentence':{sentence},'topic': {topic}}),"output":score}
            messages.append(message)
# 保存为JSONL文件
with open(jsonl_file, 'w', encoding='utf-8') as file:
    for message in messages:
        file.write(json.dumps(message, ensure_ascii=False) + '\n')
        