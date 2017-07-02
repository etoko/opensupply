/* 
 * Script handles all operations on departments such as addition of new
 * departments, updating existing departments, navigation and so on.
 */


/**
 * Function creates an environment suitable for addition of a new department
 *
 */
function newDepartment()
{
    var id = dijit.byId("Department.DepartmentId");
    var name = dijit.byId("Department.Name");
    var type = dijit.byId("Department.Type");
    var notes = dijit.byId("Department.Notes");

    dojo.xhrGet(
    {
        url: "servlets/departmentManager?operationType=add",
        load: function(response)
        {
            dojo.publish("/saved", [{message: "<font size='2'><b>Enter new Department", type: "info", duration: 15000}]);
            id.setValue("");
    name.setValue("");
    type.setValue("");
    notes.setValue("");
        },
        error: function(response)
        {
            dojo.publish("/saved", [{message: "<font size='2'><b>...Failed: " + response, type: "error", duration: 15000}]);
        }
    });
} //End of function addDepartment

/**
 *Function saves a new deparment or updates an existing department
 *
 */
function department_save()
{
    var formToValidate = dojo.byId("department_form");
    //if (formToValidate.validate())
    //{
        dojo.publish("/saving", [{message: "<font size='2'><b>Saving...", type: "info", duration: 15000}]);

        dojo.xhrGet(
        {
            form: "department_form",
            handleAs: "json",
            url: "department/save",
            load: function(response)
            {
                dojo.publish("/saved", [{message: "<font size='2'><b>...Saved", type: "info", duration: 15000}]);
                var department = dojo.fromJson(response);
                populateDepartmentControls(department);
                alert(response);
            },
            error: function(response)
            {
                dojo.publish("/saved", [{message: "<font size='2'><b>...Failed: " + response, type: "error", duration: 15000}]);
            }
        });
    //} else { 
      //  alert("Invalid form");
    //}



} //End of function deepartment_save

/**
 * Function navigates to the first department
 */
function firstDepartment()
{
    dojo.xhrGet(
    {
        url: "department/first",
        load: function(response)
        {
            var department = dojo.fromJson(response);

            populateDepartmentControls(department);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function first

/**
 * Function navigates to the previous department
 */
function previousDepartment()
{
    alert("Previous Department");
} //End of function previousDepartment

/**
 * Function navigates to the next department
 */
function nextDepartment()
{
    
    alert("Next Department");
} //End of function nextDepartment

/**
 * Function navigates to the last department
 */
function lastDepartment()
{
    dojo.xhrGet(
    {
        url: "servlets/departmentManager?operationType=last",
        load: function(response)
        {
            var department = dojo.fromJson(response);
            populateDepartmentControls(department);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function last

function populateDepartmentControls(department)
{
    var departmentName = department.name;

    if (departmentName.toString() == "none")
    {
        dojo.byId("InformationMessage").innerHTML = "There are no departments";
        dijit.byId("InformationMessageDialog").show();
        
        return;
    }

    var id = dijit.byId("department_id");
    var name = dijit.byId("department_name");
    //var type = dijit.byId("department_type");
    var notes = dijit.byId("department_notes");

    id.setValue(department.id);
    name.setValue(department.name);
    //type.setValue(department.type);
    notes.setValue(department.notes);
} //End of function populateDepartmentControls

