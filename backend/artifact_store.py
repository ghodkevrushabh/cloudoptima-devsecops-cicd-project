import os
import uuid
import zipfile
from pathlib import Path

import boto3


AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
ARTIFACT_BUCKET = os.getenv("ARTIFACT_BUCKET")


def create_iac_archive(app_name: str, generated_base_dir: str) -> str:
    """
    Create a ZIP archive containing only the generated Terraform
    and Ansible files for the requested application.

    Returns the local archive path.
    """

    base_dir = Path(generated_base_dir)
    terraform_dir = base_dir / "terraform" / app_name
    ansible_dir = base_dir / "ansible" / app_name

    if not terraform_dir.is_dir():
        raise FileNotFoundError(
            f"Terraform directory not found: {terraform_dir}"
        )

    if not ansible_dir.is_dir():
        raise FileNotFoundError(
            f"Ansible directory not found: {ansible_dir}"
        )

    archive_dir = base_dir / ".artifacts"
    archive_dir.mkdir(parents=True, exist_ok=True)

    archive_path = archive_dir / f"{app_name}-{uuid.uuid4().hex}.zip"

    with zipfile.ZipFile(
        archive_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:

        for source_dir in (terraform_dir, ansible_dir):
            for path in source_dir.rglob("*"):
                if not path.is_file():
                    continue

                # Never package Terraform state, plans, or secrets.
                if path.name.endswith(".tfstate"):
                    continue

                if path.name.endswith(".tfstate.backup"):
                    continue

                if path.suffix in {".pem", ".key"}:
                    continue

                archive.write(
                    path,
                    arcname=path.relative_to(base_dir),
                )

    return str(archive_path)


def upload_iac_archive(
    archive_path: str,
    app_name: str,
) -> str:
    """
    Upload an IaC ZIP archive to the dedicated artifact bucket.

    Returns the S3 object key.
    """

    if not ARTIFACT_BUCKET:
        raise RuntimeError(
            "ARTIFACT_BUCKET is not configured"
        )

    archive = Path(archive_path)

    if not archive.is_file():
        raise FileNotFoundError(
            f"Archive not found: {archive}"
        )

    request_id = uuid.uuid4().hex

    s3_key = (
        f"requests/{app_name}/{request_id}/"
        f"{archive.name}"
    )

    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
    )

    s3.upload_file(
        str(archive),
        ARTIFACT_BUCKET,
        s3_key,
    )

    return s3_key
