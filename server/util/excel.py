from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from openpyxl import Workbook
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook
from django.utils.encoding import escape_uri_path
from openpyxl.utils import get_column_letter
from openpyxl.styles import Side, Border, colors, PatternFill, Alignment, Font


class ExcelToModel:

    def __init__(self, file, header, serializer, first_row=1, sheet_no=0, request=None, save=True):
        """
        :param file: 上传的excel二进制数据
        :param header: # excel表头映射成模型的字段名
        :param serializer: # 序列化器 验证excel中的数据
        :param first_row: # 从哪一行开始获取数据
        :param sheet_no: # 获取excel中哪一个sheet
        :param request: # request 对象
        :param save: # 是否序列化后保存 这里的保存是一条条保存 如果数据量大 就影响数据库性能（建议批量保存 就save=false获取数据后在操作）
        """
        self.wb = openpyxl.load_workbook(file)
        sheet_names = self.wb.sheetnames
        self.worksheet = self.wb[sheet_names[sheet_no]]
        # 获取总行数
        # self.nrows = self.worksheet.max_row
        columns = self.worksheet.max_column
        excel_header = [self.worksheet.cell(row=first_row, column=i).value for i in range(1, columns + 1)]
        self.header = [header[h] for h in excel_header]
        self.first_row = first_row
        self.serializer = serializer
        self.request = request
        self.save = save

    @property
    def excel2array(self):
        datas = []
        for row in self.worksheet.iter_rows(min_row=self.first_row + 1):
            row_data = [cell.value for cell in row]
            data = dict(zip(self.header, row_data))
            serialize = self.serializer(data=data, context={'request': self.request})
            if serialize.is_valid():
                if self.save:
                    serialize.save()
                datas.append(serialize.data)
            else:
                return serialize.errors

        self.wb.close()

        return datas


class ModelToExcel:

    def __init__(self, headers: dict, data: [dict] = None, name: str = 'Sheet1', is_header: bool = False,
                 dict_data: dict = None, ext: str = '.xlsx', title: str = None, merge: list = None, beauty: bool = True,
                 cell_width=15):
        """
        :param headers: excel表格头 {'定义的名称'：’字段名',....}
        :param data: 表格数据 [{'字段名':'字段的值’}]
        :param name: 表格的sheet名
        :param is_header: 是否值导出标题头
        :param dict_data: 映射字典 例如 {'color':1} ----{1:'red'} ----> {'color':'red'}
        :param ext: 表格格式后缀 .xlsx or  .xls
        :param title: 表格标题名称
        :param merge: 合并单元格cell  例如['A1:A3'] 合并
        :param beauty: 是否美化格式 当数据量大的时候很费时间
        """
        self.data = data
        self.headers = headers
        self.name = name
        self.is_header = is_header
        self.dict_data = dict_data
        self.ext = ext
        self.title = title
        self.merge = merge
        self.beauty = beauty
        self.cell_width = cell_width

    @property
    def export_as_excel(self):

        field_names = list(self.headers.keys())  # 模型所有字段名
        filename = escape_uri_path(self.name) + self.ext
        wb = Workbook()
        ws = wb.active

        if self.title:
            leng = len(field_names)
            first_cont = [self.title] + [''] * (leng - 1)
            last_col = get_column_letter(leng)

            ws.append(first_cont)
            ws.merge_cells(f'A1:{last_col}1')
            ws.row_dimensions[1].height = 30
            bold_24_font = Font(name='等线', size=20, italic=False, color='0d0992', bold=True)
            ws['A1'].font = bold_24_font

            headline = 2
        else:
            headline = 1

        ws.append(field_names)

        orange_fill = PatternFill(fill_type='solid', fgColor="A6D5B0")
        for ci in range(len(field_names)):
            ws.cell(row=headline, column=ci + 1).fill = orange_fill
            col_letter = get_column_letter(ci + 1)
            ws.column_dimensions[col_letter].width = self.cell_width

        if not self.is_header:
            for obj in self.data:
                if self.dict_data:
                    data = [self.convert(obj.get(v)) for v in self.headers.values()]
                else:
                    data = [obj.get(v) for v in self.headers.values()]
                row = ws.append(data)

            if self.merge:
                for mer in self.merge:
                    ws.merge_cells(mer)

        if self.beauty:
            # 数据量大了后 每一cell去遍历 很花时间  注意取舍
            row_max = ws.max_row
            con_max = ws.max_column
            for xi in range(1, row_max + 1):
                for ji in range(1, con_max + 1):
                    ws.cell(row=xi, column=ji).alignment = Alignment(horizontal='center', vertical='center')
                    ws.cell(row=xi, column=ji).border = Border(top=Side(border_style='thin', color=colors.BLACK),
                                                               bottom=Side(border_style='thin', color=colors.BLACK),
                                                               left=Side(border_style='thin', color=colors.BLACK),
                                                               right=Side(border_style='thin', color=colors.BLACK))

        response = HttpResponse(content=save_virtual_workbook(wb),content_type='application/msexcel')
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        wb.close()
        return response

    def convert(self, field):

        try:
            return self.dict_data[field]
        except KeyError:
            return field
