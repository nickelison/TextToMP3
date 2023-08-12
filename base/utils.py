import boto3
from django.conf import settings
from datetime import datetime, timedelta
from botocore.signers import CloudFrontSigner
from botocore.exceptions import ClientError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from TextToMP3.utils import get_plaintext_secret

def lambda_client():
    client = boto3.client('lambda',
                          region_name=settings.AWS_REGION,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    return client

def get_presigned_s3_file_url(s3_key, s3_bucket):
    """ Generate a presigned S3 file URL given a key.

        Return the URL as a string.

        See: https://stackoverflow.com/questions/52342974/serve-static-files-in-flask-from-private-aws-s3-bucket
    """
    s3 = boto3.client('s3',
                      region_name=settings.AWS_REGION,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    url = s3.generate_presigned_url('get_object',
                                    Params={
                                        'Bucket': s3_bucket,
                                        'Key': s3_key
                                    },
                                    ExpiresIn=100)

    return url

def get_presigned_cloudfront_file_url(resource, expires=100):
    """ Generate a presigned URL for a given CloudFront resource.

        See: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html
    """
    cf_public_key_id = settings.CLOUDFRONT_PUBLIC_KEY_ID
    url = f"https://{settings.CLOUDFRONT_DISTRIBUTION_DOMAIN}/{resource}"
    expires = datetime.utcnow() + timedelta(seconds=expires)
    
    cf_signer = CloudFrontSigner(cf_public_key_id, rsa_signer)
    
    # Create signed URL that will be valid until specified expiry date.
    signed_url = cf_signer.generate_presigned_url(url, date_less_than=expires)

    return signed_url

def delete_from_s3(s3_key, s3_bucket):
    """ Remove an object from an S3 bucket given a key.
    """
    s3 = boto3.client('s3',
                      region_name=settings.AWS_REGION,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    response = s3.delete_object(Bucket=s3_bucket, Key=s3_key)
    return response

def rsa_signer(message):
    private_key_str = get_plaintext_secret(settings.CLOUDFRONT_PRIVATE_KEY_SECRET_NAME)

    private_key = serialization.load_pem_private_key(
        private_key_str.encode(),
        password=None,
        backend=default_backend()
    )

    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())
    
