# SQS Send and Receive Messages

Simple Python project for sending and receiving messages from Amazon SQS FIFO queues.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS CLI** (if not already done):
   ```bash
   aws configure
   ```

3. **Set queue name** (optional - edit `.env`):
   ```bash
   AWS_REGION=us-west-2
   SQS_QUEUE_NAME=poc-event-queue.fifo
   ```

## Usage

**Test the setup:**
```bash
python test_sqs.py
```

**Use the functions directly:**
```python
from app.sqs.queue import get_queue
from app.sqs.message import send_message, receive_messages

# Get your queue
queue = get_queue("poc-event-queue.fifo")

# Send a message
response = send_message(queue, "Hello SQS!")

# Receive messages
messages = receive_messages(queue, max_number=10, wait_time=20)
for msg in messages:
    print(f"Received: {msg.body}")
    msg.delete()  # Delete after processing
```

## Functions

- `get_queue(name)` - Get existing queue
- `send_message(queue, message_body)` - Send message (handles FIFO requirements)
- `receive_messages(queue, max_number, wait_time)` - Receive messages
