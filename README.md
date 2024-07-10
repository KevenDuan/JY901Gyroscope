# JY901Gyroscope

## Applicable Equipment

Raspberry Pi

## How to use

First, clone the project locally:

```
git clone https://github.com/KevenDuan/JY901Gyroscope.git
```

Then open the project:

```
cd JY901Gyroscope
```

Run the example code:

```
python example.py
```

You can later change the code in the project according to your needs.

## File description

- Gyroscope.py: Encapsulated library for gyroscopes.
- example.py: Example program.

## Function description

`gyroscope(port, baud)`: port use '/dev/ttyAMA0' for USB or '/dev/ttyAMA0' for GPIO.

The default baud rate for JY901 is 9600.

`gyroscope.display`: Displays gyroscope nine-axis data.

**To be updated...**



