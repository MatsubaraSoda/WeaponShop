import os
import uuid

import requests
from openai import OpenAI
from pathlib import Path
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class ImageGenerationInput(BaseModel):
    prompt: str = Field(..., description="用于生成图片的详细提示词")


def _project_root() -> Path:
    # .../src/project/tools/image_generation_tool.py -> 项目根（含 pyproject.toml）
    return Path(__file__).resolve().parents[3]


class FlowImageGeneratorTool(BaseTool):
    name: str = "Image Generator Tool"
    description: str = (
        "根据提示词生成图片，下载到项目根目录下 output/ 子目录，并返回 Markdown 格式的相对路径引用。"
    )
    args_schema: type[BaseModel] = ImageGenerationInput

    def _run(self, prompt: str) -> str:
        client = OpenAI(
            base_url=os.environ.get("IMAGE_API_BASE"),
            api_key=os.environ.get("IMAGE_API_KEY"),
        )

        try:
            response = client.images.generate(
                model="gpt-4o-image",
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
            image_url = response.data[0].url

            root = _project_root()
            save_dir = root / "output"
            save_dir.mkdir(parents=True, exist_ok=True)

            file_name = f"weapon_{uuid.uuid4().hex[:8]}.png"
            file_path = save_dir / file_name

            img_data = requests.get(image_url, timeout=120).content
            file_path.write_bytes(img_data)

            # 相对项目根的路径，便于插入 Markdown
            rel_ref = f"output/{file_name}"
            markdown_image = f"![生成图]({rel_ref})"

            return (
                "图片已成功生成并下载到本地！请在最终的 Markdown 报告中直接原样插入这行代码来显示图片：\n"
                f"{markdown_image}"
            )

        except Exception as e:
            return f"图片生成或下载失败，错误信息: {str(e)}"
