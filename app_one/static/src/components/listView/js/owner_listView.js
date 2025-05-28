/* @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class OwnerListViewAction extends Component{
     static template = "app_one.OwnerListView";

     setup(){
         this.state = useState({
             'owners' : []
         });
         this.orm = useService("orm");
         this.action = useService("action");
         this.loadOwners();

         this._intervalId = setInterval(() => {
            this.loadOwners();
        }, 3000);
         onWillUnmount(() => {
            clearInterval(this._intervalId);
        });
     };

      async loadOwners(){
         const owners  = await this.orm.searchRead("owner", [], [
                "name", "phone_number", "property_ids", "address", "e_mail"
            ]);
         for (let owner of owners) {
             if (owner.property_ids.length > 0) {
                 const propertyNames = await this.orm.call("property", "name_get", [owner.property_ids]);
                 owner.property_names = propertyNames.map((p) => p[1]).join(", ");
             }else {
                 owner.property_names = "No properties";
             }
         };
         console.log(owners);
         this.state.owners = owners;
         this.loadOwners();
     };
     async CreateRecord() {
            const result = await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "owner",
                view_mode: "form",
                views: [[false, 'form']],
                target: "new",
            });
            if (result && result.res_id) {
                this.loadOwners();
            }
     };
     async DeleteRecord(ownerId){
             const confirmDelete = window.confirm("Are you sure you want to delete this owner?");
                 if (!confirmDelete) {
                     return;
                 }
             await this.rpc("/web/dataset/call_kw", {
                 model: "owner",
                 method: "unlink",
                 args: [[ownerId]],
                 kwargs: {},
            });
            this.loadProperties();
        };
     async EditRecord(ownerId) {
            const result = await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "owner",
                res_id: ownerId,
                view_mode: "form",
                views: [[false, 'form']],
                target: "new",
            });
            if (result && result.res_id) {
                this.loadOwners();
            }
        }


}

registry.category("actions").add("app_one.owner_list_view_action", OwnerListViewAction);

