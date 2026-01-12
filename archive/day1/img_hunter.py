import requests

image_url = "https://www.python.org/static/img/python-logo.png"

response = requests.get(image_url)
save_name = "python_logo.png"

with open(save_name,"wb") as f:
    f.write(response.content)

print(f"保存完了:{save_name}")
