"""Optional independent JSON Schema check; uses an installed jsonschema package."""
from pathlib import Path
import hashlib
import json
from jsonschema import Draft202012Validator

root = Path(__file__).resolve().parent.parent
export = root / 'lyrics/site-export'
schema_path = export / 'timed-lyrics.schema.json'
schema = json.loads(schema_path.read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema)
files = sorted((export / 'tracks').glob('*.json')) + [export / 'full-album.json']
for path in files:
    validator.validate(json.loads(path.read_text()))
report = {
    'passed': True,
    'documents': len(files),
    'schema': 'JSON Schema 2020-12',
    'validator': 'Python jsonschema / Draft202012Validator',
    'schemaSha256': hashlib.sha256(schema_path.read_bytes()).hexdigest(),
}
(root / 'checks/lyrics-schema.json').write_text(json.dumps(report, indent=2) + '\n')
print(f'Schema validated: {len(files)} lyric documents.')
