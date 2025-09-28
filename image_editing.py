"""
image_editing.py
~~~~~~~~~~~~~~~~~~~~~~~~

基于 OpenCV 的图像编辑模块，提供简单易用的后期处理功能，用于调整生成图像的视觉效果。

目前支持的操作包括：

* 调整亮度和对比度
* 饱和度/色调修改
* 图像叠加（将两张图像按指定权重混合）

示例用法见 main.py。
"""

import os
import cv2
import numpy as np
from typing import Tuple


def adjust_brightness_contrast(
    image_path: str, output_path: str, brightness: int = 0, contrast: int = 0
) -> str:
    """
    调整图像的亮度和对比度并保存。

    brightness: -100 到 100 之间的整数，正值增加亮度。
    contrast: -100 到 100 之间的整数，正值增强对比度。
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"无法打开图像: {image_path}")
    # 调整亮度
    beta = np.clip(brightness, -100, 100)
    # 调整对比度
    alpha = np.clip(contrast, -100, 100) / 100.0 + 1.0
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, adjusted)
    return output_path


def blend_images(
    image_path_1: str,
    image_path_2: str,
    output_path: str,
    alpha: float = 0.5,
) -> str:
    """
    将两张图像按给定权重叠加。

    alpha：第一张图像的权重（0~1）。第二张图像权重为 (1-alpha)。
    """
    img1 = cv2.imread(image_path_1)
    img2 = cv2.imread(image_path_2)
    if img1 is None or img2 is None:
        raise FileNotFoundError("输入图像无法读取")
    # 调整图像尺寸一致
    if img1.shape[:2] != img2.shape[:2]:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    blended = cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, blended)
    return output_path


__all__ = [
    "adjust_brightness_contrast",
    "blend_images",
]
