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
}