import hashlib, magic, json, pefile
from fastapi import UploadFile
from app.utils.strings import extract_strings
from app.utils.ioc_extractor import extract_iocs
from app.services.gpt_service import ask_gpt
from app.models.analysis import AnalysisResult
from starlette.concurrency import run_in_threadpool

async def analyze_file(file: UploadFile):
    content = await file.read()

    # Hashes
    md5 = await run_in_threadpool(lambda: hashlib.md5(content).hexdigest())
    sha1 = await run_in_threadpool(lambda: hashlib.sha1(content).hexdigest())
    sha256 = await run_in_threadpool(lambda: hashlib.sha256(content).hexdigest())

    # MIME type
    mime = magic.Magic(mime=True)
    mime_type = await run_in_threadpool(mime.from_buffer, content)

    # Extract strings + IoCs
    strings = await run_in_threadpool(extract_strings, content)
    iocs = await run_in_threadpool(extract_iocs, strings)

    # PE file parsing (optional)
    pe_info = None
    if mime_type == "application/x-dosexec":
        pe = await run_in_threadpool(pefile.PE, data=content)
        pe_info = {"entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}

    # Use a different variable name to avoid conflict with the final AnalysisResult object
    analysis_data = {
        "hashes": {"md5": md5, "sha1": sha1, "sha256": sha256},
        "mime_type": mime_type,
        "iocs": iocs,
        "strings_sample": strings[:50],
        "pe_info": pe_info,
    }

    # Send to GPT for verdict
    prompt = f"""
    Analyze this static malware report.
    1. Human-friendly summary
    2. Structured JSON verdict (malicious/suspicious/clean + reasons)

    Report:
    {json.dumps(analysis_data, indent=2)}
    """

    verdict = await run_in_threadpool(ask_gpt, prompt)

    return AnalysisResult(
        hashes=analysis_data["hashes"],
        mime_type=analysis_data["mime_type"],
        iocs=analysis_data["iocs"],
        strings_sample=analysis_data["strings_sample"],
        pe_info=analysis_data["pe_info"],
        gpt_verdict=verdict,
    )

