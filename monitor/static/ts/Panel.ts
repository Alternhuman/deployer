var graphHtmlString = `<svg height="100%" width="100%" viewBox="0 0 1000 1000" version="1.1"
    xmlns="http://www.w3.org/2000/svg"
    preserveAspectRatio="none" style="max-height:200px;"><polyline points="0,0 300,500 1000,1000" style="fill:none;stroke:black;stroke-width:3"/>
</svg>
`

const htmlString = (panelTitle: string) => `<div class="panel">
    <div class="panel-title">
        <span>${panelTitle}</span>
        <span class="panel-controls">
            <span class="panel-control">
                Timeline
            </span>
            <span class="panel-control">
                Type
            </span>
            <span class="panel-control">
                Collapse
            </span>
        </span>
    </div>
    <div class="panel-content">
        
    </div>
</div>`;



export default class Panel {
    private data: any[];
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

        this.render();
    }

    /**
     * Appends a new entry to the data
     */
    appendData(d: any){
        this.data.unshift(d);
        this.render();
    }

    /**
     * Removes the currently displayed data
     */
    reset(){

    }

    render(){
        const increment = this.svgSize / this.rate;
        let pointsStr = this.data.map((d, i) => {
            return `${this.svgSize - i*increment},${this.svgSize - this.svgSize/this.maxValue * d}`;
        }).join(" ");
        //console.log(pointsStr);
        
        //(<HTMLElement>this.svg.firstChild).setAttribute('points', "0,0 300,500 440,500 1000,1000");
        (<HTMLElement>this.svg.firstChild).setAttribute('points', pointsStr);
    }
}