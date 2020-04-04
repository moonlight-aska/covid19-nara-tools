"""
opendata_covid19_NaraCity.xlsx
"""

from openpyxl import load_workbook
import os
import sys
from pathlib import Path
sys.path.append(str(Path('__file__').resolve().parent))
from common import excel_date

FILENAME = "opendata_covid19_NaraCity.xlsx"

def parse_nara_dailystatus():
    paths = [os.path.abspath(os.path.dirname(__file__)), '..', 'data', FILENAME]
    f = os.path.join(*paths)
    wb = load_workbook(f)
    ws = wb['2.感染症状況']
    patients_summary = []   # 患者数
    inspections_list = []   # 検査数
    querents_list    = []   # 相談数
    
    for row in ws.values:
        if '調査_年月日' in str(row[0]):
            continue;
        if row[0] == None :
            break;

        search_date     = row[0] # 調査_年月日
        inspection_count= row[5] # 調査実施_件数
        inspection_positive = row[6] # 陽性確認_件数
        inspection_negative = row[7] # 陰性確認_件数
        stayed_count     = row[8] # 入院者数_現在
        discharged_count = row[9] # 退院者数_累計
        querents_count   = row[10] # 相談件数
        
        # 患者数
        if inspection_positive != None :
            patients_data = {
                "日付": search_date.isoformat(timespec='milliseconds')+'Z',
                "小計": inspection_positive,
            }
            patients_summary.append(patients_data)
        
        # 陽性患者属性
        if inspection_count != None :
            inspections_data = {
                "日付": search_date.isoformat(timespec='milliseconds')+'Z',
                "小計": inspection_count,
                "陽性判定": inspection_positive,
                "陰性確認": inspection_negative,
            }
            inspections_list.append(inspections_data)

        # 相談者数
        if querents_count != None :
            querents_data = {
                "日付": search_date.isoformat(timespec='milliseconds')+'Z',
                "小計": querents_count,
            }
            querents_list.append(querents_data)

    return patients_summary, inspections_list, querents_list

"""
#   return patients_count, discharge_count, stayed_count, tiny_injury_count, severe_injury_count, data, patients_list
#    return results
"""

if __name__ == '__main__':
    patients_summary, inspections_list, querents_list = parse_nara_dailystatus()
    print( patients_summary )
    print( inspections_list )
    print( querents_list )
    
