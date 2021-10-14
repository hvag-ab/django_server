import zipfile
import pathlib
from typing import Any, Callable, Optional
from io import BytesIO


def zip(dirpath=None, files_paths=None, outfolder: Optional[str] = None, file_name: str = 'x',
        exclude_file: Optional[list] = None):
    """
    压缩指定文件夹
    :param file_name: 文件名称
    :param files_paths: 指定压缩文件路径
    :param dirpath: 目标文件夹路径
    :param outfolder: 压缩文件保存文件夹路径 默认是在目标文件夹同一个父文件夹中
    :param exclude_file list 排除不需要加入压缩的文件名字
    :return: 无
    """
    if exclude_file is None:
        exclude_file = []
    if outfolder:
        outfolder = pathlib.Path(outfolder)
    elif dirpath and not outfolder:
        p = pathlib.Path(dirpath)
        outfolder = p.parent
    else:
        raise ValueError(f'dirpath and outfolder 参数不能同时为空')

    file_path = str(outfolder / f'{file_name}.zip')
    zip = zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED)

    if dirpath:
        p = pathlib.Path(dirpath)
        for d in p.iterdir():
            name = d.name
            if name not in exclude_file:
                zip.write(d)
    elif files_paths:
        for pi in files_paths:
            zip.write(pi)
    else:
        raise ValueError('dirpath and files_paths 参数不能同时为空')
    zip.close()
    return file_path


# 多个excel直接在内存中压缩 方便直接传给前端
def zip_bytes(list_: list, func: Callable[[Any], bytes], suffix:str="xlsx") -> bytes:
    buffer = BytesIO()
    zfile = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED, allowZip64=False)

    for i, obj in enumerate(list_):
        bytes_obj = func(obj)
        zfile.writestr(f"{i}.{suffix}", bytes_obj)
    zfile.close()
    buffer.seek(0)
    zipped_file = buffer.getvalue()
    return zipped_file
