import time
from rabbitmq import RabbitMQ


events = ["CreateUserScript", "UpdateUserScript", "DeleteUserScript", "RunUserScript", "FindUsersUserScripts", "FindUserScript"]
rabbitmq = RabbitMQ()
rabbitmq.setup(events)
rabbitmq.receive()
