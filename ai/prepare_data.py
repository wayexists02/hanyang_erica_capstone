import torch
from torchvision import datasets, transforms
from torch.utils.data import SubsetRandomSampler
from PIL import Image
import numpy as np
import pathlib
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os

NUM_CLASSES = 4
NUM_STEP = 8
NOTHING_PATH = "D:/Users/jylee/Dropbox/Files/Datasets/capstonedata/total/nothing"
TRAIN_PATH = "D:/Users/jylee/Dropbox/Files/Datasets/capstonedata/train"
VALID_PATH = "D:/Users/jylee/Dropbox/Files/Datasets/capstonedata/valid"
TRAIN_PATH2 = "D:/Users/jylee/Dropbox/Files/Datasets/capstonedata2/train"
VALID_PATH2 = "D:/Users/jylee/Dropbox/Files/Datasets/capstonedata2/valid"

DETECTOR_TRAIN_PATH = "D:/Users/jylee/Dropbox/Files/Datasets/detector/train"
DETECTOR_VALID_PATH = "D:/Users/jylee/Dropbox/Files/Datasets/detector/valid"


def image_loader_trash(batch_size, train=True):

    if train:
        path = TRAIN_PATH
    else:
        path = VALID_PATH

    categories = [
        "can", "extra", "glass", "plastic"
    ]

    files = []
    cats = []

    for i, cat in enumerate(categories):
        for f in pathlib.Path(os.path.join(path, cat).replace("\\", "/")).glob("*.jpg"):
            files.append(str(f))
            cats.append(i)

    n = len(files)
    n_batches = int(np.ceil(n / batch_size))

    indices = np.arange(n)
    np.random.shuffle(indices)

    for b in range(n_batches):
        start = b * batch_size
        end = min((b+1) * batch_size, n)

        x_batch = np.zeros((end - start, 3, 128, 128))
        y_batch = np.zeros((end - start,))

        for i in range(start, end):
            index = indices[i]
            f = files[index]
            cat = cats[index]

            img = Image.open(f).resize((128, 128))
            angle = np.random.randn() * 15
            img = img.rotate(angle)

            if np.random.rand() > 0.4:
                noise = np.random.normal(0, np.random.randint(0, 15), img.size)
                img = np.array(img) + noise.reshape(*noise.shape, 1)
            else:
                img = np.array(img)

            img = (img.astype(np.float32) - 128) / 256 + 0.5
            img = img.transpose(2, 0, 1)

            x_batch[i - start] = img
            y_batch[i - start] = cat

        yield torch.FloatTensor(x_batch), torch.LongTensor(y_batch)


def image_loader_detector(batch_size, train=True):

    if train:
        path = DETECTOR_TRAIN_PATH
    else:
        path = DETECTOR_VALID_PATH

    categories = [
        "nothing", "trash"
    ]

    files = []
    cats = []

    for i, cat in enumerate(categories):
        for f in pathlib.Path(os.path.join(path, cat).replace("\\", "/")).glob("*.jpg"):
            files.append(str(f))
            cats.append(i)

    n = len(files)
    n_batches = int(np.ceil(n / batch_size))

    indices = np.arange(n)
    np.random.shuffle(indices)

    for b in range(n_batches):
        start = b * batch_size
        end = min((b+1) * batch_size, n)

        x_batch = np.zeros((end - start, 3, 128, 128))
        y_batch = np.zeros((end - start,))

        for i in range(start, end):
            index = indices[i]
            f = files[index]
            cat = cats[index]

            img = Image.open(f).resize((128, 128))
            angle = np.random.randn() * 15
            img = img.rotate(angle)

            if np.random.rand() > 0.4:
                noise = np.random.normal(0, np.random.randint(0, 15), img.size)
                img = np.array(img) + noise.reshape(*noise.shape, 1)
            else:
                img = np.array(img)

            img = (img.astype(np.float32) - 128) / 256 + 0.5
            img = img.transpose(2, 0, 1)

            x_batch[i - start] = img
            y_batch[i - start] = cat

        yield torch.FloatTensor(x_batch), torch.LongTensor(y_batch)


def korean_file_name_img(path):

    stream = open(path.encode("utf-8"), "rb")
    bytes = bytearray(stream.read())
    numpy_arr = np.asarray(bytes, dtype=np.uint8)

    return cv2.imdecode(numpy_arr , cv2.IMREAD_UNCHANGED)


def rnn_data2(batch_size, train=True):

    if train:
        path = TRAIN_PATH2
    else:
        path = VALID_PATH2

    categories = [
        "can", "extra", "glass", "plastic"
    ]

    lst = []
    clz = []

    for i, cat in enumerate(categories):
        for d in pathlib.Path(os.path.join(path, cat).replace("\\", "/")).glob("*"):
            sub_lst = []
            for f in d.glob("*.jpg"):
                sub_lst.append(str(f))

            assert len(sub_lst) == 8, f"{cat}/{d}"
            lst.append(sub_lst)
            clz.append(i)

    n = len(lst)
    n_batches = int(np.ceil(n / batch_size))

    indices = np.arange(n)
    np.random.shuffle(indices)

    for b in range(n_batches):
        start = b * batch_size
        end = min((b+1) * batch_size, n)

        x_batch = np.zeros((batch_size, 8, 3, 128, 128))
        y_batch = np.zeros((batch_size,))

        indices_slice = indices[start:end]
        i = 0

        for index in indices_slice.tolist():
            step = 0
            for f in lst[index]:
                # img = cv2.imread(f)
                # if img is None:
                #     img = korean_file_name_img(f)
                # img = cv2.resize(img, dsize=(128, 128))
                # # if r > 0.5:
                # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # img = (np.float32(img) - 123) / 123
                # img = img.transpose(2, 0, 1)
                # x_batch[i, step] = img
                # step += 1

                img = Image.open(f).resize((128, 128))
                r = np.random.randn() * 20
                img = img.rotate(r)

                if np.random.rand() > 0.4:
                    noise = np.random.normal(0, np.random.randint(0, 15), img.size)
                    img = np.array(img) + noise.reshape(*noise.shape, 1)

                img = np.array(img)
                img = (img.astype(np.float32) - 128) / 256 + 0.5

                x_batch[i, step] = img.transpose(2, 0, 1)
                step += 1

            y_batch[i] = clz[index]
            i += 1

        yield torch.FloatTensor(x_batch), torch.LongTensor(y_batch)


def rnn_data(batch_size, train=True):
    loader = image_loader(512, train=train)

    for x_batch, y_batch in loader:
        for i in range(30):
            imgs = []
            lbls = []

            cnt = 0
            c = 0

            while cnt < 4:
                indices = np.arange(y_batch.size(0))
                indices = indices[y_batch.numpy() == c]
                x_batch_i = x_batch[indices]

                r = np.random.choice(np.arange(x_batch_i.shape[0]), size=(batch_size,))

                imgs.append(x_batch_i[r])   
                lbls.append(torch.tensor([c] * (batch_size // NUM_STEP)))

                cnt += 1
                c += 1

                if c == 4:
                    c = 0

            x = torch.stack(imgs, dim=0).view((batch_size * 4) // NUM_STEP, NUM_STEP, 3, 128, 128)
            y = torch.stack(lbls, dim=0).view((batch_size * 4) // NUM_STEP,)

            yield x, y


def read_nothing_list():
    files = []

    for f in pathlib.Path(NOTHING_PATH).glob("*.jpg"):
        files.append(str(f))

    return files


def siamese_data_loader(batch_size, train=True):
    loader = image_loader(128, train)

    for imgs, lbls in loader:
        imgs = imgs.numpy()
        lbls = lbls.numpy()

        classes = np.unique(lbls)

        for e in range(10):

            x_src_batch = np.zeros((batch_size, 3, 128, 128))
            y_src_batch = np.zeros((batch_size,))

            x_pos_batch = np.zeros((batch_size, 3, 128, 128))
            y_pos_batch = np.zeros((batch_size,))

            x_neg_batch = np.zeros((batch_size, 3, 128, 128))
            y_neg_batch = np.zeros((batch_size,))
            
            for i in range(batch_size):
                pos_c = np.random.choice(classes)
                neg_c = np.random.choice(classes[classes != pos_c])

                pos_slice = imgs[lbls == pos_c]
                neg_slice = imgs[lbls == neg_c]

                src_index = np.random.randint(pos_slice.shape[0])
                x_src_batch[i] = pos_slice[src_index]
                y_src_batch[i] = pos_c

                pos_index = np.random.randint(pos_slice.shape[0])
                x_pos_batch[i] = pos_slice[pos_index]
                y_pos_batch[i] = pos_c

                neg_index = np.random.randint(neg_slice.shape[0])
                x_neg_batch[i] = neg_slice[neg_index]
                y_neg_batch[i] = neg_c

            x_src_batch = torch.FloatTensor(x_src_batch)
            y_src_batch = torch.LongTensor(y_src_batch)
            
            x_pos_batch = torch.FloatTensor(x_pos_batch)
            y_pos_batch = torch.LongTensor(y_pos_batch)
            
            x_neg_batch = torch.FloatTensor(x_neg_batch)
            y_neg_batch = torch.LongTensor(y_neg_batch)

            yield x_src_batch, y_src_batch, x_pos_batch, y_pos_batch, x_neg_batch, y_neg_batch


def get_image_loader(data_dir, batch_size):
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.RandomHorizontalFlip(0.5),
        # transforms.RandomVerticalFlip(0.5),
        transforms.ToTensor()
    ])

    dataset = torch.utils.data.ImageFolder(data_dir, transform=transform)

    n = len(dataset)
    indices = np.arange(n)
    np.random.shuffle(indices)

    train_indices = indices[:int(n*0.7)]
    valid_indices = indices[int(n*0.7):int(n*0.85)]
    test_indices = indices[int(n*0.85):]

    train_loader = torch.utils.data.DataLoader(dataset, sampler=SubsetRandomSampler(train_indices))
    valid_loader = torch.utils.data.DataLoader(dataset, sampler=SubsetRandomSampler(valid_indices))
    test_loader = torch.utils.data.DataLoader(dataset, sampler=SubsetRandomSampler(test_indices))

    return train_loader, valid_loader, test_loader