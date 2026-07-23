# VBoxctl Wrapper

## Description

**VBox Python Wrapper** is a lightweight command-line interface (CLI)
built on top of Oracle VirtualBox's `VBoxManage` utility. It simplifies
day-to-day VirtualBox administration by providing a clean,
cross-platform interface for common VM lifecycle operations without
requiring users to remember lengthy `VBoxManage` commands.

The project is intentionally designed with a modular architecture so
that VirtualBox operations are isolated from the command-line interface.
This allows future features (SSH, snapshots, cloning, GUI frontends,
REST APIs, etc.) to be added without changing the core backend.

## Current Features

-   Start virtual machines (headless by default)
-   Start virtual machines with the VirtualBox GUI
-   Gracefully stop a VM using ACPI
-   Force power off
-   Save VM state
-   Display VM status
-   Display detailed VM information
-   List all registered VMs
-   List running VMs
-   Cross-platform (Windows/Linux)
-   Automatic VBoxManage discovery
-   Verbose logging
-   Structured backend using classes, dataclasses and enums

## Planned Features

### Phase 2

-   SSH integration
-   Automatic guest IP discovery
-   Host-only / NAT detection
-   Guest Additions integration

### Phase 3

-   Snapshot management
-   Clone VMs
-   Import / Export appliances
-   Pause / Resume / Reset
-   VM configuration editing

## Goals

-   Cross-platform
-   Minimal dependencies
-   Easy automation
-   Clean architecture
-   Extensible backend
-   Suitable for homelab and development workflows

## Requirements

-   Python 3.9+
-   Oracle VirtualBox
-   `VBoxManage` available in `PATH`

## Usage

``` bash
python vbox.py <VM>
python vbox.py <VM> -g
python vbox.py <VM> --stop
python vbox.py <VM> --force
python vbox.py <VM> --save
python vbox.py --list
python vbox.py --running
python vbox.py <VM> --status
python vbox.py <VM> --info
```

## Commands

  Command              Description
  -------------------- ---------------------------
  `<VM>`               Start headless

  `-g`, `--gui`        Start with GUI

  `--stop`             Send ACPI shutdown

  `--force`            Immediate power off

  `--save`             Save VM state

  `-l`, `--list`       List all VMs

  `--running`          List running VMs

  `--status`           Print VM state

  `--info`             Show VBoxManage info

## Current Limitations

-   GUI cannot be attached to an already headless-started VM.
-   No snapshot management.
-   No configuration file.

## Planned Improvements

-   Configurable Direct SSH Connections to VM
-   Colored output
-   Better tables
-   Logging
-   Snapshot support
-   Packaging (`pip`)
-   Auto-completion

## Exit Codes

-   `0` Success
-   Non-zero Failure