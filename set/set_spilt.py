import pandas as pd

# 读取CSV文件
df = pd.read_csv('arg_quality_WA.csv')

# 根据第三列的内容拆分数据框
train_df = df[df['set'] == 'train']
dev_df = df[df['set'] == 'dev']
test_df = df[df['set'] == 'test']

# 将数据框保存为新的CSV文件
train_df.to_csv('train.csv', index=False)
dev_df.to_csv('dev.csv', index=False)
test_df.to_csv('test.csv', index=False)