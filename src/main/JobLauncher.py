import shutil
from os import path
from kubernetes import client, config


class Job:
    def __init__(self, volume_path, program_id):
        self.program_id = program_id
        self.volume_path = volume_path

    def job_starter(self, language, file):
        method_name = str(language) + '_job'
        invalid_method_name = 'Invalid Language'
        method = getattr(self, method_name, invalid_method_name)
        if method == invalid_method_name:
            return invalid_method_name
        return method(file)

    def create_job_object(self, docker_image, commands):
        # Configureate Pod template container
        volume_name = "default"
        volume_mount = client.V1VolumeMount(
            name=volume_name,
            mount_path='/mnt/src',
            read_only=True
        )
        container = client.V1Container(
            name=self.program_id,
            image=docker_image,
            command=commands,
            volume_mounts=[volume_mount]
        )

        host_path = client.V1HostPathVolumeSource(self.volume_path, "Directory")
        volume = client.V1Volume(
            name=volume_name,
            host_path=host_path,
        )
        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(restart_policy="Never", containers=[container], volumes=[volume])
        )
        # Create the specification of deployment
        spec = client.V1JobSpec(
            template=template,
            backoff_limit=4)
        # Instantiate the job object
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=self.program_id),
            spec=spec)

        return job

    def create_job(self, docker_image, commands):
        try:
            config.load_incluster_config()
        except Exception as e:
            print(e)
            config.load_kube_config()
        batch_v1 = client.BatchV1Api()

        job = self.create_job_object(docker_image, commands)
        api_response = batch_v1.create_namespaced_job(
            body=job,
            namespace="default")
        print("Job created. status='%s'" % str(api_response.status))
        shutil.rmtree(self.volume_path)

    def python_job(self, file):
        install = "if mnt/src/requirements.txt \n then pip3 install -q -r mnt/src/requirements.txt \n fi"
        run = "python mnt/src/" + file
        commands = ["/bin/sh", "-c", "ls -la"]
        return self.create_job("python", commands)

    def java_container(self, file):
        name = file.rsplit('.', 1)[0]
        copy = "cp -ar /mnt/src /mnt/new"
        go_to_folder = "cd mnt && cd new"
        commands = ["/bin/sh", "-c", copy + "&&" + go_to_folder + "&& javac " + file + " && java " + name]
        return self.create_job("openjdk", commands)

    def haskell_container(self, file):
        commands = "runhaskell mnt/src/" + file
        return self.create_job("extremedevops/haskell", commands)

    def javascript_container(self, file):
        commands = "node mnt/src/" + file
        return self.create_job("node", commands)

    def delete_job(self, api_instance):
        api_response = api_instance.delete_namespaced_job(
            name=self.program_id,
            namespace="default",
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
        print("Job deleted. status='%s'" % str(api_response.status))


def main():
    job = Job("/mnt", "test-program")
    job.python_job("test.py")


if __name__ == '__main__':
    main()