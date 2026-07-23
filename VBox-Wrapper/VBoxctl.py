#!/usr/bin/env python3

"""
vbox.py - Simple VirtualBox wrapper
@Author: Saksham Trived
@Dated: 2024-06-10
@Description: Simple VirtualBox wrapper

Features:
- Start VM (headless by default)
- Start GUI (-g/--gui)
- SSH into VM (-t/--terminal) using auto-detected NAT forward
- Stop (ACPI), Force Off, Save State
- List, Running, Status, Info

Requires VBoxManage in PATH.
"""

import argparse
import shutil
import subprocess
import sys
import time
import re

def run(*args, check=True):
    return subprocess.run(args, capture_output=True, text=True, check=check)

def vbm():
    exe = shutil.which("VBoxManage")
    if exe is None:
        sys.exit("VBoxManage not found in PATH.")
    return exe

def exists(vm):
    try:
        run(vbm(), "showvminfo", vm)
        return True
    except subprocess.CalledProcessError:
        return False

def running(vm):
    out = run(vbm(), "list", "runningvms").stdout
    return f'"{vm}"' in out

def start(vm, gui=False):
    if running(vm):
        print(f"{vm} already running.")
        return
    mode = "gui" if gui else "headless"
    run(vbm(), "startvm", vm, "--type", mode, check=False)

def acpi(vm):
    run(vbm(), "controlvm", vm, "acpipowerbutton", check=False)

def force(vm):
    run(vbm(), "controlvm", vm, "poweroff", check=False)

def save(vm):
    run(vbm(), "controlvm", vm, "savestate", check=False)

def list_vms(running_only=False):
    cmd=["list","runningvms"] if running_only else ["list","vms"]
    print(run(vbm(),*cmd).stdout)

def status(vm):
    out=run(vbm(),"showvminfo",vm,"--machinereadable").stdout
    m=re.search(r'VMState="([^"]+)"',out)
    print(m.group(1) if m else "unknown")

def info(vm):
    print(run(vbm(),"showvminfo",vm).stdout)

def ssh(vm):
    if not running(vm):
        start(vm)
        time.sleep(2)
    out=run(vbm(),"showvminfo",vm,"--machinereadable").stdout
    m=re.search(r'Forwarding\(\d+\)="[^"]*ssh[^"]*,tcp,,(\d+),,22"',out,re.I)
    if not m:
        sys.exit("No SSH NAT forwarding rule found.")
    port=m.group(1)
    sshexe=shutil.which("ssh")
    if not sshexe:
        sys.exit("ssh client not found.")
    subprocess.call([sshexe,"-p",port,"kali@127.0.0.1"])

p=argparse.ArgumentParser()
p.add_argument("vm",nargs="?")
g=p.add_mutually_exclusive_group()
g.add_argument("-g","--gui",action="store_true")
g.add_argument("-t","--terminal",action="store_true")
g.add_argument("--stop",action="store_true")
g.add_argument("--force",action="store_true")
g.add_argument("--save",action="store_true")
g.add_argument("-l","--list",action="store_true")
g.add_argument("--running",action="store_true")
g.add_argument("--status",action="store_true")
g.add_argument("--info",action="store_true")
a=p.parse_args()

if a.list:
    list_vms()
elif a.running:
    list_vms(True)
else:
    if not a.vm:
        p.error("VM name required.")
    if not exists(a.vm):
        sys.exit("VM not found.")
    if a.gui:
        start(a.vm,True)
    elif a.terminal:
        ssh(a.vm)
    elif a.stop:
        acpi(a.vm)
    elif a.force:
        force(a.vm)
    elif a.save:
        save(a.vm)
    elif a.status:
        status(a.vm)
    elif a.info:
        info(a.vm)
    else:
        start(a.vm)
