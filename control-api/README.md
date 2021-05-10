# control-api

## Requirements
- Python 3.6+

## Installation

```bash
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```
## Usage
```python
cd app
uvicorn main:app --reload
```

### Disclaimer
The operator should check the IP and PORTs used by pub/sub/req sockets in the [sensors](https://github.com/Towed-ROV/api/blob/main/control-api/app/api/endpoints/sensors.py) and [commands](https://github.com/Towed-ROV/api/blob/main/control-api/app/api/endpoints/commands.py).
