# Bài 4: Chạy song song nhiều cổng dịch vụ (Nginx Virtual Hosts)

## Giới thiệu
Bài tập này triển khai hai môi trường ứng dụng tĩnh độc lập trên cùng một máy chủ (Droplet):
1. **Beta App**: Chạy trên cổng `8080`, lưu trữ tại `/var/www/beta-app/html/`
2. **Internal App**: Chạy trên cổng `8090`, lưu trữ tại `/var/www/internal-app/html/`

## Cấu trúc thư mục dự án
```
. 
├── README.md
├── setup.py
├── multi-port.conf
├── beta_index.html
└── internal_index.html
```

## Hướng dẫn triển khai tự động

1. Yêu cầu quyền root hoặc `sudo` để thao tác với Nginx và UFW.
2. Chạy file Python tự động thiết lập:
```bash
sudo python3 setup.py
```

## Hướng dẫn triển khai thủ công

1. Tạo thư mục chứa mã nguồn:
```bash
sudo mkdir -p /var/www/beta-app/html
sudo mkdir -p /var/www/internal-app/html
```

2. Sao chép nội dung file HTML vào thư mục tương ứng:
```bash
sudo cp beta_index.html /var/www/beta-app/html/index.html
sudo cp internal_index.html /var/www/internal-app/html/index.html
```

3. Cấu hình Nginx:
```bash
sudo cp multi-port.conf /etc/nginx/sites-available/multi-port.conf
sudo ln -sf /etc/nginx/sites-available/multi-port.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

4. Mở cổng tường lửa UFW:
```bash
sudo ufw allow 8080/tcp
sudo ufw allow 8090/tcp
```

## Kiểm tra kết quả
Sử dụng lệnh `curl` để kiểm tra kết quả phản hồi từ hai cổng:
```bash
curl http://localhost:8080
curl http://localhost:8090
```