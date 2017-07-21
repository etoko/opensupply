/*
 *Script handles all operations of the items page such as navigation, adding new
 *items entities and so on
 **/
function newSupplier()
{
    var supplier_id = dojo.byId("supplier_id");
    var supplier_name = dojo.byId("supplier_name");
    var supplier_te1_1 = dojo.byId("supplier_tel_1");
    var supplier_te1_2 = dojo.byId("supplier_tel_2");
    var supplier_fax = dojo.byId("supplier_fax");
    var supplier_email = dojo.byId("supplier_email");
    var supplier_address = dojo.byId("supplier_address");
    var supplier_notes = dojo.byId("supplier_notes");

    supplier_id.value = -1;
    supplier_name.value = "";
    supplier_fax.value = "";
    supplier_email.value = "";
    supplier_address.value = "";
    
    dojo.publish("/saving", [{message: "<font size='2'><b>Enter new Supplier",
        type: "info", duration: 15000}]);
}//End of function newSupplier

/**
* function persists or mergers an entity
*/
function saveSupplier()
{
        dojo.xhrPost(
        {
            url: "/supplier/save",
            form: "supplier_form" ,
            //putData: dojo.formToJson("supplier_form"),
            //handleAs: "json",
            load: function(response)
            {
                alert(dojo.byId("supplier_operation").value);
        
                status_message_display("busy", "Creating Supplier...")
            },
            error: function(response)
            {
                dojo.publish("/saved",[{message: "<font size='2'><b>...Failed", type: "error", duration: 5000}]);
            }
        });
}

/**
 *Function navigates to
 the first supplier entity
 */
function firstSupplier()
{
    //The parameters to pass to xhrGet, the url, how to handle it, and the callbacks.
    dojo.xhrGet(
    {
        url: "/supplier/first",
        handleAs: "text",
        load: function(response)
        {
            var supplier = dojo.fromJson(response);
            
            populateSupplierControls(supplier);
        },
        error: function(response)
        {
            dojo.publish("/saved",[{message: "<font size='2'><b>...Failed<br>" + response, type: "error", duration: 5000}]);
        }
    });
}//End of function firstSupplier

/**
 * Function navigates to the previous supplier entity
 */
function previousSupplier()
{
    var position = dojo.cookie("CurrentSupplier");

    if (position == undefined)
    {
        position = 0;
    }

    position = Math.abs(position);

    if (position < 0)
    {
        position = 0;
    }

    if (position == 0)
    {
        dojo.byId("NavigationInformation").innerHTML =
            "You have reached the first supplier in the list";
        dijit.byId("NavigationDialog").show();
        firstSupplier();
        return;
    }

    position = position - 1;
    
    //The parameters to pass to xhrGet, the url, how to handle it, and the callbacks.
    dojo.xhrGet(
    {
        url: "servlets/supplierManager?operationType=previous&position=" + position,
        handleAs: "text",
        load: function(response)
        {
            var supplier = dojo.fromJson(response);
            populateSupplierControls(supplier, position);
        },
        error: function(response)
        {
            dojo.publish("/saved",[{message: "<font size='2'><b>...Failed<br>" + response, type: "error", duration: 5000}]);
        }
    });
}//End of function previousSupplier

/**
 *Function navigates to the next Supplier
 */
function nextSupplier()
{
    var position = dojo.cookie("CurrentSupplier");
    
    var supplierNumber = dojo.cookie("SupplierNumber");
    
    if (position == undefined)
    {
        position = 0;
    }

    position = Math.abs(position);
    supplierNumber = Math.abs(supplierNumber);
    
    if (position < 0)
    {
        position = 0;
    }

    position = position + 1;

    if (position >= supplierNumber)
    {
        dojo.byId("NavigationInformation").innerHTML =
            "You have reached the last supplier in the list";
        dijit.byId("NavigationDialog").show();
        lastSupplier();
        return;
    }
    
    //The parameters to pass to xhrGet, the url, how to handle it, and the callbacks.
    dojo.xhrGet(
    {
        url: "servlets/supplierManager?operationType=next&position=" + position,
        handleAs: "text",
        load: function(response)
        {
            var supplier = dojo.fromJson(response);
            populateSupplierControls(supplier, position);
        },
        error: function(response)
        {
            dojo.publish("/saved",[{message: "<font size='2'><b>...Failed<br>" + response, type: "error", duration: 5000}]);
        }
    });
}//End of function nextSupplier

function lastSupplier()
{
    var supplierSize = dojo.cookie("SupplierNumber");
    var position = (Math.abs(supplierSize) - 1);

    //The parameters to pass to xhrGet, the url, how to handle it, and the callbacks.
       dojo.xhrGet(
        {
            url: "servlets/supplierManager?operationType=last",
            handleAs: "text",
            load: function(response)
            {
                var supplier = dojo.fromJson(response);
                populateSupplierControls(supplier, position);
            },
            error: function(response)
            {
                dojo.publish("/saved",[{message: "<font size='2'><b>...Failed<br>" + response, type: "error", duration: 5000}]);
            }
        });
}//End of function lastSupplier

/**
 * Function to delete a supplier entity
 */
function deleteSupplier()
{
    var supplierDialog = dijit.byId("SupplierDeleteDialog");
    var supplierId = dijit.byId("Supplier.Id").getValue();
    
    dojo.publish("/saving",[{message: "<font size='2'><b>Deleting...<b>", type: "info", duration: 3000}]);

    dojo.xhrPost(
    {
        url: "servlets/supplierManager?operationType=delete&supplierId=" + supplierId ,
        timeout: 30000,
        load: function()
        {
            dojo.publish("/saved",[{message: "<font size='2'><b>...Deleted<b>", type: "info", duration: 5000}]);
            supplierDialog.hide();
            nextSupplier();
        },
        error: function(response)
        {
            dojo.publish("/saved",[{message: "<font size='2'><b>...Failed<br>" + response, type: "error", duration: 5000}]);
        }
    });
}//End of function deleteSupplier

/**
 *Function to search and return details of a supplier entity
 */
function findSupplier()
{
    var formToValidate = dijit.byId("Suppliers.FindDialogForm");

    if (formToValidate.validate())
    {
        var keywords = dijit.byId("supplierkeywords").getValue();

        keywords = dojo.trim(keywords);

        if (keywords.toString().length < 2)
        {
            dojo.byId("SupplierSearchResults").innerHTML = "<img src='resources/images/dialog-warning.png'> Enter a minimum of two" +
                " letters in the name";
            return;
        }

        var operationType = "find";
        var grid = dijit.byId("supplierSearchGrid");

        dojo.byId("SupplierSearchResults").innerHTML = "<img src='resources/images/loading.gif'>Searching...";

        dojo.xhrGet(
        {
            url: "servlets/supplierManager?keywords="+ keywords.toUpperCase() + "&operationType=" + operationType,
            load: function(response)
            {
                var results = dojo.fromJson(response);
                var size = Math.abs(results.size);
                var itemMessage = (size == 1 ? " supplier " : " suppliers ");

                dojo.byId("SupplierSearchResults").innerHTML = size + itemMessage + "found with the name containing keywords \"" + keywords + "\"";
                var store = new dojo.data.ItemFileWriteStore({data: results});
                grid.setStore(store);
            },
            error: function(response)
            {
                dojo.publish("/saved",[{message: "<font size='2'><b>...Failed<br>" + response, type: "error", duration: 5000}]);
            }
        });
    } //End of if statement block
}//End of function findSupplier

/**
 *Function navigates to a supplier with the supplierID specified by supplierID
*/
function navigateToSupplier(supplierId, supplierPosition)
{
    var position = supplierPosition;
    dojo.xhrGet(
    {
        url: "servlets/supplierManager?operationType=findByPK&supplierId="+supplierId,
        handleAs: "text",
        load: function(response)
        {
            var supplier = dojo.fromJson(response);
            populateSupplierControls(supplier, position)
            dojo.cookie("CurrentSupplier", supplierPosition, {expires: 5});
        },
        error: function(response)
        {
            dojo.publish("/saved",[{message: "<font size='2'><b>...Failed<br>" + response, type: "error", duration: 5000}]);
        }
    });

    dijit.byId("SuppliersFindDialog").hide();
}//End of method navigateToSupplier

/**
 * Function refreshes a suppliers details
 */
function refreshSupplier()
{
    var supplierId = dijit.byId("Supplier.Id").getValue();
    
    if ((supplierId == 0) || (supplierId.toString() == "NaN") )
    {
        var message = dojo.byId("InformationMessage");
        message.innerHTML = "You can only refresh a viewable supplier";
        dijit.byId("InformationMessageDialog").show();
        return;
    }

    var position = dojo.cookie("CurrentSupplier");
    position = Math.abs(position);

    dojo.xhrGet(
    {
        url: "servlets/supplierManager?operationType=get&output=JSON&supplierId=" + supplierId,
        load: function(response)
        {
            var supplier = dojo.fromJson(response);
            populateSupplierControls(supplier, position);
        },
        error: function(response)
        {
            dojo.publish("/saving", [{message: "<font size='2'><b>Experienced an unexpected problem: " + response,
                type: "error", duration: 5000}]);
        }
    });
} //ENd of function refreshSupplier

/**
 * Function displays the print dialog for the supplier tab.
 */
function suppliersPrint()
{
    var suppliername = dojo.byId("supplierName").value;
    var supplierContact = dojo.byId("supplierContact").value;
    var supplierTelephoneNumber = dojo.byId("supplierTelephoneNumber").value;
    var supplierFaxNumber = dojo.byId("supplierFaxNumber").value;
    var supplierEmail = dojo.byId("supplierEmailAddress").value;
    var supplierAddress = dojo.byId("supplierAddress").value;
    var supplierCity = dojo.byId("supplierCity").value;
    var supplierCountry = dojo.byId("supplierCountry").value;

    window.open('procurement/suppliersprint.jsp?name='+suppliername + '&contact=' +
        supplierContact +'&tel='+ supplierTelephoneNumber +'&fax=' + supplierFaxNumber +
        '&email=' + supplierEmail + '&address='+ supplierAddress +
        '&city='+ supplierCity +'&country=' + supplierCountry,
    '',
    'menubar=no,location=no,scrollbars=yes,resizable=yes,height=550,width=816,statusbar=yes,screenX=100,screenY=100,top=100,left=100');
}

/**
 * Function populates supplier controls
 */
function populateSupplierControls(supplier, position)
{

    var supplier_id = dijit.byId("supplier_id");
    var supplier_name = dijit.byId("supplier_name");
    var supplier_te1_1 = dijit.byId("supplier_tel_1");
    var supplier_te1_2 = dijit.byId("supplier_tel_2");
    var supplier_fax = dijit.byId("supplier_fax");
    var supplier_email = dijit.byId("supplier_email");
    var supplier_address = dijit.byId("supplier_address");
    var supplier_notes = dijit.byId("supplier_notes");

    if ((supplier.supplierId).toString() == "0")
    {
        var message = dojo.byId("InformationMessage");
        message.innerHTML = "There are no suppliers!";
        dijit.byId("InformationMessageDialog").show();

        return;
    }

    supplier_id.setValue(supplier.id);
    supplier_name.setValue(supplier.name);
    supplier_tel_1.setValue(supplier.tel_1);
    supplier_tel_2.setValue(supplier.tel_2);
    supplier_fax.setValue(supplier.fax);
    supplier_email.value(supplier.email);
    supplier_address.setValue(supplier.address);
    supplier_notes.setValue(supplier.notes)


//    var bank = supplier.bank;

  //  if (bank.toString() !== "NaN")
//    {
//        bankingB.hidden = true;
        

//        bankInfoId.innerHTML = supplier.bankingInfoId;

//        var branch = supplier.branch;
//        var accountId = supplier.accountId;
//        var accountName = supplier.accountName;

//        var banking = "<table cellspacing='5' border='0' width=\"100%\">" +
//            "<tr><td colspan='2' style='border-bottom: 1px solid silver;'><h1>Banking Info </h1></td></tr>" +
//            "<tr><td style=\"width: 22%\"><b>Bank:</b></td><td><span id='Supplier.BankValue'>" + bank + "</span></td></tr>" +
//            "<tr><td><b>Branch:</b></td><td><span id='Supplier.BranchValue'>" + branch + "</span></td></tr>" +
//            "<tr><td><b>Account #:</b></td><td><span id='Supplier.AccountIdValue'>" + accountId + "</span></td></tr>" +
//            "<tr><td><b>Account Name:</b></td><td><span id='Supplier.AccountNameValue'>" + accountName + "</span></td></tr>";
//
//        bankInfo.innerHTML = banking;
//        bankingButton.innerHTML =
//            "<a href='javascript:showAccountDialog(true)'>" +
//                "<img src='resources/images/floppy.png' height='18'/> Update Bank Info" +
//            "</a>" + " &nbsp;&nbsp;&nbsp;" +
//            "<a href='javascript:deleteSupplierBankInfo(true)'>" +
//                "<img src='resources/images/cancel.png' /> Delete Bank Info" +
//            "</a>";
//    }
//    else
//    {
//        bankingB.hidden = false;
//        
//        bankInfo.innerHTML = "";
//        bankingButton.innerHTML =
//            "<a href='javascript:showAccountDialog(false)'>" +
//                "<img src='resources/images/list-add.png'/> Add Bank Info" +
//            "</a>"
//    }

//    var size = supplier.size;

//    dojo.cookie("SupplierNumber", size, {expires: 5});
//    dojo.cookie("CurrentSupplier", position, {expires: 5});
    
//    position = Math.abs(position);
//    position = position + 1;
//    size = Math.abs(size);

//    if (position > size)
//        position = size;
    
//    navigator.innerHTML = position + " of " + size;
} //End of function populateSupplierControls

