import re
import sys
from pathlib import Path

def parse_ssh_config(filename):
    with open(filename, 'r') as file:
        content = file.read()

    parts = re.split(r'\n(?=Host\s)', content, flags=re.IGNORECASE)
    global_config = parts[0]
    host_blocks = parts[1:]

    return global_config, host_blocks

def sort_host_blocks(blocks):
    wildcard_hosts = []
    normal_hosts = []

    for block in blocks:
        host_match = re.match(r'Host\s+(.+)', block, re.IGNORECASE)
        if host_match:
            host = host_match.group(1)
            if '*' in host or '?' in host:
                wildcard_hosts.append((host, block))
            else:
                normal_hosts.append((host, block))

    normal_hosts.sort(key=lambda x: x[0].lower())

    return [block for _, block in normal_hosts + wildcard_hosts]

def write_sorted_config(filename, global_config, sorted_blocks):
    backup_file = filename.with_suffix(filename.suffix + '.bak')
    filename.rename(backup_file)

    with open(filename, 'w') as file:
        file.write(global_config)
        if not global_config.endswith('\n'):
            file.write('\n')
        file.write('\n'.join(sorted_blocks))

def main(filename):
    ssh_config = Path(filename).expanduser()
    if not ssh_config.is_file():
        print(f"錯誤：文件 {ssh_config} 不存在")
        return

    global_config, host_blocks = parse_ssh_config(ssh_config)
    sorted_blocks = sort_host_blocks(host_blocks)
    write_sorted_config(ssh_config, global_config, sorted_blocks)

    print(f"SSH 配置文件已排序。原文件備份為 {ssh_config.with_suffix(ssh_config.suffix + '.bak')}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python script.py <ssh_config_file>")
        sys.exit(1)
    main(sys.argv[1])
