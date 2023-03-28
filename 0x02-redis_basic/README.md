# Project Name
**0x02. Redis basic**

## Author's Details
Name: *Wendy Munyasi.*

Email: *wendymunyasi@gmail.com*

Tel: *+254707240068.*

##  Requirements

### Python Scripts
*   Allowed editors: `vi`, `vim`, `emacs`.
*   All your files will be interpreted/compiled on Ubuntu 20.04 LTS using gcc, using python3 (version 3.8.5).
*   All your files should end with a new line.
*   The first line of all your files should be exactly `#!/usr/bin/env python3`.
*   Your code should use the pycodestyle (version `2.8.*`).
*   All your files must be executable.
*   The length of your files will be tested using `wc`.
*   All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`).
*   All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`).
*   All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)`' and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`).
*   A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified).


## Install Redis on Ubuntu 18.04
```
$ sudo apt-get -y install redis-server
$ pip3 install redis
$ sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
```

## Project Description
Learn how to use redis for basic operations.
Learn how to use redis as a simple cache.

* **0. Writing strings to Redis** - Create a `cache` class with the given requirements. - `exercise.py`.
* **1. Reading from Redis and recovering original type** - Create a `get` method that takes a key string argument and an optional `Callable` argument named `fn`. - `exercise.py`.
* **2. Incrementing values** - Implement a system to count how many times methods of the `Cache` class are called. - `exercise.py`.
* **3. Storing lists** - Define a `call_history` decorator to store the history of inputs and outputs for a particular function. - `exercise.py`.
* **4. Retrieving lists** - Implement a `replay` function to display the history of calls of a particular function. - `web.py`.


## Collaborate

To collaborate, reach me through my email address wendymunyasi@gmail.com.
