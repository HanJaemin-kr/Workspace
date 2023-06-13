import json
import pandas as pd
import matplotlib.pyplot as plt

# 파일에서 데이터 불러오기
with open('./test/result_3.txt', 'r') as file:
    data = json.load(file)

# JSON 데이터를 Python 객체로 변환
obj_data = json.loads(json.dumps(data))

# DataFrame 생성
df = pd.DataFrame(columns=['ID', 'Algorithm', 'Value', 'Weight', 'Distance', 'Fitness', 'Time'])

# 데이터 프레임에 데이터 추가
for item in obj_data:
    for key, value in item.items():
        for inner_item in value:
            for algorithm, details in inner_item.items():
                df = df.append({
                    'ID': key,
                    'Algorithm': algorithm,
                    'Value': details['value'],
                    'Weight': details['weight'],
                    'Distance': details['distance'],
                    'Fitness': details['fitness'],
                    'Time': details['time']
                }, ignore_index=True)

# DataFrame 출력
print(df)