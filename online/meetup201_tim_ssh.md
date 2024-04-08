# MeetUp 201 - Beginners Python and Machine Learning - Wed 10 Apr 2024 - Secure Shell

Links:

- Youtube: <https://youtu.be/fxZVwRSMfc8>
- Github:  <https://github.com/timcu/bpaml-sessions/blob/master/online/meetup201_tim_ssh.md>
- Meetup:  <https://www.meetup.com/beginners-python-machine-learning/events/300141442/>

References:

- <https://openssh.com> OpenSSH

Learning objectives:

- How to install ssh
- How to securely log in to a remote computer. All traffic encrypted
- How to log in using key pair authentication.
- How to copy files to or from a remote computer
- How to run commands on a remote computer
- How to use a forwarding agent to log in to a more remote computer after logging in to a near remote computer  
- How to tunnel to a port on a remote computer
- How to set up a proxy to a remote network
- How to use a reverse tunnel to connect to an inaccessible computer behind a router
- How to create a master socket to control connections
- How to disconnect from a remote session without stopping processes

@author D Tim Cummings

Thanks to <https://asciiflow.com/> <https://app.monosketch.io/> for ascii art

## Install ssh

- Windows - Add features - SSH Client, SSH Server
- Windows (alternative to ssh client) - Install Git and ssh client available in Git Bash
- Linux (Debian) - Usually included but if not `sudo apt install openssh-server`
- Mac - included - but need to activate Remote sharing in System Preferences to connect to

## Securely log in to remote computer when username same on both computers

Example using Raspberry Pi

- `ssh ip-address`
- `ssh fully-qualified-domain-name`

```bash
# Set up variables
LOCAL_IP=192.168.1.100            # LAN IP address of the local computer
LOCAL_USER=pytho                  # username on the local computer
REMOTE1_LAN_IP=192.168.1.101      # LAN IP address of remote computer 1 which is on local LAN
REMOTE2_DMZ_IP=192.168.2.1        # LAN IP of the remote computer 2 in demilitarized zone - to which router forwards port
REMOTE3_SVR_IP=192.168.2.2        # LAN IP of the protected server 3 no direct access from the Internet 
REMOTE1_USER=bpaml                # username on the remote computer 1
REMOTE2_USER=bpaml                # username on the remote computer 2
REMOTE3_USER=bpaml                # username on the remote computer 3
LOCAL_ROUTER_IP=111.111.0.18      # Internet IP address of the local router
LOCAL_GATEWAY_IP=192.168.1.1      # LAN IP address of the local gateway
REMOTE_ROUTER_IP=222.222.0.17     # Internet IP address of the remote router
REMOTE_GATEWAY_IP=192.168.2.1     # LAN IP address of the remote gateway
```

```bash
ssh $REMOTE1_USER@$REMOTE1_LAN_IP
```

```ascii
                               LAN = SAME SUBNET (255.255.255.0)                                 
                               ssh remote-ip-address                        
                                                                                 
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│                                 │           │                                 │
│                                 │           │                                 │
│    LOCAL                        ├──────────►│22         REMOTE 1              │
│                                 │           │                                 │
│    192.168.1.100                │           │           192.168.1.101         │
│                                 │           │                                 │
└─────────────────────────────────┘           └─────────────────────────────────┘
```

- First time connecting need to accept fingerprint is correct. Before connecting through ssh, log in through a console to remote and run the following command

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

If it is the same fingerprint then you can establish the first connection.

## Securely log in to remote computer when username different on both computers

Example using Raspberry Pi

- `ssh user@ip-address`
- `ssh user@fully-qualified-domain-name`

```bash
ssh $REMOTE1_USER@$REMOTE1_LAN_IP
```

## Generate a key pair

Back on local computer. There are different types. I have chosen ed25519 which is an elliptical algorithm which chooses the shortest keys for the same security level.

```bash
ssh-keygen -t ed25519 -a 200 -C "$LOCAL_USER@bpaml-local-computer"
```

This creates two files in folder ~/.ssh

- `id_ed25519.pub` public key which you can safely give to any one you know, even strangers
- `id_ed25519` private key which you should never disclose to anyone
- never make a copy outside this computer (except sometimes Windows doesn't generate keys properly so I generate them on a Linux box first and then copy them to Windows box)
- passphrase protect these keys during the creation stage for even better security
- difficult to use a passphrase protection when using keys in scripts. I use keychain to do this

## Enable use of this key pair to authenticate user

1. Copy id_ed25519.pub to remote computer
2. Append it to a file called ~/.ssh/authorized_keys (or ~/.ssh/authorized_keys2 on some old Solaris computers)
3. Ensure ~/.ssh/authorized_keys has chmod 600 and chown owner of home directory.

Fortunately there is a command from the local computer which does all this as long as password access is currently enabled.

```bash
ssh-copy-id $REMOTE1_USER@$REMOTE1_LAN_IP
# Now I can connect without typing password for remote computer
ssh $REMOTE1_USER@$REMOTE1_LAN_IP
```

Now can disable password connections on remote computer. Disable root login at the same time.

```bash
cat <<EOF | sudo tee />etc/ssh/sshd_config/bpaml.conf
PasswordAuthentication no
PermitRootLogin no
EOF
sudo systemctl restart sshd
```

## How to copy files to or from a remote computer

The scp command is just like the cp command but over a secure network link. Can specify relative to home or absolute path names. Permissions are those of logged in user.

```bash
scp meetup201_tim_ssh.md $REMOTE1_USER@$REMOTE1_LAN_IP:meetup201_tim_ssh.md
scp meetup201_tim_ssh.md $REMOTE1_USER@$REMOTE1_LAN_IP:/home/$REMOTE1_USER/meetup201_tim_ssh_2.txt
```

## How to run commands on a remote computer

Add a command to the end of an ssh command and it will run on the remote computer and not keep a shell open

```bash
ssh $REMOTE1_USER@$REMOTE1_LAN_IP ls -al
ssh $REMOTE1_USER@$REMOTE1_LAN_IP hostname
```

## How to use a forwarding agent to log in to a more remote computer after logging in to a near remote computer

```ascii
   DIFFERENT SUBNETS JOINED BY ROUTER WITH PORT FORWARDING                          
                                                                                    
                                                                                    
     ┌───────────────┐           ┌───────────────┐                                  
     │  111.111.0.18 │           │ 222.222.0.17  │                                  
     │    ROUTER     │           │  ROUTER       │                                  
     │               │           │  Port Fwd     │                                  
     │   GATEWAY     │  INTERNET │22             │                                  
     │          ┌────┼───────────┼─────┐         │                                  
     └──────────┼────┘           └─────┼─────────┘                                  
                │                      │                                            
                │                      │                                            
                │                      │                                            
                │                      │                                            
┌───────────────┴────┐           ┌─────▼──────────────┐       ┌────────────────────┐
│                    │           │    22              │       │                    │
│  LOCAL             │           │     REMOTE2_DMZ    │       │   REMOTE3_SVR      │
│  192.168.1.100     │           │     192.168.2.1    │       │   192.168.2.2      │
│                    │           │                    │       │                    │
│                    │           │                    │       │                    │
│ ssh 222.222.0.18   │           │  ssh 192.168.2.2   ├──────►│22                  │
└────────────────────┘           └────────────────────┘       └────────────────────┘
```

On local computer, create a config file in your ssh directory

```bash
cat <<EOF | tee --append ~/.ssh/config
Host $REMOTE_ROUTER_IP
  AddKeysToAgent yes
  ForwardAgent yes
EOF
```

Now you can `ssh $REMOTE2_USER@$REMOTE_ROUTER_IP` and then from there `ssh $REMOTE3_USER@$REMOTE3_SVR_IP`

## How to tunnel to a port on a remote computer

Check firewall on remote computer. Say that only port 22 is open but want to connect to port 5000

```ascii
                                          Firewall                                              
                                                    
                                               ║                                                
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓         ║         ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                    ├────┐    ║    ┌────▶ 5000                                ┃
┃                                    ┃    │    ║    │    ┃                                     ┃
┃                                    ┃    │    ║    │    ┃                                     ┃
┃                                    ┃    │    ║    │    ┃                                     ┃
┃                          5001  ┌───┼────┘    ║    └────┼────┐                                ┃
┃                                │   ┃         ║         ┃    │                                ┃
┃                                │   ┣───────────────────┫    │                                ┃
┃                                │         Tunnel 22          │                                ┃
┃                                └────────────────────────────┘                                ┃
┃                                    ┣───────────────────┫                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛         ║         ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                               ║                                                
                                               ║                                                
                                               ║                                                
                                               ║   
```

```bash
ssh $REMOTE2_USER@$REMOTE_ROUTER_IP
sudo ufw status
exit

ssh -L 5001:localhost:5000 $REMOTE2_USER@$REMOTE_ROUTER_IP
```

Now can open http://localhost:5001 in a web browser

## How to set up a proxy to a remote network

```bash
ssh -D 9090 $REMOTE2_USER@$REMOTE_ROUTER_IP
```

Now set up socks v proxy on port 9090 to localhost and can access all computers on remote LAN

## How to use a reverse tunnel to connect to an inaccessible computer behind a router

```ascii
                                          NAT and                                               
                                          Firewall                                              
                                                                                                
                                               ║                                                
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓         ║         ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    ssh -p 1234 localhost           ├────┐    ║    ┌────▶ 22                                  ┃
┃                                    ┃    │    ║    │    ┃                                     ┃
┃                                    ┃    │    ║    │    ┃                                     ┃
┃                                    ┃    │    ║    │    ┃                                     ┃
┃                          1234  ┌───┤────┘    ║    └────┼────┐                                ┃
┃                                │   ┃         ║         ┃    │                                ┃
┃                                │   ┣───────────────────┫    │                                ┃
┃                                │   ┃     Tunnel        ┃    │                                ┃
┃                                └───────────────────────┼────┘                                ┃
┃                                    ┣───────────────────┫                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛         ║         ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                               ║                                                
                                               ║                                                
                                               ║                                                
                                               ║                                                
```

Set up reverse tunnel on remote computer

```bash
ssh -N -f -R 1234:localhost:22 $LOCAL_USER@$LOCAL_ROUTER_IP
# -N = do not execute a remote command if all you want to do is tunnel (optional)
# -f = background process so doesn't use up shell (optional)
# -R = set up reverse tunnel back to this computer
```

Now on local computer I can use reverse tunnel by doing

```bash
ssh -p 1234 $REMOTE_USER3@localhost
```

## How to create a master socket to control connections

Manual way to stop tunnel

```bash
ssh -NfR 1235:localhost:22 $REMOTE1_USER@$REMOTE1_LAN_IP
# how to stop tunnel
ps aux | grep ssh
# now kill that process
```

Alternative using master socket and connection sharing

```bash
ssh -NfR 1235:localhost:22 -M -S ~/socket_%h_%p_%r $REMOTE1_USER@$REMOTE1_LAN_IP
# check socket file exists
ls -l ~
# use socket to close tunnel
ssh -S ~/socket_%h_%p_%r -O exit $REMOTE1_USER@$REMOTE1_LAN_IP
```

## How to disconnect from a remote session without stopping processes

```bash
ssh $REMOTE_USER1@$REMOTE1_LAN_IP

cat <<EOF | tee clock.py
#!/usr/bin/env python3
import datetime
import time
with open("log-clock.txt", "w") as f:
    while True:
        f.write(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%dT%H:%M:%S") + "\n")
        f.flush()
        time.sleep(1)
EOF
chmod +x clock.py
./clock.py
```

- `<ctrl>-c` to stop running process.
- `<ctrl>-d` or `exit` to logout

Methods to run task in background so it won't stop when disconnecting

- `<ctrl>-z` to pause process. Then `jobs` to list, `bg %1` to push to background, `fg %1` to bring to foreground.
- `./clock.py &` to start in background
- Use a terminal multiplexer such as `screen` or `byobu`

Monitor whether job still running

- `tail -f log-clock.py` to monitor log file. `<ctrl>-c` to stop monitoring
- `ps aux | grep clock` to see if process still running
- `kill <process number>` to stop process

## How to do X11 forwarding over ssh

This won't work from Windows. It needs an X11 server running on local computer

```bash
ssh -X $REMOTE_USER1@$REMOTE1_LAN_IP
firefox
```

Note that many apps will crash using `-X` because it is subject to X11 SECURITY extension restrictions by default. If you want to disable the security extensions use the `-Y` option instead.
