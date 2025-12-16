# 方案为修改docker源为镜像源（如果服务名称不为docker.service, 则替换docker.service

# 确保有docker路径
mkdir -p /etc/docker
# 重置docker服务状态
systemctl reset-failed docker.service
# 编辑配置文件
cat >/etc/docker/daemon.json <<'EOF'
{
  "data-root": "/mnt/.ix-apps/docker",
  "storage-driver": "overlay2",
  "registry-mirrors": [
    "https://docker.1panel.live",
    "https://docker.m.daocloud.io",
    "https://hub-mirror.c.163.com"
  ],
  "dns": ["8.8.8.8", "1.1.1.1"],
  "default-address-pools": [
    {
      "base": "172.17.0.0/12",
      "size": 24
    }
  ],
  "exec-opts": ["native.cgroupdriver=cgroupfs"],
  "iptables": true
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