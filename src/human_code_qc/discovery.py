import zipfile
import json
from .config import DATASET_PATH

class DatasetReader:
    def __init__(self, dataset_path=DATASET_PATH):
        self.dataset_path = dataset_path

    def iter_dataset(self):
        """
        Yields (filename_prefix, py_content_string, meta_json_dict)
        without extracting the archive to the disk.
        """
        if not self.dataset_path:
            raise ValueError("DATASET_PATH is not configured.")
            
        with zipfile.ZipFile(self.dataset_path, 'r') as zip_ref:
            all_files = zip_ref.namelist()
            
            entries = {}
            for f in all_files:
                if f.endswith('.py'):
                    prefix = f[:-3]
                    entries.setdefault(prefix, {})['py'] = f
                elif f.endswith('.meta.json'):
                    prefix = f[:-10]
                    entries.setdefault(prefix, {})['meta'] = f

            for prefix, files in entries.items():
                if 'py' in files and 'meta' in files:
                    with zip_ref.open(files['py']) as py_f:
                        py_content = py_f.read().decode('utf-8')
                    with zip_ref.open(files['meta']) as meta_f:
                        meta_content = json.loads(meta_f.read().decode('utf-8'))
                    
                    yield prefix, py_content, meta_content
