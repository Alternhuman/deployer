import Panel, {htmlString} from './Panel';

const tableHtmlString = `<table class="netstat" style="width:100%;height:100%; max-height:200px"></table>
`;

const header = `<thead>
<tr><th>Iface</th>
<th>RX-OK</th>
<th>TX-OK</th>
</tr>
</thead>`;
const row = (d : Network) => `<tr>
<td>${d.Iface}</td>
<td>${d['RX-OK']}</td>
<td>${d['TX-OK']}</td>
</tr>`;

export default class NetworkPanel extends Panel {
    data : Array<Array<Network>> = [];

    constructor(parent: HTMLElement, title: string, maxValue: number = 100){
        super(parent, title, maxValue);
        this.parent = parent;
        let template = document.createElement('template');
        template.innerHTML = htmlString(title);
        this.element = <HTMLElement>template.content.firstChild;
        this.parent.appendChild(this.element);
        const content = this.element.getElementsByClassName('panel-content')[0];
        template = document.createElement('template');
        template.innerHTML = tableHtmlString;
        this.svg = <HTMLElement>template.content.firstChild;
        content.appendChild(this.svg);

        this.maxValue = maxValue;

        this.reset = this.reset.bind(this);

        this.bindEvents();
        this.render();
    }

    appendData(d : Array<Network>) : void {
        this.data.push(d);
        this.render();
    }

    reset() : void {

    }

    render(){
        if(!this.data.length){
            return;
        }
        const l = this.data.length-1;
        if(!this.data[l].length){
            // TODO: Display 'No data available'
        }else{
            const htmlString = this.data[l].map(n => {
                return row(n);
            }).join("\n");
            this.svg.innerHTML = header + htmlString;
        }
        
        /*const increment = this.svgSize / this.rate;
        const points = this.data.map((m: Memory, i)=>{
            return {
                "MemFree": `${this.svgSize - i*increment}, ${this.svgSize - this.svgSize*(m.MemTotal-m.MemFree-m.Cached)/m.MemTotal}`,
            }
        });

        //const pointsStrs : string[] = [];
        let memFreePoints = [];
        for(const k of points){
            memFreePoints.push(k.MemFree);
        }
        let pointsStrs = [`<polyline points="${memFreePoints.join(' ')}" style="fill:none;stroke:blue;stroke-width:3" />;stroke-width:3"`]
        this.svg.innerHTML = pointsStrs.join("\n");*/
    
    }
}