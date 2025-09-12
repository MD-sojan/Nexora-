import hashlib, magic, json, pefile
from fastapi import UploadFile
from app.utils.strings import extract_strings
from app.utils.ioc_extractor import extract_iocs
from app.services.gpt_service import ask_gpt

async def analyze_file(file: UploadFile):
    content = await file.read()

    # Hashes
    md5 = hashlib.md5(content).hexdigest()
    sha1 = hashlib.sha1(content).hexdigest()
    sha256 = hashlib.sha256(content).hexdigest()

    # MIME type
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(content)

    # Extract strings + IoCs
    strings = extract_strings(content)
    iocs = extract_iocs(strings)

    # PE file parsing (optional)
    pe_info = None
    if mime_type == "application/x-dosexec":
        pe = pefile.PE(data=content)
        pe_info = {"entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}

    analysis = {
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
    {json.dumps(analysis, indent=2)}
    """

    verdict = ask_gpt(prompt)

    return {"analysis": analysis, "gpt_verdict": verdict}
