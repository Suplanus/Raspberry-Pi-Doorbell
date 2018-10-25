# Raspberry-Pi-Doorbell
A simple doorbell written in python. Makes a photo and send a push notification via Pushover

## Setup
- Enable camera on the pi with config tool
- Edit `myToken` and `myUser` with your credentials in the `doorbell.py`

## Autostart
Ohne sudo!

```shell
crontab -e
```
Am Ende einfügen:
```shell
@reboot sudo python Desktop/doorbell/doorbell.py
```

```
[Desktop Entry]
Version=1.0
Type=Application
StartupNotify=true
Name=Doorbell
Terminal=true
Exec=sudo su pi -c "python Desktop/doorbell/doorbell.py"
```
