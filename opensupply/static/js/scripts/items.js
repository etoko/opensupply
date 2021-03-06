/**
 * Script handles all operations on Items such as creation of new Items, updating
 * existing items, deletion of items and suchalike operations.
 */

/*
 *Script handles all operations of the items page such as navigation, adding new
 *items entities and so on
 */
function newItem()
{   
    var itemId = dojo.byId("item_id");
    var itemName = dojo.byId("item_name");
    var itemUnitMeasurement = dojo.byId("item_unit_measurement");
    var itemNotes = dojo.byId("item_notes");

    itemId.value = -1;
    itemName.value = "";
    itemUnitMeasurement.value = "";
    itemNotes.value = "";
} //End of function newItem

function saveItem()
{
        dojo.xhrPost(
        {
            url: "items/save" ,
            form: "item_form",
            timeout: 60000,
            handleAs: "json",
            load: function(response)
            {
                alert(response);
            },
            error: function(response)
            {
                alert(response);
            }
        });

}//End of function saveItem

/**
 * Function navigates to the first Item
*/
function firstItem()
{
   dojo.xhrGet(
    {
        url: "items/first",
        handleAs: "json",
        load: function(response)
        {
            var item = dojo.fromJson(response);
            populateItemsControls(item);
        },
        error: function(response)
        {
           alert(response);
        }
    });
}//End of function firstItem

/**
 * Function navigates to the previous Item
 */
function previousItem()
{
   // var position = dojo.cookie("currentitem");

    //if (position == undefined)
  //      position = 0;

  //  position = Math.abs(position);
  //  position--;
    
  // / if (position < 0)
  //  {
  //      var message = dojo.byId("InformationMessage");
  //      message.innerHTML = "You have reached the first item";
  //      dijit.byId("InformationMessageDialog").show();
  //      firstItem();
        
  //      return;
 //   }

    dojo.xhrGet(
    {
        url: "/items/previous",
        handleAs: "json",
        form: "item_form",
        load: function(response)
        {
            var item = dojo.fromJson(response);
            populateItemsControls(item);
        },
        error: function(response)
        {
            alert(response.status);
        }
    });
}//End of function previousItem

/**
 * Function navigates to the next item
 */
function nextItem()
{
//      var position = dojo.cookie("currentitem");
//      var number = dojo.cookie("numberofitems");

//      if (number == undefined)
//        number = 0;
    
//      number = Math.abs(number);
      
//      if (position == undefined)
//          position = 0;

//      position = Math.abs(position);
//      position++;

//      if (position >= number)
//      {
//            var message = dojo.byId("InformationMessage");
//            message.innerHTML = "You have reached the last item";
//            dijit.byId("InformationMessageDialog").show();
//            lastItem();
            
//            return;
//      }
      //alert(dijit.byId("item_id").get("value"));
      //return;

      dojo.xhrGet(
      {
            url: "/items/next",
            handleAs: "json",
            form: "item_form",
            load: function(response)
            {
                var item = dojo.fromJson(response);
                populateItemsControls(item);
            },
            error: function(response)
            {
                alert(response);
            }
        });
}//End of function nextItem

/**
 * Function navigates to the last Item
 */
function lastItem()
{
    dojo.xhrGet(
    {
        url: "items/last",
        handleAs: "json",
        load: function(response)
        {
            var item = dojo.fromJson(response);
            populateItemsControls(item);
        },
        error: function(response)
        {
            alert(response);
        }
    });
}//End of function lastItem

/**
 * Function deletes an Item
 */
function deleteItem()
{
    var itemDialog = dijit.byId("ItemDeleteDialog");
    itemDialog.show();
    return;
    var itemId = dijit.byId("Items.Id").getValue();
    var number = dojo.cookie("numberofitems");
    number = Math.abs(number);
    
    dojo.publish("/saving", [{message: "<font size='2'><b>Deleting...", type: "info", duration: 5000}]);

    dojo.xhrPost(
    {
        url: "servlets/itemManager?operationType=delete&ItemId=" + itemId ,
        timeout: 60000,
        load: function(response)
        {
            dojo.cookie("numberofitems", (number - 1), {expires: 5});
            nextItem();
            itemDialog.hide();
            dojo.publish("/saved", [{message: "<font size='2'><b>...Deleted", type: "info", duration: 5000}]);
        },
        error: function(response)
        {
            dojo.publish("/saved", [{message: "<font size='2'><b>...Failed " + response, type: "error", duration: 5000}]);
        }
    });
}//End of function deleteItem

function findItem()
{
    var keywords = dijit.byId("itemNamekeywords").getValue();
    var grid = dijit.byId("itemSearchGrid");

    keywords = dojo.trim(keywords);
    keywords = keywords.toString();

    if ((keywords.length < 2))
    {
        dojo.byId("ItemSearchResults").innerHTML =
            "<img src='resources/images/dialog-warning.png'> Enter a minimum of two" +
            " letters in the name";
        return;
    } //End of if statement block
    
    var operationType = "find";
    dojo.byId("ItemSearchResults").innerHTML = "<img src='resources/images/loading.gif'>Searching...";

    dojo.xhrGet(
    {
        url: "servlets/itemManager?keywords="+ keywords.toUpperCase() + "&operationType=" + operationType,
        timeout: 50000,
        load: function(response)
        {
            var results = dojo.fromJson(response);
            var size = Math.abs(results.size);
            var itemMessage = (size == 1 ? " item " : " items ");
            dojo.byId("ItemSearchResults").innerHTML = size + itemMessage + "found with the name containing keywords \"" + keywords + "\"";

            var store = new dojo.data.ItemFileWriteStore({data: results});
            grid.setStore(store);
        },
        error: function(response)
        {
            dojo.byId("ItemSearchResults").innerHTML = response;
        }
    });
}//End of function findItem


function navigateToItem(itemId, itemPosition)
{
    dojo.xhrGet(
    {
        url: "servlets/itemManager?operationType=findByPK&itemId="+itemId,
        handleAs: "text",
        load: function(response)
        {
            var item = dojo.fromJson(response);

            populateItemsControls(item, itemPosition);
        },
        error: function(response)
        {
            dojo.publish("/saving", [{message: "<font size='2'><b>...Failed " + response, type: "error", duration: 5000}]);
        }
    });
    
    var searchDialog = dijit.byId("ItemFindDialog");
    searchDialog.hide();
}//End of function navigateToItem




function itemsPrint()
{
    var itemname = dojo.byId("itemName").value;
    var itemContact = dojo.byId("itemContact").value;
    var itemTelephoneNumber = dojo.byId("itemTelephoneNumber").value;
    var itemFaxNumber = dojo.byId("itemFaxNumber").value;
    var itemEmail = dojo.byId("itemEmailAddress").value;
    var itemAddress = dojo.byId("itemAddress").value;
    var itemCity = dojo.byId("itemCity").value;
    var itemCountry = dojo.byId("itemCountry").value;

    window.open('procurement/itemsprint.jsp?name='+itemname + '&contact=' +
        itemContact +'&tel='+ itemTelephoneNumber +'&fax=' + itemFaxNumber +
        '&email=' + itemEmail + '&address='+ itemAddress +
        '&city='+ itemCity +'&country=' + itemCountry,
    '',
    'menubar=no,location=no,scrollbars=yes,resizable=yes,height=550,width=816,statusbar=yes,screenX=100,screenY=100,top=100,left=100');
}//End of function itemsPrint

function populateItemsControls(item)
{

//    if (item.id == "0")
//    {
//        dojo.byId("InformationMessageInformation").innerHTML = "No Items in List"
//        dijit.byId("InformationMessageDialog").show();
//        return;
//    }

    var itemId = dojo.byId("item_id");
    var itemName = dojo.byId("item_name");
    var itemCategory = dijit.byId("item_category");
    var itemUnitMeasurement = dojo.byId("item_unit_measurement");
    var itemNotes = dojo.byId("item_notes");

    itemId.value = item.id;
    itemName.value = item.name;
    itemCategory.set("value", item.category);
    itemUnitMeasurement.value = item.measurement;
    itemNotes.value = item.notes;

//    var navigator = dojo.byId("itemsNavigator");
//    var number = item.size;

//    position = Math.abs(position);
//    number = Math.abs(number);

//    if (position > number)
//    {
//        position = number;
//    }
    
//    navigator.innerHTML = (position + 1) + " of " + (number);
//    dojo.cookie("currentitem", position, {expires: 5});
//    dojo.cookie("numberofitems", number, {expires: 5});
} //End of function populateItemsControls
