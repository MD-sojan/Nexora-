from pydantic import BaseModel
from typing import Dict, List, Optional

class AnalysisRequest(BaseModel):
    file_name: str
    file_size: int

class AnalysisResult(BaseModel):
    hashes: Dict[str, str]
    mime_type: str
    iocs: Dict[str, List[str]]
    strings_sample: List[str]
    pe_info: Optional[Dict]
    gpt_verdict: str
