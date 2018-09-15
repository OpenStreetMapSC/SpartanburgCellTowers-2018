'''
A translation function for Spartanburg county shp Cell towers data


The following fields are used:    

Field           Used For            Reason
STREET_NUM      addr:housenumber    Street number
STREET_ADD      addr:streetname     Street name
CITY            addr:city           City
ZIP             addr:postal_code    Zip code
TYPE            tower:construction  type of construction / support
    LATTICE     lattice
    GUYED       guyed
    MONOPOLE    monipole
    SS Tower    freestanding
    WATER       man_made=water_tower
HEIGHT          height              height in feet (')
APPROVAL        start_date          Year began.  Validate > 1900
'''




def translateSuffix(rawname):
    '''
    A general purpose name expander.
    '''
    suffixlookup = {
    'Aly':'Alley',
    'Ave':'Avenue',
    'Br':'Branch',
    'Blf':'Bluff',
    'Rd':'Road',
    'Hts':'Heights',
    'St':'Street',
    'Pl':'Place',
    'Hl':'Hill',
    'Holw':'Hollow',
    'Pk':'Park',
    'Cres':'Crescent',
    'Blvd':'Boulevard',
    'Dr':'Drive',
    'Dwns':'Downs',
    'Ext':'Extension',
    'Pkwy':'Parkway',
    'Lndg':'Landing',
    'Xing':'Crossing',
    'Lane':'Lane',
    'Cv':'Cove',
    'Crt':'Court',
    'Trl':'Trail',
    'Tr':'Trail',
    'Ter':'Terrace',
    'Trc':'Trace',
    'Trce':'Trace',
    'Vly':'Valley',
    'Xovr':'Crossover',
    'Gr':'Grove',
    'Grv':'Grove',
    'Ln':'Lane',
    'Lk':'Lake',
    'Cl':'Close',
    'Cv':'Cove',
    'Cir':'Circle',
    'Ct':'Court',
    'Est':'Estate',
    'Rdg':'Ridge',
    'Plz':'Plaza',
    'Pne':'Pine',
    'Pte':'Pointe',
    'Pnes':'Pines',
    'Pt':'Point',
    'Ctr':'Center',
    'Rwy':'Railway',
    'Div':'Diversion',
    'Mnr':'Manor',
    'Hwy':'Highway',
    'Hwy':'Highway',
    'Conn': 'Connector',
    'Chase': 'Chase',
    'View': 'View',
    'Cliff': 'Cliff',
    'Walk': 'Walk',
    'Gate': 'Gate',
    'Grove': 'Grove',
    'Path': 'Path',
    'Trail': 'Trail',
    'Place': 'Place',
    'Real': 'Realignment',
    'Pass': 'Pass',
    'Row': 'Row',
    'Way': 'Way',
    'Farm': 'Farm',
    'Run': 'Run',
    'Drive': 'Drive',
    'Loop': 'Loop',
    'Line': 'Line',
    'E':'East',
    'S':'South',
    'N':'North',
    'W':'West'}
	
    newName = ''
    for partName in rawname.split():
        trns = suffixlookup.get(partName,partName)
        if (trns == partName):
            if partName not in suffixlookup:
                print ('Unknown suffix translation - ', partName)
        newName = newName + ' ' + trns

    return newName.strip()


# Only apply translation to first and last word
def translateFullName(rawname):
    newName = ''
    nameParts = rawname.split()
    for idx, partName in enumerate(nameParts):
        if idx == 0:
            partName = translatePrefix(partName)
        elif idx == (len(nameParts)-1):
            partName = translateSuffix(partName)
        newName = newName + ' ' + partName

    return newName.strip()


def translatePrefix(rawname):
    '''
    Directional name expander.
    '''
    prefixLookup = {
        'Hwy':'Highway',
        'O':'Old',
        'N':'New',
        'Nw':'NorthWest',
        'Ne':'NorthEast',
        'Se':'SouthEast',
        'Sw':'SouthWest',
        'E':'East',
        'S':'South',
        'N':'North',
        'W':'West'}

    newName = ''
    for partName in rawname.split():
        newName = newName + ' ' + prefixLookup.get(partName,partName)

    return newName.strip()

    
def filterTags(attrs):
    if not attrs:
        return
    tags = {}
    




    tags['man_made'] = 'mast'

    # Note leading and trailing spaces to force JOSM validation message
    tags['fixme'] = ' ** Check before uploading ** '
        
    if 'TYPE' in attrs:
        typ = attrs['TYPE'].strip()
        if typ == 'LATTICE':
            tags['tower:construction'] = 'lattice'
        elif typ == 'GUYED':
            tags['tower:construction'] = 'guyed'
        elif typ == 'MONOPOLE':
            tags['tower:construction'] = 'monopole'
        elif typ == 'SS Tower':
            tags['tower:construction'] = 'freestanding'
        elif typ == 'WATER':
            tags['man_made'] = 'water_tower'


    if 'HEIGHT' in attrs:
        height = attrs['HEIGHT']
        if (height <> '') and (height <> "0"):
            tags['height'] = height + "'"

    if 'APPROVAL' in attrs:
        year = attrs['APPROVAL'].strip()
        if (year <> '') and (year > "0"):
            tags['start_date'] = year


    if 'STREET_ADD' in attrs:
        stname = attrs['STREET_ADD'].title().strip()
        if stname <> '':
            tags['addr:street'] = translateFullName(stname)

    if 'STREET_NUM' in attrs:
        housenum = attrs['STREET_NUM'].strip()
        if (housenum <> ''):
            tags['addr:housenumber'] = housenum
    if 'CITY' in attrs:
        city = attrs['CITY'].title().strip()
        if (city <> ''):
            tags['addr:city'] = city
            tags['addr:state'] = 'SC'

    if 'ZIP' in attrs:
        zip =attrs['ZIP'].strip()
        if zip <> '':
            tags['postal_code'] = zip

    return tags