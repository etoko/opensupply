
/* 
 * Script handles all operations on requisitions such as addition of new
 * requisitions, updating existing requisitions, navigation and so on.
 */


/**
 * Function creates an environment suitable for addition of a new requisition
 *
 */
function newDepartment()
{
    //alert("Clicked First!");
    var id = dijit.byId("requisition_id");
    var name = dijit.byId("requisition_name");
    var notes = dijit.byId("requisition_notes");

    id.setValue(-1);
    name.setValue("");
    notes.setValue("");
} //End of function addDepartment

/**
 *Function saves a new deparment or updates an existing requisition
 *
 */
function requisition_save()
{
    //var formToValidate = dojo.byId("requisition_form");
    //if (formToValidate.validate())
    //{
        //dojo.publish("/saving", [{message: "<font size='2'><b>Saving...", type: "info", duration: 15000}]);

        dojo.xhrGet(
        {
            form: "requisition_form",
            handleAs: "text",
            url: "requisitions/save",
            load: function(response)
            {
                //dojo.publish("/saved", [{message: "<font size='2'><b>...Saved", type: "info", duration: 15000}]);
                //var requisition = dojo.fromJson(response);
//                informationMessage("Successfully Saved");  
                //populateDepartmentControls(requisition);
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
 * Function navigates to the first requisition
 */
function firstDepartment()
{
    dojo.xhrGet(
    {
        url: "requisitions/first",
        load: function(response)
        {
            var requisition = dojo.fromJson(response);

            populateDepartmentControls(requisition);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function first

/**
 * Function navigates to the previous requisition
 */
function previousDepartment()
{
    id = dijit.byId("requisition_id").attr('value');
    if (id == "")
    {  
        firstDepartment();
        return;
    }

    dojo.xhrGet(
    {
        form: "requisition_form",
        url: "requisitions/previous",
        //handleAs: "json",
        load: function(response)
        {
            var requisition = dojo.fromJson(response);
            populateDepartmentControls(requisition);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function previousDepartment

/**
 * Function navigates to the next requisition
 */
function nextDepartment()
{
    id = dijit.byId("requisition_id").attr('value');
    if (id == "")
    {  
        firstDepartment();
        return;
    }

    dojo.xhrGet(
    {
        form: "requisition_form",
        url: "requisitions/next",
        //handleAs: "json",
        load: function(response)
        {
            var requisition = dojo.fromJson(response);
            populateDepartmentControls(requisition);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function nextDepartment

/**
 * Function navigates to the last requisition
 */
function lastDepartment()
{
    dojo.xhrGet(
    {
        form: "requisition_form",
        url: "requisitions/last",
        load: function(response)
        {
            var requisition = dojo.fromJson(response);
            populateDepartmentControls(requisition);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function last

function populateDepartmentControls(requisition)
{
    //var requisitionName = requisition.name;

    //if (requisitionName.toString() == "none")
    //{
    //    dojo.byId("InformationMessage").innerHTML = "There are no requisitions";
    //    dijit.byId("InformationMessageDialog").show();
        
    //    return;
    //}

    var id = dijit.byId("requisition_id");
    var name = dijit.byId("requisition_name");
    //var type = dijit.byId("requisition_type");
    var notes = dijit.byId("requisition_notes");

    id.setValue(requisition.id);
    name.setValue(requisition.name);
    //type.setValue(requisition.type);
    notes.setValue(requisition.notes);
} //End of function populateDepartmentControls

