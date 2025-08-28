# echo.rslv.xyz

A reflector site, returning the request as JSON, excluding the body.

Deployed at echo.rslv.xyz

Example:

```shell
$ curl "https://echo.rslv.xyz/some/fake/path?and=query&foo=bar"
{
  "url": "https://echo.rslv.xyz/some/fake/path?and=query&foo=bar", 
  "method": "GET", 
  "path": "some/fake/path", 
  "query": {
    "and": "query", 
    "foo": "bar"
  }, 
  "headers": {
    "accept": "*/*", 
    "forwarded": "for=24.126.83.201;host=echo.rslv.xyz;proto=https;sig=0QmVhcmVyIGM3YTdjZTlmOWYyZmMzNWYzOTBiNjExNTkzZjA2MGU2OGFhZDY4NzgxYzczZTdlODUxMTI1NzE4NWQyMTA1OWM=;exp=1711976059", 
    "host": "echo.rslv.xyz", 
    "user-agent": "curl/8.4.0", 
    "x-forwarded-for": "24.126.83.201", 
    "x-forwarded-host": "echo.rslv.xyz", 
    "x-forwarded-proto": "https", 
    "x-real-ip": "24.126.83.201"
  }
}
```

Run locally:

```
git clone https://github.com/datadavev/echo.rslv.xyz.git
cd echo.rslv.xyz
uv run python -m echo
```

Deploy on Vercel:

```
vercel --prod
```

# Simple K8s Deployment for Echo Service

## Deployment

The container will crash/restart unless it finds the application files mounted in `/app/` -- see [First Time Setup](#first-time-setup), below. 
Once that's done, deploy with:

```shell
kubectl apply -f deploy.yaml
```
Uninstall with:

```shell
kubectl delete -f deploy.yaml
```

## First Time Setup

The container will crash and restart unless it finds the application files mounted in `/app/`. Therefore, the first time you run this, you have to add an infinite loop in the command, so the pod keeps running.

To do so, temporarily change from:
```yaml
      args:
        - pip install --no-cache-dir -r requirements.txt uvicorn &&
          python -m uvicorn echo.fapi:app --host 0.0.0.0 --port 80
```
...to:
```yaml
      args:
        - while true; do sleep 500; done; pip install --no-cache-dir -r requirements.txt uvicorn &&
          python -m uvicorn echo.fapi:app --host 0.0.0.0 --port 80
```
...and while editing the file, set the correct `host` in the `ingress` spec (currently set to `metacat-dev.test.dataone.org`)

Then deploy:
```shell
kubectl apply -f deploy.yaml
```
Tar up the source files from https://github.com/datadavev/echo.rslv.xyz and `kubectl cp` the tarball into the pod at `/app/`.

In a shell inside the pod, Untar the files and move them all to the top level inside `/app/`; i.e.:
```shell
/app/
├── echo
│   ├── __init__.py
│   ├── __main__.py
│   └── fapi.py
├── LICENSE
├── pyproject.toml
├── README.md
├── requirements.txt
├── uv.lock
└── vercel.json
```

Finally, remove the `while true; do sleep 500; done;` from the command above, and redeploy