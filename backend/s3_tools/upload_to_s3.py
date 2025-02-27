import datetime
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import uuid
import pprint
import os
from dotenv import load_dotenv

# TODO: load these from environment variables

# Load environment variables from .env file
load_dotenv()

# Constants
S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET')
REGION_NAME = os.getenv('AWS_REGION')

s3_client = boto3.client(
    's3',
    region_name=REGION_NAME,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


# Global mapping (for demonstration, use a database in production)
document_mapping = {}


def create_document(file_bytes):
    # Generate a new UUID to use as both the document's public ID and S3 key
    doc_uuid = str(uuid.uuid4())
    s3_key = f"{doc_uuid}.pdf"

    try:
        # Upload file to S3 using the generated key
        s3_client.put_object(Bucket=S3_BUCKET_NAME,
                             Key=s3_key, Body=file_bytes, ContentType='application/pdf')
        # Generate the presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': s3_key, },
            ExpiresIn=3600,  # expires in 1 hour
            # 'ResponseContentDisposition': 'inline'
        )
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

    # Calculate the expiration time
    expires_at = datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(seconds=3600)
    # Store the mapping with additional metadata if needed
    document_mapping[doc_uuid] = {
        "s3_key": s3_key,
        "presigned_url": presigned_url,
        "expires_at": expires_at,
        "filename": s3_key,
        "filetype": "application/pdf"
    }

    pprint.pprint(document_mapping)

# Return the document UUID (and optionally the presigned URL if needed immediately)
    return doc_uuid, presigned_url


def upload_to_s3(file_bytes):

    OBJECT_NAME = f'{uuid.uuid4()}.pdf'

    try:
        s3_client.put_object(Bucket=S3_BUCKET_NAME,
                             Key=OBJECT_NAME, Body=file_bytes)
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': S3_BUCKET_NAME,
                                                            'Key': OBJECT_NAME},
                                                    ExpiresIn=3600)
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

    return response

# fetch pdf from s3 bucket

# Instead of returned the file, we should return the presigned url


def fetch_file_from_s3(doc_id):
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=doc_id)
        return response['Body'].read()
    except Exception as e:
        print(f"Error fetching file: {e}")
        return None
