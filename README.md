# GPS Server

A GPS Server with web interface powered by SQlite3, Flask, and Python.


## How to use?
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
