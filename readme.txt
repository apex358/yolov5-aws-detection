Name: Mohamadu Hanifa Mohamadu Hamas

Project: Implementing an Image Object Identification System on AWS
Course: ITC5205 - Assignment 2
Institution: Apex Australia Higher Education

Description:
This project implements a serverless image object detection system on AWS
using YOLOv5, AWS Lambda, Amazon API Gateway, and Amazon S3.

Users upload an image to the S3 bucket and trigger the API Gateway endpoint
with the image details. The Lambda function downloads the image from S3,
runs YOLOv5 object detection, and saves the detected objects as a JSON
result file back to S3.

AWS Services Used:
- EC2 (yolov5-instance, t3.micro, Ubuntu 22.04) - YOLOv5 environment
- S3 (yolov5-detection-bucket) - Image and result storage
- Lambda (yolov5-detection-function, Python 3.11) - Detection trigger
- API Gateway (yolov5-api) - REST API endpoint
- IAM (yolov5-ec2-role) - Access management

API Endpoint:
POST https://3btfikjtb4.execute-api.us-east-1.amazonaws.com/prod/detect
Body: {"bucket_name": "yolov5-detection-bucket", "image_key": "your-image.jpg"}

Folder Structure:
/code     - All source code (lambda_function.py)
/deploy   - Deployable Lambda zip file
/images   - Screenshots used in the report

