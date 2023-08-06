declare type TeXMacros = {
    [key: string]: string | [string, number];
};
export declare function tex2svg(formula: string, macros?: TeXMacros): HTMLElement;
export declare function ascii2svg(_formula: string): HTMLElement;
export declare function mathml2svg(formula: string): HTMLElement;
export {};
//# sourceMappingURL=index.d.ts.map