# robotsparsetools
robots.txt is important when crawling website  

This module will help you parse robots.txt

# Install
```bash
$ pip install robotsparsetools
```

# Usage
## Parse
Please create an Parse instance first  

```python
from robotsparsetools import Parse

url = "URL of robots.txt you want to parse"
p = Parse(url) # Create an instance. Returns a Parse class with the useragent as the key

# Get allow list
p.Allow(useragent)

# Get disallow list
p.Disallow(useragent)

# Get value of Crawl-delay(Return value is int or None)
p.delay(useragent)

# Find out if crawls are allowed
p.can_crawl(url, useragent)
```

If no useragent is specified, the value of '*' will be referenced  

Also, since the Parse class inherits from dict, you can also use it like dict

```python
from robotsparsetools import Parse

p = Parse(url)
p["*"]
p.get("*") # Can also use get method
```  

## Read(✨ new in 1.2.0)
By passing the text to the Read function, it will parse that content

```python
from robotsparsetools import Read
import requests

url = "URL of robots.txt you want to parse"
r = requests.get(url)
p = Read(r.text) # The return value is a Parse instance
```

## Error Classes
Also, there are two error classes

```python
from robotsparsetools import NotURLError, NotFoundError
```

# License
This program's license is [MIT](https://github.com/mino-38/robotsparsetools/blob/main/LICENSE)
