import os
import json
import random as rd


class SeedManager:
    def __init__(self):
        self.__seed_list = []
        self.__seed_aliases = []

    def read(self, seed_file_path, dump_charmap_to:str=None, dump_aliasmap_to:str=None):
        """

        :param seed_file_path: the path to seed. A seed can be a character or digit or punctuation mark.
        1. seeds are distinguished by line
        2. a seed can have alias, splited by `tab`. eg. `#\thashtag`
        :param dump_charmap_to: if it is not `None`, make a charmap json file after the reading is done,
        and dump the charmap to this path.
        :param dump_aliasmap_to: the same as above
        :return:
        """
        with open(seed_file_path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip('\n').split(' ')
                char = parts[0]
                alias = parts[-1] if len(parts) > 1 else char
                self.__seed_list.append(char)
                self.__seed_aliases.append(alias)

        if dump_charmap_to is not None:
            charmap = {}
            for idx, alias in enumerate(self.__seed_aliases):
                charmap[alias] = idx
            with open(dump_charmap_to, 'w', encoding='utf-8') as j:
                json.dump(charmap, j, ensure_ascii=False, indent=2)
            print('Dump charmap to %s' % dump_charmap_to)

        if dump_aliasmap_to is not None:
            aliasmap = {}
            for alias, char in zip(self.__seed_aliases, self.__seed_list):
                aliasmap[alias] = char
            with open(dump_aliasmap_to, 'w', encoding='utf-8') as j2:
                json.dump(aliasmap, j2, ensure_ascii=False, indent=2)
            print('Dump aliasmap to %s' % dump_aliasmap_to)

        return self

    def random_make(self, min_len, max_len, space_insertion_probability=0.0):
        assert 0 <= space_insertion_probability <= 1
        assert len(self.__seed_aliases) == len(self.__seed_list)
        length = rd.randint(min_len, max_len)
        num_seeds = len(self.__seed_list)
        string = ""
        alias_string = ""
        for _ in range(length):
            ptr = rd.randint(0, num_seeds-1)
            char, alias = self.__seed_list[ptr], self.__seed_aliases[ptr]
            string += char
            alias_string += alias
        return string, alias_string

    def get_by_order(self):
        for char, alias in zip(self.__seed_list, self.__seed_aliases):
            yield char, alias
