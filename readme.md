# WiNG User Search 
## user_search.py
### Purpose
Once filling out the WiNG controller information and entering a rf-domain and a eap username, the script will make an API call to the WiNG controller collecting all clients for the entered rf-domain. Then search through all clients to find a client that matches the entered username. Once found, the users mac address, ip address, ssid, connected ap and the connected ap mac address are collected and printed on screen.

### User Input Data
###### lines 10-17
```
#Wing Controller info
wlc = "<IP ADDRESS OR DNS NAME>"
login = {"user":"<NAME>","password":"<PASSWORD>"}

# rf-domain name or device name
rf_domain = '<RF-DOMAIN>'
#user to search
username ='<USER NAME>'
```
### User Output Format
```
          User                    SSID                 IP Address             MAC Address             Access Point               AP MAC         
        tsmith24             Extreme-dot1x              10.0.4.9           78-4F-43-96-9F-95       AP-OFFICE-7532-01       74-67-F7-A4-9C-E0    
```
### Requirements
The python requests module will need to be installed

## app.py
### Purpose
Using flask, this will give a web interface, allowing rf-domain and user names to be entered and searched using the user_search.py script. The WiNG controller will need to be filled out and saved in the user_search.py script. The flask app can be installed on an apache server to be reachable by any internal user. 

### User Input Data
<p align="center">
<img src="../master/images/user_location_input.png" alt="User Location Input" height="400px">
</p>

### User Output
<p align="center">
<img src="../master/images/user_location_output.png" alt="User Location Output" height="100px">
</p>

### Requirements
in addition to the requests module required for user_search.py, the flask app will require 3 additional modules. flask, flask-bootstrap, flask-wtf
