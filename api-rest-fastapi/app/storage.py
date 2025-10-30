from __future__ import annotations

from threading import RLock
from typing import Dict, List, Optional
from pathlib import Path
import json

from .models import Envio


class InMemoryEnvioStorage:
    def __init__(self) -> None:
        self._lock = RLock()
        self._envios_by_id: Dict[str, Envio] = {}
        # Default path: use camel output if available, otherwise local data directory
        self._json_path = self._resolve_default_json_path()
        self._load_from_disk()

    def list_envios(self) -> List[Envio]:
        with self._lock:
            return list(self._envios_by_id.values())

    def get_envio(self, envio_id: str) -> Optional[Envio]:
        with self._lock:
            return self._envios_by_id.get(envio_id)

    def create_envio(self, envio: Envio) -> bool:
        with self._lock:
            if envio.id_envio in self._envios_by_id:
                return False
            self._envios_by_id[envio.id_envio] = envio
            # Persist after creation
            self._save_to_disk()
            return True

    def _resolve_default_json_path(self) -> Path:
        # api-rest-fastapi/app/storage.py -> .../api-rest-fastapi
        project_root = Path(__file__).resolve().parents[1]
        camel_output = project_root.parent / "camel-lab" / "output" / "envios.json"
        local_data = project_root / "data" / "envios.json"
        if camel_output.exists():
            return camel_output
        return local_data

    def _load_from_disk(self) -> None:
        try:
            if self._json_path.exists():
                data = json.loads(self._json_path.read_text(encoding="utf-8"))
                # Expecting a list of objects with id_envio, cliente, direccion, estado
                self._envios_by_id = {
                    item["id_envio"]: Envio(**item) for item in data
                    if isinstance(item, dict) and "id_envio" in item
                }
                print(f"[INFO] Archivo cargado con {len(self._envios_by_id)} registros.")
            else:
                print("[INFO] No se encontró envios.json, almacenamiento vacío en memoria.")
        except Exception as exc:
            print(f"[ERROR] No se pudo cargar envios.json: {exc}")

    def _save_to_disk(self) -> None:
        try:
            self._json_path.parent.mkdir(parents=True, exist_ok=True)
            payload = [envio.model_dump() for envio in self._envios_by_id.values()]
            self._json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            print(f"[ERROR] No se pudo guardar envios.json: {exc}")


storage = InMemoryEnvioStorage()
