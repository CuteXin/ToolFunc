# 方案为修改docker源为镜像源（如果服务名称不为docker.service, 则替换docker.service

# 确保有docker路径
mkdir -p /etc/docker
# 重置docker服务状态
systemctl reset-failed docker.service
# 编辑配置文件
cat >/etc/docker/daemon.json <<'EOF'
{
    "registry-mirrors": [
        "https://docker.1ms.run"
    ]
}
EOF
# 重新加载systemd配置
systemctl daemon-reload
# 重启Docker服务
systemctl restart docker.service
# 检查状态
systemctl status docker.service

#恢复原设置（卸载以上配置
rm /etc/docker/daemon.json
systemctl restart docker.service
