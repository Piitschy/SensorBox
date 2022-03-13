# IW-Sensor-Testing
 
## Pinning

Das ist das Pinning vom Raspberry über die Relays zur Robotersteuerung:

| **IN/OUT** |  **Function**  | **GPIO** | **Pin** | **Wire** |
|:----------:|:--------------:|:--------:|:-------:|:--------:|
|      I     | start          |    12    |    32   |    13    |
|      I     | request        |    16    |    36   |    14    |
|      I     | turn off laser |    20    |    38   |    15    |
|      O     | running meas.  |    19    |    35   |    11    |
|      O     | binary 1       |     4    |     7   |     1    |
|      O     | binary 2       |    17    |    11   |     2    |
|      O     | binary 4       |    18    |    12   |     3    |
|      O     | binary 8       |    27    |    13   |     4    |
|      O     | binary 16      |    25    |    22   |     5    |
|      O     | binary 32      |    23    |    16   |     6    |
|      O     | binary 64      |    24    |    18   |     7    |
|      O     | binary 128     |     5    |    29   |     8    |
|      O     | binary 256     |     6    |    31   |     9    |
|      O     | binary 512     |    26    |    37   |    12    |

## Beep-Codes

Momentan laufen die Beep-Codes nur in der Routine der Pin-control:

1 Piep: Start/Pause der Messung

2 Piep: Stop der Messung und Beginn der Auswertung und Übertragung

3 Piep: Reset, bereit zum erneuten Starten
