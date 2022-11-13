# Docker Observer

Record the commands you run in a container. Helps you get it fully set up and reproduce the set up to create a Dockerfile.

## Basics 
To attach to a container:

```
python observer.py <container id>
```

This gives you a shell you can use to configure your container. Once you quit the shell, `observer` will produce two output files:

* `observer_log.txt`: A log of all commands executed in the shell along with output codes.
* `observer_checked_in_files.txt`: The list of "checked in" files from the shell session.

The latter is a list of files that will then be copied into a local directory called `container_files`. 

To add a file to the checked in list, run this in the container shell:

```
checkin <file>
```

With this, the file will be copied into the `container_files` structure when you exit the shell. For example, let's say that you `checkin some_text_file.txt` and `some_text_file.txt` is at `/root/some_text_file.txt`. Then, when you exit the container shell, `some_text_file.txt` will be copied from the container to `container_files/root/some_text_file.txt`. 

This can then be used in your updated Dockerfile.


## Known limitations
- If you switch users in the shell, it won't record the actions you take the secondary user. The workaround here is using `su <other_user> -s <command>` instead of switching users.
