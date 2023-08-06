import { BaseText } from "./base_text";
import * as p from "../../core/properties";
export declare namespace PlainText {
    type Attrs = p.AttrsOf<Props>;
    type Props = BaseText.Props & {
        text: p.Property<string>;
    };
}
export interface PlainText extends PlainText.Attrs {
}
export declare class PlainText extends BaseText {
    properties: PlainText.Props;
    constructor(attrs?: Partial<PlainText.Attrs>);
}
//# sourceMappingURL=plain_text.d.ts.map