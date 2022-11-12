# Docker Observer

Record the commands you run in a container. Helps you get it fully set up and reproduce the set up to create a Dockerfile.

## Known limitations
- If you switch users in the shell, it won't record the actions you take the secondary user. The workaround here is using `su <other_user> -s <command>` instead of switching users.
