# ORVYN’s Myoelectric ExoHand 🦾

Hi there! This is the software repo for **ORVYN**, an active exoskeleton hand I'm building to assist stroke patients. The idea is simple: it reads the faint electrical signals from your arm muscles (EMG) and uses motors to help you move your fingers if you can't do it on your own.

This folder contains the Python "brain" behind the project, plus some simulation scripts I wrote to test things out when I didn't have the hardware with me.

---

## What's in this repository?

Here is a quick rundown of the files, what they do, and what output you should expect:

* **`ML_Python.py`**
    * **What it does:** This is the main machine learning script. It trains a Support Vector Machine (SVM) to process the EMG signals and figure out if you're trying to make a fist, extend your hand, or just resting.
    * **Output:** When you run this, it will print some accuracy stats and then a block of **C++ code** (arrays called `svm_weights` and `svm_bias`). You literally copy-paste that text directly into your Arduino/Teensy sketch.

* **`example.py`**
    * **What it does:** Raw muscle signals are super noisy, so I wrote this to demonstrate how to clean them up. It processes some dummy data (from `.mat` files) by filtering out the noise and calculating the "envelope" (strength) of the signal.
    * **Output:** It will pop up a **graph window** with three plots stacked on top of each other: the messy raw EMG signal, the filtered version, and the final smooth line (RMS envelope) that we actually use to control the motors.

* **`svm.py`**
    * **What it does:** I wanted to really understand how SVMs work under the hood, so I wrote this simple version from scratch without using big libraries like `scikit-learn`. It's mostly for learning purposes—it classifies data points similar to how we classify muscle signals.
    * **Output:** It prints out the mathematical results of the training—specifically the **"Angle Vector" (w) and "Offset" (b)**—and then shows a few test predictions.

* **`teensy.py`**
    * **What it does:** A simulator for the Teensy microcontroller. Since I couldn't always have the robot strapped to my arm while coding, this script generates fake high-speed EMG data (voltages) so I could test my receiving code on the laptop.
    * **Output:** It prints a continuous stream of simulated readings to the console, like: `Teensy Output -> Raw: 512 | Voltage: 1.65V`. It keeps running until you hit Ctrl+C.

* **`esp_32.py`**
    * **What it does:** Similar to the Teensy script, this simulates the ESP32 module. We use the ESP32 for wireless communication, and this script generates dummy data packets to verify that the data logging and transmission systems are working correctly.
    * **Output:** Just like the Teensy script, this streams mock data packets to the console (e.g., `ESP32_DATA: ...`) to confirm the connection is active.

---

## Getting Started

```bash
pip install numpy scikit-learn scipy matplotlib
