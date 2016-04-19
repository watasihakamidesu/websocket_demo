<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<form action="/login" method="post">
<p>name:<input type="text" name="name" id="name" /></p>
<input type="submit" value="Submit" />
 ${ xsrf_form_html() }
</form>
</body>
</html>
