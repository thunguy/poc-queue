#!/usr/bin/env python3
"""
Test script for SQS send and receive functionality.
"""
import logging
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Test SQS send and receive operations."""
    from app.sqs.queue import get_queue
    from app.sqs.message import send_message, receive_messages
    from config import Config

    print("SQS Send/Receive Test")
    print("=" * 30)
    print(f"Queue: {Config.SQS_QUEUE_NAME}")
    print(f"Region: {Config.AWS_REGION}")
    print()

    try:
        # Get the queue
        queue = get_queue(Config.SQS_QUEUE_NAME)
        logger.info(f"Connected to queue: {queue.url}")

        # Send a test message
        test_message = {
            "message": "Hello from SQS test!",
            "timestamp": time.time(),
            "test_id": "test_001"
        }

        logger.info("Sending test message...")
        response = send_message(queue, json.dumps(test_message))
        logger.info(f"Message sent! ID: {response['MessageId']}")

        # Wait and receive messages
        logger.info("Waiting 2 seconds before receiving...")
        time.sleep(2)

        logger.info("Receiving messages...")
        messages = receive_messages(queue, max_number=10, wait_time=5)

        if messages:
            logger.info(f"Received {len(messages)} messages:")
            for i, msg in enumerate(messages, 1):
                logger.info(f"Message {i}: {msg.body}")

                # Delete the message after processing
                msg.delete()
                logger.info(f"Message {msg.message_id} deleted")
        else:
            logger.info("No messages received")

        logger.info("Test completed successfully!")

    except Exception as e:
        logger.error(f"Test failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
