import time
from kubernetes import client, config


def create_files_command(files):
    command = ""
    for file in files:
        filename = file["filename"]
        content = file["content"]
        command += f"cat << EOF > {filename}\n{content}\nEOF\n"
    return command


class Job:
    def __init__(self, program_id):
        self.program_id = program_id

    def job_starter(self, language, files, mainfile):
        method_name = str(language) + '_job'
        invalid_method_name = 'Invalid Language'
        method = getattr(self, method_name, invalid_method_name)
        if method == invalid_method_name:
            return invalid_method_name
        return method(files, mainfile)

    def create_job_object(self, docker_image, commands):
        # Configureate Pod template container
        container = client.V1Container(
            name=self.program_id,
            image=docker_image,
            command=commands,
            # volume_mounts=[volume_mount]
        )

        # Create and configurate a spec section
        template = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(restart_policy="Never", containers=[container])
        )

        # Create the specification of deployment
        spec = client.V1JobSpec(
            template=template,
            backoff_limit=4,
        )

        # Instantiate the job object
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=self.program_id),
            spec=spec
        )

        return job

    def create_job(self, docker_image, commands):
        try:
            config.load_incluster_config()
        except Exception as e:
            print(e)
            config.load_kube_config()

        batch_v1 = client.BatchV1Api()
        job = self.create_job_object(docker_image, commands)
        batch_v1.create_namespaced_job(
            body=job,
            namespace="default"
        )

        print("Now sleeping...")
        time.sleep(60)
        print("Fetching output...")
        output = self.get_output(batch_v1)
        print("Done fetching output. Logging to database now...")
        self.log_output(output)
        print("Deleting job...")
        self.delete_job(batch_v1)

    def get_output(self, api_instance):
        job_def = api_instance.read_namespaced_job(name=self.program_id, namespace='default')
        controllerUid = job_def.metadata.labels["controller-uid"]

        core_v1 = client.CoreV1Api()

        pod_label_selector = "controller-uid=" + controllerUid
        pods_list = core_v1.list_namespaced_pod(
            namespace='default',
            label_selector=pod_label_selector,
            timeout_seconds=10
        )
        pod_name = pods_list.items[0].metadata.name
        try:
            pod_log_response = core_v1.read_namespaced_pod_log(name=pod_name, namespace='default')
            return pod_log_response
        except client.rest.ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)

    def log_output(self, output):
        from mongodb import MongoDbActions
        mg = MongoDbActions("user_script")
        mg.create_log(output, self.program_id)

    def python_job(self, files, mainfile):
        install = "pip3 install -q -r requirements.txt"
        command = create_files_command(files)
        command += install + " && "
        command += "python " + mainfile
        commands = ["/bin/sh", "-c", command]
        return self.create_job("python", commands)

    def java_job(self, files, mainfile):
        name = mainfile.rsplit('.', 1)[0]
        command = create_files_command(files)
        command += "javac " + mainfile + " && "
        command += "java " + name
        commands = ["/bin/sh", "-c", command]
        return self.create_job("openjdk", commands)

    def haskell_job(self, files, mainfile):
        command = create_files_command(files)
        command += "runhaskell " + mainfile
        commands = ["/bin/sh", "-c", command]
        return self.create_job("extremedevops/haskell", commands)

    def javascript_job(self, files, mainfile):
        command = create_files_command(files)
        command += "node " + mainfile
        commands = ["/bin/sh", "-c", command]
        return self.create_job("node", commands)

    def delete_job(self, api_instance):
        api_response = api_instance.delete_namespaced_job(
            name=self.program_id,
            namespace="default",
            body=client.V1DeleteOptions(propagation_policy='Foreground'),
            grace_period_seconds=0
        )
        print("Job deleted. status='%s'" % str(api_response.status))
