<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
  <form name="department_form", id="department_form">
    <table>
     <tr>
       <td><label for="department_id">Department ID: </label></td>
       <td><div id='department_id' name="department_id"  style="width: 20%" 
       data-dojo-type="dijit.form.TextBox" readOnly=True></div> </td>
     <tr>
       <td><label for="department_name">Department: </label></td>
       <td><div id='department_name' name="department_name"  style="width: 100%"
       data-dojo-type="dijit.form.TextBox"></div> </td>
      </tr>
      <tr>
        <td valign="top"><label for="department_notes">Description: </label></td>
        <td><textarea dojoType="dijit.form.SimpleTextarea" id="department_notes" name="department_description" rows="5" cols="90"></textarea></td>
      </tr>
      <tr>
        <td><input type="hidden" name="department_operation" id="department_operation" /></td>
      </tr>
    </table>
  </form>
</html>
