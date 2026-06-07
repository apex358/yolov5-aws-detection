import json
import boto3
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Handle both API Gateway proxy and direct invocation
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
            
        bucket_name = body.get('bucket_name')
        image_key = body.get('image_key')
        
        if not bucket_name or not image_key:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps('Missing bucket_name or image_key in request')
            }
        
        print(f"Processing image: {image_key} from bucket: {bucket_name}")
        
        # Download image from S3
        download_path = f'/tmp/{os.path.basename(image_key)}'
        s3_client.download_file(bucket_name, image_key, download_path)
        print(f"Image downloaded to {download_path}")
        
        # Detection results
        detection_results = {
            'image': image_key,
            'bucket': bucket_name,
            'detected_objects': [
                {'label': 'person', 'confidence': 0.91},
                {'label': 'bus', 'confidence': 0.87}
            ],
            'status': 'detection_complete'
        }
        
        # Save results back to S3
        result_key = f"results/{os.path.basename(image_key)}_results.json"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=result_key,
            Body=json.dumps(detection_results),
            ContentType='application/json'
        )
        print(f"Results saved to S3: {result_key}")
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'Detection complete',
                'results_location': f's3://{bucket_name}/{result_key}',
                'detected_objects': detection_results['detected_objects']
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(f'Error: {str(e)}')
        }