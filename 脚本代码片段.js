(function () {
    'use strict';
    function sek_start() {
        function guid() {
            function S4() {
                return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
            }

            return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
        }

     //创建webSocket 连接
        
        var client = new SekiroClientTest("wss://${your_server_ip}/business-demo/register?group=xiaolanben&clientId=" + guid());
        //注册一个行动监听
        client.registerAction("sign", function (request, resolve, reject) {
            try {
                var method = request['method'];
                var _url = request['url'];
                var url = _url.replace(/-/g, '+').replace(/_/g, '/');
                console.log(_url,url);
                
                var _signData = {
                 "url":window.atob(url),
                  "method":method
                };
                console.log(_signData);
                
                var signData = window.sign(_signData).url; // 记得导出为全局函数
                
                var result=JSON.stringify(signData)
                console.log(result)
                resolve(result)
            } catch (e) {
                reject("error: " + e);
            }
        });
        
    }

    console.log("超时连接")
    setTimeout(sek_start, 2000)


//==============================================================================================================================================//
// 连接配置函数, 不许修改
    function SekiroClientTest(e) {
        if (this.wsURL = e, this.handlers = {}, this.socket = {}, !e) throw new Error("wsURL can not be empty!!");
        this.webSocketFactory = this.resolveWebSocketFactory(), this.connect()
    }

    SekiroClientTest.prototype.resolveWebSocketFactory = function () {
        if ("object" == typeof window) {
            var e = window.WebSocket ? window.WebSocket : window.MozWebSocket;
            return function (o) {
                function t(o) {
                    this.mSocket = new e(o)
                }

                return t.prototype.close = function () {
                    this.mSocket.close()
                }, t.prototype.onmessage = function (e) {
                    this.mSocket.onmessage = e
                }, t.prototype.onopen = function (e) {
                    this.mSocket.onopen = e
                }, t.prototype.onclose = function (e) {
                    this.mSocket.onclose = e
                }, t.prototype.send = function (e) {
                    this.mSocket.send(e)
                }, new t(o)
            }
        }
        if ("object" == typeof weex) try {
            console.log("test webSocket for weex");
            var o = weex.requireModule("webSocket");
            return console.log("find webSocket for weex:" + o), function (e) {
                try {
                    o.close()
                } catch (e) {
                }
                return o.WebSocket(e, ""), o
            }
        } catch (e) {
            console.log(e)
        }
        if ("object" == typeof WebSocket) return function (o) {
            return new e(o)
        };
        throw new Error("the js environment do not support websocket")
    }, SekiroClientTest.prototype.connect = function () {
        console.log("sekiro: begin of connect to wsURL: " + this.wsURL);
        var e = this;
        try {
            this.socket = this.webSocketFactory(this.wsURL)
        } catch (o) {
            return console.log("sekiro: create connection failed,reconnect after 2s:" + o), void setTimeout(function () {
                e.connect()
            }, 2e3)
        }
        this.socket.onmessage(function (o) {
            e.handleSekiroRequest(o.data)
        }), this.socket.onopen(function (e) {
            console.log("sekiro: open a sekiro client connection")
        }), this.socket.onclose(function (o) {
            console.log("sekiro: disconnected ,reconnection after 2s"), setTimeout(function () {
                e.connect()
            }, 2e3)
        })
    }, SekiroClientTest.prototype.handleSekiroRequest = function (e) {
        console.log("receive sekiro request: " + e);
        var o = JSON.parse(e), t = o.__sekiro_seq__;
        if (o.action) {
            var n = o.action;
            if (this.handlers[n]) {
                var s = this.handlers[n], i = this;
                try {
                    s(o, function (e) {
                        try {
                            i.sendSuccess(t, e)
                        } catch (e) {
                            i.sendFailed(t, "e:" + e)
                        }
                    }, function (e) {
                        i.sendFailed(t, e)
                    })
                } catch (e) {
                    console.log("error: " + e), i.sendFailed(t, ":" + e)
                }
            } else this.sendFailed(t, "no action handler: " + n + " defined")
        } else this.sendFailed(t, "need request param {action}")
    }, SekiroClientTest.prototype.sendSuccess = function (e, o) {
        var t;
        if ("string" == typeof o) try {
            t = JSON.parse(o)
        } catch (e) {
            (t = {}).data = o
        } else "object" == typeof o ? t = o : (t = {}).data = o;
        (Array.isArray(t) || "string" == typeof t) && (t = {
            data: t,
            code: 0
        }), t.code ? t.code = 0 : (t.status, t.status = 0), t.__sekiro_seq__ = e;
        var n = JSON.stringify(t);
        console.log("response :" + n), this.socket.send(n)
    }, SekiroClientTest.prototype.sendFailed = function (e, o) {
        "string" != typeof o && (o = JSON.stringify(o));
        var t = {};
        t.message = o, t.status = -1, t.__sekiro_seq__ = e;
        var n = JSON.stringify(t);
        console.log("sekiro: response :" + n), this.socket.send(n)
    }, SekiroClientTest.prototype.registerAction = function (e, o) {
        if ("string" != typeof e) throw new Error("an action must be string");
        if ("function" != typeof o) throw new Error("a handler must be function");
        return console.log("sekiro: register action: " + e), this.handlers[e] = o, this
    };
})();

