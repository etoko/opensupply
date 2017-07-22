
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
  <form name="item_category_form", id="item_category_form">
    <table>
     <tr>
       <td><label for="item_category_id">Item Category ID: </label></td>
       <td><div id='item_category_id' name="item_category_id"  style="width: 20%" 
       data-dojo-type="dijit.form.TextBox" readOnly=True></div> </td>
     <tr>
       <td><label for="item_category_name">Item Category: </label></td>
       <td><div id='item_category_name' name="item_category_name"  style="width: 100%"
       data-dojo-type="dijit.form.TextBox"></div> </td>
      </tr>
      <tr>
        <td valign="top"><label for="item_category_notes">Additional Notes: </label></td>
        <td><textarea dojoType="dijit.form.SimpleTextarea" id="item_category_notes" name="item_category_notes" rows="5" cols="90"></textarea></td>
      </tr>
      <tr>
        <td><input type="hidden" name="item_category_operation" id="item_category_operation" /></td>
      </tr>
    </table>
  </form>
</html>
