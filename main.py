import os
import subprocess
import sys

def run_cmd(command):
    print(f"[RUN] {command}")
    res = subprocess.run(command, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[OK] {res.stdout.strip()}")
    else:
        print(f"[ERROR] {res.stderr.strip()}")
    return res.returncode

def setup_environment():
    beta_dir = "/var/www/beta-app/html"
    internal_dir = "/var/www/internal-app/html"
    
    os.makedirs(beta_dir, exist_ok=True)
    os.makedirs(internal_dir, exist_ok=True)
    
    beta_html = """<!DOCTYPE html>
<html>
<head>
    <title>Beta App</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Trang kiểm thử ứng dụng (Beta App)</h1>
    <p>Chạy trên cổng 8080</p>
</body>
</html>"""

    internal_html = """<!DOCTYPE html>
<html>
<head>
    <title>Internal App</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Trang thông tin nội bộ (Internal App)</h1>
    <p>Chạy trên cổng 8090</p>
</body>
</html>"""

    with open(os.path.join(beta_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(beta_html)
        
    with open(os.path.join(internal_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(internal_html)

    nginx_conf = """server {
    listen 8080;
    listen [::]:8080;

    server_name _;
    root /var/www/beta-app/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 8090;
    listen [::]:8090;

    server_name _;
    root /var/www/internal-app/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
"""

    conf_file = "/etc/nginx/sites-available/multi-port.conf"
    enabled_link = "/etc/nginx/sites-enabled/multi-port.conf"

    try:
        with open(conf_file, "w", encoding="utf-8") as f:
            f.write(nginx_conf)
        print(f"Đã ghi cấu hình Nginx vào {conf_file}")
    except PermissionError:
        print("Cần quyền root (sudo) để ghi file cấu hình Nginx!")
        sys.exit(1)

    if not os.path.exists(enabled_link):
        os.symlink(conf_file, enabled_link)
        print(f"Đã tạo symlink {enabled_link}")

    run_cmd("ufw allow 8080/tcp")
    run_cmd("ufw allow 8090/tcp")

    if run_cmd("nginx -t") == 0:
        run_cmd("systemctl reload nginx")
        print("Cấu hình Nginx hoàn tất thành công!")

if __name__ == "__main__":
    setup_environment()
