import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from app.main import app


def export_openapi(output_path: Path) -> None:
    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        description=app.description,
    )
    output_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OpenAPI exportado en: {output_path}")


if __name__ == "__main__":
    export_openapi(Path("openapi.json"))
