import csv

def extract_columns(file_path, columns):
    extracted_data = []
    with open(file_path, 'r',encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= max(columns) + 1:             #原始数据集存在缺失的情况
                extracted_row = [row[i] for i in columns]
                extracted_data.append(extracted_row)
    return extracted_data

def write_to_csv(file_path, data):
    with open(file_path, 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)



# 提取B文件的第3和第4列
B_data = extract_columns('arg_quality_rank_30k.csv', [0,1,2,3])

# 行对齐
max_rows = len(B_data)

B_data.extend([[''] * len(B_data[0])] * (max_rows - len(B_data)))

# 拼接数据
data = [B_row for B_row in B_data]

# 写入新文件
write_to_csv('merged_file.csv', data)

print("文件提取完成！")