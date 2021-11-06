from datetime import datetime
import pandas as pd
from pprint import pprint

class ExcelService:
    def __init__(self):
        pass

    @staticmethod
    def replace_none_with_empty_str(some_dict):
        return { k: ('=' if v is None else v) for k, v in some_dict.items() }

    @staticmethod
    def create_table(hars):

        base_keys = ['Артикул',
                     'Идентификатор',
                     'Заголовок',
                     'Цена',
                     'Цена со скидкой',
                     'В наличии',
                     'Количество продаж',
                     'Категория',
                     'Аксесуары',
                     'Краткое описание',
                     'Длинное описание',
                     'Картинки',
                     'Бренд']
        
        unique_keys = set()
        for _ in hars:
            unique_keys |= _['hars'].keys()
        unique_keys = list(unique_keys)
        
        datacaption = dict.fromkeys(base_keys+unique_keys)

        datalist = []
        for _ in hars:
            datadict = _['hars']
            if _['art_found']:
                dataline = {**datacaption,**datadict}
                dataline['Артикул'] = _['art']
                datadict = _['hars']
                dataline['Краткое описание'] = _['dshort']
                dataline['Длинное описание'] = _['dlong']
                dataline['Бренд'] = _['brand']
                datalist.append(ExcelService.replace_none_with_empty_str(dataline))
            else:
                dataline = {**datacaption,**datadict}
                dataline['Артикул'] = _['art']
                datalist.append(ExcelService.replace_none_with_empty_str(dataline))
                
        
        df = pd.DataFrame(datalist, columns=base_keys+unique_keys)

        df.to_csv(f'excel_out_{datetime.now().strftime("%d_%b_%Y_%H_%M")}.csv',sep=',',encoding='utf-8',index=False)

        # file = xlwt.Workbook()
        # sheet = file.add_sheet("parsed")
        #
        # count = 0
        #
        # sheet.write(0, count, "Артикул")
        # sheet.col(count).width = 256 * 20
        # count += 1
        #
        # sheet.write(0, count, "Идентификатор")
        # sheet.col(count).width = 256 * 5
        # count += 1
        #
        # sheet.write(0, count, "Заголовок")
        # sheet.col(count).width = 256 * 5
        # count += 1
        #
        # sheet.write(0, count, "Цена")
        # sheet.col(count).width = 256 * 5
        # count += 1
        #
        # sheet.write(0, count, "Цена со скидкой")
        # sheet.col(count).width = 256 * 5
        # count += 1
        #
        # sheet.write(0, count, "В наличии")
        # sheet.col(count).width = 256 * 5
        # count += 1
        #
        # sheet.write(0, count, "Количество продаж")
        # sheet.col(count).width = 256 * 5
        # count += 1
        #
        # sheet.write(0, count, "Категория")
        # sheet.col(count).width = 256 * 5
        # count += 1
        #
        # sheet.write(0, count, "Аксессуары")
        # sheet.col(count).width = 256 * 5
        # count += 1
        #
        # sheet.write(0, count, "Краткое описание")
        # sheet.col(count).width = 256 * 20
        # count += 1
        #
        # sheet.write(0, count, "Длинное описание")
        # sheet.col(count).width = 256 * 20
        # count += 1
        #
        # sheet.write(0, count, "Картинки")
        # sheet.col(count).width = 256 * 20
        # count += 1
        #
        # sheet.write(0, count, "Бренд")
        # sheet.col(count).width = 256 * 20
        # count += 1
        #
        # for _ in unique_keys:
        #     sheet.write(0, count, _)
        #     sheet.col(count).width = 256 * 20
        #     count += 1
        #
        # for i, val in enumerate(hars):
        #
        #     if val['art_found']:
        #         sheet.write(i+1, 0, val['art'])
        #         sheet.col(0).width = 256 * 20
        #
        #         count = 8
        #
        #         sheet.write(i+1, count, val['dshort'])
        #         sheet.col(count).width = 256 * 20
        #         count += 1
        #
        #         sheet.write(i+1, count, val['dlong'])
        #         sheet.col(count).width = 256 * 20
        #         count += 1
        #
        #         sheet.write(i+1, count, val['img'])
        #         sheet.col(count).width = 256 * 20
        #         count += 1
        #
        #         sheet.write(i+1, count, val['brand'])
        #         sheet.col(count).width = 256 * 20
        #         count += 1
        #
        #         for _ in unique_keys:
        #             if _ in val['hars'].keys():
        #                 cell = val['hars'][_]
        #             else:
        #                 cell = '='
        #             sheet.write(i+1, count, cell)
        #             sheet.col(count).width = 256 * 20
        #             count += 1
        #     else:
        #         sheet.write(i+1, 0, val['art'])
        #         sheet.col(0).width = 256 * 20
