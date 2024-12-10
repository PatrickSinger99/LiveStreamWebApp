PII#!/bin/bash
cd /home/admin/amazon-kinesis-video-streams-producer-sdk-cpp/build
export GST_PLUGIN_PATH=/home/admin/amazon-kinesis-video-streams-producer-sdk-cpp/build
export AWS_DEFAULT_REGION=eu-west-1
export AWS_ACCESS_KEY_ID=***
export AWS_SECRET_ACCESS_KEY= ***
./kvs_gstreamer_sample OnlyFish