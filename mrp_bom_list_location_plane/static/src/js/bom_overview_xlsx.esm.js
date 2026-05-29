/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewComponent } from "@mrp/components/bom_overview/mrp_bom_overview";
import { BomOverviewControlPanel } from "@mrp/components/bom_overview_control_panel/mrp_bom_overview_control_panel";

patch(BomOverviewComponent.prototype, {
    onClickExportXlsx() {
        return this.actionService.doAction({
            type: "ir.actions.report",
            report_type: "xlsx",
            report_name: "mrp_bom_list_location_plane.report_bom_structure_xlsx",
            report_file: "mrp_bom_list_location_plane.report_bom_structure_xlsx",
            data: {
                quantity: this.state.bomQuantity || 1,
                variant: this.showVariants && this.state.currentVariantId ? this.state.currentVariantId : false,
                warehouse_id: this.state.currentWarehouse ? this.state.currentWarehouse.id : false,
                unfolded_ids: JSON.stringify(Array.from(this.unfoldedIds)),
                availabilities: String(this.state.showOptions.availabilities),
                costs: String(this.state.showOptions.costs),
                operations: String(this.state.showOptions.operations),
                lead_times: String(this.state.showOptions.leadTimes),
            },
            context: {
                active_model: "mrp.bom",
                active_ids: [this.activeId],
            },
        });
    },
});

BomOverviewControlPanel.props = {
    ...BomOverviewControlPanel.props,
    exportXlsx: { type: Function, optional: true },
};

