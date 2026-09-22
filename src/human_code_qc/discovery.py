import zipfile
import json
import logging
import os
from collections import defaultdict
from typing import Dict, List, Optional, Any, Set, Tuple
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class DiscoveryRecord(BaseModel):
    solution_id: Optional[str] = None
    problem_id: Optional[str] = None
    language: Optional[str] = None
    code_path: Optional[str] = None
    metadata_path: Optional[str] = None
    code_present: bool = False
    metadata_present: bool = False
    code_size: int = 0
    metadata_size: int = 0
    metadata_parseable: bool = False
    schema_fingerprint: Optional[str] = None
    repository: Optional[str] = None
    error: Optional[str] = None

class DiscoveryReport(BaseModel):
    total_entries: int = 0
    directories: int = 0
    code_files: int = 0
    metadata_files: int = 0
    other_files: int = 0
    files_by_extension: Dict[str, int] = {}
    files_by_language: Dict[str, int] = {}
    valid_pairs: int = 0
    orphan_code: int = 0
    orphan_metadata: int = 0
    unique_solution_ids: int = 0
    unique_problem_ids: int = 0
    solutions_per_language: Dict[str, int] = {}
    solutions_per_problem: Dict[str, int] = {}
    problem_language_matrix: Dict[str, Dict[str, bool]] = {}
    unexpected_paths: List[str] = []
    unexpected_extensions: List[str] = []
    schema_fingerprints: Dict[str, int] = {}

class ZipInspector:
    def __init__(self, archive_path: str):
        self.archive_path = archive_path
        self.CODE_EXTENSIONS = {'.c': 'c', '.cpp': 'cpp', '.java': 'java', '.js': 'javascript', '.py': 'python'}
        
    def safe_inventory(self) -> Dict[str, Any]:
        """Safely enumerates the ZIP without extracting."""
        inventory = {
            "directories": set(),
            "code_files": set(),
            "metadata_files": set(),
            "other_files": set(),
            "sizes": {},
            "errors": []
        }
        
        seen_names = set()
        
        with zipfile.ZipFile(self.archive_path, 'r') as zf:
            for info in zf.infolist():
                path = info.filename
                
                # Security checks
                if path.startswith('/') or path.startswith('\\') or ".." in path:
                    inventory["errors"].append(f"Suspicious path rejected: {path}")
                    continue
                if path in seen_names:
                    inventory["errors"].append(f"Duplicate member: {path}")
                    continue
                seen_names.add(path)
                
                if info.is_dir():
                    inventory["directories"].add(path)
                    continue
                    
                inventory["sizes"][path] = info.file_size
                
                if path.endswith(".meta.json"):
                    inventory["metadata_files"].add(path)
                else:
                    ext = os.path.splitext(path)[1].lower()
                    if ext in self.CODE_EXTENSIONS:
                        inventory["code_files"].add(path)
                    else:
                        inventory["other_files"].add(path)
                        
        return inventory

class MetadataParser:
    def __init__(self, archive_path: str):
        self.archive_path = archive_path
        
    def parse(self, metadata_path: str) -> Dict[str, Any]:
        with zipfile.ZipFile(self.archive_path, 'r') as zf:
            try:
                with zf.open(metadata_path) as f:
                    content = f.read().decode('utf-8')
                    data = json.loads(content)
                    if not isinstance(data, dict):
                        return {"error": "JSON root is not an object"}
                    
                    schema_keys = sorted(data.keys())
                    fingerprint = ",".join(schema_keys)
                    
                    # Extract fields resiliently
                    solution_id = data.get("solutionId")
                    problem_id = data.get("problemId") or (data.get("problem", {}).get("problemId") if isinstance(data.get("problem"), dict) else None)
                    lang = data.get("language")
                    repo = data.get("repository", {}).get("url") if isinstance(data.get("repository"), dict) else None
                    
                    return {
                        "solution_id": str(solution_id) if solution_id else None,
                        "problem_id": str(problem_id) if problem_id else None,
                        "language": lang,
                        "repository": repo,
                        "fingerprint": fingerprint,
                        "parseable": True
                    }
            except Exception as e:
                return {"error": str(e), "parseable": False}

class RecordPairer:
    def __init__(self, inventory: Dict[str, Any]):
        self.inventory = inventory
        self.CODE_EXTENSIONS = {'.c': 'c', '.cpp': 'cpp', '.java': 'java', '.js': 'javascript', '.py': 'python'}
        
    def pair_records(self) -> List[DiscoveryRecord]:
        code_files = sorted(list(self.inventory["code_files"]))
        metadata_files = sorted(list(self.inventory["metadata_files"]))
        
        records_by_base = {}
        
        for cp in code_files:
            base = os.path.splitext(cp)[0]
            records_by_base[base] = DiscoveryRecord(
                code_path=cp,
                code_present=True,
                code_size=self.inventory["sizes"].get(cp, 0),
                language=self.CODE_EXTENSIONS.get(os.path.splitext(cp)[1].lower())
            )
            
        for mp in metadata_files:
            if mp.endswith(".meta.json"):
                base = mp[:-10]  # strip ".meta.json"
                if base in records_by_base:
                    rec = records_by_base[base]
                    rec.metadata_path = mp
                    rec.metadata_present = True
                    rec.metadata_size = self.inventory["sizes"].get(mp, 0)
                else:
                    records_by_base[base] = DiscoveryRecord(
                        metadata_path=mp,
                        metadata_present=True,
                        metadata_size=self.inventory["sizes"].get(mp, 0)
                    )
                    
        # Sort output deterministically
        return [records_by_base[k] for k in sorted(records_by_base.keys())]

def run_discovery(archive_path: str, limit: int = 0) -> Tuple[List[DiscoveryRecord], DiscoveryReport]:
    inspector = ZipInspector(archive_path)
    inventory = inspector.safe_inventory()
    
    pairer = RecordPairer(inventory)
    records = pairer.pair_records()
    
    if limit > 0:
        records = records[:limit]
        
    parser = MetadataParser(archive_path)
    
    report = DiscoveryReport()
    report.total_entries = len(inventory["directories"]) + len(inventory["code_files"]) + len(inventory["metadata_files"]) + len(inventory["other_files"])
    report.directories = len(inventory["directories"])
    report.code_files = len(inventory["code_files"])
    report.metadata_files = len(inventory["metadata_files"])
    report.other_files = len(inventory["other_files"])
    report.unexpected_paths = inventory["errors"]
    
    # Extension counting
    for cf in inventory["code_files"]:
        ext = os.path.splitext(cf)[1].lower()
        report.files_by_extension[ext] = report.files_by_extension.get(ext, 0) + 1
        
    for of in inventory["other_files"]:
        ext = os.path.splitext(of)[1].lower()
        report.unexpected_extensions.append(ext)
    report.unexpected_extensions = sorted(list(set(report.unexpected_extensions)))
    
    # Enrich records and build stats
    sol_ids = set()
    prob_ids = set()
    
    for rec in records:
        if rec.code_present and rec.metadata_present:
            report.valid_pairs += 1
        elif rec.code_present:
            report.orphan_code += 1
        elif rec.metadata_present:
            report.orphan_metadata += 1
            
        if rec.metadata_present and rec.metadata_path:
            meta_info = parser.parse(rec.metadata_path)
            rec.metadata_parseable = meta_info.get("parseable", False)
            if rec.metadata_parseable:
                rec.schema_fingerprint = meta_info.get("fingerprint")
                rec.solution_id = meta_info.get("solution_id")
                rec.problem_id = meta_info.get("problem_id")
                rec.repository = meta_info.get("repository")
                
                if meta_info.get("language") and not rec.language:
                    rec.language = meta_info.get("language").lower()
            else:
                rec.error = meta_info.get("error")
                
        if rec.language:
            report.files_by_language[rec.language] = report.files_by_language.get(rec.language, 0) + 1
            if rec.code_present and rec.metadata_present:
                report.solutions_per_language[rec.language] = report.solutions_per_language.get(rec.language, 0) + 1
                
        if rec.solution_id:
            sol_ids.add(rec.solution_id)
        if rec.problem_id:
            prob_ids.add(rec.problem_id)
            report.solutions_per_problem[rec.problem_id] = report.solutions_per_problem.get(rec.problem_id, 0) + 1
            
            if rec.language:
                if rec.problem_id not in report.problem_language_matrix:
                    report.problem_language_matrix[rec.problem_id] = {}
                report.problem_language_matrix[rec.problem_id][rec.language] = True
                
        if rec.schema_fingerprint:
            report.schema_fingerprints[rec.schema_fingerprint] = report.schema_fingerprints.get(rec.schema_fingerprint, 0) + 1

    report.unique_solution_ids = len(sol_ids)
    report.unique_problem_ids = len(prob_ids)
    
    return records, report
