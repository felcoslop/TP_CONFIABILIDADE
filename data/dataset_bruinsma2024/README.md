# Motor Current and Vibration Monitoring Dataset for various Faults in an E-motor-driven Centrifugal Pump

**Authors:** S. Bruinsma, R.D. Geertsma, R. Loendersloot, T. Tinga  
**Institutions:** Royal Netherlands Navy, Netherlands Defence Academy, University of Twente — Applied Mechanics  
**Corresponding author:** sj.bruinsma.01@mindef.nl  
**License:** CC0 (Public Domain)

## Introduction

This dataset contains experimental vibration and motor current and voltage data of an electric motor pump set up,
acquired at Fieldlab Techport as part of a research effort of the Royal Netherlands Navy.
The experiments consist of measurements with a wide variety of faults, distributed over 2 set ups.
One setup was operated at three different speeds, the other setup was operated at a single speed.
The majority of faults were applied in multiple levels of severity.

The file folder structure segments the measurements per measurement method, per set up, per speed
and finally per fault and severity level. The `.csv` file name contains this folder break-down and
is further separated per measurement channel.

Supplementary reports and overviews are in a separate folder to the dataset.
The overview (`measurement_overview.xlsx`) contains motor speed, fluid flow and discharge pressure
for each implemented fault. Furthermore, there are folders containing balancing reports of the
impellers and alignment reports. Datasheets of the electric motor pumps are added as well.

> The dataset itself is compressed using the built-in Windows tool 7z.  
> The compressed dataset requires **90 GB** of free hard disk space.

## Data Explanation

### Vibration Data

Collected by five Wilcoxon 786B-10 (100 mV/g) single-axis accelerometers:

| Channel | Location | Direction |
|---------|----------|-----------|
| ch1 | Electric Motor — non-driven end bearing | Horizontal |
| ch2 | Electric Motor — driven end bearing | Vertical |
| ch3 | Electric Motor — driven end bearing | Axial |
| ch4 | Pump — driven end bearing | Horizontal |
| ch5 | Pump — non-driven end bearing | Vertical |

- **Sample rate:** 20 kHz
- **Units:** g (acceleration due to gravity); first column is measurement time in seconds
- **Duration per record:** 12 seconds

### Current and Voltage Data

Collected using three CR Magnetics CR3110 current clamps and three Wago 855 voltage taps:

- Channels 1–3: three-phase current (Amperes)
- Channels 4–6: three-phase voltage (Volts)
- **Sample rate:** 20 kHz
- **Duration per record:** 15 seconds

## Dataset Location

The raw CSV files are stored under `Dataset/Dataset/` (not included in this repository due to size ~80 GB).
Download from the official source:

- **Article DOI:** [10.1016/j.dib.2023.109987](https://doi.org/10.1016/j.dib.2023.109987)
- **Dataset DOI:** [10.4121/2b61183e-c14f-4131-829b-cc4822c369d0](https://doi.org/10.4121/2b61183e-c14f-4131-829b-cc4822c369d0)

For detailed documentation of the full dataset structure, fault categories and CSV format, see
[`DATASET_README.md`](DATASET_README.md).
