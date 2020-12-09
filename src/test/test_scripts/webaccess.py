import requests as req

resp = req.get("https://docs.docker.com/")
print(resp.status_code)