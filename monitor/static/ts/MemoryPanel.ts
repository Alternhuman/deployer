import Panel from './Panel';

const graphHtmlString = `<svg height="100%" width="100%" viewBox="0 0 1000 1000" version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    preserveAspectRatio="none" style="max-height:200px;">
</svg>
`

const htmlString = (panelTitle: string) => `<div class="panel">
    <div class="panel-title">
        <span>${panelTitle}</span>
        <div class="panel-controls">
            <span class="panel-control">
                Timeline
            </span>
            <button class="panel-control panel-control-reset">
                Reset
            </button>
            <span class="panel-control">
                Type
            </span>
            <span class="panel-control">
                Collapse
            </span>
        </div>
    </div>
    <div class="panel-content">
        
    </div>
</div>`;

export default class MemoryPanel extends Panel {
    private data: Memory[];
    
    constructor(parent: HTMLElement, title: string, maxValue: number = 100){
        super(parent, title, maxValue);
        this.parent = parent;
        let template = document.createElement('template');
        template.innerHTML = htmlString(title);
        this.element = <HTMLElement>template.content.firstChild;
        this.parent.appendChild(this.element);
        const content = this.element.getElementsByClassName('panel-content')[0];
        template = document.createElement('template');
        template.innerHTML = graphHtmlString;
        this.svg = <HTMLElement>template.content.firstChild;
        content.appendChild(this.svg);

        this.maxValue = maxValue;
        this.data = [];

        this.reset = this.reset.bind(this);

        this.bindEvents();
        this.render();
    }

    appendData(d: Memory){
        this.data.unshift(d);
        this.render();
    }

    reset(){
        this.data.length = 0;
        this.render();
    }

    render(){
        if(!this.data.length){
            return;
        }
        
        const increment = this.svgSize / this.rate;
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
        this.svg.innerHTML = pointsStrs.join("\n");
    
    }
}