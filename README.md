# py-yt-server

A really barebone chrome extension and a python server/worker to send the URL of the currently open Tab to yt-dlp. Multiple downloads are managed in a redis queue. After sending the URL the current tab is closed (you can easily disable this).

It's been at least 6 years since the first version so there might be a way better project by now.

It was never intended to be used by anyone else but me but as I'm trying to get more into developing I thought there might be people who have nice ideas or code recommendations.

I'm using another Docker Image for VPN & HTTP Proxy but this isn't a requirement:
https://hub.docker.com/r/rundqvist/openvpn-tinyproxy

## Requirements
1. You need a valid https endpoint as chrome didn't like unsecure connections.
2. docker-compose
3. ipvanish for my setup. Reconfigure docker-compose network_mode to skip this.

## Usage
Be warned: This isn't user friendly yet. Sorry.

1. Change the https endpoint in chrome-extension/push.js

2. Add the extension to Chrome (there is an option to add th extension dir)

3. Setup docker-compose as the example and your environment.
* If you didn't use build yet, change the `build` option to th path of this repo.
* Set the path of the SSL Certificate & Key in the Server.
* Change the volumes for the DESTINATION_DIR and the archive file. Just comment the archive volume if you don't want to use this.
* Remove network_mode from each container and delete the ipvanish one if not using ipvanish vpn.

4. Build with `docker compose build && docker compose pull && docker compose up -d`

5. Visit any yt-dlp supported website, click on the extension and hope everything works

6. (optional) IF you are using ipvanish and my example, create a 2nd chrome profile, add the extension there, install the extension Proxy Switchy Omega and configure the ipvanish container as HTTP Proxy.

## Not so optimal things...
Everything works BUT not everything is looking good or let's your eyes bleed while reading the code.

1. The Chrome extension... While porting the extension to Manifest V3 i noticed xmlhttp isn't supported anymore but it still works. I couldn't figure out the new push() function and http post yet.

2. The worker is executing the yt-dlp binary and not importing it as a lib. I couldn't figure out a good way to keep the parameter option in the docker compose file. This is a HUGH security risk but as it is hosted only in my home net I didn't care too much.

3. The containers are running in their own network which isn't accessable by my traefik and I didn't know hot to get this running. This would eliminate the need for a ssl cert/key.