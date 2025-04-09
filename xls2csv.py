import pandas as pd

# 读取Excel文件并转换为DataFrame对象
df1 = pd.read_excel('1.xls')
df2 = pd.read_excel('2.xls')

# 将DataFrame对象写入CSV文件
df1.to_csv('1.csv', index=False)
df2.to_csv('2.csv', index=False)