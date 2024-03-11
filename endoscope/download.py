import boto3
import argparse
import csv
import os
from tqdm import tqdm

s3_client = boto3.client('s3')
csv_bucket = "spinai-query-output"
data_buket = "spinai-after-labeled"

def parse_args():
    parser = argparse.ArgumentParser(description="Download CSV and associated image and JSON files from S3")
    parser.add_argument('key', type=str, help='The key of the CSV file in the S3 bucket')
    return parser.parse_args()

# CSV 파일을 로컬 시스템에 다운로드
def get_csv(key):
    csv_file_name = key.split('/')[-1]
    s3_client.download_file(csv_bucket, key, csv_file_name)
    return csv_file_name

def download_file(img_list):
    for target in tqdm(img_list):
        # aws s3 key path construct
        tokens = target.split('_')
        path = '/'.join([tokens[0], tokens[1], tokens[2], target])
        img_key = '/'.join(['images', path])
        json_key = '/'.join(['labels', path.replace('.png', '.json')])

        # 파일 다운로드
        s3_client.download_file(data_buket, img_key, f"./dataset/{target}")
        s3_client.download_file(data_buket, json_key, f"./dataset/{target.replace('.png', '.json')}")

def read_csv(csv_file_name):
    target_img_list = []
    with open(csv_file_name, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)  # csv.reader 대신 csv.DictReader 사용
        for row in csv_reader:
            # CSV 파일의 각 줄에서 이미지 파일 경로 추출
            img_path = row['imagepath']  # 딕셔너리 키 접근 방식 사용
            target_img_list.append(img_path)
    
    return target_img_list

if __name__ == "__main__":
    args = parse_args()
    
    csv_file_name = get_csv(args.key)
    target_img_list = read_csv(csv_file_name)
    download_file(target_img_list)
    print("Download completed. Target images lenght :", len(target_img_list))
    # 다운로드된 CSV 파일 삭제
    os.remove(csv_file_name)
