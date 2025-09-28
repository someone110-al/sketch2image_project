# Sketch2Image Project / 草图成像项目

本仓库提供中英文双语说明，为便于阅读使用，请展开下列语言版本：

<details>
<summary><strong>中文说明（点击展开）</strong></summary>

### 项目简介

该项目旨在构建一个基于**前沿图像生成模型**的室内设计应用，可以把简单的线稿或文本描述转换为写实的室内设计效果图。主要技术包括：

1. **扩散模型（Stable Diffusion XL/3.5 等）**：用于根据文字或草图生成高质量图像。研究指出 Stable Diffusion 3.5 Large 在图像质量与文本一致性方面表现优异【632959316964011†L374-L387】；ControlNet 等扩展可在生成过程中利用线稿或边缘条件进行精准控制【632959316964011†L451-L459】。
2. **图像编辑技术**（基于 OpenCV）：用于对生成结果进行亮度、色调及图像叠加等后期处理，满足用户个性化需求。

最终项目提供命令行工具，演示从室内线稿或文本描述到成品图像的完整流程，并附带示例图片。

### 功能特点

- **文本到图像生成**：使用预训练的 SDXL/SD3.5 模型，根据用户提供的中文或英文描述生成室内效果图。
- **草图到图像生成**：利用 ControlNet 技术，将黑白线稿作为结构约束，引导扩散模型生成符合线稿结构的写实效果。
- **图像编辑**：提供基于 OpenCV 的基础图像处理操作，如调整亮度/对比度、图像叠加等，可对生成结果进行微调。
- **可扩展接口**：代码预留调用 diffusers 库的接口，在具备 PyTorch 环境时可直接加载模型；若无法安装深度学习库，脚本会提示并跳过生成步骤。
- **示例与结果**：仓库中包含示例图片，用于展示从线稿到最终效果的转换。

### 使用说明

#### 环境准备
1. 安装 Python 3.8+，建议在虚拟环境中运行。
2. 若有条件安装深度学习库，可执行：
   ```bash
   pip install torch diffusers opencv-python pillow
   ```
   若无法安装 PyTorch，可忽略安装，仅体验图像编辑功能。

#### 运行示例
1. **文本生成**：
   ```bash
   python main.py --prompt "一个极简日式风格的客厅，干净的线条、木质家具和榻榻米"
   ```
2. **草图生成**：
   ```bash
   python main.py --sketch_path samples/room_sketch.png --prompt "极简日式客厅"
   ```
3. **图像编辑**（调整亮度和对比度）：
   ```bash
   python main.py --input_image samples/room_generated.png --edit brightness_contrast --brightness 30 --contrast 10
   ```
更多参数请参考 `main.py` 中的 argparse 定义。

#### 项目结构

- **`generator.py`**：封装文本/草图到图像生成的核心逻辑，默认使用 diffusers 中的 SDXL 模型。
- **`image_editing.py`**：基于 OpenCV 的图像编辑函数，如亮度/对比度调整、图像叠加等。
- **`main.py`**：命令行入口，根据参数调用生成或编辑功能。
- **`samples/`**：示例输入与输出图像，包括线稿和生成结果，可供快速测试。
- **`requirements.txt`**：所需依赖列表。

#### 局限与展望

- **硬件要求**：运行 Stable Diffusion 3.5 或 SDXL 等大型模型需要较高显存（官方建议至少 8 GB）。使用 SDXL-Lightning 等蒸馏模型可降低资源需求【632959316964011†L586-L604】。
- **库依赖**：若环境无法安装 PyTorch/diffusers，则只能体验 OpenCV 的编辑功能。未来可引入轻量化模型（如 StyleGAN 或 SDXL-Lightning 量化版）以缓解资源限制。
- **模型版权**：生成模型可能基于包含版权素材的数据集训练，商业化使用时需遵循相应许可。

#### 文件说明

| 文件/目录 | 用途 |
|-----------|------|
| `generator.py` | 定义 `generate_text_to_image` 与 `generate_sketch_to_image` 函数，负责加载模型并生成图像。 |
| `image_editing.py` | 提供 `adjust_brightness_contrast` 和 `blend_images` 等函数，用于图像后期处理。 |
| `main.py` | 命令行入口，解析参数并调用生成或编辑功能。 |
| `samples/` | 存放示例输入输出图像，可快速测试程序效果。 |
| `requirements.txt` | 列举所需第三方库，便于安装依赖。 |
| `README.md` | 介绍项目背景、安装使用方法、文件说明等（本文件）。 |

#### 示例图片

| 草图示例 | 生成结果 |
|-----------|-----------|
| ![sketch]({{file:file-RW7GEL2wLCbefUkhG1S4QP}}) | ![result]({{file:file-9h3ABpLob4RFXXLHX1fjWJ}}) |

通过上述示例可见，控制模型能够按照线稿提供的结构生成符合描述风格的室内效果图。

</details>

<details>
<summary><strong>English Description (click to expand)</strong></summary>

### Introduction

This project aims to build an interior-design application based on **state‑of‑the‑art image‑generation models**. It can convert simple sketches or textual descriptions into photorealistic room renderings. The core techniques are:

1. **Diffusion models (Stable Diffusion XL/3.5, etc.)** for generating high‑quality images from text or sketches. Research shows that Stable Diffusion 3.5 Large achieves excellent image quality and prompt adherence among open‑source models【632959316964011†L374-L387】. Extensions like ControlNet allow precise conditioning on edge maps or sketches during generation【632959316964011†L451-L459】.
2. **Image editing using OpenCV**, which adjusts brightness, contrast and blends images to personalise the final result.

The project provides a command‑line utility demonstrating the complete workflow from sketch or text to finished image and includes sample images.

### Features

- **Text‑to‑image generation** using pretrained SDXL/SD3.5 models based on Chinese or English prompts.
- **Sketch‑to‑image generation** using ControlNet to guide the diffusion model according to a black‑and‑white outline.
- **Image editing** via basic OpenCV operations like brightness/contrast adjustment and image blending.
- **Extensible interface**: the code is ready to call diffusers models directly when PyTorch is available; otherwise, it will gracefully skip generation and inform the user.
- **Examples and results**: the repository includes sample images demonstrating the sketch‑to‑image conversion.

### Usage

#### Environment
1. Install Python 3.8+ and preferably work within a virtual environment.
2. If your environment can install deep‑learning libraries, run:
   ```bash
   pip install torch diffusers opencv-python pillow
   ```
   These packages load Stable Diffusion models and handle image processing. If you cannot install PyTorch, you can still explore the editing functions.

#### Running examples
1. **Generate from text**:
   ```bash
   python main.py --prompt "A minimalist Japanese living room with clean lines, wooden furniture and tatami mats"
   ```
2. **Generate from sketch**:
   ```bash
   python main.py --sketch_path samples/room_sketch.png --prompt "minimalist Japanese living room"
   ```
3. **Image editing** (adjust brightness & contrast):
   ```bash
   python main.py --input_image samples/room_generated.png --edit brightness_contrast --brightness 30 --contrast 10
   ```
See `main.py` for more parameters.

#### Project structure

- **`generator.py`** – defines `generate_text_to_image` and `generate_sketch_to_image` using diffusers.
- **`image_editing.py`** – provides image post‑processing functions like brightness/contrast adjustment and blending.
- **`main.py`** – command‑line entry point, parses arguments and calls generation or editing.
- **`samples/`** – contains example inputs and outputs for quick testing.
- **`requirements.txt`** – lists required third‑party packages.
- **`README.md`** – this document, describing the project in Chinese & English, with installation, usage and file descriptions.

#### Limitations & future work

- **Hardware requirements**: Running Stable Diffusion 3.5 or SDXL requires significant VRAM (official recommendation ≥8 GB). Using distilled variants like SDXL‑Lightning can reduce resource demands【632959316964011†L586-L604】.
- **Library dependencies**: Without PyTorch/diffusers, only the OpenCV editing functions can be used. In the future, lighter models (e.g., StyleGAN or quantised SDXL‑Lightning) could be integrated.
- **Model licensing**: Generated images might be based on training data containing copyrighted material; please check licences before commercial use.

#### File descriptions

| File/Directory | Purpose |
|---------------|--------|
| `generator.py` | Provides `generate_text_to_image` & `generate_sketch_to_image` functions to load models and generate images. |
| `image_editing.py` | Contains image post‑processing functions like `adjust_brightness_contrast` and `blend_images`. |
| `main.py` | Command‑line entry point; parses arguments and calls generation or editing. |
| `samples/` | Includes example input and output images for quick testing. |
| `requirements.txt` | Lists dependencies for installation. |
| `README.md` | This file, describing the project in Chinese and English. |

#### Example images

| Sketch | Generated result |
|-------|-----------------|
| ![sketch]({{file:file-RW7GEL2wLCbefUkhG1S4QP}}) | ![result]({{file:file-9h3ABpLob4RFXXLHX1fjWJ}}) |

The example shows that the model can follow the outline provided by the sketch to create a photorealistic interior rendering matching the prompt.

</details>
