# 负责 20001----30000 的数据
import json
import csv
import io
from openai import OpenAI
import openai
# 设置OpenAI API密钥


client = OpenAI()
# 定义源CSV文件和目标CSV文件的路径
input_file_path = 'arg_quality_rank_30k.csv'
output_file_path = 'rowprocessed2.csv'

token_count=225425

def trans(text):
    global token_count
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """你是一个翻译专家，请将给你的英文翻译为中文,只输出中文，不能出中间过程和英文"""},{"role": "user", "content": text}
    ]
    )
    print(response.choices[0].message.content)
    token_count+=int(response.usage.total_tokens)
    print(token_count)
    return response.choices[0].message.content



# 打开源文件和目标文件
with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file_path, mode='a', newline='', encoding='utf-8') as outfile:
    # 创建读取器对象和写入器对象
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # 遍历源文件中的每一行，但只处理前100行
    for i, row in enumerate(reader):
        if 30000> i >= 21252:  # 只处理前100行
        # 取前两列
            first_two_columns = row[:2]
            # 对这两列的数据进行翻译
            translated_row = [trans(cell) for cell in first_two_columns]
            # 将翻译后的行写入目标文件
            writer.writerow([i+1]+translated_row)
            print(i+1)


print("处理完成，处理后的数据已写入:", output_file_path)
