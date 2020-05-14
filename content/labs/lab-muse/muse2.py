from muselsl import stream, list_muses, record

muses = list_muses()

if not muses:
    print("No Muses found")
else:
    stream(muses[0]['address'])

    print('Stream has ended')