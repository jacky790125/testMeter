# testMeter

## deploy
```
cp meter.service /lib/systemd/system
systemctl enable meter
systemctl start meter
```

## Exec
```
pipenv run python3 meter.py
```

## config
```
ExecStart $CMD
WorkingDirectory= {$PATH}
```
