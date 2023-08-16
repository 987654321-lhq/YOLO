import os
from lxml.etree import Element, SubElement, tostring

def Sort(txt_path):
    Name_y_x = []
    f = open(txt_path, 'r')
    for line in f.readlines():
        Name_y_x_ = []
        line = line.strip('\n').split()
        Name_y_x_.append(line[0])

        box_ymid = int(float(line[2]) + float(line[4])) / 2
        box_xmid = int(float(line[3]) + float(line[1])) / 2
        Name_y_x_.append(box_ymid)
        Name_y_x_.append(box_xmid)
        Name_y_x_.append(line[1])
        Name_y_x_.append(line[2])
        Name_y_x_.append(line[3])
        Name_y_x_.append(line[4])
        Name_y_x.append(Name_y_x_)
    Name_y_x = sorted(Name_y_x, key=lambda x: (x[1], x[2]))

    math_list = []
    for i in range(len(Name_y_x)):
        if i != 0:
            math = Name_y_x[i][1] - Name_y_x[i - 1][1]
            if math > 50:
                math_list.append(i)

    _list = []
    _list_name = []
    a = 0
    while a <= len(math_list):
        _list.append([])
        # _list_name.append([])
        if a == 0:
            for i in range(0, math_list[a]):
                _list[a].append(Name_y_x[i])
                _list[a] = sorted(_list[a], key=lambda x: (x[2]))
            for j in range(len(_list[a])):
                _list_name.append(_list[a][j])
        elif a == len(math_list):
            for i in range(math_list[a - 1], len(Name_y_x)):
                _list[a].append(Name_y_x[i])
                _list[a] = sorted(_list[a], key=lambda x: (x[2]))
            for j in range(len(_list[a])):
                _list_name.append(_list[a][j])
        else:
            for i in range(math_list[a - 1], math_list[a]):
                _list[a].append(Name_y_x[i])
                _list[a] = sorted(_list[a], key=lambda x: (x[2]))
            for j in range(len(_list[a])):
                _list_name.append(_list[a][j])
        a += 1
    for i in range(len(_list_name)):
        index_to_delete = [1,2]
        for index in reversed(index_to_delete):
            _list_name[i].pop(index)
    print(_list_name)
    return _list_name

def create_xml(list_xml,list_images,save_dir,file_name):

    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'Images'
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = str(list_images[3])
    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(list_images[0])
    node_height = SubElement(node_size, 'height')
    node_height.text = str(list_images[1])
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(list_images[2])

    if len(list_xml)>=1:
        for list_ in list_xml:
            node_object = SubElement(node_root, 'object')
            node_name = SubElement(node_object, 'name')
            node_name.text = str(list_[0])
            node_difficult = SubElement(node_object, 'difficult')
            node_difficult.text = '0'
            node_bndbox = SubElement(node_object, 'bndbox')
            node_xmin = SubElement(node_bndbox, 'xmin')
            node_xmin.text = str(list_[1])
            node_ymin = SubElement(node_bndbox, 'ymin')
            node_ymin.text = str(list_[2])
            node_xmax = SubElement(node_bndbox, 'xmax')
            node_xmax.text = str(list_[3])
            node_ymax = SubElement(node_bndbox, 'ymax')
            node_ymax.text = str(list_[4])
    xml = tostring(node_root, pretty_print=True)
    xml_name = file_name.replace(".txt", '.xml')
    filename = save_dir + "/{}".format(xml_name)
    f = open(filename, "wb")
    f.write(xml)
    f.close()

def save_xml_file(txt_dir,list_images,save_dir):
    txt_01 = os.listdir(txt_dir)
    if '.DS_Store' in txt_01:
        txt_01.remove('.DS_Store')
    txt_01.sort(key=lambda x: int(x[:-4]))
    for txt in txt_01:
        txt_path = os.path.join(txt_dir,txt)
        Name_y_x = []
        f = open(txt_path, 'r')
        for line in f.readlines():
            Name_y_x_ = []
            line = line.strip('\n').split()
            Name_y_x_.append(line[0])

            box_ymid = int(float(line[2]) + float(line[4])) / 2
            box_xmid = int(float(line[3]) + float(line[1])) / 2
            Name_y_x_.append(box_ymid)
            Name_y_x_.append(box_xmid)
            Name_y_x_.append(line[1])
            Name_y_x_.append(line[2])
            Name_y_x_.append(line[3])
            Name_y_x_.append(line[4])
            Name_y_x.append(Name_y_x_)
        create_xml(Name_y_x,list_images,save_dir,txt)

if __name__ == '__main__':
    txt_dir = r"/Users/loufengbin/Documents/python/pythonProject/tensorflow/YOLO/yolov5-6.1/runs/detect/exp2/labels"
    save_dir = "/Users/loufengbin/Documents/python/pythonProject/tensorflow/YOLO/yolov5-6.1/runs/detect/exp/xml"

    save_xml_file(txt_dir,[640,640,3,'000001'],save_dir)








