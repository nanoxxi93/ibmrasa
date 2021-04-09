import os
import io
import json
import datetime
import re

def formatIntent(filename):
    # archivo entrada
    filein = open('{}.txt'.format(filename), 'rt', encoding='utf8')
    # archivo salida
    fileout = open('{}_{}.txt'.format(filename, datetime.datetime.now().strftime('%Y%m%d_%H%M%S')), 'a', encoding='utf8')
    category = ''
    for x in filein:
        if (x.split(',')[-1] != category):
            category = x.split(',')[-1]
            fileout.write('## intent:{}'.format(category))
        fileout.write('- {}\n'.format(x.replace(','+category,'')))
    fileout.close()
    filein.close()
    return ""

def listIntent(filename):
    # archivo entrada
    filein = open('{}.txt'.format(filename), 'rt', encoding='utf8')
    # archivo salida
    fileout = open('{}_{}.txt'.format(filename, datetime.datetime.now().strftime('%Y%m%d_%H%M%S')), 'a', encoding='utf8')
    category = ''
    for x in filein:
        if (x.split(',')[-1] != category):
            category = x.split(',')[-1]
            fileout.write('- {}'.format(category))
    fileout.close()
    filein.close()
    return ""

def watsonjson(filename):
    filedomain = open('domain.txt', 'a', encoding='utf8')
    with open('{}.json'.format(filename), 'rt', encoding='utf8') as filein:
        developer = json.load(filein)
        for key, value in developer.items():
            if (key == 'intents'):
                filedomain.write('intents:\n')
                fileout = open('intents.txt', 'a', encoding='utf8')
                for v in value:
                    filedomain.write('- {}\n'.format(v['intent'].lower()))
                    fileout.write('## intent:{}\n'.format(v['intent'].lower()))
                    for e in v['examples']:
                        example = e['text']
                        for r in re.findall('[\@][\w]+[\s]', example):
                            example = example.replace(r,'[]({}) '.format(r[1:-1]))
                        for r in re.findall('[\@][\w]+', example):
                            example = example.replace(r,'[]({})'.format(r[1:]))
                        fileout.write('- {}\n'.format(example))
                    fileout.write('\n')
                fileout.close()
            if (key == 'entities'):
                filedomain.write('entities:\n')
                fileout = open('entities.txt', 'a', encoding='utf8')
                for v in value:
                    filedomain.write('- {}\n'.format(v['entity'].lower()))
                    fileout.write('## lookup:{}\n'.format(v['entity'].lower()))
                    fileout.write('data/entities_{}.txt\n\n'.format(v['entity'].lower()))
                    fileout2 = open('entities_{}.txt'.format(v['entity'].lower()), 'a', encoding='utf8')
                    for e in v['values']:
                        if (e['type'] == 'synonyms' and len(e['synonyms']) > 1):
                            fileout.write('## synonym:{}\n'.format(e['value'].lower()))
                            fileout2.write('{}\n'.format(e['value'].lower()))
                            for s in e['synonyms']:
                                fileout.write('- {}\n'.format(s).lower())
                            fileout.write('\n')
                        if (e['type'] == 'patterns'):
                            fileout.write('## regex:{}\n'.format(e['value'].lower()))
                            fileout2.write('{}\n'.format(e['value'].lower()))
                            for s in e['patterns']:
                                fileout.write('- {}\n'.format(s))
                            fileout.write('\n')
                    fileout2.close()
                fileout.close()
            if (key == 'dialog_nodes'):
                filedomain.write('responses:\n')
                fileout = open('responses.txt', 'a', encoding='utf8')
                for v in value:
                    filedomain.write('  {}:\n'.format(v['dialog_node'].lower()))
                    if ('conditions' in v):
                        condition = v['conditions'].lower()
                    else:
                        condition = ''
                    condition = condition.replace('#','')
                    condition = condition.replace('||','OR')
                    for r in re.findall('[\@][\w\:]+[\s]', condition):
                        if (r.__contains__(':')):
                            condition = condition.replace(r,'{'+'"{}"'.format(r[1:-1])+'} ')
                            condition = condition.replace(r[1:-1],'{}'.format(r[1:-1].replace(':','":"')))
                        else:
                            condition = condition.replace(r,'{'+'{}'.format(r[1:-1])+'} ')
                    for r in re.findall('[\@][\w\:]+[\)]', condition):
                        if (r.__contains__(':')):
                            condition = condition.replace(r,'{'+'"{}"'.format(r[1:-1])+'})')
                            condition = condition.replace(r[1:-1],'{}'.format(r[1:-1].replace(':','":"')))
                        else:
                            condition = condition.replace(r,'{'+'{}'.format(r[1:-1])+'})')
                    for r in re.findall('[\@][\w\:]+', condition):
                        if (r.__contains__(':')):
                            condition = condition.replace(r,'{'+'"{}"'.format(r[1:])+'}')
                            condition = condition.replace(r[1:],'{}'.format(r[1:].replace(':','":"')))
                        else:
                            condition = condition.replace(r,'{'+'{}'.format(r[1:])+'} ')
                    fileout.write('## {}\n'.format(condition))
                    fileout.write('* {}\n'.format(condition))
                    fileout.write('  - {}\n'.format(v['dialog_node'].lower()))
                    if 'output' in v :
                        for t in v['output']['generic'][0]['values']:
                            text = t['text'].replace('\n','\n    ').lower()
                            filedomain.write('  - {}\n'.format(text))
    return ""

watsonjson('skill-Asistente-VCA')