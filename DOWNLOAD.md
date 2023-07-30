Dataset **OPPD** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/F/x/H3/gh3LhNG7E4kFgBDGeDXWnkR0lao32XDBSwE8gx77W6E5qBeTAL7kD8IQz3gIa7MEzCJsSMUKnY9PR2O47itqesoaeWTaiIL2giBlbVMe7wF7sOn81EFjlcXiGljo.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='OPPD', dst_path='~/dtools/datasets/OPPD.tar')
```
The data in original format can be 🔗[downloaded here](https://gitlab.au.dk/AUENG-Vision/OPPD)