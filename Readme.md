# Create Admin user
```curl
curl -X POST http://127.0.0.1:5000/auth/admin/register -H "Content-Type: application/json" -H "X-API-KEY: api-key" -d "{\"name\":\"Super Admin\",\"email\":\"test@gmail.com\",\"password\":\"test\"}"
```

# run docker container
```bash
docker run --name mysql-ecommerce -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=e_commerce -e MYSQL_USER=e_commerce -e MYSQL_PASSWORD=password -p 3306:3306 -d mysql:8.0
```