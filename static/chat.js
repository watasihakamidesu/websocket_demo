// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

$(document).ready(function() {
    //绑定事件
    $("#messageform").on("submit", function() {
	newMessage($(this));
	return false;
    });
    $("#messageform").on("keypress", function(e) {
	if (e.keyCode == 13) {
	    newMessage($(this));
	    return false;
	}
    });
    $("#message").select();
    updater.start();//建立websocket连接

});

function newMessage(form) {
    var message = form.formToDict();
    //数据序列号成字典发送
    updater.socket.send(JSON.stringify(message));
    //清空发送框并选择
    form.find("#message").val("").select();
}

//表单数据转成字典
jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
	json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
	var url = "ws://" + location.host + "/chatsocket?id="+$("#id").val()+"&name="+$("#name").val();
	updater.socket = new WebSocket(url);
	updater.socket.onmessage = function(event) {
	    updater.showMessage(JSON.parse(event.data));
	}
    },

    showMessage: function(message) {
	//var node = $(message.html);
	$("#inbox").append("<div class='message'>["+message.typename+"]"+ message.name +":"+ message.body +"</div>");
    }
};

//私聊显示名字文本框
$("#type").on("change",function(){
    if($(this).val()=="2")
    {
	$("#user_div").show()
    }
    else{
	$("#user_div").hide()
    }
})
