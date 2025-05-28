/* @odoo-module */

import { Component, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component{
     static template = "todo_task.ListView";

     setup(){
         this.state = useState({
             'tasks' : []
         });
         this.orm = useService("orm");
         this.rpc = useService("rpc");
         this.action = useService("action");
         this.loadTasks();

         this._intervalId = setInterval(() => {
            this.loadTasks();
        }, 4000);
         onWillUnmount(() => {
            clearInterval(this._intervalId);
        });
     };


     async loadTasks(){
            const result = await this.rpc("/web/dataset/call_kw", {
                 model: "todo.list",
                 method: "search_read",
                 args: [[]],
                 kwargs:{ fields: ["id","name", "assign_to", "description", "due_date", "expected_date", "ref", "state"]},
            });
            console.log(result);
            this.state.tasks = result;
       };


      async CreateRecord() {
            const result = await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "todo.list",
                view_mode: "form",
                views: [[false, 'form']],
                target: "new",
            });
            if (result && result.res_id) {
                this.loadTasks();
            }
      }
     async DeleteRecord(taskId){
             const confirmDelete = window.confirm("Are you sure you want to delete this task?");
                 if (!confirmDelete) {
                     return;
                 }
             await this.rpc("/web/dataset/call_kw", {
                 model: "todo.list",
                 method: "unlink",
                 args: [[taskId]],
                 kwargs: {},
            });
            this.loadTasks();
     };
     async EditRecord(taskId) {
            const result = await this.action.doAction({
                type: "ir.actions.act_window",
                res_model: "todo.list",
                res_id: taskId,
                view_mode: "form",
                views: [[false, 'form']],
                target: "new",
            });
            if (result && result.res_id) {
                this.loadTasks();
            }
        }

}

registry.category("actions").add("todo_task.action_list_view", ListViewAction);

