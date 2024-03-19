import json
import os
from PIL import Image, ImageDraw
from glob import glob
from tqdm import tqdm

def set_label_id():
    # 각 클래스에 대응하는 label ID를 설정
    label_class = {
        'Bone': 1, 'LF': 2, 'Vessel': 3, 'Fat': 4,
        'SoftTissue': 5, 'Disc': 6, 'Instrument': 7,
        'Cage': 8, 'Screw': 9, 'Care': 10, 'BF': 11
    }

    # 각 클래스에 대한 색상을 정의 (R, G, B 형식)
    class_colors = {
        'Bone': (153,153,153),  # 밝은 회색
        'LF': (107,142, 35),  # 올리브색
        'Vessel': (0, 255, 0),  # 초록색
        'Fat': (255, 255, 0),  # 노란색
        'SoftTissue': (70,130,180),  # 청록색
        'Disc': (0, 0, 255),  # 파란색
        'Instrument': (119, 11, 32), # 어두운 자주색
        'Cage':(  0,  0, 70),  # 매우 어두운 파란색
        'Screw': (255, 165, 0),  # 주황색
        'Care': (64, 224, 208),  # 터콰이즈
        'BF':     (220, 20, 60),  # 밝은 빨간색
    }

    return label_class, class_colors

def process_masking(json_file, label_class, class_colors, dest):
    # JSON 파일 로드
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # 빈 이미지 생성
    image_width = data['imageWidth']
    image_height = data['imageHeight']
    gt_color_image = Image.new('RGB', (image_width, image_height), (0, 0, 0))
    gt_label_image = Image.new('RGB', (image_width, image_height), (0, 0, 0))
    
    # 이미지에 polygon 적용
    draw_color = ImageDraw.Draw(gt_color_image)
    draw_label = ImageDraw.Draw(gt_label_image)
    
    for shape in data['shapes']:
        label = shape['label']
        # JSON에서 읽은 좌표를 평평한 리스트로 변환
        polygon = sum(shape['points'], [])

        if label in class_colors:
            color = class_colors[label]
            draw_color.polygon(polygon, fill=color)
        
            label_id = label_class[label]
            fill_color = (label_id, label_id, label_id)
            draw_label.polygon(polygon, fill=fill_color)

    # 결과 이미지 저장
    base_name = os.path.splitext(os.path.basename(json_file))[0]
    gt_color_image.save(os.path.join(dest, f'{base_name}_gtFine_color.png'))
    gt_label_image.save(os.path.join(dest, f'{base_name}_gtFine_labelIds.png'))

if __name__ == "__main__":
    # target directory 설정
    directory = 'dataset'

    # output directory 설정
    dest = 'output'
    os.makedirs(dest, exist_ok=True)

    # 해당 디렉토리의 *.json 파일 읽어오기, glob 사용
    json_list = glob(os.path.join(directory, '*.json'))

    # label_class 및 class_colors 설정
    label_class, class_colors = set_label_id()
    print(label_class, '\n', class_colors)
    
    # 각 JSON 파일에 대해 masking 프로세스 처리
    for json_file in tqdm(json_list):
        process_masking(json_file, label_class, class_colors, dest)