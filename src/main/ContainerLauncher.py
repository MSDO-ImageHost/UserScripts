import docker


def split_name_and_type(string):
    return string.rsplit('.', 1)[0]


class Container:
    def __init__(self, volume_path):
        self.volumes = {volume_path: {'bind': '/mnt/src', 'mode': 'rw'}}
        self.client = docker.from_env()

    def container_starter(self, language, file):
        method_name = str(language) + '_container'
        method = getattr(self, method_name, lambda: "Invalid Language")
        return method(file)

    def python_container(self, file):
        output = self.client.containers.run("python", "python mnt/src/test.py", volumes=self.volumes, remove=True)
        return output

    def java_container(self, file):
        container = self.client.containers.create(image="openjdk", volumes=self.volumes, working_dir='/mnt/src')
        container.start()
        result = container.exec_run('javac ' + file)    #TODO compiled class file in test_scripts?
        name = split_name_and_type(file)
        output = container.exec_run('java ' + name)
        container.stop()
        container.remove()
        return output

    def haskell_container(self, file):
        output = self.client.containers.run("haskell", "runhaskell mnt/src/test.hs", volumes=self.volumes, remove=True)
        return output

    def javascript_container(self, file):
        output = self.client.containers.run("node", "node mnt/src/test.js", volumes=self.volumes, remove=True)
        return output

