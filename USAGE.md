# 使用说明与 Git 推送流程

本文档提供对 Sketch2Image 项目的详细使用指南，以及如何将本地代码推送到 GitHub 的示例命令和作用说明。

## 一、项目使用

### 1. 环境配置

1. 确保安装 Python 3.8 及以上版本。
2. （可选）创建并激活虚拟环境，以隔离依赖：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 下使用 venv\Scripts\activate
   ```
3. 安装依赖库：
   ```bash
   pip install -r requirements.txt
   ```
   如果无法安装 `torch` 或 `diffusers`，仍可使用 OpenCV 编辑功能。

### 2. 生成图像

1. **根据文本生成**：
   ```bash
   python main.py generate --prompt "一个现代感十足的客厅，有落地窗和绿植"
   ```
   - `generate` 为子命令表示生成模式。
   - `--prompt` 后跟描述文本，支持中文或英文。
   - 程序会在 `outputs/` 目录下保存 `text_generated.png`。

2. **根据线稿生成**：
   ```bash
   python main.py generate --prompt "极简日式客厅" --sketch_path samples/room_sketch.png
   ```
   - 增加 `--sketch_path` 参数指定线稿路径，程序将使用 ControlNet 控制生成过程。
   - 生成结果保存为 `outputs/sketch_generated.png`。

### 3. 编辑图像

1. **调整亮度/对比度**：
   ```bash
   python main.py edit --input_image samples/room_generated.png --edit brightness_contrast --brightness 30 --contrast 10
   ```
   - `edit` 为编辑子命令。
   - `--input_image` 指定要编辑的图片。
   - `--edit brightness_contrast` 表示进行亮度/对比度调整。
   - `--brightness` 与 `--contrast` 控制调整幅度，范围通常为 -100～100。
   - 输出文件默认保存至 `outputs/edited.png`。

2. **图像叠加**：
   ```bash
   python main.py edit --input_image img1.png --edit blend --blend_image img2.png --alpha 0.6
   ```
   - `--edit blend` 表示将两张图片叠加。
   - `--blend_image` 指定第二张图片。
   - `--alpha` 控制权重，0.6 表示 60% 权重给第一张图。
   - 输出保存为 `outputs/blended.png`。

## 二、Git 推送流程

以下是将本地项目推送到 GitHub 仓库的常见步骤，假设您已经安装 Git 并登录了正确的 GitHub 账户（此处为 `someone110-al`）。

1. **初始化 Git 仓库**（如果尚未完成）：
   ```bash
   git init
   ```
   - 在项目根目录执行。创建 `.git/` 目录，使当前目录成为 Git 仓库。

2. **配置用户信息**（首次使用 Git 时）：
   ```bash
   git config user.name "你的姓名"
   git config user.email "your.email@example.com"
   ```
   - 配置提交者信息，提交历史中会显示这些信息。
   - `--global` 可用于全局设置，当前项目可省略。

3. **将文件添加到暂存区**：
   ```bash
   git add .
   ```
   - `.` 表示添加当前目录所有变化的文件到暂存区，准备提交。

4. **提交到本地仓库**：
   ```bash
   git commit -m "初始化项目"
   ```
   - `-m` 后跟提交信息，描述此次提交内容。

5. **关联远程仓库**：
   ```bash
   git remote add origin https://github.com/someone110-al/sketch2image_project.git
   ```
   - 创建 GitHub 仓库后，使用其 HTTPS 地址替换示例中的 URL。
   - `origin` 是常用的远程名称，指向 GitHub 仓库。

6. **推送到远程仓库**：
   ```bash
   git push -u origin master
   ```
   - 将本地 `master`（或 `main`）分支推送至远程 `origin` 仓库。
   - `-u` 参数会在本地建立跟踪关系，下次只需执行 `git push` 即可。

7. **后续更新**：
   - 修改文件后，重复执行 `git add`、`git commit`、`git push` 即可同步更新至远程仓库。

## 三、常见问题

1. **无法安装 PyTorch/diffusers**：
   - 如果安装困难，可仅使用项目的 OpenCV 编辑功能。生成图片功能需要具备支持的深度学习环境。
2. **推送时报权限错误**：
   - 确认远程仓库 URL 正确，且当前 GitHub 账户有权限。
   - 如使用 HTTPS 方式推送，需要确保缓存的凭据正确，或在命令行中输入个人访问令牌。

## 四、总结

按照本文档的步骤，您可以在自己的机器上安装依赖、运行生成和编辑功能，并将代码推送到 GitHub。若有更多自定义需求，可参考源代码自行修改。
