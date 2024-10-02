from xml.dom import minidom



class DIDReader:

    def __init__(self, filepath=None):
        self.filepath = filepath
        self.allconfigs = {}
        return None
    
    def read_mdx(self):
        dom = minidom.parse(self.filepath)
        elements = dom.getElementsByTagName('DID')
        names = dom.getElementsByTagName('NAME')
        defaults = dom.getElementsByTagName('DEFAULT_VALUE')
        values = dom.getElementsByTagName('ENUM_VALUE')
        DIDS_IDS = {}
        DID_BY_NAME = {}
        CONFIGS = {}
        for element in elements:
            dids = element.getElementsByTagName('SUB_FIELD')
            ID = element.attributes['ID'].value[4:]
            DIDS_IDS.setdefault(ID.lower(),{})
        for n in names:
            if n.parentNode.attributes.get('ID') and 'did_' in n.parentNode.attributes['ID'].value:
                dad_did = n.parentNode.attributes['ID'].value.split('_')
                id = dad_did[1].lower()
                DIDS_IDS[id][n.firstChild.nodeValue] = []
                DID_BY_NAME.setdefault(n.firstChild.nodeValue,[]).append(id)
            CONFIGS = {}
            for d in defaults:
                me = d.parentNode
                go_on = True
                mysibilingname = me.previousSibling
                while go_on==True:
                    if mysibilingname.nodeName=='NAME':
                        go_on = False
                    else:
                        mysibilingname = mysibilingname.previousSibling
                
                dadid = mysibilingname.parentNode.attributes['ID'].value
                if 'did_' in dadid:
                    mylsb = me.previousSibling.previousSibling.previousSibling.previousSibling.firstChild.nodeValue
                    mymsb = me.previousSibling.previousSibling.firstChild.nodeValue
                    bite = (int(mymsb) - int(mylsb)) + 1
                    CONFIGS.setdefault(dadid.split('_')[1].lower(), {}).setdefault(mysibilingname.firstChild.nodeValue,[]).append([d.firstChild.nodeValue, bite])
        self.allconfigs = CONFIGS
        return CONFIGS
    
    def get_config(self, config='de00'):
        return self.allconfigs.get(config,{})
    
    def get_bus(self, items = None):
        if not items: 
            return False
        
        serie = [vl for ix,vl in items.items()]
        counter = 0
        matx = []
        serie = []
        for ky,item in items.items():
            counter += item[0][1]
            matx.append(bin(int(item[0][0],16))[2:].zfill(item[0][1]))
            if counter == 8: 
                serie.append(matx)
                matx = []    
                counter = 0

        deseried = [hex(int(''.join(x),2)) for x in serie]
        return deseried