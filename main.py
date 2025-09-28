"""
main.py
~~~~~~~~~~~~~

命令行脚本，用于演示基于 Stable Diffusion 的图像生成和 OpenCV 图像编辑功能。

用法示例：

生成图片：

```bash
python main.py --prompt "极简日式客厅"
```

根据线稿生成：

```bash
python main.py --prompt "极简日式客厅" --sketch_path samples/room_sketch.png
```

图像编辑：

```bash
python main.py --input_image samples/generated.png --edit brightness_contrast --brightness 20 --contrast 10
```

"""

import argparse
import os

from generator import generate_text_to_image, generate_sketch_to_image
from image_editing import adjust_brightness_contrast, blend_images


def run_generation(args: argparse.Namespace) -> None:
    # 选择模式：有 sketch_path 就使用 sketch 控制
    output_dir = args.output_dir or "outputs"
    os.makedirs(output_dir, exist_ok=True)
    if args.sketch_path:
        out_path = os.path.join(output_dir, "sketch_generated.png")
        result = generate_sketch_to_image(
            prompt=args.prompt,
            sketch_path=args.sketch_path,
            output_path=out_path,
            device=args.device,
        )
    else:
        out_path = os.path.join(output_dir, "text_generated.png")
        result = generate_text_to_image(
            prompt=args.prompt, output_path=out_path, device=args.device
        )
    if result is not None:
        print(f"成功生成图像：{result}")
    else:
        print("生成失败，请检查依赖或参数。")


def run_edit(args: argparse.Namespace) -> None:
    output_dir = args.output_dir or "outputs"
    os.makedirs(output_dir, exist_ok=True)
    if args.edit == "brightness_contrast":
        out_path = os.path.join(output_dir, "edited.png")
        result_path = adjust_brightness_contrast(
            args.input_image,
            out_path,
            brightness=args.brightness or 0,
            contrast=args.contrast or 0,
        )
        print(f"完成亮度/对比度调整：{result_path}")
    elif args.edit == "blend":
        if not args.blend_image:
            raise ValueError("blend 模式需要 --blend_image 参数。")
        out_path = os.path.join(output_dir, "blended.png")
        result_path = blend_images(
            args.input_image,
            args.blend_image,
            out_path,
            alpha=args.alpha or 0.5,
        )
        print(f"完成图像叠加：{result_path}")
    else:
        raise ValueError("未知的编辑操作。可选值：brightness_contrast, blend")


def main():
    parser = argparse.ArgumentParser(description="Sketch2Image 工具")
    subparsers = parser.add_subparsers(dest="mode", required=False)

    # 生成子命令
    gen_parser = subparsers.add_parser("generate", help="生成图像")
    gen_parser.add_argument(
        "--prompt", type=str, required=True, help="文本提示，用于控制生成风格"
    )
    gen_parser.add_argument(
        "--sketch_path", type=str, help="线稿图像路径 (可选)"
    )
    gen_parser.add_argument(
        "--output_dir", type=str, default="outputs", help="输出目录"
    )
    gen_parser.add_argument(
        "--device", type=str, default="cpu", help="推断设备，如 'cpu' 或 'cuda'"
    )

    # 编辑子命令
    edit_parser = subparsers.add_parser("edit", help="编辑图像")
    edit_parser.add_argument(
        "--input_image", type=str, required=True, help="待编辑的图像路径"
    )
    edit_parser.add_argument(
        "--edit",
        type=str,
        choices=["brightness_contrast", "blend"],
        required=True,
        help="选择编辑类型：brightness_contrast 或 blend",
    )
    edit_parser.add_argument(
        "--brightness", type=int, help="亮度调整值 (-100~100)，仅 brightness_contrast 模式有效"
    )
    edit_parser.add_argument(
        "--contrast", type=int, help="对比度调整值 (-100~100)，仅 brightness_contrast 模式有效"
    )
    edit_parser.add_argument(
        "--blend_image", type=str, help="叠加的另一张图像路径，仅 blend 模式有效"
    )
    edit_parser.add_argument(
        "--alpha",
        type=float,
        help="叠加权重 (0~1)，越大则更偏向输入图像，仅 blend 模式有效",
    )
    edit_parser.add_argument(
        "--output_dir", type=str, default="outputs", help="输出目录"
    )

    # 无子命令时的默认行为：尝试生成
    parser.add_argument(
        "--prompt",
        type=str,
        help="文本提示 (默认行为下使用)，与 generate 子命令参数一致",
    )
    parser.add_argument(
        "--sketch_path",
        type=str,
        help="线稿 (默认行为下使用)，与 generate 子命令参数一致",
    )
    parser.add_argument(
        "--input_image",
        type=str,
        help="输入图像 (默认行为下用作编辑)",
    )
    parser.add_argument(
        "--edit",
        type=str,
        help="默认行为下的编辑类型",
    )
    parser.add_argument(
        "--brightness", type=int, help="默认行为下的 brightness 参数"
    )
    parser.add_argument(
        "--contrast", type=int, help="默认行为下的 contrast 参数"
    )
    parser.add_argument(
        "--blend_image", type=str, help="默认行为下的 blend_image 参数"
    )
    parser.add_argument(
        "--alpha", type=float, help="默认行为下的 alpha 参数"
    )
    parser.add_argument(
        "--output_dir", type=str, help="默认行为下的输出目录"
    )
    parser.add_argument(
        "--device", type=str, help="默认行为下的设备"
    )

    args = parser.parse_args()

    # 根据子命令分发
    if args.mode == "generate":
        run_generation(args)
    elif args.mode == "edit":
        run_edit(args)
    else:
        # 如果未显式指定子命令，则根据提供的参数自动决定
        if args.input_image and args.edit:
            run_edit(args)
        elif args.prompt:
            run_generation(args)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
