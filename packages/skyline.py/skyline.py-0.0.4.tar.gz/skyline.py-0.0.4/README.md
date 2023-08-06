# skyline.py
A Python Package used to interact with the [Skyline Bots](https://skylinebots.ml/) API

**This package is still in development, bugs may be present!**

---

# Features
The Features of `skyline.py` are the following:

- Posting Server Count
- Posting Uptime (coming soon!)
- And even more!

---

# Installing
You can install skyline.py by installing Python then running `pip install skyline.py` in your terminal.

---

# Feature Examples
Here are all the examples for the different features of skyline.py!

---

## Posting Server Count
```python
import skyline
import discord
from skyline import psc
from discord.ext import commands

client = commands.Bot(command_prefix="!")

"""

  psc takes in the following arguments:

  1. Your discord.py client (any)
  2. Your client's ID (string)
  3. The API Key for your bot (string)

"""
psc(client, "80954809548095480989", "insert-your-api-key-here")

client.run("token")
```

---

# Support
Here are all the ways you can get support with this package!

- ### Join the [Support Server](https://discord.gg/ygK56KaxHC)
- ### [Email](mailto:<yoshiboi18303.t@gmail.com>) the author

---