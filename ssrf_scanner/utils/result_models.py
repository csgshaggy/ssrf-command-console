from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ProbeResult:
    url: str
    status: Optional[int]
    elapsed: float
    error: Optional[str]
    content_preview: str
    headers: Dict[str, str]

    def is_timeout(self) -> bool:
        return self.error == "timeout"

    def is_connection_error(self) -> bool:
        return self.error == "connection_error"

    def is_empty(self) -> bool:
        return not self.content_preview.strip()
