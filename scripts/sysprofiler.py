#!/usr/bin/env python3
# pylint: disable=C0301,C0116,C0103,R0903

"""
This script was created by Coopydood as part of the ultimate-macOS-KVM project.

https://github.com/user/Coopydood
https://github.com/Coopydood/ultimate-macOS-KVM
Signature: 4CD28348A3DD016F

"""


import os
import time
import subprocess
import re 
import json
import argparse
import platform
import datetime
import hashlib
import sys
sys.path.append('./resources/python')
import distro
import cpuinfo
import psutil
from cpydColours import color
from datetime import datetime
try:
    from pypresence import Presence
    depRPC = 1
except:
     depRPC = 0

detectChoice = 1
latestOSName = "Sonoma"
latestOSVer = "14"

scriptName = "System Profile Tool"
script = "sysprofiler.py"
scriptID = "SPT"
scriptVendor = "Coopydood"
scriptVer = 1.0
branch = "Unknown"

version = open("./.version")
version = version.read()

versionDash = version.replace(".","-")

def clear(): print("\n" * 150)

cS = 5

clear()

for x in range(1,1):
    print("\nThis script will check your system to ensure it is ready for basic KVM. \nChecks will begin in",cS,"seconds. \nPress CTRL+C to cancel.")
    cS = cS - 1
    time.sleep(1)
    clear()

clear()

print("\n\n   "+color.BOLD+color.BLUE+"SYSTEM PROFILE TOOL"+color.END,"")
print("   Gathering system information")
print("\n   Please wait while the tool gathers info\n   about your system. No personal data is\n   included in the report.\n\n\n\n\n\n   ")
def progressUpdate(progressVal,*args):
    progress = progressVal
    if progress <= 5:
        progressGUI = (color.BOLD+""+color.GRAY+"━━━━━━━━━━━━━━━━━━━━")
    elif progress > 5 and progress <= 10:
        progressGUI = (color.BOLD+"━"+color.GRAY+"━━━━━━━━━━━━━━━━━━━")
    elif progress > 10 and progress <= 20:
        progressGUI = (color.BOLD+"━━"+color.GRAY+"━━━━━━━━━━━━━━━━━━")
    elif progress > 20 and progress <= 25:
        progressGUI = (color.BOLD+"━━━"+color.GRAY+"━━━━━━━━━━━━━━━━━")
    elif progress > 25 and progress <= 30:
        progressGUI = (color.BOLD+"━━━━"+color.GRAY+"━━━━━━━━━━━━━━━━")
    elif progress > 30 and progress <= 35:
        progressGUI = (color.BOLD+"━━━━━"+color.GRAY+"━━━━━━━━━━━━━━━")
    elif progress > 35 and progress <= 40:
        progressGUI = (color.BOLD+"━━━━━━"+color.GRAY+"━━━━━━━━━━━━━━")
    elif progress > 40 and progress <= 45:
        progressGUI = (color.BOLD+"━━━━━━━"+color.GRAY+"━━━━━━━━━━━━━")
    elif progress > 45 and progress <= 50:
        progressGUI = (color.BOLD+"━━━━━━━━"+color.GRAY+"━━━━━━━━━━━━")
    elif progress > 50 and progress <= 55:
        progressGUI = (color.BOLD+"━━━━━━━━━"+color.GRAY+"━━━━━━━━━━━")
    elif progress > 55 and progress <= 60:
        progressGUI = (color.BOLD+"━━━━━━━━━━"+color.GRAY+"━━━━━━━━━━")
    elif progress > 60 and progress <= 65:
        progressGUI = (color.BOLD+"━━━━━━━━━━━"+color.GRAY+"━━━━━━━━━")
    elif progress > 65 and progress <= 70:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━"+color.GRAY+"━━━━━━━━")
    elif progress > 70 and progress <= 75:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━"+color.GRAY+"━━━━━━━")
    elif progress > 75 and progress <= 80:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━"+color.GRAY+"━━━━━━")
    elif progress > 80 and progress <= 85:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━"+color.GRAY+"━━━━━")
    elif progress > 85 and progress <= 90:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━━"+color.GRAY+"━━━━")
    elif progress > 90 and progress <= 95:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━━━"+color.GRAY+"━━━")
    elif progress > 95 and progress <= 98:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━━━━━"+color.GRAY+"━")
    elif progress > 98 and progress <= 99:
        progressGUI = (color.BOLD+"━━━━━━━━━━━━━━━━━━━━"+color.GRAY+"")
    elif progress >= 100:
        progressGUI = (color.BOLD+color.GREEN+"━━━━━━━━━━━━━━━━━━━━"+color.GRAY+"")
    sys.stdout.write('\033[F\033[F\033[F\033[F\033[2K\033[1G')
    print('   \r    {0}                 '.format((progressGUI+"  "+color.END+color.BOLD+str(progress)+"% "+color.END),('')), end='\n\n\n\n')
    

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", " K", " M", " G", " T", " P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

global logTime
global logFile
global warningCount
logTime = str(datetime.today().strftime('%d-%m-%Y_%H-%M-%S'))

if not os.path.exists("./logs"):
    os.system("mkdir ./logs")

   
os.system("echo ULTMOS SYSTEM REPORT "+str(datetime.today().strftime('%d-%m-%Y %H:%M:%S'))+" > ./logs/SPT_"+logTime+".log")
os.system("echo ───────────────────────────────────────────────────────────────────"+" >> ./logs/SPT_"+logTime+".log")
os.system("echo This report was generated by user request, and includes basic "+" >> ./logs/SPT_"+logTime+".log")
os.system("echo information about your system hardware, as well as your current"+" >> ./logs/SPT_"+logTime+".log")
os.system("echo ULTMOS software environment. "+" >> ./logs/SPT_"+logTime+".log")
os.system("echo "+" >> ./logs/SPT_"+logTime+".log")
os.system("echo This information may help project developers"+" >> ./logs/SPT_"+logTime+".log")
os.system("echo in assisting you in any issues you might have."+" >> ./logs/SPT_"+logTime+".log")

global apFilePath
global apFilePathNOPT
global apFilePathNOUSB

apFile = None
apFilePath = None
apFilePathNOPT = None
apFilePathNOUSB = None

warn = False
warningCount = 0
criticalCount = 0
warnings = []
criticals = []
logFile = open("./logs/SPT_"+logTime+".log", "a")
time.sleep(0.1)
progressUpdate(2)
def cpydProfile(logMsg,warn=None):
    global warningCount
    if warn == True:
        entryLine = ("⚠ "+str(logMsg)+"\n")
        warningCount = warningCount + 1
    else:
        entryLine = ("   "+str(logMsg)+"\n")
    logFile.write(entryLine)

######################### BRAINS #######################

output_stream = os.popen("git branch --show-current")
branch = output_stream.read()
branch = branch.replace("\n","")

time.sleep(0.1)
progressUpdate(4)

if os.path.exists("./blobs/user/USR_CFG.apb"):
    
    global macOSVer
    global mOSString

    apFilePath = open("./blobs/user/USR_CFG.apb")
    apFilePath = apFilePath.read()
    if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"):
        macOSVer = open("./blobs/user/USR_TARGET_OS_NAME.apb")
        macOSVer = macOSVer.read()

    macOSVer = open("./blobs/user/USR_TARGET_OS.apb")
    macOSVer = macOSVer.read()
    if int(macOSVer) <= 999 and int(macOSVer) > 99:
        macOSVer = str(int(macOSVer) / 100)
        mOSString = "Mac OS X"
    else:
        mOSString = "macOS"
    if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"):
        macOSVer = open("./blobs/user/USR_TARGET_OS_NAME.apb")
        macOSVer = macOSVer.read()
    if os.path.exists("./"+apFilePath):
        global REQUIRES_SUDO
        global VALID_FILE
        global VALID_FILE_NOPT
        global VALID_FILE_NOUSB

        VALID_FILE = 0
        VALID_FILE_NOPT = 0
        VALID_FILE_NOUSB = 0

        apFile = open("./"+apFilePath,"r")

        

        if "REQUIRES_SUDO=1" in apFile.read():
            REQUIRES_SUDO = 1
        else:
            REQUIRES_SUDO = 0

        apFile.close()

        apFile = open("./"+apFilePath,"r")

        apFilePathNOPT = apFilePath.replace(".sh","-noPT.sh")
        apFilePathNOUSB = apFilePath.replace(".sh","-noUSB.sh")
        
        if "APC-RUN" in apFile.read():
            VALID_FILE = 1

time.sleep(0.1)
progressUpdate(8)
output_stream = os.popen("lsmod | grep \"vfio_pci\"")
checkStream = output_stream.read()
if "vfio_pci" in checkStream and "vfio_pci_core" in checkStream and "vfio_iommu_type1" in checkStream:
    vfcKernel = 1
else:
    vfcKernel = 0

if os.path.exists("/sys/firmware/efi"):
    vfcUefi = 1
else:
    vfcUefi = 0

output_stream = os.popen("./scripts/iommu.sh")
checkStream = output_stream.read()
if "Group 0" in checkStream:
    vfcIommu = 1
else:
    vfcIommu = 0

output_stream = os.popen("lspci -k | grep -B2 \"vfio-pci\"")
checkStream = output_stream.read()
if "Kernel driver in use: vfio-pci" in checkStream:
    vfcStubbing = 1
else:
    vfcStubbing = 0

output_stream = os.popen("systemctl status libvirtd")
checkStream = output_stream.read()
if "active (running)" in checkStream:
    vfcLibvirtd = 2
elif "enabled" in checkStream:
    vfcLibvirtd = 1
else:
    vfcLibvirtd = 0

if os.path.exists("./scripts/autopilot.py") and os.path.exists("./scripts/vfio-ids.py") and os.path.exists("./scripts/vfio-pci.py") and os.path.exists("./resources/baseConfig") and os.path.exists("./resources/ovmf/OVMF_CODE.fd") and os.path.exists("./resources/oc_store/compat_new/OpenCore.qcow2"):
    vfcIntegrity = 1
else:
    vfcIntegrity = 0


output_stream = os.popen("whereis libvirt")
vfcLibvirtChk = output_stream.read()
if "libvirt:\n" == vfcLibvirtChk: # or "virsh:\n" == vfcLibvirtChk1
    depLibvirt = 0
else:
    depLibvirt = 1

vfcQemuChk = output_stream.read()

output_stream = os.popen("whereis qemu-x86_64")
vfcQemuChk1 = output_stream.read()

output_stream = os.popen("whereis qemu-img")
vfcQemuChk2 = output_stream.read()

output_stream = os.popen("whereis qemu-img")
vfcQemuChk2 = output_stream.read()

if "qemu-system-x86_64:\n" == vfcQemuChk or "qemu-x64:\n" == vfcQemuChk1 or "qemu-img:\n" == vfcQemuChk2:
    depQemu = 0
else:
    depQemu = 1

output_stream = os.popen("whereis nbd")
vfcChk = output_stream.read()
if "nbd:\n" == vfcChk:
    depNbd = 0
else:
    depVirtman = 1


output_stream = os.popen("whereis virt-manager")
vfcVirtmanChk = output_stream.read()
if "virt-manager:\n" == vfcVirtmanChk:
    depVirtman = 0
else:
    depVirtman = 1

output_stream = os.popen("whereis qemu-nbd")
vfcChk = output_stream.read()
if "nbd:\n" == vfcChk:
    depNbd = 0
else:
    depNbd = 1

output_stream = os.popen("whereis virsh")
vfcChk = output_stream.read()
if "virsh:\n" == vfcChk:
    depVirsh = 0
else:
    depVirsh = 1

output_stream = os.popen('lspci')
vmc1 = output_stream.read()

detected = 0

global isVM

isVM = False

if "VMware" in vmc1:
   detected = 1

if "VirtualBox" in vmc1 or "Oracle" in vmc1:
   detected = 1

if "Redhat" in vmc1 or "RedHat" in vmc1 or "QEMU" in vmc1:
   detected = 1

if "Bochs" in vmc1 or "Sea BIOS" in vmc1 or "SeaBIOS" in vmc1:
   detected = 1

if detected == 1:
    isVM == True


vfio_ids = os.popen("lspci -nnk | grep -B2 \"vfio-pci\" | grep -P \"[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9A-Fa-f]\" | grep -oP \"[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}\" | sort -u | tr '\n' ' '").read().split(" ")
# Remove the empty thingy
vfio_ids.pop(-1)

# Get PCI IDs
pci_ids = os.popen("lspci -nnk | grep -B2 \"vfio-pci\" | grep -P \"[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9A-Fa-f]\" | awk '{print $1}' | sort -u | tr '\n' ' '").read().split(" ")
# Remove the empty thingy
pci_ids.pop(-1)

# Get GPU IDs
gpu_ids = os.popen("lspci -nnk | grep -B2 \"vfio-pci\" | grep \"VGA compatible controller\" | grep -P \"[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-9A-Fa-f]\" | awk '{print $1}' | sort -u | tr '\n' ' '").read().split(" ")
# Remove the empty thingy
gpu_ids.pop(-1)

# Get PCI Names
vfio_names = os.popen("lspci -nnk | grep -B2 \"vfio-pci\" | grep -P \"[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\\.[0-9A-Fa-f]\" | sort -u | sed -E 's/[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}\.[0-9A-Fa-f] ((\w|-)+( )?)* \[[0-9A-Fa-f]*\]: //' | sed -E 's/\[[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}\]( \(.*\))?//' | sed 's/Advanced Micro Devices, Inc. \[AMD\/ATI\] //g' | tr '\n' '@'").read().split("@")
# Remove the empty thingy
vfio_names.pop(-1)

if os.path.exists("./resources/script_store/main.py"):
    vfcScrStr = 1
else:
    vfcScrStr = 0

if os.path.exists("./resources/baseConfig") and os.path.exists("./resources/baseDomain"):
    vfcBase = 1
else:
    vfcBase = 0

if os.path.exists("./resources/dmg2img"):
    vfcBin = 1
else:
    vfcBin = 0

ovmfStore = []

for x in os.listdir("./resources/ovmf/"):
    if ".fd" in x:
        ovmfStore.append(x)

if len(ovmfStore) > 9:
    vfcOvmf = 1
else:
    vfcOvmf = 0

if os.path.exists("./.git/index") and os.path.exists("./resources/.upgrade"):
    vfcGit = 1
else:
    vfcGit = 0

##############################################################################

cpydProfile(" ")
cpydProfile(("Name       : "+scriptName))
cpydProfile(("File       : "+script))
cpydProfile(("Identifier : "+scriptID))
cpydProfile(("Version    : "+str(scriptVer)))
cpydProfile(("Vendor     : "+scriptVendor))
cpydProfile(" ")
cpydProfile("Date       : "+str(datetime.today().strftime('%d/%m/%Y')))
cpydProfile("Time       : "+str(datetime.today().strftime('%H:%M:%S')))
cpydProfile(" \n")
time.sleep(0.1)
progressUpdate(11)
cpydProfile("ULTMOS")
cpydProfile("────────────────────────────────────────────────────────")
cpydProfile(("Version    : "+version))
if branch != "main":
    cpydProfile(("Branch     : "+branch),True)
    warnings.append(("This version of ULTMOS is from the "+branch+" branch, which"))
    warnings.append("is not considered stable and bugs are likely\n")
else:
    cpydProfile(("Branch     : "+branch))
cpydProfile((" \n"))
cpydProfile("OPERATING SYSTEM")
cpydProfile("────────────────────────────────────────────────────────")

time.sleep(0.1)
progressUpdate(16)
if platform.system() != "Linux":
    cpydProfile("OS         : "+platform.system(),True)
    criticals.append("The system is running "+str(platform.system())+" which is an unsupported")
    criticals.append("operating system. Use with caution. Linux is required\n")
    warningCount = warningCount - 1
    criticalCount = criticalCount + 1
else:
    cpydProfile("OS         : "+platform.system())
time.sleep(0.1)
progressUpdate(18)
cpydProfile("Distro     : "+distro.name())

cpydProfile("Release    : "+distro.version())

cpydProfile("Kernel     : "+platform.release())
if isVM == False:
    cpydProfile("VM         : NO")
else:
    cpydProfile("VM         : YES",True)
    warnings.append(("Virtual machine as host detected, this is likely"))
    warnings.append("some sort of mad inception shenanigans\n")
time.sleep(0.1)
progressUpdate(20)
cpydProfile(" \n")
time.sleep(0.1)
progressUpdate(22)
cpydProfile("PROCESSOR")
cpydProfile("────────────────────────────────────────────────────────")
cpydProfile("Model      : "+f"{cpuinfo.get_cpu_info()['brand_raw']}")
time.sleep(0.1)
progressUpdate(26)
cpydProfile("Physical   : "+str(psutil.cpu_count(logical=False)))
time.sleep(0.1)
progressUpdate(28)
logCPUCores = psutil.cpu_count(logical=True)
if logCPUCores <= 2:
    cpydProfile(("Logical    : "+str(logCPUCores)),True)
    warnings.append("System processor appears as having only "+str(logCPUCores)+" logical cores")
    warnings.append("which is at or below the project's minimum requirements\n")
else:
    cpydProfile("Logical    : "+str(logCPUCores))
time.sleep(0.1)
progressUpdate(33)
if platform.machine() != "x86_64":
    cpydProfile("Arch       : "+platform.machine(),True)
    criticals.append("System processor architecture detected as "+str(platform.machine())+", which")
    criticals.append("is unsupported. An x86_64 processor is required\n")
    warningCount = warningCount - 1
    criticalCount = criticalCount + 1
else:
    cpydProfile("Arch       : "+platform.machine())
time.sleep(0.1)
progressUpdate(36)
cpydProfile(" \n")
cpydProfile("MEMORY")
cpydProfile("────────────────────────────────────────────────────────")
svmem = psutil.virtual_memory()
time.sleep(0.1)
progressUpdate(37)
if svmem.total >= 4004255385:
    cpydProfile("Total      : "+f"{get_size(svmem.total)}")
else:
    cpydProfile("Total      : "+f"{get_size(svmem.total)}",True)
    warnings.append("The system only has a total of "+str(get_size(svmem.total))+" of RAM, which is")
    warnings.append("at or below the project's minimum requirements\n")

time.sleep(0.1)
progressUpdate(39)
cpydProfile("Used       : "+f"{get_size(svmem.used)}")
time.sleep(0.1)
progressUpdate(42)
if svmem.available >= 4004255385:
    cpydProfile("Available  : "+f"{get_size(svmem.available)}")
else:
    cpydProfile("Available  : "+f"{get_size(svmem.available)}",True)
    warnings.append("The system only has "+str(get_size(svmem.available))+" of RAM available, which")
    warnings.append("may severely degrade performance of virtual machines\n")

cpydProfile("Free       : "+f"{get_size(svmem.free)}")
time.sleep(0.1)
progressUpdate(50)
time.sleep(0.1)
progressUpdate(52)

cpydProfile(" \n")
cpydProfile("CONFIGURATION")
cpydProfile("────────────────────────────────────────────────────────")
if vfcUefi == 1:
    cpydProfile(("BootMode   : "+"UEFI"))
if vfcUefi == 0:
    cpydProfile(("BootMode   : "+"BIOS / Legacy"),True)
    criticals.append("Host UEFI firmware was not detected, OS likely")
    criticals.append("booted in legacy BIOS mode, this is unsupported\n")
    warningCount = warningCount - 1
    criticalCount = criticalCount + 1
time.sleep(0.1)
progressUpdate(54)
time.sleep(0.1)
progressUpdate(55)
if vfcIommu == 1:
    cpydProfile(("IOMMU      : "+"Available"))
if vfcIommu == 0:
    cpydProfile(("IOMMU      : "+"Unavailable"),True)
    warnings.append("NO IOMMU groups are accessible on the system,")
    warnings.append("kernel parameters or UEFI settings may be wrong\n")
time.sleep(0.1)
progressUpdate(57)
if vfcLibvirtd == 1:
    cpydProfile(("Libvirtd   : "+"Enabled"))
if vfcLibvirtd == 2:
    cpydProfile(("Libvirtd   : "+"Enabled and running"))
if vfcLibvirtd == 0:
    cpydProfile(("Libvirtd   : "+"Disabled"),True)
    warnings.append("The libvirt daemon does not appear to be enabled")
cpydProfile(" ")

if depQemu == 0:
    cpydProfile(("QEMU       : "+"Not installed"),True)
    criticals.append("Missing required dependency: QEMU\n")
    warningCount = warningCount - 1
    criticalCount = criticalCount + 1
if depQemu == 1:
    cpydProfile(("QEMU       : "+"Installed"))

if depLibvirt == 0:
    cpydProfile(("Libvirt    : "+"Not installed"),True)
    criticals.append("Missing required dependency: Libvirt\n")
    warningCount = warningCount - 1
    criticalCount = criticalCount + 1
if depLibvirt == 1:
    cpydProfile(("Libvirt    : "+"Installed"))

if depVirsh == 0:
    cpydProfile(("Virsh      : "+"Not installed"),True)
    warnings.append("Missing core dependency: Virsh\n")
if depVirsh == 1:
    cpydProfile(("Virsh      : "+"Installed"))

if depVirtman == 0:
    cpydProfile(("VirtMan    : "+"Not installed"))
if depVirtman == 1:
    cpydProfile(("VirtMan    : "+"Installed"))

if depRPC == 0:
    cpydProfile(("Pypresence : "+"Not installed"))
if depRPC == 1:
    cpydProfile(("Pypresence : "+"Installed"))

if depNbd == 0:
    cpydProfile(("NBD        : "+"Not installed"))
if depNbd == 1:
    cpydProfile(("NBD        : "+"Installed"))

cpydProfile(" \n")
cpydProfile("VFIO-PCI")
cpydProfile("────────────────────────────────────────────────────────")
if vfcKernel == 1:
    cpydProfile(("Kernel     : "+"Configured"))
if vfcKernel == 0:
    cpydProfile(("Kernel     : "+"Misconfigured"),True)
    warnings.append("The kernel does not appear to be set up correctly,")
    warnings.append("expected drivers are not available / running\n")
cpydProfile(("Stubbed    : "+str(len(pci_ids))))
if len(pci_ids) > 0:
    for i in range(len(pci_ids)): # thanks dom <3
        if (i < 10):
            if (pci_ids[i]):
                cpydProfile(f"Device{i}    : {pci_ids[i]} {vfio_names[i]}")

time.sleep(0.1)
progressUpdate(59)
cpydProfile(" \n")
cpydProfile("INTEGRITY")
cpydProfile("────────────────────────────────────────────────────────")
if vfcIntegrity == 1:
    cpydProfile(("Core       : "+"PASS"))
if vfcIntegrity == 0:
    cpydProfile(("Core       : "+"FAIL"),True)
    criticals.append("Core repository integrity check failed, the")
    criticals.append("current repo instance is damaged and should")
    criticals.append("be replaced or restored\n")
    warningCount = warningCount - 1
    criticalCount = criticalCount + 1

if vfcScrStr == 1:
    cpydProfile(("ScriptStr  : "+"PASS"))
if vfcScrStr == 0:
    cpydProfile(("ScriptStr  : "+"FAIL"),True)
    warnings.append("User script store backup is damaged, restore")
    warnings.append("tools using local files likely won't work\n")

if vfcOvmf == 1:
    cpydProfile(("OVMFStr    : "+"PASS"))
if vfcOvmf == 0:
    cpydProfile(("OVMFStr    : "+"FAIL"),True)
    criticals.append("OVMF store integrity check failed, one or")
    criticals.append("more files are missing or damaged\n")
    warningCount = warningCount - 1
    criticalCount = criticalCount + 1

if vfcBase == 1:
    cpydProfile(("BaseFiles  : "+"PASS"))
if vfcBase == 0:
    cpydProfile(("BaseFiles  : "+"FAIL"),True)
    criticals.append("Base config files used to generate user files")
    criticals.append("required by AutoPilot are missing or damaged\n")
    warningCount = warningCount - 1
    criticalCount = criticalCount + 1

if vfcBin == 1:
    cpydProfile(("InclBin    : "+"PASS"))
if vfcBin == 0:
    cpydProfile(("InclBin    : "+"FAIL"),True)
    warnings.append("Bundled binary file(s) are missing or")
    warnings.append("damaged, features may break at random\n")


if vfcGit == 1:
    cpydProfile(("DeltaData  : "+"PASS"))
if vfcGit == 0:
    cpydProfile(("DeltaData  : "+"FAIL"),True)
    warnings.append("Metadata required for delta updates is missing")
    warnings.append("or damaged, updating via UDU will be restricted\n")


time.sleep(0.1)
progressUpdate(62)
cpydProfile(" \n")

cpydProfile("AUTOPILOT")
cpydProfile("────────────────────────────────────────────────────────")
cpydProfile(("FeatureLvl : "+"8"))
time.sleep(0.1)
progressUpdate(63)
userBlobList = os.listdir("./blobs/user")
if ".user_control" in userBlobList: userBlobList.remove(".user_control")

staleBlobList = os.listdir("./blobs/stale")
if ".stale_control" in staleBlobList: staleBlobList.remove(".stale_control")
time.sleep(0.1)
progressUpdate(64)
liveBlobList = []
for x in os.listdir("./blobs/"):
    if ".apb" in x:
        liveBlobList.append(x)
if ".cdn_control" in liveBlobList: liveBlobList.remove(".cdn_control")
time.sleep(0.1)
progressUpdate(65)
if len(userBlobList) > 0:
    if len(userBlobList) < 17:
        cpydProfile(("UserBlobs  : YES ("+str(len(userBlobList))+" total)"),True)
        warnings.append("Only "+str(len(userBlobList))+" user blobs are present while more are expected,")
        warnings.append("might be from an old repo version or integrity damage\n")
    else:
        cpydProfile(("UserBlobs  : YES ("+str(len(userBlobList))+" total)"))
    #cpydProfile("             ⌈ ")
else:
    cpydProfile(("UserBlobs  : NO"),True)
    warnings.append("NO user blobs were found\n")

time.sleep(0.1)
progressUpdate(70)
for x in userBlobList[0:(len(userBlobList)-1)]:
    cpydProfile("             ├ "+x)
if len(userBlobList) > 0: cpydProfile("             └ "+userBlobList[-1])

if len(userBlobList) > 0: cpydProfile(" ")
time.sleep(0.1)
progressUpdate(72)
if len(staleBlobList) > 0:
    cpydProfile(("StaleBlobs : YES ("+str(len(staleBlobList))+" total)"))
else:
    cpydProfile(("StaleBlobs : NO"))
time.sleep(0.1)
progressUpdate(73)
if len(liveBlobList) > 0:
    cpydProfile(("LiveBlobs  : YES ("+str(len(liveBlobList))+" total)"),True)
    warnings.append("Live AutoPilot blobs were found, did AutoPilot finish")
    warnings.append("running, or did it suffer a fatality?\n")
    
    for f in liveBlobList[0:(len(liveBlobList)-1)]:
        cpydProfile("             ├ "+f)
    cpydProfile("             └ "+liveBlobList[-1])
else:
    cpydProfile(("LiveBlobs  : NO"))
cpydProfile((" "))
time.sleep(0.1)
progressUpdate(77)
if os.path.exists("./boot/OpenCore.qcow2"):
    ocInPlace = "YES"
    ocHash = hashlib.md5(open('./boot/OpenCore.qcow2','rb').read()).hexdigest()
    
    ocStockHashes = []
    ocStockHashes.append(hashlib.md5(open('./resources/oc_store/compat_new/OpenCore.qcow2','rb').read()).hexdigest())
    ocStockHashes.append(hashlib.md5(open('./resources/oc_store/compat_old/OpenCore.qcow2','rb').read()).hexdigest())
    ocStockHashes.append(hashlib.md5(open('./resources/oc_store/legacy_new/OpenCore.qcow2','rb').read()).hexdigest())
    ocModded = "Unknown"
    if ocHash not in ocStockHashes:
        ocModded = "YES"
    else:
        ocModded = "NO"
    ocSize = get_size(os.path.getsize("./boot/OpenCore.qcow2"))
else:
    ocHash = "N/A"
    ocModded = "N/A"
    ocInPlace = "NO"
time.sleep(0.1)
progressUpdate(78)
cpydProfile(("OCInPlace  : "+ocInPlace))
if ocModded == "YES":
    cpydProfile(("OCModded   : "+ocModded),True)
    warnings.append("OpenCore image is very likely to have been modified")
    warnings.append("by the user, integrity can't be verified\n")

else:
    cpydProfile(("OCModded   : "+ocModded))
time.sleep(0.1)
progressUpdate(82)
if os.path.exists("./boot/OpenCore.qcow2"):
    if os.path.getsize("./boot/OpenCore.qcow2") < 18000000: 
        cpydProfile(("OCSize     : "+ocSize),True)
        warnings.append(("OpenCore image file is only "+ocSize+" in size,"))
        warnings.append("which is much smaller than expected\n")
    else: cpydProfile(("OCSize     : "+ocSize))
    if ocModded == "YES":
        cpydProfile(("OCHashMD5  : "+ocHash),True)
        warnings.append("OpenCore image MD5 hash does not match any stock")
        warnings.append("OC images supplied with the project\n")

    else:
        cpydProfile(("OCHashMD5  : "+ocHash))
else:
     cpydProfile(("OCSize     : N/A"))   
     cpydProfile(("OCHashMD5  : N/A"))   
cpydProfile((" "))
time.sleep(0.1)
progressUpdate(83)

if apFilePath is not None:
    cpydProfile(("APFileName : "+apFilePath))
    if apFile is not None:
        cpydProfile(("APFilePath : "+str(os.path.realpath(apFile.name))))
    else:
        cpydProfile(("APFilePath : Unknown"),True)
        warnings.append("AutoPilot blobs reference a boot script that does not")
        warnings.append("actually seem to exist - may cause quirky issues\n")
else:
    cpydProfile(("APFileName : N/A"))
    cpydProfile(("APFilePath : N/A"))
time.sleep(0.1)
progressUpdate(84)
cpydProfile((" \n"))

if apFilePath is not None:
    cpydProfile("GENERATED DATA / "+apFilePath.upper()+"")
    cpydProfile("────────────────────────────────────────────────────────")
    cpydProfile(("Name       : "+apFilePath))
    if apFile is not None:
        cpydProfile(("Path       : "+str(os.path.realpath(apFile.name))))
    else:
        cpydProfile(("Path       : Unknown"))
    cpydProfile(" ")
    if os.path.exists("./blobs/user/USR_TARGET_OS_NAME.apb"): 
        targetOSName = open("./blobs/user/USR_TARGET_OS_NAME.apb")
        targetOSName = targetOSName.read()
    else: 
        targetOSName = "Unknown"
    
    if os.path.exists("./blobs/user/USR_TARGET_OS.apb"):
        targetOS = open("./blobs/user/USR_TARGET_OS.apb")
        targetOS = targetOS.read()
    else:
        targetOS = "Unknown"

    if os.path.exists("./blobs/user/USR_HDD_PATH.apb"):
        targetHDDPath = open("./blobs/user/USR_HDD_PATH.apb")
        targetHDDPath = targetHDDPath.read()
        targetHDDPath = targetHDDPath.replace("$REPO_PATH",os.path.realpath(os.path.curdir))
    else:
        targetHDDPath = "Unknown"
    
    if os.path.exists("./blobs/user/USR_HDD_SIZE.apb"):
        targetHDDSize = open("./blobs/user/USR_HDD_SIZE.apb")
        targetHDDSize = targetHDDSize.read()
        targetHDDSize = targetHDDSize.replace("G"," GB")
    else:
        targetHDDSize = "Unknown"

    if os.path.exists("./blobs/user/USR_HDD_TYPE.apb"):
        targetHDDType = open("./blobs/user/USR_HDD_TYPE.apb")
        targetHDDType = targetHDDType.read()
    else:
        targetHDDType = "Unknown"
    
    if os.path.exists("./blobs/user/USR_HDD_ISPHYSICAL.apb"):
        targetHDDPhysical = open("./blobs/user/USR_HDD_ISPHYSICAL.apb")
        targetHDDPhysical = targetHDDPhysical.read()
    else:
        targetHDDPhysical = "Unknown"

    if os.path.exists(targetHDDPath):
        if targetHDDPhysical != "True": targetHDDSizeReal = get_size(os.path.getsize(targetHDDPath))
        else: targetHDDSizeReal = "N/A"
    else:
        targetHDDSizeReal = "Unknown"

    if os.path.exists("./blobs/user/USR_BOOT_FILE.apb"):
        recoveryImagePath = open("./blobs/user/USR_BOOT_FILE.apb")
        recoveryImagePath = recoveryImagePath.read()
    else:
        recoveryImagePath = "Unknown"

    cpydProfile(("OS         : macOS "+str(targetOSName)))
    cpydProfile(("Version    : "+str(targetOS)))
    cpydProfile(" ")
    if os.path.exists(targetHDDPath):
        cpydProfile(("DiskPath   : "+str(targetHDDPath)))
        cpydProfile(("DiskSize   : "+str(targetHDDSizeReal)))
    else:
        cpydProfile(("DiskPath   : "+str(targetHDDPath)),True)
        cpydProfile(("DiskSize   : "+str(targetHDDSizeReal)),True)
        warnings.append("AutoPilot blobs reference a disk file that does not")
        warnings.append("actually seem to exist - boot will likely fail\n")

        warnings.append("Current virtual hard disk size cannot be determined")
        warnings.append("because the file does not appear to exist\n")
    
    
    cpydProfile(("DiskMax    : "+str(targetHDDSize)))
    cpydProfile(("DiskType   : "+str(targetHDDType)))
    if targetHDDPhysical == "True":
        cpydProfile(("DiskIsReal : "+"YES"))
    else:
        cpydProfile(("DiskIsReal : "+"NO"))
    
    cpydProfile(" ")

    if recoveryImagePath != "-1" and recoveryImagePath != "-2":
        cpydProfile(("RecImgPath : "+str(recoveryImagePath)))
        if os.path.exists(recoveryImagePath): 
            recoveryImageSize = get_size(os.path.getsize(recoveryImagePath))
            recoveryImageHash = hashlib.md5(open(recoveryImagePath,'rb').read()).hexdigest()
            if os.path.getsize(recoveryImagePath) < 2004255385:
                cpydProfile(("RecImgSize : "+str(recoveryImageSize)),True)
                warnings.append(("macOS Recovery image file is only "+str(recoveryImageSize)+" in size,"))
                warnings.append("which is much smaller than expected (did conversion fail?)\n")
            else:
                cpydProfile(("RecImgSize : "+str(recoveryImageSize)))
            cpydProfile(("RecImgHash : "+str(recoveryImageHash)))
        else: recoveryImageSize = "Unknown"
        cpydProfile(("RecImgFrom : Local file"))
        
    else:
        if os.path.exists("./BaseSystem.img"):
            recoveryImagePath = os.path.realpath("./BaseSystem.img")
            if os.path.exists(recoveryImagePath): recoveryImageSize = get_size(os.path.getsize(recoveryImagePath))
            else: recoveryImageSize = "Unknown"
            recoveryImageHash = hashlib.md5(open(recoveryImagePath,'rb').read()).hexdigest()
            
            cpydProfile(("RecImgPath : "+str(recoveryImagePath)))
            if os.path.getsize(recoveryImagePath) < 2004255385:
                cpydProfile(("RecImgSize : "+str(recoveryImageSize)),True)
                warnings.append(("macOS Recovery image file is only "+str(recoveryImageSize)+" in size,"))
                warnings.append("which is much smaller than expected (did conversion fail?)\n")
            else:
                cpydProfile(("RecImgSize : "+str(recoveryImageSize)))
            cpydProfile(("RecImgHash : "+str(recoveryImageHash)))
            cpydProfile(("RecImgFrom : Downloaded with APC"))
        else:
            cpydProfile(("RecImgPath : Unknown"))
            cpydProfile(("RecImgSize : Unknown"))
            cpydProfile(("RecImgHash : Unknown"))
            cpydProfile(("RecImgFrom : Unknown"))

    cpydProfile((" \n"))
time.sleep(0.1)
progressUpdate(86)
time.sleep(1)
if criticalCount > 0:
    cpydProfile((" \n"))
    cpydProfile("CRITICAL ("+str(criticalCount)+")")
    cpydProfile("────────────────────────────────────────────────────────")
    for x in criticals:
        cpydProfile(x)

if warningCount > 0:
    cpydProfile((" \n"))
    cpydProfile("WARNINGS ("+str(warningCount)+")")
    cpydProfile("────────────────────────────────────────────────────────")
    for x in warnings:
        cpydProfile(x)
logFile.close()
time.sleep(0.1)
progressUpdate(100)
os.system("xdg-open ./logs/SPT_"+logTime+".log")