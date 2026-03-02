# mqttLedSign

A simple Python program for controlling an RGB LED matrix panel via MQTT.
Designed to run on a Raspberry Pi using the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.

## Features

- Display time, scrolling messages, and countdown to events
- Control lines, colors, and modes through MQTT topics
- Configuration via environment variables (supports `.env` files)

## Getting Started

### Prerequisites

- Raspberry Pi (or Linux system) with the `rpi-rgb-led-matrix` library installed
- Python 3.7+
- MQTT broker accessible on network

Install the Python dependencies:

```sh
python -m pip install -r requirements.txt
```

> **Note:** `rpi-rgb-led-matrix` is not available on PyPI. Clone
> and install it following the instructions in its repository.

### Configuration

Copy `env.sample` to `.env` and fill in your MQTT connection details:

```txt
MQTT_BROKER=yourbroker.example
MQTT_USERNAME=username
MQTT_PASSWORD=secret
```

Alternatively export the environment variables directly.

### Usage

Run the sign program with appropriate flags for your LED panel:

```sh
sudo python mqttSign.py --led-chain=3 --led-rows=16
```

The script will connect to the MQTT broker and subscribe to topics
prefixed with `ledSign/` and `nextEvent/`.

### MQTT Topics

| Topic                     | Description                                |
|--------------------------|--------------------------------------------|
| `ledSign/line1`          | Text for first line                        |
| `ledSign/line2`          | Text for second line                       |
| `ledSign/line3`          | Text for third line                        |
| `ledSign/color`          | RGB color, comma separated e.g. `255,0,0`  |
| `ledSign/mode`           | Display mode (`clock`, `bigClock`, etc.)   |
| `ledSign/EN`             | `ON`/`OFF` to enable or disable display    |
| `nextEvent/<field>`      | Event details for countdown mode           |

### Service Unit

An example `ledSign.service` unit file is included for systemd-based
systems. Adjust paths as necessary.

## Development

- Additional comments are embedded in the source to explain logic.
- Use `python -m pylance` or other linters to check the code.

## License

MIT, see LICENSE file (if applicable).