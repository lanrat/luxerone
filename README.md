# Luxer One API

A Python API client to the [Luxer One Residential](https://www.luxerone.com/market/residential/) API.

## Example

```python
import luxerone

# credentials
username = "YOUR_EMAIL@example.com"
password = "**********"

# authenticate
token = luxerone.login(username, password)

# print all pending packages
pending = luxerone.pending(token)
print("pending (%d):" % len(pending))
luxerone.print_packages(pending)
```

See [example_client.py](example_client.py) for a more comprehensive example API client.
