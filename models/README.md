# Local model adapters

The application intentionally does not download or invoke a cloud model. Install OmniShotCut v1.5 and optionally TransNet V2 using the maintainers' local instructions, then provide a command that writes JSON to stdout:

```json
{"boundaries": [{"frame": 1260, "confidence": 0.91}]}
```

For example:

```bash
python -m app.cli analyze input.mp4 \
  --omnishotcut-command 'python /opt/omnishotcut/run.py --input {video} --json-stdout'
```

The frame value must be the zero-based first frame of the new shot. The adapter process is local and is invoked once per detector; it is responsible for loading its model once. Model checkpoint licences and exact invocation options are model-distribution-specific, so no checkpoint is bundled in this repository.
