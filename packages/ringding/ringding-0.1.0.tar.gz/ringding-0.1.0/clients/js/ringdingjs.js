let _w3cWebSocket;
try {
    // Browser
    _w3cWebSocket = WebSocket
} catch (e) {
    // NodeJs
    _w3cWebSocket = require('websocket').w3cwebsocket;
}


MESSAGE_TYPE_ONESHOT = 0
MESSAGE_TYPE_REQUEST = 1
MESSAGE_TYPE_RESPONSE = 2
MESSAGE_TYPE_ERROR = 3
MESSAGE_TYPE_BROADCAST = 4


class _ringdingjs {

    /**
     * Connect to the backend. This is the first function you want to call. You want
     * to call it as least as possible, so ideally (for single page applications) one
     * time during the app initialization.
     * Can be awaited to continue after the connection has been established.
     * @param ws_url - URL for WebSocket backend, e.g. "ws://localhost:8001" or "wss://server.com:8001".
     * @param message_handler - Optional: A message handler that you can provide, e.g. for debugging. Will log the network communication.
     * @returns {Promise<null>}
     */
    connect = (ws_url, message_handler) => {
        if (message_handler) {
            this._logger = message_handler
        }
        this.ws_url = ws_url || this.ws_url
        this._logger('Connecting to ' + this.ws_url + '...')
        let resolver_function;
        let error_function;
        const promise = new Promise((resolve, reject) => {
            resolver_function = resolve;
            error_function = reject;
        })
        this._pending_events['wsopen'] = {resolver_function, error_function}
        this.ws = new this._wsBase(this.ws_url)
        this.ws.onopen = this._on_connect
        this.ws.onmessage = this._on_message
        this.ws.onerror = this._on_error
        this.ws.onclose = this._on_close
        return promise
    }

    /**
     * Disconnect from the server. Resets ringding.
     * Can be awaited to continue once cleanup is done.
     * @returns {Promise<null>}
     */
    disconnect = () => {
        let resolver_function;
        let error_function;
        const promise = new Promise((resolve, reject) => {
            resolver_function = resolve;
            error_function = reject;
        })
        this._pending_events['wsclose'] = {resolver_function, error_function}
        this.ws.close()
        return promise
    }

    /**
     * Call a function on the backend and retrieve its return value.
     * @param cmd - The command string e.g. "MyApi.sum(*)"
     * @param parameters - The keyword arguments as dict.
     * @returns {Promise<any>} - Will return a promise that will contain the return value of the called function once resolved.
     */
    call = (cmd, parameters) => {
        let rdtrace = cmd.__rdtrace__;
        if (rdtrace !== undefined) {
            cmd = rdtrace[0].join('.')
            parameters = rdtrace[1]
        }
        const message = {
            cmd,
            type: MESSAGE_TYPE_REQUEST,
            id: this._get_id()
        }
        if (!parameters || Object.keys(parameters).length > 0) {
            message.param = parameters
        }
        let resolver_function;
        let reject_function;
        const promise = new Promise((resolve, reject) => {
            resolver_function = resolve;
            reject_function = reject;
        })
        this._pending_events[message.id] = [resolver_function, reject_function]
        this._logger(">>> " + JSON.stringify(message))
        this.ws.send(JSON.stringify(message))
        return promise
    }

    /**
     * Call a function on the server. This does not give you any feedback on whether the call was successful or not.
     * @param cmd - The command string to call, e.g. "MyApi.sum(*)"
     * @param [parameters] - The keyword arguments as dict.
     */
    notify = (cmd, parameters) => {
        let rdtrace = cmd.__rdtrace__;
        if (rdtrace !== undefined) {
            cmd = rdtrace[0].join('.')
            parameters = rdtrace[1]
        }
        const message = {
            cmd,
            type: MESSAGE_TYPE_ONESHOT,
        }
        if (!parameters || Object.keys(parameters).length > 0) {
            message.param = parameters
        }
        this._logger(">>> " + JSON.stringify(message))
        this.ws.send(JSON.stringify(message))
    }

    constructor() {
        this._set_defaults()
    }

    /** Extract the initialization into a separate method to make the cleanup after
     * closing the socket easier.
     * @private
     */
    _set_defaults = () => {
        this.ws = null
        this.ws_url = 'ws://localhost:36097'
        this._wsBase = _w3cWebSocket
        this._logger = this._empty_logger
        this._pending_events = {}
        this._next_id = 0
    }

    /**
     * This obviously doesn't log anything but is used as a dummy method that is called
     * during logging.
     * @private
     */
    _empty_logger = () => {
    }

    /**
     * Return an ID unique in this session. Used to identify messages.
     * @returns number
     * @private
     */
    _get_id = () => {
        const next_id = this._next_id + 1
        this._next_id = next_id
        return next_id
    }

    _on_connect = () => {
        const resolver_function = this._pending_events['wsopen'].resolver_function
        delete this._pending_events['wsopen']
        resolver_function()
    }

    _on_error = (error) => {
        this._logger('Could not connect, an error occured: ', error)
        this._pending_events['wsopen'].error_function()
        delete this._pending_events['wsopen']
        setTimeout(this.connect, 3000)
    }

    _on_message = (messageEvent) => {
        this._logger('<<< ' + messageEvent.data)
        const message = JSON.parse(messageEvent.data)
        var [resolve, reject] = this._pending_events[message.id]
        if (message.type === MESSAGE_TYPE_ERROR) {
            reject(message.error)
        } else if (resolve) {
            resolve(message.data)
        }
    }

    _on_close = () => {
        const resolver_function = this._pending_events['wsclose'].resolver_function
        delete this._pending_events['wsclose']
        this._set_defaults()
        resolver_function()
    }
}


function _empty_function() {
}

/**
 * This function will return an ApiProxy which is an object that emulates API calls.
 * It "remembers" the chain of the attributes that has been accessed and fires an actual
 * API call when the final method is called.
 * It has to be wrapped in an own function to make it possible that each CallApi() returns
 * an independent ApiProxy that does not interfear with others.
 * @private
 */
function _get_api_proxy() {
    const access_list = []
    const _ApiProxy = {
        get: function (target, prop) {
            access_list.push(prop)
            return new Proxy(_empty_function, _ApiProxy)
        },
        apply: function (target, thisarg, argumentslist) {
            let command = access_list.join('.')
            let parameters = {}
            if (argumentslist.length > 0) {
                command += '(*)'
                parameters = argumentslist[0]
            } else {
                command += '()'
            }
            return RD.call(command, parameters)
        },
        has: function () {
            return true
        }
    }
    return _ApiProxy
}


// For Browser
const RD = new _ringdingjs()
const CallApi = function () {
    return new Proxy(_empty_function, _get_api_proxy())
}

// For NodeJS
try {
    module.exports = {
        RD: RD,
        CallApi: CallApi
    }
} catch (error) {
    // No NodeJS environment (e.g. Browser environment)
}
