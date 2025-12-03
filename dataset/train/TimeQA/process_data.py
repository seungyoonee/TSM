# Original code is based on the paper Time-Sensitive-QA (https://github.com/wenhuchen/Time-Sensitive-QA)
import json
import random
import re
import copy
import gzip
import os
from tqdm import tqdm

# --- Time Class and Utils (Adapted from Process.ipynb) ---

mapping = {1: 'Jan', 2: 'Feb', 3: "Mar", 4: "Apr", 5: "May",
           6: 'Jun', 7: 'Jul', 8: "Aug", 9: "Sep", 10: 'Oct',
           11: "Nov", 12: 'Dec'}

imapping = {v: k for k, v in mapping.items()}
imapping.update({
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,'July': 7, 'August': 8, 'September': 9, 'October': 10,
    'November': 11, 'December': 12
})

class Time(object):
    def __init__(self, time_str):
        splits = [int(_) for _ in time_str.split('-')]
        
        self.year = max(splits[0], 1)
        self.month = splits[1]
        self.date = splits[2]

        if self.month == 1 and self.date == 1:
            self.month = 0
            self.date = 0
        elif self.month == 0 or self.date == 0:
            self.month = 0
            self.date = 0
        
        assert self.year > 0
            
    def __gt__(self, other):
        assert isinstance(other, Time)
        if self.year > other.year:
            return True
        elif self.year < other.year:
            return False
        else:
            if self.month > other.month:
                return True
            elif self.month < other.month:
                return False
            else:
                if self.date > other.date:
                    return True
                else:
                    return False
    
    def __eq__(self, other):
        assert isinstance(other, Time), other
        return self.year == other.year and self.month == other.month and self.date == other.date
    
    def __lt__(self, other):
        assert isinstance(other, Time)
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        else:
            if self.month < other.month:
                return True
            elif self.month > other.month:
                return False
            else:
                if self.date < other.date:
                    return True
                else:
                    return False
    
    def __repr__(self):
        if self.month == 0:
            return '{}'.format(self.year)
        else:
            return '{} {}'.format(mapping[self.month], str(self.year))
    
    def __str__(self):
        return self.__repr__()
    
    @classmethod
    def parse(cls, time):
        assert isinstance(time, str)
        if ' ' not in time:
            return cls(f'{time}-0-0')
        else:
            month, year = time.split(' ')
            month = month.lower().capitalize()
            month = imapping[month]
            return cls(f'{year}-{month}-1')
    
    @classmethod
    def minus_one_year(cls, time):
        return cls('{}-{}-{}'.format(time.year - 1, time.month, time.date))

    @classmethod
    def minus_k_year(cls, time, k):
        return cls('{}-{}-{}'.format(max(time.year - k, 2), time.month, time.date))
    
    @classmethod
    def add_one_year(cls, time):
        return cls('{}-{}-{}'.format(time.year + 1, time.month, time.date))

    @classmethod
    def add_k_year(cls, time, k):
        return cls('{}-{}-{}'.format(time.year + k, time.month, time.date))      
    
    @classmethod
    def add_one_month(cls, time):
        new_time = copy.deepcopy(time)
        if new_time.month < 12:
            new_time.month += 1
            return new_time
        else:
            new_time.month = 1
            new_time.year += 1
            return new_time

def random_pop(time_range):
    cur = time_range[0]
    end = time_range[1]
    candidates = []
    cur = Time.add_one_month(cur)
    while cur < end or cur == end:
        candidates.append(cur)
        cur = Time.add_one_month(cur)

    if candidates:
        return random.choice(candidates)
    else:
        return random.choice(time_range)

def too_close(time1, time2):
    delta = (time2.year - time1.year) * 12
    delta += time2.month - time1.month
    return delta <= 2

def link_2_name(string):
    string = string.replace('/wiki/', '')
    string = string.replace('_', ' ')
    return string

def enc(string, split):
    string = json.dumps(string)
    return string + '\n'

def split_paragraphs(paras):
    # Process the data
    ctxs = []
    buffer = {"title": paras[0], "text": ""}
    for para in paras[1:]:
        if para[0].isupper() and len(para.split(' ')) <= 4:
            if len(buffer["text"].split(' ')) > 15:
                ctxs.append(buffer)
            buffer = {"title": para.strip(' .'), "text": ""}
        else:
            if len(buffer['text'].split(' ')) + len(para.split(' ')) > 100:
                if len(buffer['text'].split(' ')) > 15:
                    ctxs.append(buffer)
                    buffer = {"title": ctxs[-1]['title'], "text": ""}
                tokens = para.split(' ')
                for j in range(0, len(tokens), 100):
                    buffer['text'] = ' '.join(tokens[j: j + 100])
                    ctxs.append(buffer)
                    buffer = {"title": ctxs[-1]['title'], "text": ""}
            else:
                buffer['text'] += ' ' + para

    if buffer['text']:
        ctxs.append(buffer)
    ctxs = ctxs[:100]
    return ctxs

# --- New Logic ---

def generate_all_specifiers(time_range, first_last):
    """
    Generates all valid specifiers for a given time range.
    Returns a dict: {specifier_type: specifier_string}
    """
    specifiers = {}
    
    # 1. from_to (equivalent to 'between' in original code)
    # Always valid
    specifiers['from_to'] = 'from {} to {}'.format(str(time_range[0]), str(time_range[1]))
    
    # 2. in
    # Always valid (every interval has points)
    # Pick a random point
    t_in = random_pop(time_range)
    specifiers['in'] = 'in {}'.format(str(t_in))
    
    # 3. in_early / in_late
    # Dependent on 'in' logic
    if time_range[1].year // 10 > time_range[0].year // 10:
        if time_range[1].year % 10 >= 3:
            specifiers['in_early'] = 'in early {}s'.format(time_range[1].year // 10 * 10)
        if time_range[0].year % 10 <= 7:
            specifiers['in_late'] = 'in late {}s'.format(time_range[0].year // 10 * 10)
            
    # 4. between_and (equivalent to 'between-subset' in original code)
    x1 = random_pop(time_range)
    x2 = random_pop((x1, time_range[1]))
    specifiers['between_and'] = 'between {} and {}'.format(str(x1), str(x2))
    
    # 5. before
    if first_last == 'first':
        x = random_pop(time_range)
        specifiers['before'] = 'before {}'.format(str(x))
        
    # 6. after
    if first_last == 'last':
        x = random_pop(time_range)
        specifiers['after'] = 'after {}'.format(str(x))
        
    return specifiers

def main():
    # Load relations
    with open('./original/relations.json', 'r') as f:
        relations = json.load(f)
    
    splits = ['train', 'dev'] # We use original TimeQA test set provided by the author
    specifier_types = ['in', 'after', 'before', 'in_early', 'in_late', 'between_and', 'from_to']

    for split in splits:
        print(f"Processing split: {split}")
        input_path = f'./original/annotated_{split}.json'
        if not os.path.exists(input_path):
            print(f"File not found: {input_path}, skipping.")
            continue
            
        with open(input_path, 'r') as f:
            data = json.load(f)
            
        # Open output files
        output_files = {}
        for spec in specifier_types:
            # Output to dataset/TimeQA/
            output_files[spec] = open(f'./{split}_{spec}.jsonl', 'w')
            
        for d in tqdm(data, desc=f'{split}'):
            assert isinstance(d['type'], str)
            
            templates = relations[d['type']]['template']
            if not templates:
                continue
                
            template_base = random.choice(templates)
            template_base = template_base.replace('$1', link_2_name(d['link']))
            
            # Check if template has time slot
            if '$4' not in template_base and '$2' not in template_base:
                continue

            for i, entry in enumerate(d['questions']):
                # Filter unanswerable samples
                # Check if answers are empty strings
                answers = [_['answer'] for _ in entry[1]]
                valid_answers = [a for a in answers if a]
                if not valid_answers:
                    continue

                time_step = [Time.parse(entry[0][0]), Time.parse(entry[0][1])]
                
                # Determine first/last
                first_last = None
                if i == 0:
                    first_last = 'first'
                elif i == len(d['questions']) - 1:
                    first_last = 'last'
                
                # Generate all specifiers
                specs = generate_all_specifiers(time_step, first_last)
                
                for spec_type, spec_str in specs.items():
                    # Replace in template
                    if '$4' in template_base:
                        question = template_base.replace('$4', spec_str)
                    elif '$2' in template_base:
                        question = template_base.replace('$2', spec_str)
                    else:
                        continue
                    
                    # Extract positive contexts
                    # Use original paragraphs indicated by 'para' index in answers
                    # We deduplicate if multiple answers point to the same paragraph
                    positive_ctx_indices = set()
                    for ans in entry[1]:
                        if ans['answer']: # Only consider valid answers
                            positive_ctx_indices.add(ans['para'])
                    
                    positive_ctxs = [{'text': d['paras'][idx]} for idx in sorted(list(positive_ctx_indices))]
                    
                    
                    tmp = {
                        'question': question,
                        'positive_ctxs': positive_ctxs
                    }
                    output_files[spec_type].write(enc(tmp, split))

        # Close files
        for f_handle in output_files.values():
            f_handle.close()

if __name__ == '__main__':
    main()
