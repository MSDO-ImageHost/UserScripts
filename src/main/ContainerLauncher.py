import docker
import docker.errors
import docker.types


def split_name_and_type(string):
    return string.rsplit('.', 1)[0]


class Container:
    def __init__(self, volume_path):
        self.volumes = {volume_path: {'bind': '/mnt/src', 'mode': 'ro'}}
        self.client = docker.from_env()
        ipam_pool = docker.types.IPAMPool(subnet='60.42.0.0/16', iprange='60.42.0.0/8')
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        try:
            self.nt = self.client.networks.create("communist_network", ipam=ipam_config, check_duplicate=True)
        except docker.errors.APIError:
            self.prune_networks("communist_network")

    def prune_networks(self, name):
        removed_networks = 0
        network_list = self.client.networks.list()
        for network in network_list:
            if network.name == name:
                network.remove()
                removed_networks += 1
        return removed_networks

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
        install = "pip3 install -q -r mnt/src/requirements.txt"
        run = "python mnt/src/" + file
        commands = ["/bin/sh", "-c", install + "&&" + run]
        return self.language_container("python", commands)

    def java_container(self, file):
        name = split_name_and_type(file)
        copy = "cp -ar /mnt/src /mnt/new"
        go_to_folder = "cd mnt && cd new"
        commands = ["/bin/sh", "-c", copy + "&&" + go_to_folder + "&& javac " + file + " && java " + name]
        return self.language_container("openjdk", commands)

    def haskell_container(self, file):
        commands = "runhaskell mnt/src/" + file
        return self.language_container("extremedevops/haskell", commands)

    def javascript_container(self, file):
        commands = "node mnt/src/" + file
        return self.language_container("node", commands)
