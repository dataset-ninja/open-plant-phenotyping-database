# https://vision.eng.au.dk/open-plant-phenotyping-database/

import json
import os

import gdown
import numpy as np
import supervisely as sly
import tqdm
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    list_files_recursively,
)

import src.settings as s

# def download_dataset():
#     archive_path = os.path.join(sly.app.get_data_dir(), "OPPD-master.zip")

#     if not os.path.exists(archive_path):
#         if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
#             gdown.download(s.DOWNLOAD_ORIGINAL_URL, archive_path, quiet=False)
#         if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
#             for name, url in s.DOWNLOAD_ORIGINAL_URL:
#                 gdown.download(url, os.path.join(archive_path, name), quiet=False)
#     else:
#         sly.logger.info(f"Path '{archive_path}' already exists.")
#     return unpack_if_archive(archive_path)


eppo_2_human_name = {
    "ALOMY": ["Alopecurus myosuroides", "Blackgrass"],
    "ANGAR": ["Anagallis arvensis", "Scarlet pimpernel"],
    "APESV": ["Apera spica-venti", "Loose silky-bent"],
    "ARTVU": ["Artemisia vulgaris", "Common mugwort"],
    "AVEFA": ["Avena fatua", "Common wild oat"],
    "BROST": ["Bromus sterilis", "Barren brome"],
    "BRSNN": ["Brassica napus", "Rapeseed"],
    "CAPBP": ["Capsella bursa-pastoris", "Shepherd's purse"],
    "CENCY": ["Cyanus segetum", "Cornflower"],
    "CHEAL": ["Chenopodium album", "Fat-hen"],
    "CHYSE": ["Glebionis segetum", "Corn marigold"],
    "CIRAR": ["Cirsium arvense", "Creeping thistle"],
    "CONAR": ["Convolvulus arvensis", "Field bindweed"],
    "EPHHE": ["Euphorbia helioscopia", "Umbrella milkweed"],
    "EPHPE": ["Euphorbia peplus", "Stinging milkweed"],
    "EROCI": ["Erodium cicutarium", "Common stork's-bill"],
    "FUMOF": ["Fumaria officinalis", "Common fumitory"],
    "GALAP": ["Galium aparine", "Cleavers"],
    "GERMO": ["Geranium molle", "Dove's-foot crane's-bill"],
    "LAPCO": ["Lapsana communis", "Nipplewort"],
    "LOLMU": ["Lolium multiflorum", "Italian ryegrass"],
    "LYCAR": ["Anchusa arvensis", "Common bugloss"],
    "MATCH": ["Matricaria chamomilla", "Scented mayweed"],
    "MATIN": ["Tripleurospermum inodorum", "Scentless mayweed"],
    "MELNO": ["Silene noctiflora", "Night-flowering catchfly"],
    "MYOAR": ["Myosotis arvensis", "Field forget-me-not"],
    "PAPRH": ["Papaver rhoeas", "Common poppy"],
    "PLALA": ["Plantago lanceolata", "Narrowleaf plantain"],
    "PLAMA": ["Plantago major", "Broadleaf plantain"],
    "POAAN": ["Poa annua", "Annual bluegrass"],
    "POLAV": ["Polygonum aviculare", "Prostrate knotweed"],
    "POLCO": ["Fallopia convolvulus", "Black bindweed"],
    "POLLA": ["Persicaria lapathifolia", "Pale smartweed"],
    "POLPE": ["Persicaria maculosa", "Redshank"],
    "RUMCR": ["Rumex crispus", "Curly dock"],
    "SENVU": ["Senecio vulgaris", "Common groundsel"],
    "SINAR": ["arvensis	Charlock", "Sinapis"],
    "SOLNI": ["Solanum nigrum", "Black nightshade"],
    "SONAS": ["Sonchus asper", "Spiny sowthistle"],
    "SONOL": ["Sonchus oleraceus", "Common sowthistle"],
    "STEME": ["Stellaria media", "Common chickweed"],
    "THLAR": ["Thlaspi arvense", "Field penny-cress"],
    "URTUR": ["Urtica urens", "Small nettle"],
    "VERAR": ["Veronica arvensis", "Corn speedwell"],
    "VERPE": ["Veronica persica", "Common field speedwell"],
    "VICHI": ["Vicia hirsuta", "Common hairy tare"],
    "VIOAR": ["Viola arvensis", "Field pansy"],
}


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    batch_size = 30
    ds_name = "ds0"
    ann_ext = ".json"
    img_ext = ".jpg"
    dataset_path = "/home/grokhi/rawdata/oppd/OPPD-master/DATA/images_full"

    def create_ann(image_path, eppo_boxname):
        global meta
        labels, tags = [], []
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        ann_name = get_file_name(image_path) + ann_ext
        ann_path = os.path.dirname(image_path) + "/" + ann_name

        if file_exists(ann_path):
            with open(ann_path) as json_file:
                ann_json = json.load(json_file)

            for plant in ann_json["plants"]:
                xmin = plant["bndbox"]["xmin"]
                ymin = plant["bndbox"]["ymin"]
                xmax = plant["bndbox"]["xmax"]
                ymax = plant["bndbox"]["ymax"]
                bbox = sly.Rectangle(top=ymin, left=xmin, bottom=ymax, right=xmax)
                class_name = plant["eppo"]

                if class_name is None:
                    continue
                class_name =class_name.strip()
                
                obj_class = meta.get_obj_class(class_name)
                if obj_class is None:
                    obj_class = sly.ObjClass(class_name, sly.Rectangle)
                    meta = meta.add_obj_class(obj_class)
                    api.project.update_meta(project.id, meta)
                label = sly.Label(bbox, obj_class)
                labels.append(label)

            vals = [
                eppo_boxname,
                eppo_2_human_name[eppo_boxname][0],
                eppo_2_human_name[eppo_boxname][1],
                ann_json["upload_id"],
                ann_json["image_id"],
                ann_json["date"],
                ann_json["trial_id"],
                ann_json["box_id"],
                ann_json["growth_condition"],
            ]
            for tag_name, val in zip(tag_names, vals):
                tags += [
                    sly.Tag(tag_meta, val) for tag_meta in tag_metas if tag_meta.name == tag_name
                ]
        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_classes = [sly.ObjClass(cls_name, sly.Rectangle) for cls_name in os.listdir(dataset_path)]
    tag_names = [
        "eppo",
        "latin",
        "english",
        "upload_id",
        "image_id",
        "date",
        "trial_id",
        "box_id",
        "growth_condition",
    ]
    tag_types = [
        sly.TagValueType.ANY_STRING,
        sly.TagValueType.ANY_STRING,
        sly.TagValueType.ANY_STRING,
        sly.TagValueType.ANY_NUMBER,
        sly.TagValueType.ANY_NUMBER,
        sly.TagValueType.ANY_STRING,
        sly.TagValueType.ANY_STRING,
        sly.TagValueType.ANY_STRING,
    ]
    tag_metas = [sly.TagMeta(name, typ) for name, typ in zip(tag_names, tag_types)]

    project = api.project.create(workspace_id, project_name)

    global meta
    meta = sly.ProjectMeta(
        obj_classes=obj_classes,
        tag_metas=tag_metas,
    )
    api.project.update_meta(project.id, meta.to_json())
    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    all_paths = list_files_recursively(dataset_path, valid_extensions=[img_ext])

    for eppo_boxname in os.listdir(dataset_path):
        img_paths = list_files_recursively(
            dataset_path + "/" + eppo_boxname, valid_extensions=[img_ext]
        )

        progress = sly.Progress(
            "Create dataset '{}' for class '{}', total={}".format(
                ds_name, eppo_boxname, len(all_paths)
            ),
            len(img_paths),
        )

        for img_pathes_batch in sly.batched(img_paths, batch_size=batch_size):
            img_names_batch = [os.path.basename(img_path) for img_path in img_pathes_batch]
            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)

            img_ids = [im_info.id for im_info in img_infos]
            anns_batch = [create_ann(image_path, eppo_boxname) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))

    return project
