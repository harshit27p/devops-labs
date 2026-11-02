# Project Structure and CLI Design

Suggested layout:
```text
aws-automation/
├── aws_automation/
│   ├── __init__.py
│   ├── config.py
│   ├── identity.py
│   ├── inventory/
│   ├── cleanup/
│   └── reporting/
├── tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

A useful CLI might expose:
```text
python -m aws_automation inventory --services ec2,s3 --region ap-south-1
python -m aws_automation cleanup-plan --policy policies/lab.yaml
python -m aws_automation cleanup-plan --policy policies/lab.yaml --execute
```

The execute flag should be unavailable unless account, region, policy and approval checks pass. Keep inventory and cleanup commands separate.

Exercises: design argparse subcommands, validate region/account and write a machine-readable report.
