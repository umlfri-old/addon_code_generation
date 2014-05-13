def GetProperty(item, key = None):
    if key is None:
        return {
        'dest': item.GetDestination(),
        'name': item.GetValue('name'),
        'source': item.GetSource(),
        'type': item.GetType()
        }
    else:
        if (key=='type'):
            return item.GetType()
        elif (key=='name'):
            return item.GetName()
        elif (key=='dest'):
            return item.GetDestination()
        elif (key=='source'):
            return item.GetSource()
            
            