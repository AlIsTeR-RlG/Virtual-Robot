# Secure UDP Teleoperation Protocol for a Networked Robot

## Overview

This project is a Python implementation of a secure and reliable teleoperation protocol for a simulated networked robot. It was inspired by the challenges faced by organisations such as CERN, where robots are remotely operated over unreliable and potentially insecure networks for tasks including inspection and maintenance in hazardous environments.

The project demonstrates how reliable communication can be built on top of UDP while introducing security mechanisms to prevent spoofing and replay attacks. Rather than relying on TCP, the protocol implements its own lightweight reliability layer, making it a useful exercise in networking, protocol design and cybersecurity.

The robot itself is a simple simulation that maintains an **x position**, **y position** and **heading**. A separate controller application sends movement commands over UDP, while the robot interprets those commands and updates its state accordingly.

This project implements a custom binary communication protocol that provides reliable command delivery over UDP through acknowledgements, retransmissions, sequence numbers and heartbeat monitoring. To secure the communication channel, packets are authenticated using HMAC-SHA256 with replay protection, ensuring that only trusted commands are executed by the robot. Together these features demonstrate practical concepts in computer networking, distributed systems and cybersecurity, closely reflecting the challenges of designing communication protocols for remotely operated robotic systems.

---

## Repository Structure

```text
Virtual-Robot/
│
├── README.md
│
└── src/
    ├── attacker/
    │   └── attacker.py
    │
    ├── common/
    │   ├── config.py
    │   ├── packets.py
    │   ├── protocols.py
    │   └── security.py
    │
    ├── controller/
    │   └── controller.py
    │
    └── robot/
        ├── motion.py
        └── robot.py
```

---

## Running the Project

Open **two terminals**.

### Terminal 1 – Start the Robot

```bash
cd src
python -m robot.robot
```

### Terminal 2 – Start the Controller

```bash
cd src
python -m controller.controller
```

The controller accepts the following commands:

| Key | Action |
|------|--------|
| W | Move Forward |
| A | Turn Left |
| S | Move Backward |
| D | Turn Right |
| X | Stop |

The robot terminal will display its updated position and heading as commands are received.

---

## Demonstrating an Attack

With the robot and controller running, open a third terminal and execute:

```bash
cd src
python -m attacker.attacker
```

The attacker sends a spoofed UDP packet without a valid authentication tag. The robot verifies every incoming packet using HMAC-SHA256 before executing it, rejecting any unauthenticated or replayed packets.

---

## Technologies Used

- Python 3
- UDP Sockets
- `socket`
- `struct`
- `threading`
- `hashlib`
- `hmac`

---

## Project Status

This project is still under active development. Future work will focus on evaluating the protocol under adverse network conditions by introducing simulated latency, jitter and packet loss using network emulation tools. Planned additions also include automated performance testing, telemetry from the robot back to the controller, packet capture analysis with Wireshark, statistical reporting, and visualisation of reliability metrics to further demonstrate the protocol's robustness in conditions similar to those encountered by remotely operated robotic systems.