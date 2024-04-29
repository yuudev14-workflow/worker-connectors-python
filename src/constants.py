from dotenv import load_dotenv
import os

load_dotenv()


MQ_URL = os.getenv("MQ_URL", "amqp://guest:guest@127.0.0.1/")

WORKFLOW_QUEUE = os.getenv("WORKFLOW_QUEUE", "workflow")
WORKFLOW_PROCESSOR_QUEUE = os.getenv("WORKFLOW_PROCESSOR_QUEUE", "workflow_processor")