
import xml.etree.ElementTree as ET
import os
import imgaug as ia
import numpy as np
import shutil
from tqdm import tqdm
from PIL import Image
from imgaug import augmenters as iaa

ia.seed(1)

def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id))
    tree = ET.parse(in_file)  #xml读取待修改文件
    root = tree.getroot() #获取根节点
    bndboxlist = []

    for object in root.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        xmin = int(bndbox.find('xmin').text)
        xmax = int(bndbox.find('xmax').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        # print(xmin,ymin,xmax,ymax)
        bndboxlist.append([xmin, ymin, xmax, ymax])
        # print(bndboxlist)

    bndbox = root.find('object').find('bndbox')
    return bndboxlist


def change_xml_annotation(root, image_id, new_target):
    new_xmin = new_target[0]
    new_ymin = new_target[1]
    new_xmax = new_target[2]
    new_ymax = new_target[3]

    in_file = open(os.path.join(root, str(image_id) + '.xml'))  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    object = xmlroot.find('object')
    bndbox = object.find('bndbox')
    xmin = bndbox.find('xmin')
    xmin.text = str(new_xmin)
    ymin = bndbox.find('ymin')
    ymin.text = str(new_ymin)
    xmax = bndbox.find('xmax')
    xmax.text = str(new_xmax)
    ymax = bndbox.find('ymax')
    ymax.text = str(new_ymax)
    tree.write(os.path.join(root, str("%06d" % (str(id) + '.xml')))) #写回到原文件


def change_xml_list_annotation(root, image_id, new_target, saveroot, id):
    in_file = open(os.path.join(root, str(image_id) + '.xml'))  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    elem = tree.find('filename')  # 修改增强后的xml文件中的filename
    elem.text = (str(id) + '.jpg')
    xmlroot = tree.getroot()
    elem = tree.find('path') # 修改增强后的xml文件中的path
    if elem != None:
        elem.text = (saveroot + str(id) + '.jpg')

    index = 0
    for object in xmlroot.findall('object'):  # 找到root节点下的所有country节点
        bndbox = object.find('bndbox')  # 子节点下节点rank的值

        # xmin = int(bndbox.find('xmin').text)
        # xmax = int(bndbox.find('xmax').text)
        # ymin = int(bndbox.find('ymin').text)
        # ymax = int(bndbox.find('ymax').text)

        new_xmin = new_target[index][0]
        new_ymin = new_target[index][1]
        new_xmax = new_target[index][2]
        new_ymax = new_target[index][3]

        xmin = bndbox.find('xmin')
        xmin.text = str(new_xmin)
        ymin = bndbox.find('ymin')
        ymin.text = str(new_ymin)
        xmax = bndbox.find('xmax')
        xmax.text = str(new_xmax)
        ymax = bndbox.find('ymax')
        ymax.text = str(new_ymax)

        index = index + 1

    tree.write(os.path.join(saveroot, str(id + '.xml')))


def mkdir(path):

    path = path.strip()   # 去除首位空格
    path = path.rstrip("\\")  # 去除尾部 \ 符号
    isExists = os.path.exists(path)  # 判断路径是否存在(存在True)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


if __name__ == "__main__":

    IMG_DIR = "D:/YOLO/VOC2007/image/img_3"  # 图片路径
    XML_DIR = "D:/YOLO/VOC2007/image/xml_3"  # 标签路径，voc格式

    AUG_XML_DIR = "D:/YOLO/VOC2007/augmentation/xml_3"  # 存储增强后的XML文件夹路径
    try:
        shutil.rmtree(AUG_XML_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_XML_DIR)

    AUG_IMG_DIR = "D:/YOLO/VOC2007/augmentation/img_3"  # 存储增强后的影像文件夹路径
    try:
        shutil.rmtree(AUG_IMG_DIR)
    except FileNotFoundError as e:
        a = 1
    mkdir(AUG_IMG_DIR)

    AUGLOOP = 3   # 每张影像增强的数量

    boxes_img_aug_list = []
    new_bndbox = []
    new_bndbox_list = []

    # 产生一个处理图像的sequential，里面定义各种用于数据增强的方法
    seq = iaa.Sequential([
        # 随机选择1到3种方法做变换，每个batch中的Augmenters顺序不一样
        iaa.SomeOf((1,3),
                   [
                       iaa.imgcorruptlike.MotionBlur(severity=(1, 2)),  # 像素移动模糊
                       iaa.Clouds(),  # 云雾
                       iaa.Rain(drop_size=(0.3, 0.6), speed=(0.05, 0.1)),  # 雨
                       iaa.Snowflakes(flake_size=(0.3, 0.6), speed=(0.2, 0.5)),  # 雪点
                       iaa.imgcorruptlike.Fog(severity=(1, 2)),  # 多雾/霜
                       iaa.imgcorruptlike.Snow(severity=(1, 2)),  # 大雪
                       iaa.imgcorruptlike.DefocusBlur(severity=(1, 2)), #虚焦
                       iaa.AdditiveGaussianNoise(scale=0.1 * 255, per_channel=True),  #添加拉普拉斯噪声到图像中，信道从N（0，0.result*255）中采样。



                       # 对比度 亮度 饱和度 选其一
                       iaa.SomeOf((1, 1),
                                  [
                                      iaa.imgaug.augmenters.contrast.LinearContrast((0.5, 2), per_channel=0.5), # 图像对比度变为原来的一半或者二倍
                                      iaa.imgcorruptlike.Brightness(severity=(1, 2)),  # 图像亮度增加
                                      iaa.imgcorruptlike.Saturate(severity=(1, 2)),  # 色彩饱和度
                                  ]
                                  )
                   ],
                   # 随机顺序运行augmentations
                   random_order=True
                   )
    ], random_order=True)  # 随机运行augmenters数量

    for name in tqdm(os.listdir(XML_DIR), desc='Processing'):

        bndbox = read_xml_annotation(XML_DIR, name)

        # 保存原xml文件
        # shutil.copy(os.path.join(XML_DIR, name), AUG_XML_DIR)
        # 保存原图
        og_img = Image.open(IMG_DIR + '/' + name[:-4] + '.jpg')
        # og_img.convert('RGB').save(AUG_IMG_DIR + name[:-4] + '.jpg', 'JPEG') #原图和影像增强图保存在一起
        og_xml = open(os.path.join(XML_DIR, name))
        tree = ET.parse(og_xml)
        # 修改增强后的xml文件中的filename
        elem = tree.find('filename')
        elem.text = (name[:-4] + '.jpg')
        # tree.write(os.path.join(AUG_XML_DIR, name)) #原xml与增强后xml保存同一文件

        for epoch in range(AUGLOOP):
            seq_det = seq.to_deterministic()  # 保持坐标和图像同步改变，而不是随机
            # 读取图片
            img = Image.open(os.path.join(IMG_DIR, name[:-4] + '.jpg'))
            # sp = img.size
            img = np.asarray(img)
            # bndbox 坐标增强
            for i in range(len(bndbox)):
                bbs = ia.BoundingBoxesOnImage([
                    ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2], y2=bndbox[i][3]),
                ], shape=img.shape)

                bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                boxes_img_aug_list.append(bbs_aug)

                # new_bndbox_list:[[x1,y1,x2,y2],...[],[]]
                n_x1 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x1)))
                n_y1 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y1)))
                n_x2 = int(max(1, min(img.shape[1], bbs_aug.bounding_boxes[0].x2)))
                n_y2 = int(max(1, min(img.shape[0], bbs_aug.bounding_boxes[0].y2)))
                if n_x1 == 1 and n_x1 == n_x2:
                    n_x2 += 1
                if n_y1 == 1 and n_y2 == n_y1:
                    n_y2 += 1
                if n_x1 >= n_x2 or n_y1 >= n_y2:
                    print('error', name)
                new_bndbox_list.append([n_x1, n_y1, n_x2, n_y2])
            # 存储变化后的图片
            image_aug = seq_det.augment_images([img])[0]
            path = os.path.join(AUG_IMG_DIR,
                                str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            image_auged = bbs.draw_on_image(image_aug, size=0)
            Image.fromarray(image_auged).convert('RGB').save(path)

            # 存储变化后的XML
            change_xml_list_annotation(XML_DIR, name[:-4], new_bndbox_list, AUG_XML_DIR,
                                       str(name[:-4]) + '_' + str(epoch))
            # print(str(str(name[:-4]) + '_' + str(epoch)) + '.jpg')
            new_bndbox_list = []
    print('Finish!')