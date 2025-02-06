usage: `./run_all.sh <output folder> <initial prompt>` 

need to fill `.env` file first with the following variables:

```
DEFAULT_INPUT_DEVICE_NAME = <input device name to use as default>
EXECUTABLE_PATH = <path to pre-built whisper.cpp executable>
MODEL_PATH = <path to whisper weights>
```
jupyter notebook will list all the devices available

ui will start at http://127.0.0.1:8050/

Tested on python 3.10