import docker
import docker.errors


def split_name_and_type(string):
    return string.rsplit('.', 1)[0]


class Container:
    def __init__(self, volume_path):
        self.volumes = {volume_path: {'bind': '/mnt/src', 'mode': 'rw'}}
        self.client = docker.from_env()

    def container_starter(self, language, file):
        method_name = str(language) + '_container'
        invalid_method_name = 'Invalid Language'
        method = getattr(self, method_name, invalid_method_name)
        if method == invalid_method_name:
            return invalid_method_name
        return method(file)

    def language_container(self, docker_image: str, commands):
        container = self.client.containers.run(
            image=docker_image, command=commands, volumes=self.volumes, detach=True
        )
        try:
            container.stop(timeout=120)
            output = container.logs()
        except docker.errors.APIError:
            output = "APIError"
        container.remove(v=True)
        return output

    def python_container(self, file):
        commands = "python mnt/src/" + file
        return self.language_container("python", commands)

    def java_container(self, file):
        name = split_name_and_type(file)
        go_to_folder = "cd mnt && cd src"
        commands = ["/bin/sh", "-c", go_to_folder + "&& javac " + file + " && java " + name]
        return self.language_container("openjdk", commands)

    def haskell_container(self, file):
        commands = "runhaskell mnt/src/" + file
        return self.language_container("extremedevops/haskell", commands)

    def javascript_container(self, file):
        commands = "node mnt/src/" + file
        return self.language_container("node", commands)
