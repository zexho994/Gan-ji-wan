from get_info_list import get_goods_link
from get_table_links import channel_list
from multiprocessing import Pool

def get_table_links_all(channel):
    for num in range(1,5):
        get_goods_link(channel,num)



if __name__ == '__main__':
    map(get_table_links_all,channel_list.split())
    