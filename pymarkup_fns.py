import csv
import toml
import json
import os
import time
import locale
from datetime import datetime
# Above imports are OK

from jinja_renderer import render_template

# from markdown2 import Markdown
# from xhtml2pdf import pisa
# from simpleeval import simple_eval, NameNotDefined



def convertHtmlToPdf(sourceHtml, outputFilename):
    with open(outputFilename, "w+b") as resultFile:
        pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile)
        return pisaStatus.err # return True on success and False on errors


def get_macros():
    macros = {
        'macrotest': 'Lorem ipsum'
    }
    return macros


def printdic(dic, savename=None):
    jsontext = json.dumps(dic,indent=4)
    # print(jsontext)
    if savename:
        with open(savename,'w+',encoding='UTF-8') as file:
            file.write(jsontext)


def parse_pz_comp(text):
    
    # Split lines using newline or comma as the delimeter
    lines = text.replace(',','\n').splitlines()

    dic = {}
    for line in lines:
        key,value = line.split('=')
        dic[key.strip().lower()] = float(value.strip())

    return dic


def read_csv(path, delimiter=','):

    if not os.path.exists(path):
        return {}

    lines = []
    with open(path,'r+',encoding='UTF-16') as file:
        lines = file.read().splitlines()

    header = lines[0].split(delimiter)

    csvdic = {}
    for row in lines[1:]:
        values = row.split(delimiter)
        row_key = values[0].lower()

        # Skip this row if it's empty
        if row_key == '':
            continue

        dic = {}
        for i in range(len(values)):
            key = header[i]
            if key == 'pz-comp':
                dic['pz-comp'] = parse_pz_comp(values[i])
            elif key == 'id':
                dic[key] = values[i].lower()
            else:
                try:
                    dic[key] = float(values[i])
                except ValueError:
                    dic[key] = values[i]
        csvdic[row_key] = dic

    return csvdic


def read_csv_adv(path):

    if not os.path.exists(path):
        return {}

    macros = {}
    with open(path,'r+',encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            row_id,value_it,value_en = row
            macros[row_id] = {
                'it': value_it,
                'en': value_en,
            }
    return macros


def get_images(path):

    if path is None:
        return {}

    imgdic = {}

    extensions = ['.jpg','.png']

    for filename in os.listdir(path):
        name,ext = os.path.splitext(filename)
        if ext.lower() in extensions:
            imgdic[filename.lower()] = os.path.join(path,filename)

    return imgdic


def add_br(text):
    # Convert pipes to newlines
    text = text.strip().replace('|','\n')

    # Split giant string into separate lines (removing initial tabs/spaces)
    lines = [line.strip() for line in text.split('\n')]
    
    # Add html linebreaks
    return '<br/>'.join(lines)


def load_css():
    return open('main.css').read()


# Split actual toml and markdown
def split_toml(text):
    parts = [subtext.strip() for subtext in text.split('\n---')]
    return [parts[0], parts[1] if len(parts)>1 else '']


def preprocess_toml(text):
    evals = 0

    lines = []
    for line in text.splitlines():
        if '=' in line:
            parts = line.split('=')
            if len(parts)>1:
                operation = parts[1].strip()
                # Don't eval if the line starts with < " > or < ' >
                if operation[0] not in ['"',"'"]:
                    try:
                        evals += 1
                        parts[1] = simple_eval(str(parts[1].strip()))
                        lines.append('='.join([str(p) for p in parts]))
                        continue
                    except NameNotDefined:
                        pass

        lines.append(line)

    # print('Simple evals:',evals)
    return '\n'.join(lines)


def read_toml(text, css=''):

    toml_text,md_text = split_toml(text)

    toml_text = preprocess_toml(toml_text)
    # with open('dumps/preprocessed_text.toml','w+',encoding='UTF-8') as file:
    #     file.write(toml_text)

    data_toml = toml.loads(toml_text)

    data_toml['md_text'] = md_text

    toml_tables = []
    for key,value in data_toml.items():
        if key.startswith('tab'):
            for row in value['riga']:

                '''
                if 'nota' in row:
                    row['nota'] = add_br(row['nota'])

                if 'desc' in row:
                    row['desc'] = add_br(row['desc'])
                    if 'sub' in row:
                        for subrow in row['sub']:
                            subrow['desc'] = add_br(subrow['desc'])
                '''
            toml_tables.append(value)

    # data_toml['tables'] = tables
    # handle_tables(toml_tables)
    # print(json.dumps(toml_tables,indent=4))
    # print('-----------------')

    defaults = {
        
        'localized_it': {
            "qty": "Qtà",
            "wgt": "Peso",
            "pcs": "Pz",
            "desc": "Descrizione",
            "price_unit": "Prezzo",
            "subtot": "Subtot.",
            "vat": 'IVA',
            "tot": "Totale",
            "fullname": "Nome e cognome",
            "signed": "Firma",
            "page": "Pag.",
            "of": "di",
            "estimate": "Preventivo",
            "proforma": "Fattura pro forma",
        },

        'localized_en': {
            "qty": "Qty",
            "wgt": "Wgt",
            "pcs": "Pcs",
            "desc": "Description",
            "price_unit": "Price",
            "subtot": "Subtot.",
            "vat": 'VAT',
            "tot": "Total",
            "fullname": "Full name",
            "signed": "Signed",
            "page": "Page",
            "of": "of",
            "estimate": "Estimate",
            "proforma": "Pro forma invoice",
        },

        'lingua': 'it',
        'data': datetime.today().strftime('%d/%m/%Y'),
        'css': css,
        # 'imgfolder': 'D:/Desktop/Dev/PyMarkup/img/',
        'tag_br': '<br/>',
    }

    # print(json.dumps(data_toml,indent=4))

    for key,value in defaults.items():
        data_toml.setdefault(key,value)
        # if key not in data_toml:
            # data_toml[key] = value

    # print(data_toml['lingua'],data_toml['lingua']=='it')
    data_toml['localized'] = data_toml['localized_it']
    if data_toml['lingua']=='en':
        data_toml['localized'] = data_toml['localized_en']
    # print(data_toml['localized'])

    # data_toml['cliente'] = add_br(data_toml['cliente'])
    data_toml['tables'] = toml_tables

    # printdic(data_toml, 'data_toml.json')

    return data_toml


def get_subitems(singles):

    subitem_dic = {}

    for single_id,rowdic in singles.items():
        for comp_id,pz_per_comp in rowdic['pz-comp'].items():

            if not comp_id in subitem_dic:
                subitem_dic[comp_id] = {}

            subitem_dic[comp_id][single_id] = pz_per_comp
    
    return subitem_dic


def merge(toml_model, singles, subitems, macros, images):

    # row[key] = simple_eval(row[key])

    # printdic(subitems,'dumps/subitems.json')

    logs = []

    # row_defaults = {
    #     'um': 'mq',
    # }

    # printdic(toml_model, 'dumps/toml_model.json')
    # print('----------------')

    table_defaults = {
        'iva': True,
        'img': True,
        'nota': '',
    }

    for table in toml_model['tables']:

        for key,value in table_defaults.items():
            table.setdefault(key,value)

        for row in table['riga']:

            # for key in ['mq','pz','kg','tot','pz-pa','pz-ca']:
            #     if key in row:
            #         row[key] = 

            # Add default values from database table
            if 'id' in row and row['id'] in singles:
                for key,value in singles[row['id']].items():
                    row.setdefault(key,value)

                if toml_model['lingua'] == 'it':
                    row['desc'] = row['desc-it']
                else:
                    row['desc'] = row['desc-en']

            # If no unit of measure was set in toml, default to 'mq'
            row.setdefault('um','mq')
            
            '''
            # Add default values from database table
            if 'id' in row and row['id'] in singles:
                for key_toml,key_singles in key_mapping.items():
                    if key_toml not in row: # Do not overwrite values already set in toml
                        row_id = row['id']
                        row[key_singles] = singles[row_id][key_singles]
            '''

            if 'img' in row:
                imgname = row['img']
                if imgname in images:
                    # print(imgname,images[imgname])
                    row['imgpath'] = images[imgname]
                '''
                imgpath = os.path.join(toml_model['imgfolder'], row['img'])
                if os.path.exists(imgpath):
                    row['imgpath'] = imgpath
                else:
                    # del row['img']
                    error_msg = '[error] image not found: '+imgpath
                    logs.append(error_msg)
                    print(error_msg)
                '''

            # row['info'] = [
            #     'Pz/pallet: {}'.format(row.get('pz-pa','?')),
            #     'Pz/cassa: {}'.format(row.get('pz-ca','?')),
            # ]

            # Add sub-rows if not specified
            if 'id' in row and 'sub' not in row:
                # row['um'] = 'mq'
                # print(row.keys())
                # row['tot'] = row['eur'] * row['mq']
                # row['tot'] = 1
                if row['id'] in subitems:
                    row['um'] = 'mq'
                    row['sub'] = []
                    for single_id,pcs in subitems[row['id']].items():
                        subrow = singles[single_id]
                        subrow['pz'] = row['mq'] * pcs
                        subrow['kg'] = subrow['pz'] * subrow['kg-pz']
                        # subrow['mq'] = 1
                        # subrow['eur'] = 1
                        # subrow['um'] = 'mq'
                        # subrow['tot'] = 1
                        subrow['desc'] = subrow['desc-it'] if toml_model['lingua']=='it' else subrow['desc-en']
                        row['sub'].append(subrow)
                
                if row['id'] not in singles:
                # else:
                    row.setdefault('error','Errore ID: '+row['id'])
                    row_id = row['id']
                    logs.append(f'{row_id} not in singles: {row_id in singles}')
                    # print(row_id)
                    # print(singles.keys())
                    # print(row_id in singles)
                # except KeyError as e:
                #     logs.append('Key error: '+str(e))
                

            row['info'] = []
            if 'sub' not in row:
                for key in ['pz-mq','pz-pa','pz-ca']:
                    if row.get(key,'') == '':
                        row['info'].append(f'{key}: ?')
                    else:
                        row['info'].append(f'{key}: {row[key]}')

            # Round all numbers
            for key in row:
                try:
                    row[key] = float(row[key])
                except:
                    pass

            # Calculate missing values: mq, pz, kg, tot, pa, ca

            # MQ
            if 'pz' in row and 'mq' not in row and 'pz-mq' in row:
                row['mq'] = row['pz'] / row['pz-mq']

            # PZ
            if 'mq' in row \
            and 'pz' not in row \
            and 'pz-mq' in row \
            and 'sub' not in row:
                row['pz'] = row['pz-mq'] * row['mq']

            # KG
            if 'kg' not in row and 'pz' in row:
                row['kg'] = row['pz'] * row['kg-pz']

            # TOT = pz * (mq or pz or kg)
            if 'tot' not in row and 'um' in row and 'eur' in row:
                um = row['um']
                if um in row:
                    row['tot'] = row['eur'] * row[um]

            # to do: PA & CA

            if 'tot' not in row and 'sub' not in row:
                row['tot'] = -1
                row.setdefault('error','[Errore: "tot" mancante]')



    # Calculate total eur and total kg for each table
    for table in toml_model['tables']:
        table_tot_eur = 0
        table_tot_kg = 0

        for row in table['riga']:

            table_tot_eur += row.get('tot',0)

            # Add up weights in subrow
            row_tot_kg = 0
            for subrow in row.get('sub',[]):
                row_tot_kg += subrow.get('kg',0)
            row.setdefault('kg',row_tot_kg)
            table_tot_kg += row['kg']
        
        table.setdefault('tot',table_tot_eur)
        table.setdefault('kg',table_tot_kg)



    # Add 'even' key/value used for css alternate row coloring
    for table in toml_model['tables']:
        for i in range(len(table['riga'])):
            table['riga'][i]['even'] = (i%2 != 0)


    # merged_model = {}
    # for key,value in toml_model.items():
    #     if key not in ['tab']:
    #         merged_model[key] = value

    # merged_model['tables'] = toml_model['tables']


    # printdic(toml_model)

    
    # Convert markdown to html
    md = Markdown(extras=["tables"])
    md_text = []
    lan = toml_model['lingua']
    for line in toml_model['md_text'].splitlines():
        if line.startswith('$') and line[1:] in macros:
            md_text.append(macros[line[1:]][lan])
        else:
            md_text.append(line)
    toml_model['notes_html'] = md.convert('\n'.join(md_text))
    # print('-----------')
    # print('MD conversion ms:',time.time()-start)
    # print('-----------')


    if len(logs) > 0:
        print('{} errors/warnings:'.format(len(logs)))
        for log in logs:
            print(log)

    return toml_model


def add_br_tags(text):
    # Convert pipes to newlines
    text = text.strip().replace('|','\n')

    # Split giant string into separate lines (removing initial tabs/spaces)
    lines = [line.strip() for line in text.split('\n')]
    
    # Add html linebreaks
    return '<br/>'.join(lines)


def format_number_comma(value):
    text = "{:,.2f}".format(value)
    return text


def format_number_point(value):
    text = format_number_comma(value)
    text = text.replace(',',';')
    text = text.replace('.',',')
    text = text.replace(';','.')
    return text

def format_info(strlist):
    return '<br/><span class="info">' + '<br/>'.join(strlist) + '</span>'

'''
Takes a dictionary with all the parameters needed by jinja
'''
def render_html(data, preview=True, **kwargs):
    
    filters = {
        # 'allcaps': allcaps,
        'format_number': format_number_comma if data['lingua']=='it' else format_number_point,
        'add_br_tags': add_br_tags,
        'format_info': format_info,
    }
    
    # print('Preview:',preview)
    html = render_template('template.html', output='rendered.html', filters=filters, preview=preview, **data, **kwargs)
    return html

def render_pdf(html):
    convertHtmlToPdf(html, 'rendered.pdf')
