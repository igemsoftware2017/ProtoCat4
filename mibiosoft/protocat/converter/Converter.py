﻿import json

class converter():
    def __init__(self):
        pass
    
    def convert_cat_to_io(self, cat_json):
        pass

    def convert_io_to_cat(self, io_json):
        #http://protocat.org/api/protocol/
        cat_json = {}
        if 'protocol_name' in io_json:
            cat_json['title'] = io_json['protocol_name']
        else:
            cat_json['title'] = "Untitled"

        if 'description' in io_json:
            cat_json['description'] = io_json['description']
        else:
            cat_json['description'] = "No Description provided"       
        protocol_url = 'https://www.protocols.io/view/' + io_json['uri']
        
        if cat_json['description']:
            cat_json['description'] += '\n\nTaken from <a href=' + protocol_url + '>' + protocol_url + '</a>'
        else:
            cat_json['description'] = '\n\nTaken from <a href=' + protocol_url + '>' + protocol_url + '</a>'

        if 'materials' in io_json and len(io_json['materials']) > 0:
            reagent_list = []
            for dict_ in io_json['materials']:
                name = dict_['reagent_name']
                name = "<a href='" + dict_['reagent_url'] + "'>" + name + "</a>"
                reagent_list.append(name)
            cat_json['materials'] = "<br/>".join(reagent_list)
        else:
            cat_json['materials'] = "No Materials Provided"

        cat_json['protocol_steps'] = []
        step_number = 1
        if 'steps' in io_json:
            for step in io_json['steps']:
                cat_step = {}
                cat_step['step_number'] = step_number
                step_number += 1
                #print(step['components'],'\n####################')
                cat_step['action'] = ""
                for comp in step['components']:
                    if not isinstance(comp, dict):
                        #case where we have a dict here
                        comp = step['components'][comp]

                    try:
                        if comp['name'] == "Description":
                            cat_step['action'] += comp['data']
                        elif comp['name'] == "Protocol":
                            #print(step['components'][comp])
                            url_ = "https://www.protocols.io/view/{}".format(comp['source_data']['uri'])
                            cat_step['action'] += """ <a href="{}">{}</a> """.format(url_, url_)
                        elif comp['name'] == "Section":
                            cat_step['title'] = comp['data']
                        elif comp['name'] == 'Duration / Timer':
                            cat_step['time'] = comp['data']
                        else:
                            raise Exception
                    except Exception as e:
                        print(step['components'][comp])
                        print(e, "Unknown how to handle this", comp)
                        cat_step['action'] += "\n\nError ocurred while parsing"
                #print(cat_step)
                if "title" not in cat_step or cat_step['title'] is None:
                    cat_step['title'] = ""
                if "time" not in cat_step:
                    cat_step['time'] = -1
                if "warning" not in cat_step:
                    cat_step['warning'] = ""
                if "time_scaling" not in cat_step:
                    cat_step['time_scaling'] = 2
                if "reagents" not in cat_step:
                    cat_step['reagents'] = []
                if "action" not in cat_step:
                    cat_step['action'] = ""
                if cat_step['action'][0:2] != "<p>":
                    cat_step['action'] = "<p>" + cat_step['action'] + "</p>"
                cat_json['protocol_steps'].append(cat_step)
            
        cat_json['category'] = None 
        cat_json['change-log'] = ""
        cat_json['previous_revision'] = "-1"
        return cat_json
