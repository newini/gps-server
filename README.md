# GPS Server

A GPS Server with web interface powered by SQlite3, Flask, and Python.


## How to use?
### Install MongoDB
/etc/yum.repos.d/mongodb-org.repo
```
[mongodb-org-4.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
```

```
sudo dnf install mongodb-org
```

```
systemctl enable mongod
systemctl start mongod
```

## Install Apache2
allow the httpd process make network request to access to MongoDB

```
sudo /usr/sbin/setsebool -P httpd_can_network_connect 1
```


### Install python packages
```
cd gps-server
pip3 install --user --upgrade pip
pip3 install -r requirements.txt
```


# Code Detail
## A. API
### Detail
- /api/push [POST]
post data:
{imei: "", passwd: "", gps_data: ""}

return data:
{command: "", value: ""}
commands:
"idle", "run"


## B. Viewer

### 1. Pages
- /dashboard
- /login
- /manage
- /track

### 2. Classes
- Device
imei, name

## C. Command
