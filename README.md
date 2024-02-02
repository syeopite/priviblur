<div align="center"> 
  <h1> Priviblur </h1>
  <blockquote> <h4> Inspired by projects like <a href="https://github.com/iv-org/invidious"> Invidious</a></h4> </blockquote>
  <h3> Priviblur is an alternative frontend to Tumblr with a touch of modern design </h3>
</div>

<br/>

![Example output](./screenshots/example.png)

Priviblur is a proxy. It makes requests to Tumblr in lieu of you allowing you browse without being tracked. 

It has no account requirement either. Allowing you to view your favorite blogs without ever needing to login.

It is lightweight and works without Javascript. Allowing for a much faster experience compared with Tumblr.

It has a modern design. Although perhaps not quite there yet, the project aims to replicate the experience seen on modern software.

It is licensed under the AGPLv3 ensuring that itself and all instances are free and open. Forever. 

## Instances

[A list of public instances can be found here.](./instances.md)

Priviblur has no official instance

## Installation

```bash

git clone "https://github.com/syeopite/priviblur"
cd priviblur 

git checkout "v0.1.0"

python -m venv venv 
source venv/bin/activate

pip install -r requirements.txt

pybabel compile -d locales -D priviblur

python -m src.server

# You can also launch Priviblur through Sanic (our web framework)'s CLI tool
# Prefix any environmental variables with PRIVIBLUR_ instead of SANIC_
# For more information see https://sanic.dev/en/guide/deployment/running.html and related pages
sanic src.server.app  --host 0.0.0.0  --worker <WORKERS>
```

## Configuration

[Example config provided here](./config.example.toml)

## Donate 

Bitcoin (BTC): bc1qas50t647kclvhv4ra4h0zw0kmh8wd9jqt6yk9u

Monero (XMR): 89bn95bwPaqD3t7EDjAKKnYJYPRZDLBym8DV1Spyc4LEaVezknHur7DG5iXxg1e7Jwcr9v8MSFmvj6VvDNARwTcUBeSfB2P
