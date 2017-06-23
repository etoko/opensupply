<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
      xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>IMS</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="pyramid web application" />
  <link rel="stylesheet" href="static/dojo/../dijit/themes/claro/claro.css">

<script>dojoConfig = {parseOnLoad: true}</script>
	<script src='static/dojo/dojo.js'></script>
	
	<script>
require(["dojo/parser", "dijit/form/Form", "dijit/form/Button", "dijit/form/ValidationTextBox", "dojox/validate"]);
	</script>

</head>
<body class="claro">
  <div id="wrap">
    <div id="top-small">
      <div class="top-small align-center">
        <div>
          <img width="220" height="50" alt="Organisation Logo"
           src="static/pyramid.png" />
           ${message}
        </div>
      </div>
    </div>
    <div id="middle">
      <div class="middle align-right">
        <div id="left" class="app-welcome align-left">
          <b>Login</b><br/>
          <span tal:replace="message"/>
        </div>
        <div id="right" class="app-welcome align-right"></div>
      </div>
    </div>
    <div id="bottom">
      <div class="bottom">
        <form action="${url}" method="post">
          <input type="hidden" name="came_from" value="${came_from}"/>
          <input type="text" name="login" value="${login}" data-dojo-type="dijit/form/ValidationTextBox" /><br/>
          <input type="password" name="password" value="${password}"
           data-dojo-type="dijit/form/ValidationTextBox"/><br/>
          <input data-dojo-type="dijit/form/Button" type="submit" name="form.submitted" value="Log In"/>
        </form>
      </div>
    </div>
  </div>
  <div id="footer">
    <div class="footer"
         >&copy; 2012, XYZ Organisation</div>
  </div>


</body>
</html>


