import logging

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)

def _get_sqs_resource():
    """Get configured SQS resource."""
    try:
        from config import Config
        session = boto3.Session(**Config.get_boto3_session_kwargs())
        return session.resource("sqs")
    except ImportError:
        # Fallback to default configuration
        return boto3.resource("sqs")

sqs = _get_sqs_resource()


def get_queue(name):
    """
    Gets an SQS queue by name.

    :param name: The name that was used to create the queue.
    :return: A Queue object.
    """
    try:
        queue = sqs.get_queue_by_name(QueueName=name)
        logger.info("Got queue '%s' with URL=%s", name, queue.url)
    except ClientError as error:
        logger.exception("Couldn't get queue named %s.", name)
        raise error
    else:
        return queue


def create_queue(name, attributes=None):
    """
    Creates an SQS queue with the specified name.

    :param name: The name of the queue to create.
    :param attributes: Optional dictionary of queue attributes.
    :return: A Queue object for the created queue.
    """
    if attributes is None:
        attributes = {}

    try:
        if attributes:
            queue = sqs.create_queue(QueueName=name, Attributes=attributes)
        else:
            queue = sqs.create_queue(QueueName=name)
        logger.info("Created queue '%s' with URL=%s", name, queue.url)
    except ClientError as error:
        logger.exception("Couldn't create queue named %s.", name)
        raise error
    else:
        return queue


def get_or_create_queue(name, attributes=None):
    """
    Gets an existing queue or creates it if it doesn't exist.

    :param name: The name of the queue.
    :param attributes: Optional dictionary of queue attributes for creation.
    :return: A Queue object.
    """
    try:
        # Try to get existing queue first
        return get_queue(name)
    except ClientError as error:
        if error.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
            # Queue doesn't exist, create it
            logger.info("Queue '%s' doesn't exist, creating it...", name)
            return create_queue(name, attributes)
        else:
            # Some other error occurred
            raise error
