import zipfile
import os
import pathlib


def zipDir(dirpath, outfolder: str = None, file_name='x', exclude_file: list = None):
    """
    压缩指定文件夹
    :param file_name: 文件名称
    :param dirpath: 目标文件夹路径
    :param outfolder: 压缩文件保存文件夹路径 默认是在目标文件夹同一个父文件夹中
    :param exclude_file list 排除不需要加入压缩的文件名字
    :return: 无
    """
    if not outfolder:
        p = pathlib.Path(dirpath)
        outfolder = p.parent
    else:
        outfolder = pathlib.Path(outfolder)
    file_path = str(outfolder / f'{file_name}.zip')
    zip = zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED)

    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标根路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        if exclude_file:
            filenames = list(set(filenames) - set(exclude_file))

        for filename in filenames:
            print(filename)
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()



