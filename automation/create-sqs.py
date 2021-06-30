import boto3
import botocore.errorfactory

queuename = "processing-queues"

# create a boto3 client
client = boto3.client('sqs')

# Check if queue exists
def check_queue_exists(queue):
    try:
        # create the test queue
        queue = client.get_queue_url(QueueName=queuename)
    except:
        print("Queue does not exist!")
        return False
    return True

if(check_queue_exists(queuename)):
    print("Queue is already created!")
else:
    client.create_queue(QueueName=queuename)