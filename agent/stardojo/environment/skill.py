import base64
import time
import json
from typing import Type, AnyStr, Any

import numpy as np
import dill
from dataclasses import dataclass
from dataclass_wizard import JSONWizard
from dataclass_wizard.abstractions import W
from dataclass_wizard.type_def import JSONObject, Encoder
import os

from stardojo.config import Config

config = Config()


@dataclass
class Skill(JSONWizard):

    skill_name: str
    skill_function: Any
    skill_embedding: np.ndarray
    skill_code: str
    skill_code_base64: str


    def __call__(self, *args, **kwargs):
        return self.skill_function(*args, **kwargs)


    @classmethod
    def from_dict(cls: Type[W], o: JSONObject) -> W:
        # Backward-compatible loading:
        # - Old format stored `skill_function` (dill hex)
        # - New format omits it and reconstructs the function from `skill_code`
        skill_function_hex = o.get("skill_function", "")
        if skill_function_hex:
            skill_function = dill.loads(bytes.fromhex(skill_function_hex))  # Load skill function from hex string
        else:
            # Reconstruct from code to avoid huge/slow dill blobs in the skill library file.
            ns: dict[str, Any] = {}
            exec(o["skill_code"], ns, ns)
            skill_function = ns.get(o["skill_name"])
            if not callable(skill_function):
                # Fallback: pick the first callable defined by the snippet.
                for v in ns.values():
                    if callable(v) and getattr(v, "__name__", "").startswith("_") is False:
                        skill_function = v
                        break
            if not callable(skill_function):
                raise ValueError(f"Failed to reconstruct skill_function for skill '{o['skill_name']}' from skill_code.")
        skill_embedding = np.frombuffer(base64.b64decode(o['skill_embedding']), dtype=np.float64)

        return cls(
            skill_name=o['skill_name'],
            skill_function=skill_function,
            skill_embedding=skill_embedding,
            skill_code=o['skill_code'],
            skill_code_base64=o['skill_code_base64']
        )


    def to_dict(self) -> JSONObject:
        # Storing pickled functions makes the skill library JSON huge and slow to write.
        # Default to NOT storing it; reconstruct from `skill_code` on load.
        # Set STARDOJO_STORE_SKILL_FUNCTION=1 if you need the legacy behavior.
        store_func = os.getenv("STARDOJO_STORE_SKILL_FUNCTION", "0") in ("1", "true", "True")
        skill_function_hex = dill.dumps(self.skill_function).hex() if store_func else ""
        skill_embedding_base64 = base64.b64encode(self.skill_embedding).decode('utf-8')

        out = {
            'skill_name': self.skill_name,
            'skill_embedding': skill_embedding_base64,
            'skill_code': self.skill_code,
            'skill_code_base64': self.skill_code_base64
        }
        if store_func:
            out["skill_function"] = skill_function_hex
        return out


    def to_json(self: W, *,
                encoder: Encoder = json.dumps,
                **encoder_kwargs) -> AnyStr:
        return json.dumps(self.to_dict(), **encoder_kwargs)


    @classmethod
    def from_json(cls: Type[W], s: AnyStr, *,
                  decoder: Any = json.loads,
                  **decoder_kwargs) -> W:
        return cls.from_dict(json.loads(s, **decoder_kwargs))


def post_skill_wait(wait_time = config.DEFAULT_POST_ACTION_WAIT_TIME):
    """Wait for skill to finish. Like if there is an animation"""
    time.sleep(wait_time)
