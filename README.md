# Unofficial Luxer One Python Client

An unofficial Python client for the [Luxer One Residential](https://www.luxerone.com/market/residential/) API. 

## Example

```python
from luxerone.client import LuxerOneClient

# credentials
username = "youremail@example.com"
password = "your_password"

# authenticate
luxer_one_client = LuxerOneClient(username, password)
# print all pending packages
pending = luxer_one_client.get_pending_packages()
print(f'Number of pending packages:{len(pending)}')
print("=======================================")
for package in pending:
    print(f'Package id: {package.id}, Locker: {package.locker}, Access Code: {package.accessCode}')

# logout
luxer_one_client.logout()

```

For more details, please see the docs.