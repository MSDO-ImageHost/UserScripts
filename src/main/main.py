import time
from rabbitmq import RabbitMQ

time.sleep(10)

events = ["CreateUserScript", "UpdateUserScript", "DeleteUserScript", "RunUserScript", "FindUsersUserScripts"]
rabbitmq = RabbitMQ()
rabbitmq.setup(events)
rabbitmq.receive()
