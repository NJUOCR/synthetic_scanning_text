from printer import Printer
import utils.uimg as uimg
import utils.utility as util


def init_img():
    printer = Printer('fonts/fangsong_GB2312.ttf', 20)
    img = printer.print_one(256, 64, "测试用例")
    return img


if __name__ == '__main__':
    config = util.read_config('config/template.json')
    ops = config['ops']

    im = init_img()
    uimg.show(im)
    operation, p = ops[0]
    for idx in range(10):
        out, val = operation.interfere(im)
        print(out.shape)
        uimg.show(out)
        # uimg.save("%s/%d.jpg" % ("out", idx), out)


