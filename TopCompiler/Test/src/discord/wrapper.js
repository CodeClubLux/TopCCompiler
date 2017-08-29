var _discord = require("discord.js")

function toTopMessage(message) {
    message.reply = toAsync(message.reply.bind(message))
    //message.server = message.server || "";
    console.log(message.channel.id)
    return message
}

function _discord_client(options) {
    var client = new _discord.Client();
    var lengthOfOn = 2;

    if(options["onReady"]) {
        client.on("ready", toSync(options.onReady))
    }

    if (options["onMessage"]) {
        client.on("message", function(message) {
            options.onMessage(toTopMessage(message), _empty_func)
        })
    }

    client.login = toAsync(client.login.bind(client))

    return client
}