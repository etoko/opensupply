<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
  <form name="department_form", id="department_form">
    <table>
     <tr>
       <td><label for="department_name">Department: </label></td>
       <td><div id='department_name' name="department_name" 
       data-dojo-type="dijit.form.TextBox"></div> </td>
      </tr>
      <tr>
        <td valign="top"><label for="department_description">Description: </label></td>
        <td><textarea dojoType="dijit.form.SimpleTextarea" id="department_description" name="department_description" rows="5", cols="50"></textarea></td>
      </tr>
    </table>
  </form>
</html>
