

def parse_slots(self, data):
    '''
    We extract the slots as a dict
    '''
    slot_value = list()
    slot_data = dict()

    for slot in data['slots']:
        if slot_data.get(slot['slotName'], None) == None: #therefore it hadn't read it before
            slot_data[slot['slotName']] = []
            if slot['value']['kind'] == 'TimeInterval':
                slot_data[slot['slotName']] = [[slot['value']['from'], slot['value']['to']]]
                    
            else:
                slot_data[slot['slotName']] = [slot['value']['value']]
                
        else: # read it before and trying to add a new value
            if slot['value']['kind'] == 'TimeInterval':
                slot_data[slot['slotName']].append([slot['value']['from'], slot['value']['to']])
            else:
                slot_data[slot['slotName']].append(slot['value']['value'])
        
    for k, v in slot_data.items(): # if slot is a single list object, just make it a string
        if len(v) < 2:
            slot_data[k] = v[0]
            
#    self.log("__function__, {}".format(slot_data), level='INFO')
    return slot_data
