/**
 * Created by jeff on 15/11/28.
 */
window.onload = function() {
    var master = new Master()
    master.init()
}

var Master = function() {
    this.socket = null;
}

Master.prototype = {
    init: function() {
        var master = this
        this.console = document.getElementById('console')

        // connect to server
        this.socket = io.connect()
        this._print("connect to socket server ...")

        this.socket.on('logs', function(msg){
            master._print(msg)
        })
    },

    _print: function(msg){
        var master = this
        msg_to_display = document.createElement('p')
        msg_to_display.innerHTML = msg
        master.console.appendChild(msg_to_display)
        master.console.scrollTop = master.console.scrollHeight;
    }
}