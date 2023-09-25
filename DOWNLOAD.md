Dataset **OPPD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/H/B/4x/jNIu4fm0gmWlr2MkjlBw301AFPvvC2Cthbss5JtO7IvCnL8xBt0FKjFebnoWej3gVFkg7I5K2FoHvUqZygxkbMUFFasPNaE3yXSqVhFwEIY3gF41H27veBXg3jPW.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='OPPD', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://gitlab.au.dk/AUENG-Vision/OPPD).