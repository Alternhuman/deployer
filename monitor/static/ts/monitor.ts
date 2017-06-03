import CPUPanel from './CPUPanel';
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
var panels: CPUPanel[] = [];

function onMonitorMessage(ev: MessageEvent){
    const monitorData : MonitorMessage = parseMonitorMessage(ev.data);
    const cpuAll : CPU = monitorData.cpu.filter(c => c['cpu'] == 'all')[0];
    panels[0].appendData(monitorData.cpu);
    console.log(monitorData)
}

function start() : void {
    ws = new WebSocket(generateWSAddress());
    ws.onopen = ()=>console.log("Connection open");
    ws.onmessage = onMonitorMessage;
    var panelCPU = new CPUPanel(document.getElementById("container"), 'CPU');
    panels.push(panelCPU)
}

window.onload = start;
