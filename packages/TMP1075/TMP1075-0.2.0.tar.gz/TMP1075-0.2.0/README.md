# TMP1075
A Python driver for the [TI TMP1075 temperature sensor](http://www.ti.com/product/TMP1075)

Currently only supports querying of the temperature.

## Usage

```python
from TMP1075 import TMP1075

tmp = TMP1075()
tmp.get_temperature()
```