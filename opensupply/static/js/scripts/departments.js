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
    //alert("Clicked First!");
    var id = dijit.byId("department_id");
    var name = dijit.byId("department_name");
    var notes = dijit.byId("department_notes");

    id.setValue(-1);
    name.setValue("");
    notes.setValue("");
} //End of function addDepartment

/**
 *Function saves a new deparment or updates an existing department
 *
 */
function department_save()
{
    //var formToValidate = dojo.byId("department_form");
    //if (formToValidate.validate())
    //{
        //dojo.publish("/saving", [{message: "<font size='2'><b>Saving...", type: "info", duration: 15000}]);

        dojo.xhrGet(
        {
            form: "department_form",
            handleAs: "text",
            url: "department/save",
            load: function(response)
            {
                //dojo.publish("/saved", [{message: "<font size='2'><b>...Saved", type: "info", duration: 15000}]);
                //var department = dojo.fromJson(response);
//                informationMessage("Successfully Saved");  
                //populateDepartmentControls(department);
    dojo.byId("InformationMessage").innerHTML = "Sucess "+ response;
   dijit.byId("InformationMessageDialog").show();
                
            },
            error: function(response)
            {
                //informationMessage("Message");  
                alert("ERROR: " + response);
                //dojo.publish("/saved", [{message: "<font size='2'><b>...Failed: " + response, type: "error", duration: 15000}]);
            }
        });
    //} else { 
      //  alert("Invalid form");
    //}



} //End of function deepartment_save


//function informationMessage(message)
//{
//    dojo.byId("InformationMessage").innerHTML = message;
 //   dijit.byId("InformationMessageDialog").show();
//}

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
    dojo.xhrGet(
    {
        form: "department_form",
        url: "department/previous",
        //handleAs: "json",
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
} //End of function previousDepartment

/**
 * Function navigates to the next department
 */
function nextDepartment()
{
    id = dijit.byId("department_id").attr('value');
    if (id == "")
    {  
        firstDepartment();
        return;
    }

    dojo.xhrGet(
    {
        form: "department_form",
        url: "department/next",
        //handleAs: "json",
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
} //End of function nextDepartment

/**
 * Function navigates to the last department
 */
function lastDepartment()
{
    dojo.xhrGet(
    {
        form: "department_form",
        url: "department/last",
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
    //var departmentName = department.name;

    //if (departmentName.toString() == "none")
    //{
    //    dojo.byId("InformationMessage").innerHTML = "There are no departments";
    //    dijit.byId("InformationMessageDialog").show();
        
    //    return;
    //}

    var id = dijit.byId("department_id");
    var name = dijit.byId("department_name");
    //var type = dijit.byId("department_type");
    var notes = dijit.byId("department_notes");

    id.setValue(department.id);
    name.setValue(department.name);
    //type.setValue(department.type);
    notes.setValue(department.notes);
} //End of function populateDepartmentControls

