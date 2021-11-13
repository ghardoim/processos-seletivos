import requests as rq

def compare(version, latest_version):
    for i, v in enumerate(version):
        if int(v) > int(latest_version[i]):
            return False
        elif int(v) < int(latest_version[i]):
            return True
        else: continue

with open("requirements.txt", "r") as requirements:
    libs_infos = []
    for line in requirements.readlines():
        line = line.replace("[standard]", "")
        if not line.startswith("\n"):
            lib, version = tuple(line.split("==") if "==" in line else line.split(">=") if ">=" in line else [line.strip(),  "latest"])
            latest_version = rq.get(f"https://pypi.org/pypi/{lib}/json").json()["info"]["version"]
            version = version.strip()
            libs_infos.append({
                "packageName": f"{lib.strip()}",
                "currentVersion": f"{version}",
                "latestVersion": f"{latest_version}",
                "outOfDate": False if "latest" in version else compare(version.split("."), latest_version.split("."))
            })
    print(libs_infos)