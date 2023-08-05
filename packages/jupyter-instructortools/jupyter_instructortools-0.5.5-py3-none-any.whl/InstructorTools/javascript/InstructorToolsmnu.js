function createInstructorToolsMenu(){
    var donotinstall = Jupyter.notebook.metadata.noinstructortool;
    if (donotinstall){
        alert('Instructor Tools may not be installed in this notebook!');
        deleteInstructorToolsMenuPerm();
        return;
    }
    if(!document.getElementById('InstructorToolsmnu')){
        var newselect=document.createElement('select');
        newselect.id = 'InstructorToolsmnu';
        newselect.classList.add('form-control'); //class to match notebook formatting
        newselect.classList.add('select-xs'); //class to match notebook formatting
        newselect.setAttribute('style','color:blue;');
        newselect.onchange=function(){
            var lastvalue = this.value;
            this.value='Instructor Tools';
            if (lastvalue=='Insert Data Entry Table...'){
                get_table_dim();
            }
            if (lastvalue=='Mark Cell as Instructions'){
                indicate_cell_contains_instructions();
            }
            if (lastvalue=='Protect Selected Cells'){
                protect_selected_cells();
            }
            if (lastvalue=='Deprotect Selected Cells'){
                deprotect_selected_cells();
            }
            if (lastvalue=='Indicate Protected Cells'){
                mark_protected_cells();
            }
            if (lastvalue=='Allow Hiding Selected Cells'){
                set_hide_selected_cells_on_print();
            }
            if (lastvalue=='Disallow Hiding Selected Cells'){
                unset_hide_selected_cells_on_print();
            }
            if (lastvalue=='Indicate Cells Allowed to Hide'){
                mark_hide_on_print_cells();
            }
            if (lastvalue=='Allow Hiding Selected Code'){
                set_hide_code_on_print();
            }
            if (lastvalue=='Disallow Hiding Selected Code'){
                unset_hide_code_on_print();
            }
            if (lastvalue=='Indicate Code Allowed to Hide'){
                mark_hide_code_on_print_cells();
            }
            if (lastvalue=='Test Hide on Print'){
                JPSLUtils.hide_hide_on_print_cells();
            }
            if (lastvalue=='Undo Hide on Print'){
                JPSLUtils.show_hide_on_print_cells();
            }
            if (lastvalue=='Set Hide Code in JPSL'){
                set_hide_code();
            }
            if (lastvalue=='Unset Hide Code in JPSL'){
                unset_hide_code();
            }
            if (lastvalue=='Indicate Hide Code in JPSL'){
                mark_hide_code_cells();
            }
            if (lastvalue=='Insert get names and timestamp'){
                insert_getnames_timestamp();
            }
            if (lastvalue=='Deactivate this menu'){
                deleteInstructorToolsMenu();
            }
            if (lastvalue=='!deactivate permanently!'){
                deleteInstructorToolsMenuPerm();
            }
            if (lastvalue=='Insert initialization boilerplate'){
                insert_init_boilerplate();
            }
        }
        var optiontxt = '<option title="Choose an option below"> \
        Instructor Tools</option>';
        optiontxt+='<option title="Insert cell below selected and create a \
        data entry table.">Insert Data Entry Table...</option>';
        optiontxt+='<option title="Add light blue color bar to left of \
        markdown cell. Used to indicate instructions.">Mark Cell as \
        Instructions</option>';
        optiontxt+='<option disabled>----</option>';
        optiontxt+='<option title="Prevent editing of selected cells."> \
        Protect Selected Cells</option>';
        optiontxt+='<option title="Allow editing of selected cells."> \
        Deprotect Selected Cells</option>';
        optiontxt+='<option title="Temporarily highlight protected cells in \
        pink.">Indicate Protected Cells</option>';
        optiontxt+='<option disabled>----</option>';
        optiontxt+='<option title="Set selected cells to hide-on-print."> \
        Allow Hiding Selected Cells</option>';
        optiontxt+='<option title="Unset hide-on-print of selected cells."> \
        Disallow Hiding Selected Cells</option>';
        optiontxt+='<option title="Temporarily highlight hide-on-print cells \
        in magenta">Indicate Cells Allowed to Hide</option>';
        optiontxt+='<option title="Set selected to hide-code-on-print."> \
        Allow Hiding Selected Code</option>';
        optiontxt+='<option title="Unset selected to hide-code-on-print."> \
        Disallow Hiding Selected Code</option>';
        optiontxt+='<option title="Temporarily highlight hide-code-on-print \
        cells in orange.">Indicate Code Allowed to Hide</option>';
        optiontxt+='<option title="Hide cells set to hide-on-print or \
        hide-code-on-print">Test Hide on Print</option>';
        optiontxt+='<option title="Redisplay cells set to hide-on-print"> \
        Undo Hide on Print</option>';
        optiontxt+='<option disabled>----</option>';
        optiontxt+='<option title="Set selected to hide-code in JPSL."> \
        Set Hide Code in JPSL</option>';
        optiontxt+='<option title="Unset selected to hide-code in JPSL."> \
        Unset Hide Code in JPSL</option>';
        optiontxt+='<option title="Temporarily highlight hide-code in JPSL \
        cells in yellow.">Indicate Hide Code in JPSL</option>';
        optiontxt+='<option disabled>----</option>';
        optiontxt+='<option title="Insert get names and timestamp function \
        into current cell. Also locks the cell to editing.">';
        optiontxt+='Insert get names and timestamp</option>';
        optiontxt+='<option title="Insert boilerplate about initialization in \
        next cell">Insert initialization boilerplate</option>';
        optiontxt+='<option disabled>----</option>';
        optiontxt+='<option title="Remove/deactivate this menu. Use python \
        command `import InstructorTools` to reactivate">';
        optiontxt+='Deactivate this menu</option>';
        optiontxt+='<option title="Remove menu permanently. Blocks reinstalling.">';
        optiontxt+='!deactivate permanently!</option>';
        newselect.innerHTML=optiontxt;
        document.getElementById('maintoolbar-container').appendChild(newselect);
    }
}

function deleteInstructorToolsMenu(){
    if(document.getElementById('InstructorToolsmnu')){
        document.getElementById('InstructorToolsmnu').remove();
    }
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        var should_delete = false;
        if(celllist[i].get_text().indexOf('from InstructorTools import *') !== -1){
            should_delete = true
        }
        if (celllist[i].get_text().indexOf('import InstructorTools')!== -1){
            should_delete = true
        }
        if(celllist[i].get_text().indexOf('instmenu_act()') !== -1){
            should_delete = true
        }
        if (should_delete){
            //delete the cell
            var cellindex=Jupyter.notebook.find_cell_index(celllist[i]);
            //alert('cellindex: '+cellindex)
            Jupyter.notebook.delete_cell(cellindex);
        }
    }
}
function deleteInstructorToolsMenuPerm(){
    if(document.getElementById('InstructorToolsmnu')){
        document.getElementById('InstructorToolsmnu').remove();
    }
    Jupyter.notebook.metadata.noinstructortool=true;
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        if(celllist[i].get_text().indexOf('from InstructorTools import *') !== -1){
            //delete the cell
            var cellindex=Jupyter.notebook.find_cell_index(celllist[i]);
            //alert('cellindex: '+cellindex)
            Jupyter.notebook.delete_cell(cellindex);
        }
        if(celllist[i].get_text().indexOf('instmenu_act()') !== -1){
            //delete the cell
            var cellindex=Jupyter.notebook.find_cell_index(celllist[i]);
            //alert('cellindex: '+cellindex)
            Jupyter.notebook.delete_cell(cellindex);
        }
    }
}

function protect_selected_cells(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        celllist[i].metadata.editable=false;
        celllist[i].element.children()[0].setAttribute("style","background-color:pink;");
        }
}

function deprotect_selected_cells(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        celllist[i].metadata.editable=true;
        celllist[i].element.children()[0].removeAttribute("style");
    }
}

function mark_protected_cells(){
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        if (celllist[i].metadata.editable==false){
        celllist[i].element.children()[0].setAttribute("style","background-color:pink;");
        } else {
        celllist[i].element.children()[0].removeAttribute("style");
        }
    }
}

function set_hide_selected_cells_on_print(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        if (!celllist[i].metadata.JPSL){
        celllist[i].metadata.JPSL={}}
        celllist[i].metadata.JPSL.hide_on_print=true;
        celllist[i].element.children()[0].setAttribute("style",
        "background-color:magenta;");
        }
}

function unset_hide_selected_cells_on_print(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        if (!celllist[i].metadata.JPSL){
        celllist[i].metadata.JPSL={}}
        celllist[i].metadata.JPSL.hide_on_print=false;
        celllist[i].element.children()[0].removeAttribute("style");
    }
}

function mark_hide_on_print_cells(){
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        if (celllist[i].metadata.JPSL){
            if (celllist[i].metadata.JPSL.hide_on_print==true){
                celllist[i].element.children()[0].setAttribute("style",
                "background-color:magenta;");
                } else {
                celllist[i].element.children()[0].removeAttribute("style");
            }
        }
    }
}

function set_hide_code_on_print(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        if (!celllist[i].metadata.JPSL){
        celllist[i].metadata.JPSL={}}
        celllist[i].metadata.JPSL.hide_code_on_print=true;
        celllist[i].element.children()[0].setAttribute("style",
        "background-color:orange;");
        }
}

function unset_hide_code_on_print(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        if (!celllist[i].metadata.JPSL){
        celllist[i].metadata.JPSL={}}
        celllist[i].metadata.JPSL.hide_code_on_print=false;
        celllist[i].element.children()[0].removeAttribute("style");
        }
}

function mark_hide_code_on_print_cells(){
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        if (celllist[i].metadata.JPSL){
            if (celllist[i].metadata.JPSL.hide_code_on_print==true){
                celllist[i].element.children()[0].setAttribute("style",
                "background-color:orange;");
                } else {
                celllist[i].element.children()[0].removeAttribute("style");
            }
        }
    }
}

function set_hide_code(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        if (!celllist[i].metadata.JPSL){
        celllist[i].metadata.JPSL={}}
        celllist[i].metadata.JPSL.hide_code=true;
        celllist[i].element.children()[0].setAttribute("style",
        "background-color:yellow;");
        }
}

function unset_hide_code(){
    var celllist = Jupyter.notebook.get_selected_cells();
    for (var i = 0;i<celllist.length;i++){
        if (!celllist[i].metadata.JPSL){
        celllist[i].metadata.JPSL={}}
        celllist[i].metadata.JPSL.hide_code=false;
        celllist[i].element.children()[0].removeAttribute("style");
        }
}

function mark_hide_code_cells(){
    var celllist = Jupyter.notebook.get_cells();
    for (var i = 0;i<celllist.length;i++){
        if (celllist[i].metadata.JPSL){
            if (celllist[i].metadata.JPSL.hide_code==true){
                celllist[i].element.children()[0].setAttribute("style",
                "background-color:yellow;");
                } else {
                celllist[i].element.children()[0].removeAttribute("style");
            }
        }
    }
}
function insert_getnames_timestamp(){
    var text = 'import JPSLUtils\nJPSLUtils.record_names_timestamp()';
    JPSLUtils.insert_newline_at_end_of_current_cell(text);
    protect_selected_cells();
}

function indicate_cell_contains_instructions(){
    var text = '<div style="border-color:lightblue;border-style:solid; \
    float:left;height:100%;margin-right:4px;margin-bottom:94px;"></div>\n\n';
    JPSLUtils.insert_text_at_beginning_of_current_cell(text);
    var currentcell = Jupyter.notebook.get_selected_cell();
    var cellindex=Jupyter.notebook.find_cell_index(currentcell);
    Jupyter.notebook.to_code(cellindex);
    Jupyter.notebook.to_markdown(cellindex);
    Jupyter.notebook.focus_cell();
    Jupyter.notebook.get_selected_cell().execute();
}

function insert_init_boilerplate(){
    var mkdstr = "### You must initialize the software each time you use \
    this notebook.\n";
    mkdstr += " 1. First, check that the notebook is \"Trusted\" by looking \
    near";
    mkdstr += " the right of the Jupyter toolbars. If the notebook is not \
    trusted";
    mkdstr += " you need to click on the \"not trusted\" button and trust the";
    mkdstr += " notebook. **You should only trust notebooks that come from a";
    mkdstr += " *trusted source*, such as the class website.**\n";
    mkdstr += " 2. The cell immediately below contains code that loads the";
    mkdstr += " software modules necessary for this notebook to run. It also";
    mkdstr += " collects some bookkeeping information that can be used for";
    mkdstr += " troubleshooting. **You must run this cell each time you open";
    mkdstr += " the notebook or later cells may not work.**\n";
    mkdstr += " 3. If you are doing calculations that depend upon";
    mkdstr += " using variables passed from calculations done the previous";
    mkdstr += " time the notebook was opened, you will need to run those";
    mkdstr += " previous cells to redefine the variables.\n";
    mkdstr += " 4. *DO NOT run cells that contain plot displays of live data";
    mkdstr += " collection, as that will restart the data collection.* You can";
    mkdstr += " reload data collected from the `.csv` files  written for each";
    mkdstr += " collection run. Ideally you would do this in a new notebook.";

  Jupyter.notebook.focus_cell();
  var currentcell = Jupyter.notebook.insert_cell_below();
  currentcell.set_text(mkdstr);
  var cellindex=Jupyter.notebook.find_cell_index(currentcell);
  Jupyter.notebook.to_markdown(cellindex);
  Jupyter.notebook.focus_cell();
  Jupyter.notebook.get_selected_cell().execute();
}