import docker

client = docker.from_env()
volumes = {'C:/Users/Mikkel/code/ImageHost/UserScripts/test_scripts': {'bind': '/mnt/src', 'mode': 'rw'}}

def python_test():
    container = client.containers.run("python", "python mnt/src/test.py", volumes=volumes)
    print(container)

def java_test():
    container = client.containers.create(image="openjdk", volumes=volumes, working_dir='/mnt/src')
    container.start()
    result = container.exec_run('javac test.java')
    output = container.exec_run('java test')

    print(result)
    print(output)

    container.stop()
    container.remove()

def js_test():
    container = client.containers.run("node", "node mnt/src/test.js", volumes=volumes)
    print(container)

def haskell_test():
    container = client.containers.run("haskell", "runhaskell mnt/src/test.hs", volumes=volumes)
    print(container)

haskell_test()