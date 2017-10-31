#!/bin/bash

'''
Generate synset file according to lst file, which is generated by `im2rec.py`.
'''

def init():
    global lst_dir
    import sys

    try:
        lst_dir = sys.argv[1]
    except IndexError:
        print("IndexError: please input lst file dir")
        print("".join(["Usage: python ", sys.argv[0], " YOUR_LIST_FILE_DIRECTORY"]))
        exit(-1)

    global label_id_pattern
    global label_name_pattern

    label_id_pattern = ".*\t(.*).000000\t.*"
    label_name_pattern = ".*\t(.*)/.*"

def run():
    global label_dict

    line_idx = 0
    label_dict = dict()

    with open(lst_dir, "r") as lst_handle:
        line = lst_handle.readline()
        while line:
            line_idx += 1
            from re import findall
            label_id_res = findall(label_id_pattern, line)
            label_name_res = findall(label_name_pattern, line)
            if len(label_id_res) > 0 and len(label_name_res) > 0:
                print("id:{}\t\tname:{}".format(label_id_res[0], label_name_res[0]))
                label_dict[label_id_res[0]] = label_name_res[0]
               
            line = lst_handle.readline()


    label_dict = sorted(label_dict.iteritems(), key=lambda term: int(term[0]))

    for k in label_dict: print(k)

def gen_synset(synset_dir="synset.txt"):
    import time
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    synset_dir = "-".join([date, synset_dir])

    with open(synset_dir, 'w') as synset_handle:

        for kv in label_dict:
            line = "\t".join([kv[0], kv[1], "\n"])
            synset_handle.write(line)

    

if __name__ == "__main__":
    init()
    run()
    gen_synset()


