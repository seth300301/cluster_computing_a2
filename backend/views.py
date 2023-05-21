import couchdb

def rent_view():
    COUCHDB_SERVER='http://admin:password@172.26.136.171:5984/'
    server = couchdb.Server(COUCHDB_SERVER)

    rent_view = server['rent_sudo'].view('filterrent/rent_view', reduce=False)

    data_dict = {}
    for row in rent_view:
        year, state = row['key']
        value = row['value']
        year_key = 'rent_' + str(year)
        if year_key not in data_dict:
            data_dict[year_key] = {}
        data_dict[year_key][state] = value

    return data_dict

if __name__ == '__main__':
    print(rent_view())
