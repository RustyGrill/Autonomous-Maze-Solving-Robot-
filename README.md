# 🤖 Maze Solving Robot using Raspberry Pi (Wall-Following)

This project implements a basic autonomous maze-solving robot using a **right wall-following algorithm**. The robot uses **ultrasonic sensors** to detect walls and a **motor driver (L298N)** to control motion.

Built using **Raspberry Pi (Python + GPIO)**.

---

## 📦 Project Structure


---

## 🧰 Hardware Used

| Component              | Qty |
|------------------------|-----|
| Raspberry Pi (any model with GPIO) | 1   |
| HC-SR04 Ultrasonic Sensors        | 3   |
| L298N Motor Driver                | 1   |
| DC Motors                         | 2   |
| Wheels + Chassis                  | 1 set |
| Power Supply (battery/USB)       | 1   |
| Jumper Wires, Breadboard (optional) | — |

---

## 🧠 Algorithm (Right Wall-Following)

- If the **right wall is open**, turn right and move forward.
- Else if the **front is blocked**, turn left.
- Else, move forward.

---

## 🐍 Software Requirements

- Raspberry Pi OS (any version)
- Python 3 (default)
- GPIO Library

Install required Python package (usually pre-installed):
```bash
sudo apt update
sudo apt install python3-rpi.gpio
