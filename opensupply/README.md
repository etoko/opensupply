openSupply
===

This is the primary codebase that runs the supply chain management system

TODO
Notifications of new pending items such as new requisition requiring approval

Notifications should appear like those of emails.

When user logs into system, User should be shown page containing only pending items

Pending items (that require the approval of the individual) should appear as a list on the left page below the Reports section. This should open a page that shows portlets for each group of item requiring approval e.g. one portlet for stores requisition, another for stores requisitions.

Requisitions:

-Allow users to make requisitions. Users will enter specs of requisition and upload requisition document
-Allow requisition to be saved (pdf)
- Items: Allow items to provide for many specifications for example a computer or tractor:[22/07/2017]
   -Consider a dojo datagrid
   -Add these components into an item_details table with the following columns: id, item_id, component, required specification.
-When generating RFQ this should come out as a table with alternating colours (perhaps gray)
-Items: Create unit of measurement page for entering units of measurement
-RFQ: system should generate RFQ and export to pdf
-RFQ: System design should also consider ability to receive and record RFQ
-Procurement Process: consider if system can handle a procurement process i.e. evaluation stage, contracts committee stage
