import sys
import socket
from urllib.parse import urlparse

def main():
    url = sys.argv[1]
    resp = get(url)
    header, body = divide_http_header_body(resp)
    if (is_response_OK(header)):
        file_buffer = 2048
        write_to_file(body.encode(), "content_file", file_buffer)
        print(header)
    else:
        print("FAIL")

def get(dest_url):
    encod_const = "utf-8"
    sock = make_get_request(dest_url, encod_const)
    response_data = read_all_data_binnary(sock, encod_const)
    return response_data.decode(encod_const)


def make_get_request(dest_url, encodding):
    #prepare the request
    url_parts = urlparse(dest_url)
    netloc = url_parts.netloc
    http_request = "GET {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(url_parts.path, url_parts.netloc)
    #preapare the socket
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((netloc, 80))
    connection.sendall(http_request.encode(encodding))
    return connection


def read_all_data_binnary(sock, encodding):
    buffer_size = 4096
    result_data = bytearray()
    while (True):
        part_data = sock.recv(buffer_size)
        result_data += part_data
        if len(part_data) < buffer_size:
            return result_data


def divide_http_header_body(full_resp):
    row_by_row = full_resp.split("\r\n")
    empty_str_index = row_by_row.index("")
    res_header = "\r\n".join(row_by_row[:empty_str_index])
    res_body = "\r\n".join(row_by_row[empty_str_index+1:])
    return res_header, res_body


def is_response_OK(header):
    return "200 OK" in header


def write_to_file(content, file_name, buffer_size):
    with open(file_name, "wb", buffering=buffer_size) as file:
        file.write(content)

main()

