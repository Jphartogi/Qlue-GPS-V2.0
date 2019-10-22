# Qlue-SIM
Qlue projects using waveshare SIM7000 IoT for GPS tracking and Data sending using SIM card

This code is modified version from https://www.waveshare.com/wiki/SIM7000E_NB-IoT_HAT. This code will be then modified to suits
the needs of the project.

This is an updated project, changing from using GPRS/EDGE to Wi-Fi based requests

## To Run
to run just simply
```python3
python3 /to/your/workspace main.py
```

# Configuration
There is a config.yaml file so it can be modified outside of the code
```yaml
GPS:
    time_to_update: every x seconds the GPS will update its position
    
WEBCAM:

    Protocol : The protocol for sending the data through the SIM 7000c
    ServerIP : Server IP for the Server used to receive the picture message
    Port : Port for the server
    
```
