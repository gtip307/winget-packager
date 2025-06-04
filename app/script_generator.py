import zipfile
from pathlib import Path
from datetime import datetime

INSTALL_TEMPLATE = """winget install --id={APP_ID} --silent --accept-source-agreements --accept-package-agreements

$TaskName = "WingetAutoUpdate"
$TaskExists = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if (-not $TaskExists) {{
    $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -Command \"winget upgrade --all --silent --accept-source-agreements --accept-package-agreements\""
    $Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3am
    Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description "Weekly Winget Auto Update" -User "SYSTEM" -RunLevel Highest -Force
}}
"""

UNINSTALL_TEMPLATE = """winget uninstall --id={APP_ID} --silent
"""

DETECTION_TEMPLATE = """$packageName = "{APP_NAME}"

$installed = winget list --name $packageName | Select-String $packageName

if ($installed) {{
    exit 0  # detected
}} else {{
    exit 1  # not detected
}}
"""

def generate_script_package(app_id: str, app_name: str) -> str:
    slug = f"{app_id.replace('.', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    output_dir = Path(f"./output/{slug}")
    output_dir.mkdir(parents=True, exist_ok=True)

    install_script = INSTALL_TEMPLATE.format(APP_ID=app_id)
    uninstall_script = UNINSTALL_TEMPLATE.format(APP_ID=app_id)
    detection_script = DETECTION_TEMPLATE.format(APP_NAME=app_name)

    (output_dir / "install.ps1").write_text(install_script)
    (output_dir / "uninstall.ps1").write_text(uninstall_script)
    (output_dir / "detection.ps1").write_text(detection_script)

    zip_path = f"./output/{slug}.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(output_dir / "install.ps1", arcname="install.ps1")
        zipf.write(output_dir / "uninstall.ps1", arcname="uninstall.ps1")
        zipf.write(output_dir / "detection.ps1", arcname="detection.ps1")

    return zip_path
