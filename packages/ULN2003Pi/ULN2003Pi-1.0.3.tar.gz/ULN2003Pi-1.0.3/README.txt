# ULN2003

Package to control a ULN2003 driver for a 28BYJ-48 (or any unipolar) stepper motor on a Raspberry Pi

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ULN2003.

```bash
pip install ULN2003
```

## Usage

```python
from ULN2003 import ULN2003

pins=[26, 19, 13, 6] #The logical pins of the ULN2003 as connected to the Raspberry Pi with the pins indexed by their BCM numbering
Stepper=ULN2003(pins) #Creates an instance of the ULN2003 driver

Stepper.step(n=100) #Steps forwards by 100 steps

Stepper.step(n=-100) #Steps backwards by 100 steps
```

## License
[MIT](https://choosealicense.com/licenses/mit/)