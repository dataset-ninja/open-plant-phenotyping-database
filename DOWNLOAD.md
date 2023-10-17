Dataset **OPPD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/7/E/dt/hOS2Sv09cr1CWojMPCG1H8PuTda4QD42YWAAJAs6RuEz1yKHsuIjsPeG1gkTIFZUiHrXJPeVFPH65kQSltBqyL1yPW3eeiUbvuAzL8EKwnV0yIHrS9rLDhOQ1ZxK.tar)

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