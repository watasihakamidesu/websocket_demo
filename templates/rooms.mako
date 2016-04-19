<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
<script type="text/javascript" src="${ static_url("jquery.min.js") }" ></script>
<style type"text/css">
.distance{
margin:10px
}
</style>
<script type="text/javascript">
$(document).ready(function(){
var i=1;
do{
$("body").append("<a href='/?id="+i+"' class='distance' >房间"+i+"</a>");
i++;
}while(i<${num}+1)
})
</script>
</head>
<body>
</body>
</html>
