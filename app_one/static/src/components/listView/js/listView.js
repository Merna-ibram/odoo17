/* @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component{
     static template = "app_one.ListView";

     setup(){
         this.state = useState({
             'properties' : []
         });
         this.orm = useService("orm");
         this.rpc = useService("rpc");
         this.action = useService("action");
         this.loadProperties();

         this._intervalId = setInterval(() => {
            this.loadProperties();
        }, 3000);
         onWillUnmount(() => {
            clearInterval(this._intervalId);
        });
     };

//      async  loadProperties(){
//         const result = await this.orm.searchRead("property", [], [
//                "name", "postcode", "expected_date", "expected_price", "bedrooms", "owner_id", "state"
//            ]);
//         console.log(result);
//         this.state.properties = result;
//     };
       async loadProperties(){
            const result = await this.rpc("/web/dataset/call_kw", {
                 model: "property",
                 method: "search_read",
                 args: [[]],
                 kwargs:{ fields: ["id","name", "postcode", "expected_date", "expected_price", "bedrooms", "state"]},
            });
            console.log(result);
            this.state.properties = result;
       };
//        async CreateRecord(){
//             await this.rpc("/web/dataset/call_kw", {
//                 model: "property",
//                 method: "create",
//                 args: [{
//                 name: "new property",
//                 postcode: "1234564",
//                 bedrooms: "5",
//                 }],
//                 kwargs: {},
//            });
//            this.loadProperties();
//        };
        async CreateRecord() {
            const result = await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "property",
                view_mode: "form",
                views: [[false, 'form']],
                target: "new",
            });
            if (result && result.res_id) {
                this.loadProperties();
            }
        }

        async DeleteRecord(propertyId){
             const confirmDelete = window.confirm("Are you sure you want to delete this property?");
                 if (!confirmDelete) {
                     return;
                 }
             await this.rpc("/web/dataset/call_kw", {
                 model: "property",
                 method: "unlink",
                 args: [[propertyId]],
                 kwargs: {},
            });
            this.loadProperties();
        };
//        async EditRecord(propertyId){
//             await this.rpc("/web/dataset/call_kw", {
//                 model: "property",
//                 method: "write",
//                 args:  [[propertyId], {
//                   name: "Edited Property",
//                   bedrooms: "6",
//                   postcode: "000123",
//                   }],
//                 kwargs: {},
//            });
//            this.loadProperties();
//        };
        async EditRecord(propertyId) {
            const result = await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "property",
                res_id: propertyId,
                view_mode: "form",
                views: [[false, 'form']],
                target: "new",
            });
            if (result && result.res_id) {
                this.loadProperties();
            }
        }

}

registry.category("actions").add("app_one.action_list_view", ListViewAction);

