"""
main file
"""

import asyncio
import aio_pika
import aio_pika.abc


async def main(loop):
    # Connecting with the given parameters is also possible.
    # aio_pika.connect_robust(host="host", login="login", password="password")
    # You can only choose one option to create a connection, url or kw-based params.
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )

    async with connection:
        queue_name = "workflow"

        # Creating channel
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        # Declaring queue
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            durable=True,
            auto_delete=False,
            exclusive=False,
        )

        queue2: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            "workflow_processor",
            durable=True,
            auto_delete=False,
            exclusive=False,
        )

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    print(message.body)
                    await channel.default_exchange.publish(
                        aio_pika.Message(body=str(message.body).encode()),
                        routing_key=queue2.name,
                    )

                    if queue.name in message.body.decode():
                        break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
