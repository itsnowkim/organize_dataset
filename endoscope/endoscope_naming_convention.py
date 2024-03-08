import os
import json
from PIL import Image
from tqdm import tqdm

dir = r"C:\\Users\\taesh\\Dropbox\\006_researchdata\\0006_spine_endoscope_label_2차검수\\dataset\\doublechecked\\240306"
datetime = "240306"
index = 0

for f in tqdm(os.listdir(dir)):
    if f.endswith('.jpeg'):
        # JPEG 파일을 PNG로 변경
        old_file_path = os.path.join(dir, f)
        new_file_name = f"Endoscope_Segmentation_{datetime}_{str(index).zfill(5)}.png"
        new_file_path = os.path.join(dir, new_file_name)
        
        # 이미지 파일 변환
        with Image.open(old_file_path) as img:
            img.save(new_file_path)
        
        # 대응되는 JSON 파일 찾기 및 수정
        json_file_path = os.path.splitext(old_file_path)[0] + '.json'
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as jf:
                json_data = json.load(jf)
            
            # imagePath 필드 업데이트
            json_data["imagePath"] = new_file_name
            
            # JSON 데이터를 새 파일명으로 저장
            new_json_file_name = os.path.splitext(new_file_path)[0] + '.json'
            with open(new_json_file_name, 'w') as jf:
                json.dump(json_data, jf, indent=4)

            # 기존 JSON 파일 삭제
            os.remove(json_file_path)
        
        # 원본 JPEG 파일 삭제 (선택적)
        os.remove(old_file_path)
        
        # index 증가
        index += 1
