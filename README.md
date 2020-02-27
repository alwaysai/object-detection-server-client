# Object Detection Server/Client
Server app sets up an AlwaysAI model to run on an device where images can be sent and infereneced. The server returns the marked-up image to the client.

Client app shows how to communicate with the server.

## Setup
Deploy the server application to the device and start by using the standard aai commands; aai app deploy and aai app start. Please see docs for more information.
https://alwaysai.co/docs/getting_started/introduction.html

Inside the client side code (Line 56), change the host string to be the IP address of the device running the server. 