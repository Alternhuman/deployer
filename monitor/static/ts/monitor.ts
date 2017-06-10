import Panel from './Panel';
import CPUPanel from './CPUPanel';
import MemoryPanel from './MemoryPanel';
import NetworkPanel from './NetworkPanel';

function generateWSAddress(): string{
    const location = window.location;
    var protocol;
    if(location.protocol == 'https:'){
        protocol = 'wss:';
    }else{
        protocol = 'ws:';
    }
    return `${protocol}//${location.hostname}:${location.port}/ws/monitor`;
}

function parseMonitorMessage(data: string) : MonitorMessage{
    var parsedData = <MonitorMessage>JSON.parse(data);
    return parsedData;
}

var ws : WebSocket;
var panels: Panel[] = [];

function onMonitorMessage(ev: MessageEvent){
    const monitorData : MonitorMessage = parseMonitorMessage(ev.data);
    const cpuAll : CPU = monitorData.cpu.filter(c => c['cpu'] == 'all')[0];
    panels[0].appendData(monitorData.cpu);
    panels[1].appendData(monitorData.memory);
    panels[2].appendData(monitorData.network);
}

function start() : void {
    ws = new WebSocket(generateWSAddress());
    ws.onopen = ()=>console.log("Connection open");
    ws.onmessage = onMonitorMessage;
    const container : HTMLDivElement = <HTMLDivElement>document.getElementById("container");
    const panelCPU = new CPUPanel(container, 'CPU');
    const memoryPanel = new MemoryPanel(container, 'Memory');
    const networkPanel = new NetworkPanel(container, 'Network');
    panels.push(panelCPU)
    panels.push(memoryPanel);
    panels.push(networkPanel);
}

window.onload = start;
