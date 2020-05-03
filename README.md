# Humax router CLI

A python package and cli to interact with Humax router.

## Usage

```console
$ humax ip
160.147.189.48
```

```console
$ humax --help
usage: run_humax.py [-h] [-r ROUTER]
                    {post,list-methods,config-path,ip,get-port-forwarding} ...

Program to interact with Humax router

positional arguments:
  {post,list-methods,config-path,ip,get-port-forwarding}
                        Action to perform
    post                Make a POST request to /api
    list-methods        List available methods.
    config-path         Print config file path.
    ip                  Display WAN IP.
    get-port-forwarding
                        Display port forwarding rules.

optional arguments:
  -h, --help            show this help message and exit
  -r ROUTER, --router ROUTER
                        Specify the section in config file to use. Defaults to
                        'DEFAULT'.
```

## Installation
```
$ pip3 install --user humax
```

## Shell completion
Optionally, to install bash and fish completion run
```
$ make completions-install-bash
```
or
```
$ make completions-install-bash
```
respectively.

### Dependencies
Python packages `requests`, `pygments`, and `pyxdg`.

## Uninstallation
```
$ pip3 uninstall humax
```

## License

This project is licensed under the terms of the MIT license.
