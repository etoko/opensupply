<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
  <form name="supplier_form", id="supplier_form">
    <table>
     <tr>
       <td>
         <table>
           <tr>
             <td><label for="supplier_id">Supplier ID: </label></td>
             <td><div id='supplier_id' name="supplier_id"  style="width: 20%" 
       data-dojo-type="dijit.form.TextBox" readOnly=True></div> </td>
           </tr>
           <tr>
             <td><label for="supplier_name">Supplier: </label></td>
             <td><div id='supplier_name' name="supplier_name"  style="width: 100%"
       data-dojo-type="dijit.form.TextBox"></div> </td>
           </tr>
           <tr>

                 <td><label for="supplier_email">Email:</label></td>
                 <td><div id="supplier_email" name="supplier_email" data-dojo-type="dijit.form.TextBox" style="width: 100%"></div></td>
           </tr>
           <tr>
             <td colspan=4>
              <table border=0>
                  <tr>
                     <td width="14%"><label for="supplier_tel_1">Tel 1:</label></td>
                     <td><div id="supplier_tel_1" name="supplier_tel_1"  data-dojo-type="dijit.form.TextBox"></div></td>
                     <td><label for="supplier_tel_2">Tel 2:</label></td>
                     <td><div id="supplier_tel_2" name="supplier_tel_2" data-dojo-type="dijit.form.TextBox"></div></td>
                  </tr>
               <tr>
                 <td><label>Fax:</label></td>
                 <td><div id="supplier_fax" name="supplier_fax" data-dojo-type="dijit.form.TextBox"></div></td>
             </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td><label for="supplier_website">Website</label></td>
        <td><div id="supplier_website" name="supplier_website" data-dojo-type="dijit.form.TextBox" style="width:100%"><div>
      </tr>
      <tr>
        <td valign="top"><label for="supplier_address">Address: </label></td>
        <td><textarea dojoType="dijit.form.SimpleTextarea" id="supplier_address" name="supplier_address" rows="3" cols="90"></textarea></td>
      </tr>

      <tr>
        <td valign="top"><label for="supplier_notes">Notes: </label></td>
        <td><textarea dojoType="dijit.form.SimpleTextarea" id="supplier_notes" name="supplier_notes" rows="5" cols="90"></textarea></td>
      </tr>


           </tr>
         </table>
       </td>
     </tr>
     
      <tr>
        <td><input type="hidden" name="supplier_operation" id="supplier_operation" /></td>
      </tr>
    </table>
  </form>
</html>
