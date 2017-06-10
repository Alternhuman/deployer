# https://github.com/giampaolo/psutil/blob/master/psutil/_pslinux.py
# https://github.com/qrees/tornado-chat/tree/master/common
import os
import time
from time import localtime, mktime

from tornado import process

import conf

subprocess_opts = {'shell': True, 'stdout': process.Subprocess.STREAM}

def extract_cpu_info(cpu_info):
    result = []
    for cpu in cpu_info:
        cpu = cpu.split()
        result.append({
            "cpu": cpu[1],
            "usr": float(cpu[2].replace(',', '.')),
            "nice": float(cpu[3].replace(',', '.')),
            "sys": float(cpu[4].replace(',', '.')),
            "iowait": float(cpu[5].replace(',', '.')),
            "irq": float(cpu[6].replace(',', '.')),
            "soft": float(cpu[7].replace(',', '.')),
            "steal": float(cpu[8].replace(',', '.')),
            "guest": float(cpu[9].replace(',', '.')),
            "gnice": float(cpu[10].replace(',', '.')),
            "idle": float(cpu[11].replace(',', '.')),
        })
    return result

async def get_network_info():
    fd_network = process.Subprocess("netstat -i | tail -n +2", **subprocess_opts).stdout
    network_result = await fd_network.read_until_close()
    network_result = network_result.decode('utf-8').strip()
    network_result = network_result.split("\n")
    header = network_result[0].split()
    interfaces = network_result[1:]
    result = []
    for iface in interfaces:
        result.append({key: value for key, value in zip(header, iface.split())})
    return result

async def get_data():
    """
    Reads data sources and outputs a dictionary containing the results
    """
    response_dict = {}
    response_dict["time"] = mktime(localtime())*1000.0
    fd_uname = process.Subprocess("uname -r", **subprocess_opts).stdout

    uname_result = await fd_uname.read_until_close()
    uname_result = uname_result.decode('utf-8').strip()
    response_dict["uname"] = uname_result

    fd_uptime = process.Subprocess("uptime | tail -n 1 | awk '{print $3 $4 $5}'", **subprocess_opts).stdout

    uptime_result = await fd_uptime.read_until_close()
    response_dict["uptime"] = uptime_result.decode('utf-8').strip()

    memory = {}

    memory_data = (await process.Subprocess("egrep --color '^(MemTotal|MemFree|Buffers|Cached|SwapTotal|SwapFree)' /proc/meminfo | egrep '[0-9.]{4,}' -o", **subprocess_opts).stdout.read_until_close()).decode('utf-8').strip().split('\n')
    memory["MemTotal"] = int(memory_data[0])
    memory["MemFree"] = int(memory_data[1])
    memory["Buffers"] = int(memory_data[2])
    memory["Cached"] = int(memory_data[3])
    memory["SwapTotal"] = int(memory_data[4])
    memory["SwapFree"] = int(memory_data[5])

    response_dict["memory"] = memory

    load_data = (await process.Subprocess("uptime | grep -ohe 'load average[s:][: ].*' | awk '{ print $3\" \"$4\" \"$5 }'", **subprocess_opts).stdout.read_until_close()).decode('utf-8').strip().split(', ') # https://raymii.org/s/snippets/Get_uptime_load_and_users_with_grep_sed_and_awk.html
    load_average = {'1min': float(load_data[0].replace(',', '.')), '5min': float(load_data[1].replace(',', '.')), '15min': float(load_data[2].replace(',', '.'))}
    response_dict["load_average"] = load_average

    # TODO: Replace with /proc/net/dev: https://serverfault.com/a/533523/284322
    #response_dict["rx"] = int((await process.Subprocess("/sbin/ifconfig eth0 | grep \"RX bytes\" | awk '{ print $2 }' | cut -d\":\" -f2", **subprocess_opts).stdout.read_until_close()).decode('utf-8').strip())

    #response_dict["tx"] = int((await process.Subprocess("/sbin/ifconfig eth0 | grep \"TX bytes\" | awk '{ print $2 }' | cut -d\":\" -f2", **subprocess_opts).stdout.read_until_close()).decode('utf-8').strip())

    cpu_info = (await process.Subprocess(os.path.join(conf.BASE_DIR, "./mpstat/mpstat -P ALL 1 1 | tail -n +4"), **subprocess_opts).stdout.read_until_close()).decode('utf-8').strip().split('\n')

    cpu_info = extract_cpu_info(cpu_info)

    response_dict["cpu"] = cpu_info

    response_dict["network"] = await get_network_info()
    response_dict["timestamp"] = time.time()

    return response_dict
