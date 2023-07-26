# https://vision.eng.au.dk/open-plant-phenotyping-database/

import supervisely as sly
import gdown
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
import json
import tqdm

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


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    project = api.project.create(workspace_id, project_name)
    meta = sly.ProjectMeta()

    datasets_folder = "/mnt/c/Users/German/Documents/OPPD-master/DATA/images_full"
    datasets_paths = [f.path for f in os.scandir(datasets_folder) if f.is_dir()]

    pbar = tqdm.tqdm(desc="TOTAL DATASETS DONE", total=len(datasets_paths))
    for dataset_dir in datasets_paths:
        dataset_name = os.path.basename(dataset_dir)
        dataset = api.dataset.get_or_create(
            project.id, dataset_name
        )  # api.dataset.create(project.id, dataset_name)

        ann_paths = sly.fs.list_files(dataset_dir, valid_extensions=[".json"])
        for ann_path in ann_paths:
            with open(ann_path) as json_file:
                ann_json = json.load(json_file)

            # upload image
            img_name = ann_json["filename"]
            image_path = os.path.join(dataset_dir, img_name)
            try:
                image_info = api.image.upload_path(dataset.id, img_name, image_path)
                # (print(f"image(id:{image_info.id}) is uploaded to dataset (id:{dataset.id})."))

                # check tagmeta in project and init if needed
                tag_name = "Growth condition"
                tag_value_type = sly.TagValueType.ANY_STRING
                tag_meta = meta.get_tag_meta(tag_name)
                if tag_meta is None:
                    tag_meta = sly.TagMeta(tag_name, tag_value_type)
                    meta = meta.add_tag_meta(tag_meta)
                    api.project.update_meta(dataset.project_id, meta)

                # add tag to image
                tag = sly.Tag(tag_meta, ann_json["growth_condition"])

                labels = []
                for plant in ann_json["plants"]:
                    xmin = plant["bndbox"]["xmin"]
                    ymin = plant["bndbox"]["ymin"]
                    xmax = plant["bndbox"]["xmax"]
                    ymax = plant["bndbox"]["ymax"]
                    # xmin, ymin, xmax, ymax = list(obj["bndbox"].values())
                    bbox = sly.Rectangle(top=ymin, left=xmin, bottom=ymax, right=xmax)
                    class_name = plant["eppo"]
                    obj_class = meta.get_obj_class(class_name)
                    if obj_class is None:
                        obj_class = sly.ObjClass(class_name, sly.Rectangle)
                        meta = meta.add_obj_class(obj_class)
                        api.project.update_meta(project.id, meta)
                    label = sly.Label(bbox, obj_class)
                    labels.append(label)

                ann = sly.Annotation(
                    img_size=[image_info.height, image_info.width],
                    labels=labels,
                    img_tags=[tag],
                )
                api.annotation.upload_ann(image_info.id, ann)
            except Exception as e:
                pbar.update(1)
                print(e)
            # print(f"uploaded annotation to image(id:{image_info.id})")
        pbar.update(1)
    print(f"Projects {project.name} has been successfully processed")
    pbar.close()

    return project
