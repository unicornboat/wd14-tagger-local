import os
import sys
import pandas as pd
import numpy as np

from typing import Tuple, List, Dict
from io import BytesIO
from PIL import Image

from pathlib import Path
from huggingface_hub import hf_hub_download
import re
import json

from numpy import asarray, float32, expand_dims, exp

tag_escape_pattern = re.compile(r'([\\()])')

# 设定默认下载路径为当前文件所在目录的上级目录中的models文件夹
default_model_path = Path(__file__).resolve().parent.parent / 'models'
os.makedirs(default_model_path, exist_ok=True)  # 如果models目录不存在，则创建它

import tagger.dbimutils as dbimutils

use_cpu = True

class Interrogator:
    @staticmethod
    def postprocess_tags(
        tags: Dict[str, float],
        threshold=0.35,
        additional_tags: List[str] = [],
        exclude_tags: List[str] = [],
        sort_by_alphabetical_order=False,
        add_confident_as_weight=False,
        replace_underscore=False,
        replace_underscore_excludes: List[str] = [],
        escape_tag=False
    ) -> Dict[str, float]:
        for t in additional_tags:
            tags[t] = 1.0

        # those lines are totally not "pythonic" but looks better to me
        tags = {
            t: c

            # sort by tag name or confident
            for t, c in sorted(
                tags.items(),
                key=lambda i: i[0 if sort_by_alphabetical_order else 1],
                reverse=not sort_by_alphabetical_order
            )

            # filter tags
            if (
                c >= threshold
                and t not in exclude_tags
            )
        }

        new_tags = []
        for tag in list(tags):
            new_tag = tag

            if replace_underscore and tag not in replace_underscore_excludes:
                new_tag = new_tag.replace('_', ' ')

            if escape_tag:
                new_tag = tag_escape_pattern.sub(r'\\\1', new_tag)

            if add_confident_as_weight:
                new_tag = f'({new_tag}:{tags[tag]})'

            new_tags.append((new_tag, tags[tag]))
        tags = dict(new_tags)

        return tags

    def __init__(self, name: str, model_path='model.onnx', tags_path='tags.csv', local_model_path=default_model_path) -> None:
        self.name = name
        self.model_path = model_path
        self.tags_path = tags_path
        self.local_model_path = local_model_path / self.name.replace(' ', '_')
        os.makedirs(self.local_model_path, exist_ok=True)  # 为每个模型创建一个目录

    def load(self):
        raise NotImplementedError()

    def unload(self) -> bool:
        unloaded = False

        if hasattr(self, 'model') and self.model is not None:
            del self.model
            unloaded = True
            print(f'Unloaded {self.name}')

        if hasattr(self, 'tags'):
            del self.tags

        return unloaded

    def interrogate(
        self,
        image: Image
    ) -> Tuple[
        Dict[str, float],  # rating confidents
        Dict[str, float]  # tag confidents
    ]:
        raise NotImplementedError()

class WaifuDiffusionInterrogator(Interrogator):
    def __init__(
        self,
        name: str,
        model_path='model.onnx',
        tags_path='selected_tags.csv',
        **kwargs
    ) -> None:
        super().__init__(name)
        self.model_path = model_path
        self.tags_path = tags_path
        self.kwargs = kwargs

    def download(self) -> Tuple[os.PathLike, os.PathLike]:
        model_full_path = self.local_model_path / 'model.onnx'
        if not model_full_path.exists():
            print(f"正在下载 {self.name} 模型文件...")
            model_path = hf_hub_download(
                **self.kwargs,
                filename=self.model_path,
                local_dir=self.local_model_path,
                local_dir_use_symlinks=False
            )
            tags_path = hf_hub_download(
                **self.kwargs,
                filename=self.tags_path,
                local_dir=self.local_model_path,
                local_dir_use_symlinks=False
            )
        else:
            print(f"模型文件 {self.name} 已存在，跳过下载")

        return model_full_path, self.local_model_path / 'selected_tags.csv'

    def load(self) -> None:
        model_path, tags_path = self.download()

        from onnxruntime import InferenceSession

        # https://onnxruntime.ai/docs/execution-providers/
        # https://github.com/toriato/stable-diffusion-webui-wd14-tagger/commit/e4ec460122cf674bbf984df30cdb10b4370c1224#r92654958
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        if use_cpu:
            providers.pop(0)

        self.model = InferenceSession(str(model_path), providers=providers)

        print(f'加载 {self.name} 模型')
        self.tags = pd.read_csv(tags_path)

    def interrogate(
        self,
        image: Image
    ) -> Tuple[
        Dict[str, float],  # rating confidents
        Dict[str, float]  # tag confidents
    ]:
        # init model
        if not hasattr(self, 'model') or self.model is None:
            self.load()

        # code for converting the image and running the model is taken from the link below
        # thanks, SmilingWolf!
        # https://huggingface.co/spaces/SmilingWolf/wd-v1-4-tags/blob/main/app.py

        # convert an image to fit the model
        _, height, _, _ = self.model.get_inputs()[0].shape

        # alpha to white
        image = image.convert('RGBA')
        new_image = Image.new('RGBA', image.size, 'WHITE')
        new_image.paste(image, mask=image)
        image = new_image.convert('RGB')
        image = np.asarray(image)

        # PIL RGB to OpenCV BGR
        image = image[:, :, ::-1]

        image = dbimutils.make_square(image, height)
        image = dbimutils.smart_resize(image, height)
        image = image.astype(np.float32)
        image = np.expand_dims(image, 0)

        # evaluate model
        input_name = self.model.get_inputs()[0].name
        label_name = self.model.get_outputs()[0].name
        confidents = self.model.run([label_name], {input_name: image})[0]

        tags = self.tags[:][['name']]
        tags['confidents'] = confidents[0]

        # first 4 items are for rating (general, sensitive, questionable, explicit)
        ratings = dict(tags[:4].values)

        # rest are regular tags
        tags = dict(tags[4:].values)

        return ratings, tags

class MLDanbooruInterrogator(Interrogator):
    """ MLDanbooru 模型的 interrogator。 """
    def __init__(
        self,
        name: str,
        repo_id: str,
        model_path: str,
        tags_path='classes.json',
    ) -> None:
        super().__init__(name)
        self.model_path = model_path
        self.tags_path = tags_path
        self.repo_id = repo_id
        self.tags = None
        self.model = None

    def find_onnx_model(self):
        # 使用glob搜索onnx文件
        onnx_files = list(self.local_model_path.glob('*.onnx'))
        if onnx_files:
            # 如果找到.onnx文件，返回第一个文件的完整路径
            return onnx_files[0]
        # 如果没有找到.onnx文件，返回None
        return None


    def download(self) -> Tuple[str, str]:
        model_full_path = self.find_onnx_model()
        tags_full_path = self.local_model_path / self.tags_path

        if model_full_path is None:
            print(f"正在下载 {self.name} 模型文件...")
            model_full_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.model_path,
                local_dir=self.local_model_path,
                local_dir_use_symlinks=False
            )
            tags_full_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.tags_path,
                local_dir=self.local_model_path,
                local_dir_use_symlinks=False
            )
        else:
            print(f"模型文件 {self.name} 已经存在，跳过下载")

        return model_full_path, tags_full_path

    def load(self) -> None:
        model_path, tags_path = self.download()

        from onnxruntime import InferenceSession
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        if use_cpu:
            providers.pop(0)

        self.model = InferenceSession(str(model_path), providers=providers)
        print(f'从 {model_path} 加载 {self.name} 模型')

        self.tags = pd.read_csv(tags_path)

    def interrogate(
        self,
        image: Image
    ) -> Tuple[
        Dict[str, float],  # rating confidents
        Dict[str, float]  # tag confidents
    ]:
        # init model
        if self.model is None:
            self.load()

        image = dbimutils.fill_transparent(image)
        image = dbimutils.resize(image, 448)  # TODO CUSTOMIZE

        x = asarray(image, dtype=float32) / 255
        # HWC -> 1CHW
        x = x.transpose((2, 0, 1))
        x = expand_dims(x, 0)

        input_ = self.model.get_inputs()[0]
        output = self.model.get_outputs()[0]
        # evaluate model
        y, = self.model.run([output.name], {input_.name: x})

        # Softmax
        y = 1 / (1 + exp(-y))

        tags = {tag: float(conf) for tag, conf in zip(self.tags, y.flatten())}
        return {}, tags

    def large_batch_interrogate(self, images: List, dry_run=False) -> str:
        raise NotImplementedError()
