# Object Detection Server/Client
Server app sets up an alwaysAI model to run on a device where images can be sent and inferenced. The server then returns the marked-up image to the client, which is stored in the `inferenced` folder.

Client app shows how to communicate with the server.

## Setup
This app requires an alwaysAI account. Head to the [Sign up page](https://www.alwaysai.co/dashboard) if you don't have an account yet. Follow the instructions to install the alwaysAI toolchain on your development machine.

Next, create an empty project to be used with this app. When you clone this repo, you can run `aai app configure` within the repo directory and your new project will appear in the list.

## Usage

## Setup
Once you have the alwaysAI tools installed and the new project created, run the following CLI commands at the top level of the `server` repo:

To set the project, and select the target device run:

```
aai app configure
```

To build your app and install on the target device:

```
aai app install
```

To start the app:

```
aai app start
```

Inside the client side code (Line 56), change the host string to be the IP address of the device running the server. Add images to be inferenced in the `images` directory. Currently, it is only handling .jpg format. Then cd into the `client` repo and repeat the steps outlined above to start the client application. You will see the inferenced images appear in the `inferenced` folder.

## Troubleshoot
Please post questions and comments on your community discord channel!
https://discord.gg/R2uM36U
