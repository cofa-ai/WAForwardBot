# WAForwardBot
Commands:

command ADMIN_TOKEN add 7999999999 XXX
command ADMIN_TOKEN show
command ADMIN_TOKEN remove 7999999999
command ADMIN_TOKEN clean

## Installation

```bash
docker build -t wabot:latest .
docker run -d -p 5000:5000 --restart=always --name=wabot wabot
```
