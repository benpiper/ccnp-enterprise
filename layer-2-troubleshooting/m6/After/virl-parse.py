from lxml import etree as ET
import glob
import re
import os
from collections import defaultdict


file_pattern = input("pattern to search: ")
file_list = glob.glob(f'*{file_pattern}*.virl')

for file_name in file_list:

    node_interface = defaultdict(list)
    node_details = defaultdict(list)
    connections = []
    nodes = []
    node = ""

    with open(file_name) as file:
        virl_xml = file.read()
    directory = file_name.replace(".", "_")
    try:
        os.mkdir(directory)
    except:
        pass

    # remove the <!--comment-->, which causes the parse to crash
    virl_xml = re.sub(r"<!--.+-->", "", virl_xml)
    root = ET.fromstring(bytes(virl_xml, encoding='utf-8'))

    # remove namespace
    for elem in root.getiterator():
        elem.tag = ET.QName(elem).localname
        ET.cleanup_namespaces(root)

    # extract node, interface, and config info from xml
    for x in root.xpath("//node|//interface|//entry[@key='config']"):
        if x.tag == "node":
            node = x.attrib['name']
            node_details[node] = x.attrib['subtype']
            nodes.append(node)
        elif x.tag == "interface":
            node_interface[node].append(x.attrib['name'])
        elif x.tag == "entry":
            with open(f"{directory}/{node}-config.txt", "w") as config:
                config.write(x.text)

    # device interface connections
    for y in root.xpath("//connection"):
        dst_conn = re.findall("[0-9]{1,2}", str(y.attrib['dst']))
        src_conn = re.findall("[0-9]{1,2}", str(y.attrib['src']))
        src_node = nodes[int(src_conn[0])-1]
        dst_node = nodes[int(dst_conn[0])-1]
        src_int = node_interface[src_node][int(src_conn[1])-1]
        dst_int = node_interface[dst_node][int(dst_conn[1])-1]
        connections.append(f"{src_node},{src_int},{dst_node},{dst_int}")


    with open (f"{directory}/devices.csv", "w") as device_file:
        for d, e in node_interface.items():
            device_file.write(f"{d},{node_details[d]},")
            for f in e:
                device_file.write(f"{f},")
            device_file.write("\n")

    with open(f"{directory}/connections.csv", "w") as connections_file:
        for a in connections:
            connections_file.write(f"{a}\n")
