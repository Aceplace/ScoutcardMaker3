import traceback
import xlrd as xl


def get_script_from_excel_file(file_name, get_sheet_callback=None):
    try:
        work_book = xl.open_workbook(file_name)

        if work_book.nsheets == 1 or get_sheet_callback is None:
            sheet = work_book.sheet_by_index(0)
        else:
            sheet_name = get_sheet_callback(work_book.sheet_names())
            if not sheet_name:
                return False, 'Must choose sheet'
            sheet = work_book.sheet_by_name(sheet_name)

        # sheet = work_book.sheet_by_index(0)

        plays = []
        for index in range(1, sheet.nrows):
            row_values = sheet.row_values(index)
            play_info = {}
            try:
                play_info['Number'] = int(row_values[0])
            except ValueError:
                play_info['Number'] = row_values[0]
            play_info['Personnel'] = row_values[1]
            hash_mark = row_values[2]
            if hash_mark in ['RT', 'R', 'r', 'rt', 'Rt']:
                hash_mark = 'RT'
            elif hash_mark in ['LT', 'L', 'l', 'lt', 'Lt']:
                hash_mark = 'LT'
            else:
                hash_mark = 'MOF'
            play_info['Hash'] = hash_mark
            play_info['Dnd'] = row_values[3]
            play_info['Formation'] = row_values[4]
            play_info['Play'] = row_values[5]
            play_info['Defense'] = row_values[6]
            play_info['Note'] = row_values[7]
            play_info['Card Maker Formation'] = row_values[8].strip().upper()
            play_info['Card Maker Defense'] = row_values[9].strip().upper()
            plays.append(play_info)
    except IOError as e:
        return False, 'Couldn\'t load file'
    except Exception:
        traceback.print_exc()
        return False, 'Excel sheet incorrectly formatted'

    return True, plays

