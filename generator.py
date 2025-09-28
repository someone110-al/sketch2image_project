"""
generator.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

该模块封装了基于 Stable Diffusion 等扩散模型的图像生成函数。
如果环境中安装了 `diffusers` 和 `torch` 等库，则可以加载预训练模型进行推断；
否则，函数会提醒用户安装相关依赖。

主要功能包括：
* 文本到图像的生成（text-to-image）
* 线稿控制到图像的生成（sketch-to-image）

提示：运行扩散模型需要较高的计算资源，建议在具备 GPU 的环境中执行。
"""

import os
from typing import Optional

try:
    # 延迟导入 diffusers，如果未安装则捕获异常
    from diffusers import (
        StableDiffusionXLPipeline,
        StableDiffusionXLControlNetPipeline,
        ControlNetModel,
    )
    import torch
except ImportError:
    StableDiffusionXLPipeline = None  # type: ignore
    StableDiffusionXLControlNetPipeline = None  # type: ignore
    ControlNetModel = None  # type: ignore
    torch = None  # type: ignore


def _load_sdxl_pipeline(device: str = "cpu"):
    """加载 SDXL 基础模型。如果未安装 diffusers，则抛出 RuntimeError。"""
    if StableDiffusionXLPipeline is None:
        raise RuntimeError(
            "diffusers 未安装，请执行 `pip install diffusers torch` 并确保有合适的计算资源。"
        )
    # 加载 base 模型；使用 `sdxl-base-1.0` 作为默认权重
    model_name = "stabilityai/stable-diffusion-xl-base-1.0"
    pipe = StableDiffusionXLPipeline.from_pretrained(model_name)
    if device.startswith("cuda") and torch is not None and torch.cuda.is_available():
        pipe.to(device)
    return pipe


def generate_text_to_image(prompt: str, output_path: str, device: str = "cpu") -> Optional[str]:
    """
    根据文本提示生成图像。

    参数：
        prompt (str): 文本描述。
        output_path (str): 保存生成图像的路径。
        device (str): 推断设备，默认为 'cpu'。可设置为 'cuda' 或 'mps'。

    返回：
        输出路径或 None（如果生成失败）。
    """
    try:
        pipe = _load_sdxl_pipeline(device)
    except RuntimeError as e:
        print(e)
        return None
    # 生成
    with torch.no_grad():  # type: ignore
        image = pipe(prompt=prompt).images[0]
    # 保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    return output_path


def generate_sketch_to_image(
    prompt: str, sketch_path: str, output_path: str, device: str = "cpu"
) -> Optional[str]:
    """
    根据线稿和文本提示生成图像，使用 ControlNet 模型对结构进行约束。

    参数：
        prompt (str): 文本描述，用于控制风格或材质等信息。
        sketch_path (str): 输入线稿路径（黑白图像）。
        output_path (str): 输出图像路径。
        device (str): 推断设备。

    返回：
        输出路径或 None。
    """
    if StableDiffusionXLControlNetPipeline is None or ControlNetModel is None:
        print(
            "diffusers 未安装或 ControlNet 模型不可用，请安装 diffusers 并确保版本支持 ControlNet。"
        )
        return None
    # 加载控制网络权重：以 canny 模式为示例
    control_model_id = "diffusers/controlnet-canny-sdxl-1.0"
    controlnet = ControlNetModel.from_pretrained(control_model_id)
    # 加载生成管线
    pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", controlnet=controlnet
    )
    if device.startswith("cuda") and torch is not None and torch.cuda.is_available():
        pipe.to(device)
    # 读取线稿
    from PIL import Image
    sketch_image = Image.open(sketch_path).convert("RGB")
    # 生成
    with torch.no_grad():  # type: ignore
        image = pipe(prompt=prompt, image=sketch_image).images[0]
    # 保存
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    return output_path


__all__ = [
    "generate_text_to_image",
    "generate_sketch_to_image",
]
