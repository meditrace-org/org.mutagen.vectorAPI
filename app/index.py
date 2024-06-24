import ngtpy
import clickhouse_connect

DIM = 768


def get_top(emb, top: int = 100):
    index = ngtpy.Index(b"storage")

    with open("uuid_id.txt", "r") as file:
        uuids = file.readlines()
    send = []
    results = index.search(emb, top)
    for i, (id, distance) in enumerate(results):
        send.append(uuids[id].strip())

    return send


def update_index():
    client = clickhouse_connect.get_client(host="mutagen.space", username="default",
                                           password="iyLOLr1EXIWin8z4zMNe3UFKJ5qoba")
    uuids = []

    ngtpy.create(b"storage", DIM, distance_type="Cosine")
    index = ngtpy.Index(b"storage", zero_based_numbering=True)

    with client.query_row_block_stream(f"SELECT * from vr.embeddings") as stream:
        batch = []
        for block in stream:
            for row in block:
                batch.append(row[2])
                uuids.append(str(row[0]) + "\n")

            if len(batch) > 1000:
                index.batch_insert(batch)
                batch = []

    index.build_index()
    index.save()

    with open("uuid_id.txt", "w") as file:
        file.writelines(uuids)
    print("index rebuild")
