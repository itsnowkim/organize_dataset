import boto3
import argparse
import csv
import os
from tqdm import tqdm

s3_client = boto3.client('s3')
bucket_name = "spinai-query-output"

def parse_args():
    parser = argparse.ArgumentParser(description="Download CSV and associated image and JSON files from S3")
    parser.add_argument('key', type=str, help='The key of the CSV file in the S3 bucket')
    return parser.parse_args()

# CSV 파일을 로컬 시스템에 다운로드
def get_csv(key):
    csv_file_name = key.split('/')[-1]
    s3_client.download_file(bucket_name, key, csv_file_name)
    return csv_file_name

def download_file(key, local_path):
    # 파일 다운로드
    s3_client.download_file(bucket_name, key, local_path)

def read_csv_and_download_files(csv_file_name):
    target_img_list = []
    with open(csv_file_name, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in tqdm(csv_reader):
            # CSV 파일의 각 줄에서 이미지 파일 경로 추출
            img_path = row['imagepath']  # CSV 형식에 따라 조정이 필요할 수 있습니다.
            target_img_list.append(img_path)
            img_key = f"images/{img_path}"
            json_key = f"labels/{img_path.replace('.png', '.json')}"

            # 이미지와 JSON 파일 다운로드
            download_file(img_key, f"./dataset/{img_path}")
            download_file(json_key, f"./dataset/{img_path.replace('.png', '.json')}")
    
    return target_img_list

if __name__ == "__main__":
    args = parse_args()
    
    csv_file_name = get_csv(args.key)
    target_img_list = read_csv_and_download_files(csv_file_name)
    
    print("Download completed. Target images:", target_img_list)
    # 다운로드된 CSV 파일 삭제
    os.remove(csv_file_name)
