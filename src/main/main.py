import time
from rabbitmq import RabbitMQ


events = ["CreateUserScript", "UpdateUserScript", "DeleteUserScript", "RunUserScript", "FindUsersUserScripts"]
rabbitmq = RabbitMQ()
rabbitmq.setup(events)
rabbitmq.receive()
