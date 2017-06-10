interface Memory {
    Cached: number;
    MemFree: number;
    SwapTotal: number;
    MemTotal: number;
    SwapFree: number;
    Buffers: number;
}

interface CPU {
    irq: number;
    steal: number;
    sys: number;
    usr: number;
    cpu: string;
    iowait: number;
    gnice: number;
    soft: number;
    guest: number;
    idle: number;
    nice: number;
}

interface Network {
    Iface: string;
    MTU: number;
    "RX-OK": number;
    "RX-ERR": number;
    "RX-DRP": number;
    "RX-OVR": number;
    "TX-OK": number;
    "TX-ERR": number;
    "TX-DRP": number;
    "TX-OVR": number;
    "Flg": string;
}

interface MonitorMessage {
    time: number;
    tx: number;
    rx: number;
    memory: Memory;
    uname: string;
    load_average: {
        '1min': number;
        '5min': number;
        '15min': number;
    }
    cpu: Array<CPU>;
    network: Array<Network>;
}