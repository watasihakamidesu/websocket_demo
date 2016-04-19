<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Tornado Chat Demo</title>
    <link rel="stylesheet" href="${ static_url("chat.css") }" type="text/css">
  </head>
  <body>
    <div id="body">
      <div id="inbox">
	% for message in messages:
	<div class="message">[${message["typename"]}]
			      ${message["name"]}:
			      ${message["body"]}</div>
	% endfor
  </div>
      <div id="input">
        <form action="/a/message/new" method="post" id="messageform">
	<input type="hidden" value="${id}" id="id" />
	<input type="hidden" value="${name}" id="name" />
          <table>
            <tr>
              <td>
	<select id="type" name="type">
	  <option value="0">所有人</option><!--all-->
	  <option value="1">当前房间</option><!--room-->
	  <option value="2">私聊</option><!--one-->
	</select>
	<div id="user_div" style="float: left; display: none;" >名字:<input type="text" id="user" name="user" ></div>
	<input type="text" name="body" id="message" style="width:500px"></td>
              <td style="padding-left:5px">
                <input type="submit" value="发送">
                <input type="hidden" name="next" value="${ request.path }">
                ${ xsrf_form_html() }
              </td>
            </tr>
          </table>
        </form>
      </div>
    </div>
    <script src="${ static_url("jquery.min.js") }" type="text/javascript"></script>
    <script src="${ static_url("chat.js") }" type="text/javascript"></script>
  </body>
</html>
