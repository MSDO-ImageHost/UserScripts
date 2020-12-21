import os
import pika
import json
from typing import List, Dict, Tuple
from pika.spec import BasicProperties
from mongodb import MongoDbActions

try:
    AMQP_USER = os.environ["RABBITMQ_USERNAME"]
    AMQP_PASS = os.environ["RABBITMQ_PASSWORD"]
    AMQP_HOST = os.environ["RABBITMQ_HOST"]
except KeyError:
    AMQP_USER = "guest"
    AMQP_PASS = "guest"
    AMQP_HOST = "localhost"


class RabbitMQ:
    def __init__(self) -> None:
        credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASS)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=AMQP_HOST,
            port=5672,
            virtual_host='/',
            credentials=credentials))
        self.channel = self.connection.channel()

    def setup(self, events: List[str]) -> None:
        self.channel.exchange_declare(exchange='rapid', exchange_type='direct')
        self.channel.queue_declare(queue='user_scripts')
        for event in events:
            self.channel.queue_bind(queue='user_scripts', exchange='rapid', routing_key=event)
        print("Setup done")

    def send(self, event: str, body: str, properties: BasicProperties) -> None:
        self.channel.basic_publish(exchange='rapid', routing_key=event, body=body, properties=properties)
        self.connection.close()
        print("Sent event:", event)

    def receive(self) -> None:
        self.channel.basic_consume(queue='user_scripts', on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()


def callback(channel, method, properties, body) -> None:
    event = method.routing_key
    print(body)
    body = json.loads(body)
    body, properties = receive(event, body, properties)
    print(body)
    print(properties.headers)


def send(event: str, data: Dict, status_code: int, message: str, correlation_id: str, content_type: str, jwt: str = None) -> Tuple:
    rabbitmq = RabbitMQ()
    body = json.dumps(data, indent=4, default=str)
    headers = {"status_code": status_code, "message": message, "jwt": jwt}
    properties = BasicProperties(content_type=content_type, headers=headers, correlation_id=correlation_id)
    rabbitmq.send(event, body, properties)
    return body, properties


def handle_event(event: str, body: Dict, properties: BasicProperties) -> Tuple:
    mongo_actions = MongoDbActions("user_script")
    jwt = properties.headers["jwt"]

    if event == "CreateUserScript":
        print(body)
        inserted_id = mongo_actions.create_userscript(jwt, body["program"], body["main_file"], body["language"])
        if isinstance(inserted_id, str):
            return {}, 401, inserted_id
        return {"user_script": inserted_id}, 200, "OK"

    elif event == "RequestUserScriptStatus":
        pass

    elif event == "UpdateUserScript":
        updated = mongo_actions.update_userscript(
            jwt, body["user_script"], body["updated_language"], body["updated_files"], body["updated_main_file"]
        )
        if isinstance(updated, str):
            if updated == "Invalid jwt":
                response_code = 401
            elif updated == "Permission denied":
                response_code = 403
            else:
                response_code = 404
            return {}, response_code, updated

        return {}, 200, "OK"

    elif event == "DeleteUserScript":
        deleted = mongo_actions.delete_userscript(jwt, body["user_script"])
        if isinstance(deleted, str):
            if deleted == "Invalid jwt":
                response_code = 401
            elif deleted == "Permission denied":
                response_code = 403
            else:
                response_code = 404
            return {}, response_code, deleted

        return {}, 200, "OK"

    elif event == "RunUserScript":
        output = mongo_actions.run_userscript(jwt, body["user_script"])
        if isinstance(output, str):
            if output == "Invalid jwt":
                response_code = 401
            elif output == "Permission denied":
                response_code = 403
            else:
                response_code = 404
            return {}, response_code, output

        return {}, 200, "OK"

    elif event == "FindUsersUserScripts":
        user_scripts = mongo_actions.find_users_userscripts(jwt, body["user_id"])
        if isinstance(user_scripts, str):
            if user_scripts == "Invalid jwt":
                response_code = 401
            else:
                response_code = 403
            return {}, response_code, user_scripts

        return {"user_scripts": user_scripts}, 200, "OK"

    elif event == "FindUserScript":
        user_script = mongo_actions.find_userscript(body["scrip_id"])
        return {"user_scripts": user_script}, 200, "OK"


def receive(event: str, body: Dict, properties: BasicProperties) -> Tuple:
    responses = {
        "CreateUserScript": "ConfirmUserScriptCreation",
        "UpdateUserScript": "ConfirmUserScriptUpdate",
        "DeleteUserScript": "ConfirmUserScriptDeletion",
        "RunUserScript": "ConfirmUserScriptRunning",
        "FindUsersUserScripts": "ReturnUsersUserScripts",
        "findUserscript": "ReturnUserScript"
    }

    response_event = responses[event]
    correlation_id = properties.correlation_id
    content_type = properties.content_type
    response_data, code, message = handle_event(event, body, properties)

    return send(
        event=response_event,
        data=response_data,
        status_code=code,
        message=message,
        correlation_id=correlation_id,
        content_type=content_type
    )


def main():
    events = ["CreateUserScript", "UpdateUserScript", "DeleteUserScript", "RunUserScript", "FindUsersUserScripts"]
    rabbitmq = RabbitMQ()
    rabbitmq.setup(events)
    rabbitmq.receive()


if __name__ == "__main__":
    main()
