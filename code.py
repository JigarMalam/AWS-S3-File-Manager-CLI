import logging
import boto3
import argparse
import sys
import os
from botocore.exceptions import ClientError

# Initialize S3 Client
s3=boto3.resource("s3")

def create_bucket(bucket_name, region):
    s3_client = boto3.client('s3', region_name=region)
    location = {'LocationConstraint': region}
    s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)

    print(f"Bucket Create with name of '{bucket_name}'& at '{region}' region.")

def list_buckets():
    print("Listing all buckets...")
    for bucket in s3.buckets.all():
        print(f' {bucket.name}')

def upload_file(bucket, file_path, object_name):
    
    s3 = boto3.resource('s3')
    try:
        with open(file_path, 'rb') as data:
            s3.Bucket(bucket).put_object(Key=object_name, Body=data)
            
        print(f"Successfully uploaded {file_path} to {bucket}/{object_name}")
        
    except Exception as e:
        print(f"Upload failed: {e}")

def download_file(bucket, object_name, D_path):
    s3 = boto3.client('s3') 
    local_file_path = os.path.join(D_path, object_name)
    with open(local_file_path, 'wb') as f: 
        s3.download_fileobj(bucket, object_name, f)

    print(f"Downloading {object_name} from {bucket}...")
    
    

def delete_file(bucket, object_name):
    s3 = boto3.client('s3')
    try:
        response = s3.delete_object( Bucket = bucket, Key = object_name)
        print(f"Deleting {object_name} from {bucket}...")
        print(f"AWS Response Code: {response['ResponseMetadata']['HTTPStatusCode']}")
    except ClientError as e:
        print(f"Error deleting file: {e}")

def main():
    parser = argparse.ArgumentParser(description="AWS S3 File Manager CLI")
    
    # Main command (list, upload, download, delete, Create_Bucket)
    parser.add_argument('command', choices=['list', 'upload', 'download', 'delete','create_bucket'], help="Action to perform")
    
    # Optional arguments
    parser.add_argument('--bucket', help="Bucket name")
    parser.add_argument('--region', help="Region name")
    parser.add_argument('--file', help="Local file path (for upload/download)")
    parser.add_argument('--name', help="S3 Object name (for upload/download/delete)")
    

    args = parser.parse_args()

    try:
        if args.command == 'list':
            list_buckets()
        elif args.command == 'create_bucket':
            if not args.bucket or not args.region:
                print("Error: Requires --bucket --Region")
                return
            create_bucket(args.bucket,args.region)
            
        
        elif args.command == 'upload':
            if not args.bucket or not args.file:
                print("Error: Upload requires --bucket and --file")
                return
            # If no name provided, use the file name as the S3 object name
            #obj_name = args.name if args.name else args.file
            upload_file(args.bucket, args.file, args.name)

        elif args.command == 'delete':
            delete_file(args.bucket, args.name)
        elif args.command == 'download':
             download_file(args.bucket,args.name, args.file)   
    except Exception as e:
        print(f"An error occurred: {e}")

object_name = os.path.basename("Upload")

if __name__ == "__main__":

  

    main()