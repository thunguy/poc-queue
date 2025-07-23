#!/usr/bin/env python3
"""
Simple setup script to verify AWS connectivity.
"""
import logging
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Check AWS connectivity and list queues."""
    try:
        from config import Config

        print("SQS Setup Check")
        print("=" * 20)

        # Test AWS connectivity
        session = boto3.Session(**Config.get_boto3_session_kwargs())
        sqs = session.client('sqs')
        response = sqs.list_queues()

        print(f"✓ AWS connectivity successful! (Region: {Config.AWS_REGION})")

        if 'QueueUrls' in response:
            print(f"Found {len(response['QueueUrls'])} existing queues:")
            for url in response['QueueUrls']:
                queue_name = url.split('/')[-1]
                print(f"  - {queue_name}")
        else:
            print("No existing queues found")

        print(f"\nConfigured to use queue: {Config.SQS_QUEUE_NAME}")
        print("Run: python test_sqs.py")

    except Exception as e:
        print(f"✗ Setup failed: {e}")
        print("Make sure AWS CLI is configured: aws configure")
        exit(1)


if __name__ == "__main__":
    main()
