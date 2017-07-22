
/* 
 * Script handles all operations on item_categorys such as addition of new
 * item_categorys, updating existing item_categorys, navigation and so on.
 */


/**
 * Function creates an environment suitable for addition of a new item_category
 *
 */
function newItemCategory()
{
    //alert("Clicked First!");
    var id = dijit.byId("item_category_id");
    var name = dijit.byId("item_category_name");
    var notes = dijit.byId("item_category_notes");

    id.setValue(-1);
    name.setValue("");
    notes.setValue("");
} //End of function addItemCategory

/**
 *Function saves a new deparment or updates an existing item_category
 *
 */
function saveItemCategory()
{
    //var formToValidate = dojo.byId("item_category_form");
    //if (formToValidate.validate())
    //{
        //dojo.publish("/saving", [{message: "<font size='2'><b>Saving...", type: "info", duration: 15000}]);

        dojo.xhrGet(
        {
            form: "item_category_form",
            handleAs: "json",
            url: "item_categories/save",
            load: function(response)
            {
                //dojo.publish("/saved", [{message: "<font size='2'><b>...Saved", type: "info", duration: 15000}]);
                //var item_category = dojo.fromJson(response);
//                informationMessage("Successfully Saved");  
                //populateItemCategoryControls(item_category);
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



} //End of function saveItemCategory


//function informationMessage(message)
//{
//    dojo.byId("InformationMessage").innerHTML = message;
 //   dijit.byId("InformationMessageDialog").show();
//}

/**
 * Function navigates to the first item_category
 */
function firstItemCategory()
{
    dojo.xhrGet(
    {
        url: "item_categories/first",
        handleAs: "json",
        load: function(response)
        {
            var item_category = dojo.fromJson(response);

            populateItemCategoryControls(item_category);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function first

/**
 * Function navigates to the previous item_category
 */
function previousItemCategory()
{
    id = dijit.byId("item_category_id").attr('value');
    if (id == "")
    {  
        firstItemCategory();
        return;
    }

    dojo.xhrGet(
    {
        form: "item_category_form",
        url: "item_categories/previous",
        handleAs: "json",
        load: function(response)
        {
            var item_category = dojo.fromJson(response);
            populateItemCategoryControls(item_category);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function previousItemCategory

/**
 * Function navigates to the next item_category
 */
function nextItemCategory()
{
    id = dijit.byId("item_category_id").attr('value');
    if (id == "")
    {  
        firstItemCategory();
        return;
    }

    dojo.xhrGet(
    {
        form: "item_category_form",
        url: "item_categories/next",
        handleAs: "json",
        load: function(response)
        {
            var item_category = dojo.fromJson(response);
            populateItemCategoryControls(item_category);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function nextItemCategory

/**
 * Function navigates to the last item_category
 */
function lastItemCategory()
{
    dojo.xhrGet(
    {
        form: "item_category_form",
        url: "item_categories/last",
        handleAs: "json",
        load: function(response)
        {
            var item_category = dojo.fromJson(response);
            populateItemCategoryControls(item_category);
        },
        error: function(response)
        {
            alert(response);
        }
    });
} //End of function last

function populateItemCategoryControls(item_category)
{
    //var item_categoryName = item_category.name;

    //if (item_categoryName.toString() == "none")
    //{
    //    dojo.byId("InformationMessage").innerHTML = "There are no item_categorys";
    //    dijit.byId("InformationMessageDialog").show();
        
    //    return;
    //}

    var id = dijit.byId("item_category_id");
    var name = dijit.byId("item_category_name");
    var notes = dijit.byId("item_category_notes");

    id.setValue(item_category.id);
    name.setValue(item_category.name);
    notes.setValue(item_category.notes);
} //End of function populateItemCategoryControls

