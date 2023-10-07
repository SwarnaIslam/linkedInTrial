import pika
import time

rabbitmq_host = "rabbitmq"
rabbitmq_port = 5672
rabbitmq_user = "admin"
rabbitmq_password = "admin123"

def is_rabbitmq_ready():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                credentials=pika.credentials.PlainCredentials(
                    username=rabbitmq_user,
                    password=rabbitmq_password,
                ),
            )
        )
        
        # Create a channel for checking and creating the exchange
        channel = connection.channel()
        
        # Declare the exchange if it doesn't exist
        channel.exchange_declare(
            exchange="post",
            exchange_type="direct"
        )

        connection.close()
        return True
    except pika.exceptions.AMQPError:
        return False

def wait_for_rabbitmq(timeout_seconds=60):
    start_time = time.time()
    while not is_rabbitmq_ready():
        if time.time() - start_time > timeout_seconds:
            raise Exception("Timed out waiting for RabbitMQ to start.")
        time.sleep(2)

if __name__ == "__main__":
    wait_for_rabbitmq()
