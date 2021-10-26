This script is to compare current offset value of a consumer group between specified two clusters.

## how to use

```
$ python compare-current-offsets.py --consumer-group "app-A" --source-broker "1.1.1.1:9092" --destination-broker "2.2.2.2:9092"
consumer-group    topic               partition    source-current-offset    destination-current-offset  synced
----------------  ----------------  -----------  -----------------------  ----------------------------  --------
app-A             topic01                     0                       13                            13  True
app-A             topic02                     0                       20                            20  True
```

## build exacutable binary
Use pyinstaller

```
$ pyinstaller compare-current-offsets.py --onefile
```
