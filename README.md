# Raspberry-Pi-Doorbell
A simple doorbell written in python. Makes a photo and send a push notification via Pushover

## Setup
- Enable camera on the pi with config tool
- Edit `myToken` and `myUser` with your credentials in the `doorbell.py`

## Autostart
Call without `sudo`!

```shell
crontab -e
```
Insert at the end:
```shell
@reboot sudo python Desktop/doorbell/doorbell.py
```
