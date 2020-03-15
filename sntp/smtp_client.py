import socket
import struct
import time


SERVER = "0.uk.pool.ntp.org"
BEGIN = 2208988800
PORT = 123


def main():
    time_deltas = []
    for i in range(10):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(5.0)
        data = '\x1b' + 47 * '\0'
        sent_time = time.time() + BEGIN
        client.sendto(data.encode('utf-8'), (SERVER, PORT))
        data, address = client.recvfrom(1024)
        receive_time = time.time() + BEGIN
        if not data:
            continue
        # print(len(data))
        response = list(struct.unpack('!4B11I', data))
        # print(response)
        stratum = response[1]
        reference = response[7] + response[8] * 10 ** (-len(str(response[8])))
        originate = response[9] + response[10] * 10 ** (-len(str(response[10])))
        receive = response[11] + response[12] * 10 ** (-len(str(response[12])))
        transmit = response[13] + response[14] * 10 ** (-len(str(response[14])))
        print("Stratum: {}, reference: {}, originate: {}, receive: {}, transmit: {}"
              .format(stratum, reference, originate, receive, transmit))

        delay = (receive_time - sent_time) + (transmit - receive) / 2
        # print("Delay: {}".format(delay))
        # print("Sent time: {}, receive_time: {}".format(sent_time, receive_time))
        new_time = transmit + delay
        time_deltas.append(new_time - receive_time)
    delta = sum(time_deltas) / len(time_deltas)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() + delta)))


if __name__ == "__main__":
    main()
