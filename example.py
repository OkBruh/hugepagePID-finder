import memprocfs
import psutil

def getHugepagePID():
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if all(keyword in ' '.join(process.info['cmdline']) for keyword in ['qemu', 'hugepages']):
            return process.info['pid']

hugepagePID = getHugepagePID()

if not hugepagePID:
    print("No QEMU process that is using hugepages was found.")
    exit()

device = "qemu://hugepage-pid=" + str(hugepagePID) + ",qmp=/tmp/qmp.sock"

try:
    vmm = memprocfs.Vmm(['-device', device])
except Exception as vmmerror:
    print("Vmm failed to initialise.")
    print(f"Error: {vmmerror}")
    exit()
