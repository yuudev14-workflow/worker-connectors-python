import asyncio
import json
import aio_pika
import aio_pika.abc

from src.settings import settings
from src.core.workflow import WorkflowGraph


async def consume_messages(loop):
    # Connecting with the given parameters is also possible.
    # aio_pika.connect_robust(host="host", login="login", password="password")
    # You can only choose one option to create a connection, url or kw-based params.
    await asyncio.sleep(1)
    connection = await aio_pika.connect_robust(
       settings.mq_url, loop=loop
    )

    async with connection:
        # Creating channel
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        # Declaring queue
        worlflow_queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            settings.workflow_queue,
            durable=True,
            auto_delete=False,
            exclusive=False,
        )

        # workflow_processor_queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
        #     settings.WORKFLOW_PROCESSOR_QUEUE,
        #     durable=True,
        #     auto_delete=False,
        #     exclusive=False,
        # )

        async with worlflow_queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            print("listening to mq")
            async for message in queue_iter:
                async with message.process():
                    json_body: dict = json.loads(message.body.decode())
                    graph = json_body.get("graph")
                    task_information = json_body.get("tasks")

                    try:

                        if graph is None or task_information is None:
                            raise Exception("either graph and task_information is None")
                        
                        workflow = WorkflowGraph(graph=graph, task_information=task_information)
                        workflow.generate_chain_task()
                        print(json_body)
                        # await channel.default_exchange.publish(
                        #     aio_pika.Message(body=message.body),
                        #     routing_key=workflow_processor_queue.name,
                        # )
                    except Exception as e:
                        print(e)
                        
