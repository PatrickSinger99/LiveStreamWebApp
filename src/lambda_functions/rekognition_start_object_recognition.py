import json
import boto3
from botocore.config import Config
import re
import os

def lambda_handler(event, context):
    
    
    
    def run_rekognition():

        # set up boto3 config for boto3 clients
        my_config = Config(
            region_name = 'eu-west-1',
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        processor_name = 'RekognitionStreamProcessor'
    
        # set up boto3 clients for the used services
        rekognition_client = boto3.client("rekognition", config=my_config, aws_access_key_id=os.environ['access_key'], aws_secret_access_key=os.environ['secret_key'])
        kinesis_client = boto3.client('kinesisvideo', config=my_config, aws_access_key_id=os.environ['access_key'], aws_secret_access_key=os.environ['secret_key'])
        kinesis_video_media_client = boto3.client('kinesis-video-media', config=my_config, endpoint_url='https://***.amazonaws.com', aws_access_key_id=os.environ['access_key'], aws_secret_access_key=os.environ['secret_key']
        )
    
        #get existing stream processors
        check_stream_processors = rekognition_client.list_stream_processors()
        print(check_stream_processors)
    
        # delete stream processor if it already exists to create a new stream processor with other settings
        #delete_response = rekognition_client.delete_stream_processor(
        #Name="RekognitionStreamProcessor"
        # )
        #print(f"stream processor deleted {delete_response}")
        
        #check_stream_processors = rekognition_client.list_stream_processors()
        #print(check_stream_processors)

        # check if stream processor already exists
        if ('StreamProcessors' not in check_stream_processors.keys() or ('StreamProcessors' in check_stream_processors.keys() and check_stream_processors['StreamProcessors'][0]['Name'] != processor_name)):
    
            # create new stream processor
            stream_processing = rekognition_client.create_stream_processor(
            DataSharingPreference= { "OptIn":True
            },
            Input= {
                "KinesisVideoStream": {
                "Arn": "arn:aws:***"
                }
            },
            Name= processor_name,
            Output= {
                "S3Destination": {
                "Bucket": "rekognitionoutputbucket2",
                "KeyPrefix": "data/"
                }
            },
            NotificationChannel={
            "SNSTopicArn": "arn:aws:***"
            },
            RoleArn= "arn:aws:iam::***",
            Settings= {
                "ConnectedHome": {
                "Labels": [
                    "PET"
                ],
                "MinConfidence": 5
                }
            }
            )
    
            print(f"check stream creation {stream_processing}")

        # get fragments from kinesis stream 
        frame_response = kinesis_video_media_client.get_media(
            StreamARN='arn:aws:kinesisvideo:eu-west-1:***"',
            StartSelector={'StartSelectorType': 'NOW'},
        )
    
        payload = frame_response['Payload']
    
        # decode response StreamingBody
        payload_string = str(payload.read(amt=1024).decode('iso-8859-1'))
    
        # extract fragment number
        fragment_number = re.split(r'/(\d+)', payload_string)
    
        print(f"FRAGMENT NUMBER {fragment_number[1]}")
    
        # start stream processor
        response =  rekognition_client.start_stream_processor(
            Name=processor_name,
            StartSelector={
                'KVSStreamStartSelector': {
                    "FragmentNumber": str(fragment_number[1])
                }
            },
            StopSelector={
                'MaxDurationInSeconds': 30
            }
        )

        # check status of stream processor
        check_stream_processors = rekognition_client.list_stream_processors()
        print(f"check stream exists {check_stream_processors}")
    
        return check_stream_processors
        
        
    response = run_rekognition()

    return {
        'statusCode': 200,
        'body': response
    }