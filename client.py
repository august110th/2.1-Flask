import requests

# data = requests.post('http://127.0.0.1:5000/advt/', json={'name': 'sale bicycle', 'text': 'bicycle, 26 inch wheel, 300$'})
# data = requests.post('http://127.0.0.1:5000/advt/', json={'name': 'new store', 'text': 'we have opened, Kirova 54', 'owner_id': 1})
# data = requests.post('http://127.0.0.1:5000/owners/', json={'name': 'admin'})
# data = requests.post('http://127.0.0.1:5000/owners/', json={'name': 'guest123'})
# data = requests.post('http://127.0.0.1:5000/advt/', json={'name': 'found a cat', 'text': 'found a cat, black color', 'owner_id': 2})
# data = requests.get('http://127.0.0.1:5000/owners/1')
# data = requests.get('http://127.0.0.1:5000/advt/1')
data = requests.delete('http://127.0.0.1:5000/advt/1')
print(data.status_code)
print(data.text)