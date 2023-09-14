import boto3
import json
import pandas as pd
from datetime import datetime
'''
pwd
ls -a
nano ~/.aws/credentials
cat ~/.aws/credentials
'''
def upload_to_s3(file):
    s3 = boto3.client('s3')
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    s3.upload_file(Bucket = 'retocasas', Filename=rf'{file}',Key=f'Krend/{timestamp}')
    return 'File uploaded to S3'


