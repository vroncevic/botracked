# Tracked Robot Control Studio & Telemetry Monitor

<img align="right" src="https://raw.githubusercontent.com/vroncevic/botracked/dev/docs/botracked_logo.png" width="25%">

**botracked** is a modular Python desktop application, telemetry monitor, and mission scripting suite for tracked robotic platforms.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![botracked python checker](https://github.com/vroncevic/botracked/actions/workflows/botracked_python_checker.yml/badge.svg)](https://github.com/vroncevic/botracked/actions/workflows/botracked_python_checker.yml) [![botracked package checker](https://github.com/vroncevic/botracked/actions/workflows/botracked_package_checker.yml/badge.svg)](https://github.com/vroncevic/botracked/actions/workflows/botracked_package_checker.yml) [![botracked interface checker](https://github.com/vroncevic/botracked/actions/workflows/botracked_interface_checker.yml/badge.svg)](https://github.com/vroncevic/botracked/actions/workflows/botracked_interface_checker.yml) [![botracked isp checker](https://github.com/vroncevic/botracked/actions/workflows/botracked_isp_checker.yml/badge.svg)](https://github.com/vroncevic/botracked/actions/workflows/botracked_isp_checker.yml) [![botracked srp checker](https://github.com/vroncevic/botracked/actions/workflows/botracked_srp_checker.yml/badge.svg)](https://github.com/vroncevic/botracked/actions/workflows/botracked_srp_checker.yml) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/botracked.svg)](https://github.com/vroncevic/botracked/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/botracked.svg)](https://github.com/vroncevic/botracked/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [🏗 Architecture & SOLID Principles](#-architecture--solid-principles)
    - [SOLID Principles Compliance](#solid-principles-compliance)
    - [Automated Quality Gates (`run_quality_gates.sh`)](#automated-quality-gates-run_quality_gatessh)
  - [✨ Features](#-features)
  - [📜 Tracked Bot Domain-Specific Language (DSL) & `.track` Programs](#-tracked-bot-domain-specific-language-dsl--track-programs)
    - [Tracked Bot DSL Instruction Reference](#tracked-bot-dsl-instruction-reference)
    - [Example `.track` Program: Autonomous Perimeter Patrol](#example-track-program-autonomous-perimeter-patrol)
  - [📡 Binary Packet Communication Protocol & Framing](#-binary-packet-communication-protocol--framing)
    - [Command Frames (PC $\to$ Robot)](#command-frames-pc-%5Cto-robot)
    - [Telemetry Frames (Robot $\to$ PC)](#telemetry-frames-robot-%5Cto-pc)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
    - [CLI Command Options](#cli-command-options)
    - [Interactive Mission Planning & Telemetry Workflow](#interactive-mission-planning--telemetry-workflow)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/botracked/dev/docs/debtux.png)

[![botracked python3 build](https://github.com/vroncevic/botracked/actions/workflows/botracked_python3_build.yml/badge.svg)](https://github.com/vroncevic/botracked/actions/workflows/botracked_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**botracked** is located at **[pypi.org](https://pypi.org/project/botracked/)**.

You can install by using pip

```bash
# python3
pip3 install botracked
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/botracked/releases/)** download and extract release archive.

To install **botracked** type the following

```bash
tar xvzf botracked-x.y.z.tar.gz
cd botracked-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/botracked-*-py3-none-any.whl
rm -f get-pip.py
chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/botracked_run.py
ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/botracked_run.py /usr/local/bin/botracked_run.py
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/botracked/releases)** download and extract release archive.

To install **botracked** locate and run setup.py with arguments

```bash
tar xvzf botracked-x.y.z.tar.gz
cd botracked-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### 📦 Dependencies

**botracked** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
* [pyserial - Python Serial Port Extension](https://pypi.org/project/pyserial/) [![License: BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

### 📁 Tool structure

**botracked** is based on OOP and Clean Architecture.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
    botracked/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── connection_params.py
         │   │   ├── dsl/
         │   │   │   ├── ast_instruction.py
         │   │   │   ├── compiled_step.py
         │   │   │   ├── __init__.py
         │   │   │   ├── token.py
         │   │   │   └── token_type.py
         │   │   ├── __init__.py
         │   │   ├── motion_command.py
         │   │   ├── protocol_opcode.py
         │   │   └── telemetry_data.py
         │   └── service/
         │       ├── bot_motion_service.py
         │       ├── bot_service.py
         │       ├── bot_telemetry_service.py
         │       ├── communication/
         │       │   ├── ibinary_codec.py
         │       │   ├── ibot_transport.py
         │       │   ├── icrc8_calculator.py
         │       │   ├── __init__.py
         │       │   └── itelemetry_observer.py
         │       ├── dsl/
         │       │   ├── __init__.py
         │       │   ├── itbot_compiler.py
         │       │   ├── itbot_dsl_service.py
         │       │   ├── itbot_lexer.py
         │       │   ├── itbot_parser.py
         │       │   ├── tbot_compiler.py
         │       │   ├── tbot_dsl_service.py
         │       │   ├── tbot_lexer.py
         │       │   └── tbot_parser.py
         │       ├── ibot_connection_service.py
         │       ├── ibot_mission_service.py
         │       ├── ibot_motion_service.py
         │       ├── ibot_service.py
         │       ├── ibot_telemetry_service.py
         │       ├── __init__.py
         │       ├── mission_runner.py
         │       └── telemetry_poller.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── studio_command_definition.py
         │   │   └── studio_command_executor.py
         │   ├── communication/
         │   │   ├── binary_codec.py
         │   │   ├── crc8_calculator.py
         │   │   ├── __init__.py
         │   │   ├── preferences/
         │   │   │   ├── connection_preferences_repository.py
         │   │   │   └── __init__.py
         │   │   ├── serial_transport.py
         │   │   └── tcp_transport.py
         │   ├── config/
         │   │   ├── botracked.cfg
         │   │   ├── botracked.logo
         │   │   └── scheme.json
         │   ├── gui/
         │   │   ├── connection/
         │   │   │   ├── connection_callbacks.py
         │   │   │   ├── connection_panel.py
         │   │   │   ├── connection_panel_config.py
         │   │   │   └── __init__.py
         │   │   ├── controls/
         │   │   │   ├── __init__.py
         │   │   │   ├── jog_panel.py
         │   │   │   ├── jog_panel_callbacks.py
         │   │   │   └── jog_panel_config.py
         │   │   ├── editor/
         │   │   │   ├── dsl_editor_panel.py
         │   │   │   ├── dsl_editor_panel_config.py
         │   │   │   ├── dsl_preset_loader.py
         │   │   │   ├── dsl_syntax_highlighter.py
         │   │   │   ├── dsl_syntax_highlighter_config.py
         │   │   │   ├── __init__.py
         │   │   │   └── mission_callbacks.py
         │   │   ├── engine.py
         │   │   ├── gui_config.py
         │   │   ├── gui_event_mediator.py
         │   │   ├── igui.py
         │   │   ├── __init__.py
         │   │   ├── stream/
         │   │   │   ├── __init__.py
         │   │   │   ├── log_panel.py
         │   │   │   └── log_panel_config.py
         │   │   ├── telemetry/
         │   │   │   ├── __init__.py
         │   │   │   ├── telemetry_panel.py
         │   │   │   └── telemetry_panel_config.py
         │   │   └── theme/
         │   │       ├── colors.py
         │   │       ├── __init__.py
         │   │       └── style.py
         │   └── __init__.py
         ├── __init__.py
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     22 directories, 101 files
```
</details>

#### 🏗 Architecture & SOLID Principles

**botracked** is built on a strictly decoupled, **Layered Clean Architecture** where presentation, domain logic, AST compilation, and hardware communication are segregated through pure Python protocols:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │                       BotrackedGUI                      │ (Presenter / Main Window)
                  └────────────────────────────┬────────────────────────────┘
                                               │ Mediates UI Events via GUIEventMediator
         ┌─────────────────────────┬───────────┴─────────────┬──────────────────────────┐
         ▼                         ▼                         ▼                          ▼
┌──────────────────┐      ┌─────────────────┐      ┌───────────────────┐      ┌──────────────────┐
│ ConnectionPanel  │      │    JogPanel     │      │   DSLEditorPanel  │      │  TelemetryPanel  │
│(Serial / TCP/IP) │      │(D-Pad Controls) │      │ (Script & Runner) │      │ (Gauges & Faults)│
└────────┬─────────┘      └────────┬────────┘      └─────────┬─────────┘      └────────┬─────────┘
         │                         │                         │                         │
         └────────────┬────────────┴─────────────────────────┴─────────────────────────┘
                      │ Observes / Commands IBotService
                      ▼
         ┌──────────────────────────┐
         │        BotService        │ (Application Facade / Coordinator)
         └────────────┬─────────────┘
                      │
         ┌────────────┴────────────┬────────────────────────┬──────────────────────────┐
         ▼                         ▼                        ▼                          ▼
┌──────────────────┐      ┌──────────────────┐     ┌─────────────────┐        ┌──────────────────┐
│ BotMotionService │      │BotTelemetryServ. │     │ MissionRunner   │        │   TBotDslService │
│(Kinematic Drive) │      │ (State & Poller) │     │ (Step Execution)│        │ (Lexer & Parser) │
└────────┬─────────┘      └────────┬─────────┘     └────────┬────────┘        └────────┬─────────┘
         │                         │                        │                          │
         └────────────┬────────────┴────────────────────────┘                          ▼
                      │ Dispatches Packets via IBotTransport                  ┌──────────────────┐
                      ▼                                                       │   TBotCompiler   │
         ┌──────────────────────────┐                                         └──────────────────┘
         │  Serial / TCP Transport  │
         └────────────┬─────────────┘
                      │ Frames Packets via IBinaryCodec & ICrc8Calculator
                      ▼
         ┌──────────────────────────┐
         │ BinaryCodec & CRC8 Calc  │
         └──────────────────────────┘
```

##### SOLID Principles Compliance

* **S — Single Responsibility Principle (SRP)**:
  * Every module and class has exactly one clearly bounded reason to change.
  * Parser, lexer, and compiler logic is decomposed into dedicated handlers (`TBotLexer`, `TBotParser`, `TBotCompiler`, `TBotDslService`) rather than a monolithic interpreter.
  * GUI tabs are decomposed into panel configs, callbacks, and layout managers.
  * Enforced by automated gate: strict limit of $\le 15$ methods per class across the entire codebase.
* **O — Open/Closed Principle (OCP)**:
  * The DSL parser, compiler, and binary codec are open for extension without modifying existing code.
  * New motion opcodes and instructions plug into dedicated registries dynamically.
* **L — Liskov Substitution Principle (LSP)**:
  * Pure structural subtyping via Python `@runtime_checkable Protocol` definitions. Concrete classes never inherit concrete logic, ensuring complete interchangeability.
* **I — Interface Segregation Principle (ISP)**:
  * Clients depend only on the minimal interfaces they require (`IBotService`, `IBotMotionService`, `IBotTelemetryService`, `IBotTransport`, `IBinaryCodec`, `ICrc8Calculator`).
* **D — Dependency Inversion Principle (DIP)**:
  * Core domain entities and services have zero dependencies on lower-level infrastructure (pyserial drivers, sockets, UI widgets). All dependencies are injected via protocols.

##### Automated Quality Gates (`run_quality_gates.sh`)

Every build is validated against 4 strict automated quality gates:
1. **Structural Protocols Gate**: Verifies 100% compliance with `@runtime_checkable Protocol` structural typing.
2. **Interface Segregation Gate (ISP)**: Verifies that no bloated or unused interfaces exist.
3. **Module Limits Gate**: Enforces file length ($\le 300$ lines) and line length limits ($\le 100$ characters).
4. **Single Responsibility Gate (SRP)**: Strictly enforces $\le 15$ methods per class.

#### ✨ Features

* **Dual Transport Support**: Multi-channel USB Serial (`/dev/ttyUSB0` @ 115200 baud) and low-latency TCP Socket (`127.0.0.1:8888` or WiFi IP) streaming.
* **Interactive Jog & Navigation Cockpit**: Real-time D-Pad buttons for Forward, Backward, Skid-Turns, In-Place Spins, and instant Emergency Stop with keyboard key bindings (`W`, `A`, `S`, `D`, `Q`, `E`, `Space`).
* **Tracked Robot Mission DSL (`.track`)**: Full declarative scripting pipeline featuring lexical tokenizer, syntax parser, AST builder, and binary opcode compiler with Step, Run, Pause, and Resume execution controls.
* **Real-Time Telemetry Dashboard**: Live monitoring of system operational mode (`NORMAL`, `DEGRADED`, `PANIC`), kinematic track speeds, hardware fault counters, motor lock status, and round-trip ping latency.
* **Terminal Packet Inspector**: Bi-directional packet visualizer logging raw TX/RX frames with sequence counters, opcode labels, hex payloads, and CRC-8 integrity verification.
* **Robust CRC-8 Dallas/Maxim Codec**: High-integrity binary packet framing protocol with start-of-frame synchronization, opcode mapping, dynamic payload lengths, and checksum verification.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, $\ge 78\%$ test coverage, and 10.00 / 10.00 Pylint score.

#### 📜 Tracked Bot Domain-Specific Language (DSL) & `.track` Programs

**botracked** includes a dedicated Domain-Specific Language designed specifically for tracked mobile robots. Programs are written in plain text files with the `.track` extension:

```
                    ┌─────────────────────────┐
                    │      .track Source      │
                    └────────────┬────────────┘
                                 │ TBotLexer
                                 ▼
                    ┌─────────────────────────┐
                    │      Token Stream       │
                    └────────────┬────────────┘
                                 │ TBotParser
                                 ▼
                    ┌─────────────────────────┐
                    │      Abstract AST       │
                    └────────────┬────────────┘
                                 │ TBotCompiler
                                 ▼
                    ┌─────────────────────────┐
                    │      Compiled Steps     │ (Binary Packets & Delays)
                    └─────────────────────────┘
```

##### Tracked Bot DSL Instruction Reference

| Category | Instruction & Syntax | Parameters | Description |
|---|---|---|---|
| **Motion** | `FORWARD [duration]` | Optional duration (e.g. `2.0s`, `500ms`) | Drives both tracks forward at active speed. |
| | `BACKWARD [duration]` | Optional duration | Drives both tracks in reverse at active speed. |
| | `TURN_LEFT [duration]` | Optional duration | Differential left skid-turn (left stopped, right forward). |
| | `TURN_RIGHT [duration]` | Optional duration | Differential right skid-turn (right stopped, left forward). |
| | `SPIN_LEFT [duration]` | Optional duration | In-place counter-clockwise spin (left reverse, right forward). |
| | `SPIN_RIGHT [duration]` | Optional duration | In-place clockwise spin (left forward, right reverse). |
| | `STOP` | None | Immediate kinematic stop (PWM = 0). |
| **Dynamics**| `SPEED <pwm>` | `pwm` (`60` to `255`) | Sets active drive PWM velocity for subsequent motions. |
| | `WAIT <duration>` | Duration (e.g. `1.5s`, `250ms`) | Dwells execution for specified hardware duration. |
| **System** | `PING` | None | Transmits keepalive frame and calculates ping latency. |
| | `CLEAR_ERRORS` | None | Clears active error latches and resets fault counters. |

##### Example `.track` Program: Autonomous Perimeter Patrol

```track
# ----------------------------------------------------
# Autonomous Perimeter Patrol Mission
# ----------------------------------------------------
SPEED 180
PING
WAIT 200ms

# Leg 1: Drive forward along north boundary
FORWARD 3.0s
WAIT 500ms

# Rotate 90 degrees right in place
SPIN_RIGHT 1.2s
WAIT 300ms

# Leg 2: Drive forward along east boundary
FORWARD 3.0s
WAIT 500ms

# Rotate 90 degrees right in place
SPIN_RIGHT 1.2s
WAIT 300ms

# Leg 3: Return to home position
FORWARD 3.0s
STOP
CLEAR_ERRORS
```

#### 📡 Binary Packet Communication Protocol & Framing

All communication between **botracked** and the physical or virtual robot uses a framed binary protocol protected by Dallas/Maxim CRC-8:

* **Frame Layout**: `[0xAA] [0x55] [OPCODE] [LEN] [PAYLOAD...] [CRC8]`
* **Header**: `0xAA 0x55` (Start of Frame synchronization marker).
* **Opcode**: 1-byte command or response identifier.
* **Length**: 1-byte payload length ($0 \dots 255$).
* **Payload**: Raw parameter bytes corresponding to opcode.
* **CRC-8**: Computed over `OPCODE + LEN + PAYLOAD` using polynomial $x^8 + x^5 + x^4 + 1$ (`0x31`, init `0x00`).

##### Command Frames (PC $\to$ Robot)

| Opcode | Name | Payload Length | Description |
|---|---|:---:|---|
| `0x01` | `CMD_PING` | 0 | Heartbeat request frame. |
| `0x02` | `CMD_EMERGENCY_STOP` | 0 | Immediate safety motor lockout. |
| `0x03` | `CMD_CLEAR_ERRORS` | 0 | Reset fault registers and alarm flags. |
| `0x10` | `CMD_MOTION_STOP` | 0 | Kinematic deceleration to zero. |
| `0x11` | `CMD_MOTION_FORWARD` | 1 (`PWM`) | Forward drive at specified velocity. |
| `0x12` | `CMD_MOTION_BACKWARD` | 1 (`PWM`) | Reverse drive at specified velocity. |
| `0x13` | `CMD_MOTION_TURN_LEFT`| 1 (`PWM`) | Left differential skid-turn. |
| `0x14` | `CMD_MOTION_TURN_RIGHT`| 1 (`PWM`) | Right differential skid-turn. |
| `0x15` | `CMD_MOTION_SPIN_LEFT` | 1 (`PWM`) | Counter-clockwise in-place spin. |
| `0x16` | `CMD_MOTION_SPIN_RIGHT`| 1 (`PWM`) | Clockwise in-place spin. |
| `0x20` | `CMD_REQ_TELEMETRY` | 0 | Request full telemetry snapshot. |

##### Telemetry Frames (Robot $\to$ PC)

| Opcode | Name | Payload Length | Description |
|---|---|:---:|---|
| `0x81` | `RESP_PONG` | 0 | Heartbeat response. |
| `0x90` | `RESP_TELEMETRY` | 8 | Packed telemetry data (mode, error code, fault count, left PWM, right PWM, watchdog flag, motor lock). |
| `0xFF` | `RESP_ERROR` | 1 (`ERROR_CODE`) | Error status alert packet. |

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `botracked/__init__.py` | 9 | 0 | 100%|
| `botracked/core/__init__.py` | 9 | 0 | 100%|
| `botracked/core/model/__init__.py` | 9 | 0 | 100%|
| `botracked/core/model/connection_params.py` | 29 | 5 | 83%|
| `botracked/core/model/dsl/__init__.py` | 9 | 0 | 100%|
| `botracked/core/model/dsl/ast_instruction.py` | 33 | 9 | 73%|
| `botracked/core/model/dsl/compiled_step.py` | 23 | 2 | 91%|
| `botracked/core/model/dsl/token.py` | 22 | 2 | 91%|
| `botracked/core/model/dsl/token_type.py` | 30 | 0 | 100%|
| `botracked/core/model/motion_command.py` | 29 | 7 | 76%|
| `botracked/core/model/protocol_opcode.py` | 30 | 3 | 90%|
| `botracked/core/model/telemetry_data.py` | 71 | 35 | 51%|
| `botracked/core/service/__init__.py` | 9 | 0 | 100%|
| `botracked/core/service/bot_motion_service.py` | 55 | 13 | 76%|
| `botracked/core/service/bot_service.py` | 68 | 17 | 75%|
| `botracked/core/service/bot_telemetry_service.py` | 60 | 25 | 58%|
| `botracked/core/service/communication/__init__.py` | 9 | 0 | 100%|
| `botracked/core/service/communication/ibinary_codec.py` | 14 | 14 | 0%|
| `botracked/core/service/communication/ibot_transport.py` | 18 | 18 | 0%|
| `botracked/core/service/communication/icrc8_calculator.py` | 14 | 14 | 0%|
| `botracked/core/service/communication/itelemetry_observer.py` | 16 | 0 | 100%|
| `botracked/core/service/dsl/__init__.py` | 9 | 0 | 100%|
| `botracked/core/service/dsl/itbot_compiler.py` | 16 | 16 | 0%|
| `botracked/core/service/dsl/itbot_dsl_service.py` | 15 | 15 | 0%|
| `botracked/core/service/dsl/itbot_lexer.py` | 15 | 15 | 0%|
| `botracked/core/service/dsl/itbot_parser.py` | 16 | 16 | 0%|
| `botracked/core/service/dsl/tbot_compiler.py` | 67 | 8 | 88%|
| `botracked/core/service/dsl/tbot_dsl_service.py` | 35 | 0 | 100%|
| `botracked/core/service/dsl/tbot_lexer.py` | 67 | 4 | 94%|
| `botracked/core/service/dsl/tbot_parser.py` | 112 | 20 | 82%|
| `botracked/core/service/ibot_connection_service.py` | 16 | 0 | 100%|
| `botracked/core/service/ibot_mission_service.py` | 18 | 0 | 100%|
| `botracked/core/service/ibot_motion_service.py` | 20 | 0 | 100%|
| `botracked/core/service/ibot_service.py` | 20 | 0 | 100%|
| `botracked/core/service/ibot_telemetry_service.py` | 18 | 0 | 100%|
| `botracked/core/service/mission_runner.py` | 74 | 41 | 45%|
| `botracked/core/service/telemetry_poller.py` | 66 | 30 | 55%|
| `botracked/engine.py` | 65 | 65 | 0%|
| `botracked/infrastructure/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/cli/engine.py` | 44 | 12 | 73%|
| `botracked/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `botracked/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/cli/setup/bundle.py` | 22 | 1 | 95%|
| `botracked/infrastructure/cli/setup/factory.py` | 26 | 1 | 96%|
| `botracked/infrastructure/cli/setup/validator.py` | 35 | 5 | 86%|
| `botracked/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/command/command.py` | 16 | 0 | 100%|
| `botracked/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `botracked/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `botracked/infrastructure/command/studio_command_definition.py` | 24 | 1 | 96%|
| `botracked/infrastructure/command/studio_command_executor.py` | 41 | 16 | 61%|
| `botracked/infrastructure/communication/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/communication/binary_codec.py` | 51 | 5 | 90%|
| `botracked/infrastructure/communication/crc8_calculator.py` | 29 | 0 | 100%|
| `botracked/infrastructure/communication/preferences/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/communication/preferences/connection_preferences_repository.py` | 55 | 6 | 89%|
| `botracked/infrastructure/communication/serial_transport.py` | 60 | 35 | 42%|
| `botracked/infrastructure/communication/tcp_transport.py` | 63 | 40 | 37%|
| `botracked/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/gui/connection/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/gui/connection/connection_callbacks.py` | 16 | 0 | 100%|
| `botracked/infrastructure/gui/connection/connection_panel.py` | 106 | 28 | 74%|
| `botracked/infrastructure/gui/connection/connection_panel_config.py` | 25 | 0 | 100%|
| `botracked/infrastructure/gui/controls/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/gui/controls/jog_panel.py` | 75 | 10 | 87%|
| `botracked/infrastructure/gui/controls/jog_panel_callbacks.py` | 19 | 0 | 100%|
| `botracked/infrastructure/gui/controls/jog_panel_config.py` | 29 | 0 | 100%|
| `botracked/infrastructure/gui/editor/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/gui/editor/dsl_editor_panel.py` | 118 | 25 | 79%|
| `botracked/infrastructure/gui/editor/dsl_editor_panel_config.py` | 26 | 0 | 100%|
| `botracked/infrastructure/gui/editor/dsl_preset_loader.py` | 32 | 3 | 91%|
| `botracked/infrastructure/gui/editor/dsl_syntax_highlighter.py` | 50 | 0 | 100%|
| `botracked/infrastructure/gui/editor/dsl_syntax_highlighter_config.py` | 25 | 0 | 100%|
| `botracked/infrastructure/gui/editor/mission_callbacks.py` | 18 | 0 | 100%|
| `botracked/infrastructure/gui/engine.py` | 106 | 12 | 89%|
| `botracked/infrastructure/gui/gui_config.py` | 21 | 0 | 100%|
| `botracked/infrastructure/gui/gui_event_mediator.py` | 36 | 9 | 75%|
| `botracked/infrastructure/gui/igui.py` | 15 | 0 | 100%|
| `botracked/infrastructure/gui/stream/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/gui/stream/log_panel.py` | 69 | 19 | 72%|
| `botracked/infrastructure/gui/stream/log_panel_config.py` | 22 | 0 | 100%|
| `botracked/infrastructure/gui/telemetry/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/gui/telemetry/telemetry_panel.py` | 90 | 22 | 76%|
| `botracked/infrastructure/gui/telemetry/telemetry_panel_config.py` | 27 | 0 | 100%|
| `botracked/infrastructure/gui/theme/__init__.py` | 9 | 0 | 100%|
| `botracked/infrastructure/gui/theme/colors.py` | 27 | 0 | 100%|
| `botracked/infrastructure/gui/theme/style.py` | 43 | 1 | 98%|
| `botracked/setup/__init__.py` | 9 | 0 | 100%|
| `botracked/setup/bundle.py` | 24 | 1 | 96%|
| `botracked/setup/dep_validator.py` | 34 | 5 | 85%|
| `botracked/setup/dependencies.py` | 19 | 0 | 100%|
| `botracked/setup/factory.py` | 44 | 2 | 95%|
| `botracked/setup/keys.py` | 31 | 0 | 100%|
| `botracked/setup/opt_validator.py` | 34 | 2 | 94%|
| `botracked/setup/options.py` | 16 | 0 | 100%|
| `botracked/setup/registry.py` | 32 | 0 | 100%|
| `botracked/setup/validator.py` | 38 | 5 | 87%|
| **Total** | 3117 | 660 | 79% |

</details>

### 🛠 Usage

Install package

```bash
pip3 install botracked
```

Prepare main entry point by downloading [main.py](https://raw.githubusercontent.com/vroncevic/botracked/main/main.py) or create your own.

```bash
wget -O main.py https://raw.githubusercontent.com/vroncevic/botracked/main/main.py
```

##### CLI Command Options

Launch the graphical studio with default configuration:

```bash
python3 main.py studio
```

Launch with initial mission script and verbose logging:

```bash
python3 main.py studio --file ./missions/patrol_demo.track --verbose enable
```

| Option | Type | Choices | Description |
|---|:---:|:---:|---|
| **`--file`** | `str` | *File path* | Path to initial mission script (`.track`) to load on startup. |
| **`--verbose`** | `str` | `enable`, `disable` | Enable or disable verbose ATS operational logging. |

##### Interactive Mission Planning & Telemetry Workflow

1. **Connect to Robot Platform**:
   * Under the **Connection** panel, select your transport mode:
     * **Serial USB**: Select port (e.g. `/dev/ttyUSB0`) and baudrate (`115200`).
     * **TCP / Network**: Enter the robot IP address (e.g. `192.168.4.1` or `127.0.0.1`) and port (`8888`).
   * Click **Connect**. The status bar reflects connection state and initializes the telemetry polling loop.
2. **Manual Jog Cockpit**:
   * Navigate using the interactive D-Pad buttons or keyboard shortcuts (`W`, `A`, `S`, `D`, `Q`, `E`, `Space`).
   * Adjust drive speed smoothly with the PWM slider ($60 \dots 255$).
3. **Mission Scripting**:
   * Open the **Mission Studio** panel.
   * Write or select a bundled `.track` mission program from the Preset dropdown.
   * Click **Validate** to verify syntax with the AST parser.
   * Click **Run Mission** for automated execution, or use **Step** for single-instruction stepping.
4. **Telemetry & Log Inspection**:
   * Observe active system modes, track PWMs, error codes, and ping latency on the **Telemetry** gauges.
   * Monitor real-time TX/RX binary packets with timestamps and hex payloads in the **Terminal Log**.

### 📚 Docs

[![Documentation Status](https://readthedocs.org/projects/botracked/badge/?version=latest)](https://botracked.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [botracked.readthedocs.io](https://botracked.readthedocs.io)
* [www.python.org](https://www.python.org/)

### 👥 Contributing

[Contributing to botracked](CONTRIBUTING.md)

### 📄 Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2026 by [vroncevic.github.io/botracked](https://vroncevic.github.io/botracked)

**botracked** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/botracked/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
