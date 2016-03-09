VManage
=======

VManage is a wrapper around vagrant which detects all vagrants in use and provides simple CLI commands to manage them.

    $ vmanage --help

    usage: vmanage [-h]
               {name,box1,box2,/path/to/box/3}
               ...

    positional arguments:
        {name,box1,box2,/path/to/box/3}
        name                Give this vbox a custom name
        box1                Manage box1
        box2                Manage box2
        /path/to/box/3      Manage /path/to/box/3

    optional arguments:
        -h, --help            show this help message and exit

where `box1` and `box2` are names you give vagrant boxes.

`vmanage name box3` in /path/to/box/3 will allow you to name the current vagrant box so the name is better.

Provides:

- `vmanage box1 up`
- `vmanage box1 halt`
- `vmanage box1 ssh`


TO DO
=====

- Currently there is no unique name constraint, so multiple vagrants can have the same name and the result will be unknown.

