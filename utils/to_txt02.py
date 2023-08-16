
import os

def txt2mung(txtpath):
    Name_y_x = []
    f = open(txtpath,'r')
    for line in f.readlines():
        Name_y_x_ = []
        line = line.strip('\n').split()
        Name_y_x_.append(line[0])
        box_ymid = int(float(line[4]) + float(line[2])) / 2
        box_xmid = int(float(line[3]) + float(line[1])) / 2
        Name_y_x_.append(box_ymid)
        Name_y_x_.append(box_xmid)
        Name_y_x.append(Name_y_x_)
    Name_y_x = sorted(Name_y_x, key=lambda x: (x[1], x[2]))
    print(Name_y_x)
    math_list = []
    for i in range(len(Name_y_x)):
        if i != 0:
            math = Name_y_x[i][1] - Name_y_x[i-1][1]
            if math > 70:
                math_list.append(i)
    _list = []
    _list_name = []

    a = 0
    while a <= len(math_list):
        _list.append([])
        _list_name.append([])
        if a == 0:
            for i in range(0,math_list[a]):
                _list[a].append(Name_y_x[i])
                _list[a] = sorted(_list[a],key=lambda x: (x[2]))
            for j in range(len(_list[a])):
                _list_name[a].append(_list[a][j][0])
        elif a == len(math_list):
            for i in range(math_list[a-1],len(Name_y_x)):
                _list[a].append(Name_y_x[i])
                _list[a] = sorted(_list[a], key=lambda x: (x[2]))
            for j in range(len(_list[a])):
                _list_name[a].append(_list[a][j][0])
        else:
            for i in range(math_list[a-1],math_list[a]):
                _list[a].append(Name_y_x[i])
                _list[a] = sorted(_list[a], key=lambda x: (x[2]))
            for j in range(len(_list[a])):
                _list_name[a].append(_list[a][j][0])
        a+=1

    return _list_name


def creat_txt(txt01_path,mung_path,list_img):
    txt_01 = os.listdir(txt01_path)
    if '.DS_Store' in txt_01:
        txt_01.remove('.DS_Store')
    txt_01.sort(key=lambda x: int(x[:-4]))
    imgs_infor = []
    for txt in txt_01:
        img_information = []
        txtpath = os.path.join(txt01_path,txt)
        list_ = txt2mung(txtpath)
        img_information.append(list_img)
        img_information.append(list_)
        imgs_infor.append(img_information)
        txt_name = os.path.join(mung_path,txt)
        with open(txt_name,'w') as f:
            _str = ''
            for line in range(len(list_)):
                _list = list_[line]
                _str = ''
                for i in _list:
                    _str = _str + i + ','
                _str = _str.replace(',', ' ').strip()
                f.write(_str + '\n')
            f.close()

    return imgs_infor


if __name__ == '__main__':
    labels_path = r"/Users/loufengbin/Documents/python/pythonProject/tensorflow/YOLO/yolov5-6.1/runs/detect/exp/labels"
    exp_path = r"/Users/loufengbin/Documents/python/pythonProject/tensorflow/YOLO/yolov5-6.1/runs/detect/exp"

    list_img = [12,34]

    mung_path = os.path.join(exp_path, "mung/")
    if not os.path.isdir(mung_path):
        os.mkdir(mung_path)
    creat_txt(labels_path,mung_path,list_img)