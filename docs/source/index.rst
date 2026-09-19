Tracked Robot Control Studio & Telemetry Monitor
------------------------------------------------

**botracked** is a modular Python desktop application, telemetry monitor, and mission scripting suite for tracked robotic platforms.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|botracked python checker| |botracked python package| |botracked interface checker| |botracked isp checker| |botracked srp checker| |gplv3 license| |apache license| |python version| |github issues| |documentation status| |github contributors|

.. |botracked python checker| image:: https://github.com/vroncevic/botracked/actions/workflows/botracked_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/botracked/actions/workflows/botracked_python_checker.yml

.. |botracked python package| image:: https://github.com/vroncevic/botracked/actions/workflows/botracked_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/botracked/actions/workflows/botracked_package.yml

.. |botracked interface checker| image:: https://github.com/vroncevic/botracked/actions/workflows/botracked_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/botracked/actions/workflows/botracked_interface_checker.yml

.. |botracked isp checker| image:: https://github.com/vroncevic/botracked/actions/workflows/botracked_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/botracked/actions/workflows/botracked_isp_checker.yml

.. |botracked srp checker| image:: https://github.com/vroncevic/botracked/actions/workflows/botracked_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/botracked/actions/workflows/botracked_srp_checker.yml

.. |gplv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |apache license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |python version| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/botracked.svg
   :target: https://github.com/vroncevic/botracked/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/botracked.svg
   :target: https://github.com/vroncevic/botracked/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/botracked/badge/?version=latest
   :target: https://botracked.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
---------------

|botracked python3 build|

.. |botracked python3 build| image:: https://github.com/vroncevic/botracked/actions/workflows/botracked_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/botracked/actions/workflows/botracked_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/botracked/releases

To install **botracked** type the following

.. code-block:: bash

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

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # python3
    pip3 install botracked

📦 Dependencies
---------------

**botracked** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_ |ats gplv3| |ats apache|
* `pyserial - Python Serial Port Extension <https://pypi.org/project/pyserial/>`_ |pyserial bsd|

.. |ats gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |ats apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |pyserial bsd| image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

📁 Tool structure
-----------------

**botracked** is based on OOP and Clean Architecture.

Tool structure

.. code-block:: bash

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

✨ Features
-----------

* **Dual Transport Support**: Multi-channel USB Serial (``/dev/ttyUSB0`` @ 115200 baud) and low-latency TCP Socket (``127.0.0.1:8888`` or WiFi IP) streaming.
* **Interactive Jog & Navigation Cockpit**: Real-time D-Pad buttons for Forward, Backward, Skid-Turns, In-Place Spins, and instant Emergency Stop with keyboard key bindings (``W``, ``A``, ``S``, ``D``, ``Q``, ``E``, ``Space``).
* **Tracked Robot Mission DSL (`.track`)**: Full declarative scripting pipeline featuring lexical tokenizer, syntax parser, AST builder, and binary opcode compiler with Step, Run, Pause, and Resume execution controls.
* **Real-Time Telemetry Dashboard**: Live monitoring of system operational mode (``NORMAL``, ``DEGRADED``, ``PANIC``), kinematic track speeds, hardware fault counters, motor lock status, and round-trip ping latency.
* **Terminal Packet Inspector**: Bi-directional packet visualizer logging raw TX/RX frames with sequence counters, opcode labels, hex payloads, and CRC-8 integrity verification.
* **Robust CRC-8 Dallas/Maxim Codec**: High-integrity binary packet framing protocol with start-of-frame synchronization, opcode mapping, dynamic payload lengths, and checksum verification.
* **Strict Quality & SOLID Standards**: 100% protocol conformity, zero ISP/SRP violations, $\ge 78\%$ test coverage, and 10.00 / 10.00 Pylint score.

🏗 Architecture & SOLID Principles
----------------------------------

**botracked** is built on a strictly decoupled, **Layered Clean Architecture** where presentation, domain models, mission execution services, and physical communication adapters are segregated through pure Python protocols:

* **S — Single Responsibility Principle (SRP)**:
  * Every module and class has exactly one clearly bounded reason to change.
  * GUI tabs are partitioned into focused subcomponents (panels, configs, callbacks, mediators).
  * Enforced by automated gate: strict limit of $\le 15$ methods per class across the entire codebase.
* **O — Open/Closed Principle (OCP)**:
  * The DSL parser, compiler, and binary codec are open for extension without modifying existing code.
  * New motion opcodes and instructions plug into dedicated handlers and registries dynamically.
* **L — Liskov Substitution Principle (LSP)**:
  * Pure structural subtyping via Python ``@runtime_checkable Protocol`` definitions. Concrete classes never inherit concrete logic, ensuring complete interchangeability.
* **I — Interface Segregation Principle (ISP)**:
  * Clients depend only on the minimal interfaces they require (``IBotService``, ``IBotMotionService``, ``IBotTelemetryService``, ``IBotTransport``, ``IBinaryCodec``, ``ICrc8Calculator``).
* **D — Dependency Inversion Principle (DIP)**:
  * Core domain entities and services have zero dependencies on lower-level infrastructure (pyserial drivers, sockets, UI widgets). All dependencies are injected via protocols.

📜 Tracked Bot Domain-Specific Language (DSL)
---------------------------------------------

**botracked** includes a dedicated Domain-Specific Language designed for tracked mobile robots. Programs are written in plain text files with the ``.track`` extension:

.. list-table:: Tracked Bot DSL Instruction Reference
   :widths: 20 20 60
   :header-rows: 1

   * - Instruction & Syntax
     - Parameters
     - Description
   * - ``SPEED <pwm>``
     - ``60..255`` (PWM)
     - Sets target PWM velocity for subsequent motion commands.
   * - ``FORWARD [duration]``
     - Optional duration (e.g. ``2.0s``, ``500ms``)
     - Drives both tracks forward.
   * - ``BACKWARD [duration]``
     - Optional duration
     - Drives both tracks in reverse.
   * - ``TURN_LEFT [duration]``
     - Optional duration
     - Performs differential left skid-turn.
   * - ``TURN_RIGHT [duration]``
     - Optional duration
     - Performs differential right skid-turn.
   * - ``SPIN_LEFT [duration]``
     - Optional duration
     - Rotates in-place counter-clockwise.
   * - ``SPIN_RIGHT [duration]``
     - Optional duration
     - Rotates in-place clockwise.
   * - ``STOP``
     - None
     - Immediately commands kinematic deceleration to 0.
   * - ``WAIT <duration>``
     - Duration (e.g. ``1.5s``, ``250ms``)
     - Dwells execution for specified duration.
   * - ``PING``
     - None
     - Sends heartbeat frame to measure round-trip link latency.
   * - ``CLEAR_ERRORS``
     - None
     - Clears active error latches and resets fault counters.

📡 Binary Packet Communication Protocol
---------------------------------------

All communication between **botracked** and physical or virtual robot firmware uses a packetized binary protocol protected by Dallas/Maxim CRC-8:

* **Frame Layout**: ``[0xAA] [0x55] [OPCODE] [LEN] [PAYLOAD...] [CRC8]``
* **Synchronization**: Two-byte header ``0xAA 0x55``.
* **Opcode**: 1-byte command or response identifier.
* **Payload Length**: 1-byte payload byte count ($0 \dots 255$).
* **Checksum**: 1-byte CRC-8 computed over opcode, length, and payload.

📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package

.. code-block:: bash

    pip3 install botracked

Prepare main entry point by downloading `main.py` or create your own.

.. code-block:: bash

    wget -O main.py https://raw.githubusercontent.com/vroncevic/botracked/main/main.py

CLI Command Options
^^^^^^^^^^^^^^^^^^^

Launch the graphical studio with default configuration:

.. code-block:: bash

    python3 main.py studio

Launch with initial mission script and verbose logging:

.. code-block:: bash

    python3 main.py studio --file ./missions/patrol_demo.track --verbose enable

.. list-table:: Studio CLI Options
   :widths: 20 15 25 40
   :header-rows: 1

   * - Option
     - Type
     - Choices
     - Description
   * - **--file**
     - ``str``
     - *File path*
     - Path to initial mission script (``.track``) to load on startup.
   * - **--verbose**
     - ``str``
     - ``enable``, ``disable``
     - Enable or disable verbose ATS operational logging.

📚 Docs
-------

More documentation and info at

* `botracked.readthedocs.io <https://botracked.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to botracked <https://github.com/vroncevic/botracked/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2026 by `vroncevic.github.io/botracked <https://vroncevic.github.io/botracked>`_

**botracked** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/botracked/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.python.org/psf/donations/
