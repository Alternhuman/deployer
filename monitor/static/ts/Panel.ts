export default abstract class Panel {
    constructor(parent: HTMLElement, title: string, maxValue: number = 100){

    }
    protected element: HTMLElement;
    protected parent: HTMLElement;
    protected svg: HTMLElement;
    protected rate : number = 100;
    readonly svgSize : number = 1000;
    protected maxValue: number;

    abstract appendData(d: any) : void;

    bindEvents(){
        const resetControl: HTMLButtonElement = <HTMLButtonElement>this.element.getElementsByClassName('panel-control-reset')[0];
        resetControl.onclick = this.reset;
    }

    abstract reset() : void;
    abstract render(): void;
}

export const htmlString = (panelTitle: string) => `<div class="panel">
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
