# YOLOv5 AWS Object Detection System

**Student:** Mohamadu Hanifa Mohamadu Hamas  
**Course:** ITC5205 — Assignment 2

---

## Project Description

An end-to-end image object detection system built on AWS. Users submit an image key via a REST API, which triggers a Lambda function that sends a command to an EC2 instance running YOLOv5. The detected output image is saved back to Amazon S3.

---

## Architecture

```
User/Client
    │
    ▼
API Gateway (REST API - POST /detect)
    │
    ▼
AWS Lambda (yolov5-detection-function)
    │
    ▼
AWS SSM (sends shell command)
    │
    ▼
EC2 Instance (runs YOLOv5 detection)
    │
    ▼
Amazon S3 (stores input & output images)
```

---

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon EC2 | Hosts YOLOv5 model and runs object detection |
| Amazon S3 | Stores input images and detection results |
| AWS Lambda | Serverless coordinator between API and EC2 |
| API Gateway | REST API frontend for triggering detection |
| AWS SSM | Sends commands from Lambda to EC2 securely |
| IAM | Manages roles and permissions |
| CloudWatch | Logs and monitors Lambda execution |

---

## Project Structure

```
yolov5-aws-detection/
│
├── code/
│   ├── lambda_function.py        # Lambda function code
│   └── run_detection.sh          # YOLOv5 detection script (runs on EC2)
│
├── deploy/
│   └── deploy_instructions.md    # Step-by-step deployment guide
│
├── images/                       # Screenshots used in report
│
└── README.md                     # This file
```

---

## Prerequisites

- AWS Account with IAM permissions
- EC2 instance (Ubuntu 22.04, t2.medium or higher)
- Python 3.x, PyTorch, YOLOv5 installed on EC2
- S3 bucket created
- AWS CLI installed

---

## Quick Setup

### 1. Clone YOLOv5 on EC2
```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
python3 -m venv yolov5-env
source yolov5-env/bin/activate
pip install -r requirements.txt
```

### 2. Upload Detection Script to EC2
```bash
# Copy run_detection.sh to EC2
scp -i your-key.pem code/run_detection.sh ubuntu@your-ec2-ip:~/yolov5/
chmod +x ~/yolov5/run_detection.sh
```

### 3. Deploy Lambda Function
- Go to AWS Lambda → Create Function
- Runtime: Python 3.11
- Paste contents of `code/lambda_function.py`
- Set timeout to 3 minutes
- Attach IAM role with SSM and S3 permissions

### 4. Set Up API Gateway
- Create REST API
- Add POST method on `/detect` resource
- Link to Lambda function
- Deploy to `prod` stage
- Create API key and usage plan

---

## Usage

Upload an image to S3:
```bash
aws s3 cp your-image.jpg s3://yolov5-detection-bucket/input/your-image.jpg
```

Trigger detection via API:
```bash
curl -X POST \
  https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/detect \
  -H "x-api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image_key": "your-image.jpg"}'
```

Expected response:
```json
{
  "message": "Detection successful",
  "image_key": "your-image.jpg",
  "input": "s3://yolov5-detection-bucket/input/your-image.jpg",
  "output": "s3://yolov5-detection-bucket/output/your-image.jpg",
  "command_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

Download the result:
```bash
aws s3 cp s3://yolov5-detection-bucket/output/your-image.jpg ./result.jpg
```

---

## Dataset

- Uses COCO dataset classes (80 object categories)
- YOLOv5s pretrained weights (`yolov5s.pt`)
- Sample images from YOLOv5 built-in dataset

---

## References

- [YOLOv5 by Ultralytics](https://github.com/ultralytics/yolov5)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [AWS SSM Documentation](https://docs.aws.amazon.com/systems-manager/)
- [Amazon S3 Documentation](https://docs.aws.amazon.com/s3/)
- [PyTorch Documentation](https://pytorch.org/docs/)
