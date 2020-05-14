from muselsl import stream, list_muses, record

muses = list_muses()

if not muses:
    print("No Muses found")
else:
    record(60)

    print('Stream has ended')