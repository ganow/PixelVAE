import numpy as np
import imageio
import time
import pathlib

def make_generator(path, n_files, batch_size):
    epoch_count = [1]
    def get_epoch():
        images = np.zeros((batch_size, 3, 64, 64), dtype='int32')
        files = list(range(n_files))
        random_state = np.random.RandomState(epoch_count[0])
        random_state.shuffle(files)
        epoch_count[0] += 1
        for n, i in enumerate(files):
            image = imageio.imread("{}/{}.png".format(path, str(i+1).zfill(len(str(n_files)))))
            images[n % batch_size] = image.transpose(2,0,1)
            if n > 0 and n % batch_size == 0:
                yield (images,)
    return get_epoch

def load(batch_size, imagenet_dir=(pathlib.Path.home() / 'data/imagenet/small')):
    return (
        make_generator((imagenet_dir.expanduser() / 'train_64x64').as_posix(), 1281149, batch_size),
        # make_generator('/home/ishaan/data/imagenet64/valid_64x64', 10000, batch_size)# shorter validation set for debugging
        make_generator((imagenet_dir.expanduser() / 'valid_64x64').as_posix(), 49999, batch_size)
    )

if __name__ == '__main__':
    train_gen, valid_gen = load(64)
    t0 = time.time()
    for i, batch in enumerate(train_gen(), start=1):
        print("{}\t{}".format(str(time.time() - t0), batch[0][0,0,0,0]))
        if i == 1000:
            break
        t0 = time.time()
