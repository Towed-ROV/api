# control-api
This repository contains the REST-API used in the application layer of the total software system. The REST-API has responsibility for the communicating between the Surface Unit, Towed-ROV, Sonar API, the GUI and Database. In many ways, this repo is the glue holding the system safe and sound.


![no_image](https://github.com/Towed-ROV/api/blob/main/control-api/docs/imgs/system.png?raw=true)

## Requirements
- Python 3.6+

## Installation

```bash
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```

### Disclaimer
The operator should validate the IP and PORTs used by communcation entities in the [sensors](https://github.com/Towed-ROV/api/blob/main/control-api/app/api/endpoints/sensors.py), [commands](https://github.com/Towed-ROV/api/blob/main/control-api/app/api/endpoints/commands.py) and [videos](https://github.com/Towed-ROV/api/blob/main/control-api/app/api/endpoints/videos.py).

## Usage
```python
cd app
uvicorn main:app --reload
```


