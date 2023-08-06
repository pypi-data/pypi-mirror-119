
# Context

RecordKeeper (abbreviated to RK) is aimed at two broad goals:

1. Explaining why something happened in your platform.
   Common example that we want to support is: why event X happened at time T?
   What Models were used? Who trained them, using training data ingested from which
   datasources? It achieves it by creating graph of events.

2. Recreating platform state at that time.

# Basics

RKClient library is used to create events (PEMS) and inform RK about them.

You will need a running RecordKeeper Event Receiver to be able to work with it.

Recommended usage:

```
emitter_id = uuid.UUID('..some static uuid..')
rk_host = os.environ.get('RK_HOST')

rk_client = RKClientFactory.get(rk_host, emitter_id)
```

By using factory, automatically when `RK_MOCK=true` env variable will be defined, 
the returned client will fake the connections and return only success codes. 


## RKClient from Python console

```
cd rkclient/
python3
>>> from rkclient import RKAdmin
>>> rk = RKAdmin('http://127.0.0.1:8082')
>>> pems, msg, ok = rk.get_pems()
>>> assert ok, msg
>>> for pem in pems:
>>>   print(pem)
```

## Releasing package on PIP

### Initial setup

```
pip install twine wheel
```

Register at https://test.pypi.org/account/register/ (or real PIP),
confirm email. Then add to file `~/.pypirc`:

```
[testpypi]
username: MyUsername
```

### Release

1. Adjust version number in `VERSION.txt`
2. Document changes in `releases.txt`
3. Prepare build:
```
make release-prepare
```

4. Upload to test PyPi:
    ```
    make release-test
    ```
It might ask for password. Test that RKClient can be installed ie. 
    ```
    pip install -i https://test.pypi.org/simple/ RecordKeeper-Client==1.1.6 -v
    ```

5. Use `make release` to upload to real PIP. Now client is available at: 
   https://pypi.org/project/RecordKeeper-Client/
    and can be installed with just `pip install RecordKeeper-Client`


---
RKClient is part of ERST Recordkeeper repository.

RKClient is licensed with GNU General Public License version 3 or later,
see LICENSE file for details.

Recordkeeper is ERST's implementation of the Context Cartographer specification.

