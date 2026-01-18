# DHT11 Sensor Wiring Diagram for Raspberry Pi Pico W 2

## Pinout Overview

The DHT11 digital temperature and humidity sensor is a popular, inexpensive sensor for IoT and weather monitoring projects.

### DHT11 Pin Configuration

```
    DHT11 Sensor
    ┌─────────────┐
    │ 1  2  3  4  │
    └─────────────┘
     │  │  │  │
     │  │  │  └─ GND (Pin 4)
     │  │  └───── NC (Not Connected)
     │  └──────── Data (Pin 2)
     └──────────── VCC +5V (Pin 1)
```

## Raspberry Pi Pico W 2 Pinout

```
    Pi Pico W 2 Top View (USBA Connector on left)
    ┌─────────────────────────────┐
 GP0 │ 1                        40 │ VBUS
 GP1 │ 2                        39 │ VSYS
 GND │ 3                        38 │ GND
 GP2 │ 4                        37 │ 3V3_EN
 GP3 │ 5                        36 │ 3V3
 GP4 │ 6    Pi Pico W 2         35 │ ADC_VREF
 GP5 │ 7                        34 │ GP28
 GND │ 8                        33 │ GND
 GP6 │ 9                        32 │ GP27
 GP7 │10                        31 │ GP26
GP8 │11                        30 │ Run
GP9 │12                        29 │ GP22
GND │13                        28 │ GND
GP10│14                        27 │ GP21
GP11│15                        26 │ GP20
GP12│16                        25 │ GP19
GP13│17                        24 │ GP18
GND │18                        23 │ GND
GP14│19                        22 │ GP17
GP15│20                        21 │ GP16
    └─────────────────────────────┘
```

## Wiring Diagram: DHT11 to Pi Pico W 2

```
┌─────────────────────────────────────────────────────────┐
│  DHT11 Sensor                    Pi Pico W 2            │
│  ┌──────────┐                                           │
│  │ 1 2 3 4  │                                           │
│  └──────────┘                                           │
│    │ │ │ │                                              │
│    │ │ │ │                                              │
│    │ │ │ └─────────────┐                                │
│    │ │ │               │                                │
│    │ │ └──────────┐    │    GND (Pin 3, 8, 13, 18, 23) │
│    │ │            │    │                                │
│    │ └─ Data ─────┼────┼── GPIO 15 (Pin 20)            │
│    │              │    │                                │
│    └─ VCC +5V ────┼────┴── VBUS (Pin 40)               │
│                   │        OR 3V3 (Pin 36)             │
│                   │                                      │
│ Pull-up Resistor: │                                      │
│ 10kΩ between      │                                      │
│ Data line and VCC │                                      │
└─────────────────────────────────────────────────────────┘
```

## Detailed Wiring Instructions

### Components Needed:
- 1x DHT11 Temperature & Humidity Sensor
- 1x 10kΩ Resistor (Pull-up resistor)
- Jumper wires (Male-to-Female recommended)
- Breadboard (optional but recommended)

### Wiring Steps:

1. **VCC Connection (Pin 1 of DHT11)**
   - Connect to VBUS (Pin 40) for 5V power
   - OR Connect to 3V3 (Pin 36) for 3.3V power
   - Note: DHT11 works best at 5V, but 3.3V is acceptable

2. **Data Connection (Pin 2 of DHT11)**
   - Connect to GPIO 15 (Pin 20) on Pi Pico W 2
   - Add a 10kΩ pull-up resistor between this line and VCC
   - The pull-up resistor is ESSENTIAL for proper operation

3. **GND Connection (Pin 4 of DHT11)**
   - Connect to any GND pin:
     - Pin 3 (GND)
     - Pin 8 (GND)
     - Pin 13 (GND)
     - Pin 18 (GND)
     - Pin 23 (GND)

4. **NC Pin (Pin 3 of DHT11)**
   - Leave unconnected (NC = Not Connected)

## Complete Connection Table

| DHT11 Pin | Pin Name | Pi Pico W 2 Pin | Description |
|-----------|----------|-----------------|-------------|
| 1         | VCC      | 40 or 36        | Power (5V or 3.3V) |
| 2         | Data     | 20 (GPIO15)     | Digital Data Output |
| 3         | NC       | —               | Not Connected |
| 4         | GND      | 3, 8, 13, 18, 23| Ground |
| Pull-up   | 10kΩ     | Between Data & VCC | Required |

## Code Configuration

In the `server_pico_w2.py` file, the GPIO pin is configured as:

```python
from dht import DHT11
from machine import Pin

# GPIO15 corresponds to Pin 20 on Pico W
dht_pin = Pin(15, Pin.IN, Pin.PULL_UP)
dht = DHT11(dht_pin)
```

## Troubleshooting

### Issue: "Sensor Not Responding"
- ✓ Verify 10kΩ pull-up resistor is connected
- ✓ Check all wire connections
- ✓ Ensure power is properly supplied (5V preferred)
- ✓ Try using VBUS (5V) instead of 3V3

### Issue: "Inconsistent Readings"
- ✓ Add a 0.1µF capacitor between VCC and GND close to sensor
- ✓ Ensure stable power supply
- ✓ Check for loose connections

### Issue: "GPIO Pin Error"
- ✓ Verify Pin 20 (GPIO15) is available
- ✓ Check it's not used for other functions
- ✓ Ensure correct import: `from dht import DHT11`

## Hardware Tips

- **Breadboard Layout**: Place DHT11 on breadboard with pull-up resistor for cleaner connections
- **Cable Length**: Keep sensor cable under 1 meter for best results
- **Shielding**: For noisy environments, consider shielded twisted pair cable
- **Mounting**: Keep sensor away from direct sunlight and heat sources for accurate readings

## Alternative Pin Configuration

If GPIO15 (Pin 20) is not available, you can use any other GPIO pin:

```python
# Example: Using GPIO 14 (Pin 19) instead
dht_pin = Pin(14, Pin.IN, Pin.PULL_UP)
dht = DHT11(dht_pin)
```

Just update the pin number in the code and re-wire accordingly.

## References

- [DHT11 Datasheet](https://www.mouser.com/datasheet/2/758/DHT11-9d-000553-7ca.pdf)
- [Raspberry Pi Pico W Documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico.html)
- [MicroPython DHT Library](https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/sensor/dht)
