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


def receive_messages(queue, max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.

    :param queue: The queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time,
        )
        for msg in messages:
            logger.info("Received message: %s: %s", msg.message_id, msg.body)
    except ClientError as error:
        logger.exception("Couldn't receive messages from queue: %s", queue)
        raise error
    else:
        return messages


def send_message(queue, message_body, message_attributes=None, message_group_id=None, message_deduplication_id=None):
    """
    Send a message to an Amazon SQS queue.

    :param queue: The queue that receives the message.
    :param message_body: The body text of the message.
    :param message_attributes: Custom attributes of the message. These are key-value
                               pairs that can be whatever you want.
    :param message_group_id: Required for FIFO queues. Messages with the same
                            MessageGroupId are processed in order.
    :param message_deduplication_id: Optional for FIFO queues. Used for deduplication.
    :return: The response from SQS that contains the assigned message ID.
    """
    import time
    import hashlib

    if not message_attributes:
        message_attributes = {}

    # Check if this is a FIFO queue
    is_fifo = queue.url.endswith('.fifo')

    send_params = {
        'MessageBody': message_body,
        'MessageAttributes': message_attributes
    }

    if is_fifo:
        # FIFO queues require MessageGroupId
        if not message_group_id:
            message_group_id = 'default-group'
        send_params['MessageGroupId'] = message_group_id

        # If no deduplication ID provided, generate one based on content and timestamp
        if not message_deduplication_id:
            content_hash = hashlib.md5(f"{message_body}{time.time()}".encode()).hexdigest()
            message_deduplication_id = content_hash[:20]  # Max 128 chars, using 20
        send_params['MessageDeduplicationId'] = message_deduplication_id

    try:
        response = queue.send_message(**send_params)
    except ClientError as error:
        logger.exception("Send message failed: %s", message_body)
        raise error
    else:
        return response
