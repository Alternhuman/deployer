var graphHtmlString = `<svg height="100%" width="100%" viewBox="0 0 1000 1000" version="1.1"
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

const CPUColors = [
    '#FF6E00',
    '#EE1D00',
    '#8AE234',
    '#3465A4',
    '#3465A4',
];

export default class CPUPanel {
    private data: CPU[][];
    private element: HTMLElement;
    private parent: HTMLElement;
    private svg: HTMLElement;
    private rate : number = 100;
    readonly svgSize : number = 1000;
    private maxValue: number;

    constructor(parent: HTMLElement, title: string, maxValue: number = 100){
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

    /**
     * Appends a new entry to the data
     */
    appendData(d: CPU[]){
        this.data.unshift(d);
        this.render();
    }

    /**
     * Sets up event handling
     */
    bindEvents(){
        const resetControl: HTMLButtonElement = <HTMLButtonElement>this.element.getElementsByClassName('panel-control-reset')[0];
        resetControl.onclick = this.reset;
    }

    /**
     * Removes the currently displayed data
     */
    reset(){
        this.data.forEach(d => {
            d.length = 0;
        });
        this.render();
    }

    render(){
        if(!this.data.length){
            return;
        }
        const increment = this.svgSize / this.rate;
        let cpus = Array(this.data[0].length);
        this.data.forEach((c, i) => {
            c.forEach((d, j)=>{
                cpus[j] = cpus[j] || [];
                cpus[j].push(`${this.svgSize - i*increment},${this.svgSize - this.svgSize/this.maxValue * (d.usr+d.sys)}`);
            })
        });
        let pointsStrs = cpus.map((c, i) => {
            return `<polyline points="${c.join(' ')}" style="fill:none;stroke:${CPUColors[i%CPUColors.length]};stroke-width:3"/>`;
        })
        this.svg.innerHTML = pointsStrs.join("\n");
    }
}