"""
Configuration for SQS operations.
"""
import os

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """Configuration class for SQS settings."""

    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')
    SQS_QUEUE_NAME = os.getenv('SQS_QUEUE_NAME', 'poc-event-queue.fifo')

    @classmethod
    def get_boto3_session_kwargs(cls):
        """Get boto3 session configuration."""
        # Use AWS CLI credentials by default
        return {'region_name': cls.AWS_REGION}
