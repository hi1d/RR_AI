import requests

keyword = input()
headers = {'Authorization': f'token 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'}
test = requests.get(f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page=100", headers=headers).json()
print(len(test['items']))























# import pandas as pd
# import sys 
# import re
# col = ['월','화','수','목','금']
# ind = ['10:00 ~ 11:00','11:00 ~ 12:00','12:00 ~ 13:00','13:00 ~ 14:00','14:00 ~ 15:00','15:00 ~ 16:00','16:00 ~ 17:00','17:00 ~ 18:00',]
# con = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
# df = pd.DataFrame(con, columns=col, index=ind)

# input = sys.stdin.readline

# alba_dict = {'a': ['1000~1400', '1500~1800', '1100~1300;1400~1600', '1000~1100', '1500~1800'], 'b': ['1100~1400', '1400~1600', '1600~1800', '1000~1100;1200~1300', '1400~1600'], 'c': ['1400~1600', '1600~1800', '1000~1200', '1200~1400', '1400~1600'], 'd': ['1400~1800', '1000~1800', '1200~1400', '1400~1500;1600~1700', '1000~1200']}
# # for i in range(4):
# #     alba_dict[chr(97+i)] = list(map(lambda x : re.sub('[^0-9;~]','',x), input()[1:-1].split(',')))

# def get_time(time_list: list):
#     day = 0
#     week_time_list = []
#     for time in time_list:
#         print(time)
#         # time = time.split(';')
#         # hour_list = [0 for _ in range(9)]
#         # for hour in time:
#         #     print(hour)
            
#         # day +=1


# def make_timetable(a_time: list, b_time: list, c_time: list, d_time: list):
#     get_time(a_time)
    

# make_timetable(alba_dict['a'], alba_dict['b'], alba_dict['c'], alba_dict['d'])
    
    



