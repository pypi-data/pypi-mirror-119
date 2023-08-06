import { Model } from "../../model";
import * as p from "../../core/properties";
export declare namespace BaseText {
    type Attrs = p.AttrsOf<Props>;
    type Props = Model.Props & {
        text: p.Property<string>;
    };
}
export interface BaseText extends BaseText.Attrs {
}
export declare class BaseText extends Model {
    properties: BaseText.Props;
    constructor(attrs?: Partial<BaseText.Attrs>);
}
//# sourceMappingURL=base_text.d.ts.map