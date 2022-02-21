# IW-Sensor-Testing
 
## Pinning

Das ist das Pinning vom Raspberry über die Relays zur Robotersteuerung:

| **IN/OUT** |  **Function**  | **GPIO** | **Pin** | **Wire** |
|:----------:|:--------------:|:--------:|:-------:|:--------:|
|      I     | start          |    12    |    32   |    13    |
|      I     | request        |    16    |    36   |    14    |
|      I     | turn off laser |    20    |    38   |    15    |
|      O     | binary 1       |     4    |    7    |     1    |
|      O     | binary 2       |    17    |    11   |     2    |
|      O     | binary 4       |    18    |    12   |     3    |
|      O     | binary 8       |    27    |    13   |     4    |
|      O     | binary 16      |    23    |    16   |     6    |
|      O     | binary 32      |    24    |    18   |     7    |
|      O     | binary 64      |     5    |    29   |     8    |
|      O     | binary 128     |     6    |    31   |     9    |
|      O     | binary 256     |    13    |    33   |    10    |
|      O     | binary 512     |    26    |    37   |    12    |