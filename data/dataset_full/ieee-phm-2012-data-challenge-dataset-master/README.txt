IEEE PHM 2012 Data Challenge - PRONOSTIA Bearing Run-to-Failure Dataset

Authors: P. Nectoux, R. Gouriveau, K. Medjaher, E. Ramasso, B. Morello, N. Zerhouni, C. Varnier
FEMTO-ST Institute, AS2M Department; Besancon, France
Organizers: IEEE Reliability Society and FEMTO-ST Institute
Contact: ieee-2012-PHM-challenge@femto-st.fr


Introduction

This dataset contains experimental vibration and temperature data of rolling-element bearings
run to failure, acquired on the PRONOSTIA platform built at the AS2M department of the FEMTO-ST
Institute. It was released for the IEEE PHM 2012 Prognostic Challenge, focused on the estimation
of the Remaining Useful Life (RUL) of bearings.

The bearings were not seeded with artificial defects. A radial load exceeding the bearing's
maximum dynamic load (4000 N) was applied so the bearings degrade naturally, which means a
failed bearing usually contains several concurrent defects (balls, rings and cage). Experiments
were stopped for safety once the vibration amplitude exceeded 20 g, which also defines end of life.

A total of 17 run-to-failure experiments are provided: 6 in the learning set and 11 in the test
set, spread over three operating conditions. The 11 test bearings were truncated for the challenge
so that participants had to predict the remaining life. Experiment durations range from about 1 h
to 7 h. The file folder structure segments the measurements per set, then per bearing. Each bearing
folder contains the CSV files for that experiment, one file per acquisition snapshot, separated into
vibration files (acc_xxxxx.csv) and temperature files (temp_xxxxx.csv).

The bundled report IEEEPHM2012-Challenge-Details.pdf contains the full description of the
PRONOSTIA platform, the sensors and the challenge.


Operating conditions

Condition 1: 1800 rpm and 4000 N (Bearing1_1 to Bearing1_7)
Condition 2: 1650 rpm and 4200 N (Bearing2_1 to Bearing2_7)
Condition 3: 1500 rpm and 5000 N (Bearing3_1 to Bearing3_3)


Data explanation

Vibration data was collected by two DYTRAN 3035B 100 mV/g miniature accelerometers placed at
90 degrees to each other and mounted radially on the outer race of the test bearing:
Horizontal accelerometer (X axis)
Vertical accelerometer (Y axis)
Sample rate is set to 25.6 kHz. Each snapshot is 2560 samples (1/10 s) recorded every 10 seconds.
All vibration data is in g.

Temperature data was collected by a platinum RTD PT100 (class 1/3 DIN) probe placed in a hole
close to the outer ring. The sample rate is 10 Hz and 600 samples are recorded every minute.

CSV columns:
acc_xxxxx.csv  -> Hour, Minute, Second, micro-second, Horizontal acceleration, Vertical acceleration
temp_xxxxx.csv -> Hour, Minute, Second, 0.x second, RTD temperature
Some bearings were recorded with vibration only and have no temp_xxxxx.csv files.


Licensing

The datasets are made publicly available. Publications making use of these data are requested
to cite the following paper:
Patrick Nectoux, Rafael Gouriveau, Kamal Medjaher, Emmanuel Ramasso, Brigitte Morello,
Noureddine Zerhouni, Christophe Varnier. PRONOSTIA: An Experimental Platform for Bearings
Accelerated Life Test. IEEE International Conference on Prognostics and Health Management,
Denver, CO, USA, 2012.
