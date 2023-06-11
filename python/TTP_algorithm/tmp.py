import axios as axios
import requests


node_list = {
    'LW140C5BFFFF560096' : {
        "schema": 'hpm',
        "facility_id": 1,
        "point_id": 9
    },
    'LW140C5BFFFF560095' : {
        "schema": 'hpm',
        "facility_id": 2,
        "point_id": 11
    }
}

feature_list = {
    "H_ppm" : 320,
    "CH4_%" : 240
}



url = 'https://town.coxlab.kr/api/v1.0/nodes'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Token': 'd7cda0476142f282085d8272fe630f296ca8c81892406e870155adc701dff09d'
  }
response = requests.get(url, headers=headers)
data = response.json()  # response를 JSON 형식으로 파싱
extracted_data = {
    'utility' : [],
    'pipe' : [],
    'hpm' : [],
}

for node in data['nodes']:
    try:
        # 추출할 값들을 변수에 할당
        node_id = node['node_id']
        schema = node_list[node_id]['schema']
        facility_id = node_list[node_id]['facility_id']
        point_id = node_list[node_id]['point_id']
        last_timestamp = node['last_timestamp']
        ch4 = node['last_data']['CH4_%']
        h = node['last_data']['H_ppm']
        #gateway = node['last_data']['gateway'][0]['mac']

        # 새로운 객체에 변수들을 담고, extracted_data 리스트에 추가
        extracted_data[schema].append({
            'facility_id': facility_id,
            'point_id': point_id,
            'feature_type_id': '31',
            'last_timestamp': last_timestamp,
            'value': ch4
        })

        extracted_data[schema].append({
            'facility_id': facility_id,
            'point_id': point_id,
            'feature_type_id': '32',
            'last_timestamp': last_timestamp,
            'value': h
        })
    except:
        # 추출할 값이 없거나 KeyError가 발생할 경우, 해당 객체는 무시하고 continue
        continue


for post_direction in extracted_data:
    print(post_direction,"  :  ",extracted_data[post_direction])


#axios.post('http://pdt.ulsan.ac.kr/'schema)
