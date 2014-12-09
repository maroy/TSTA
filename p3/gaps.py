import dateutil.parser

max_gap = 10

with open('created.txt', 'rb') as f:
    last_dt = None
    for line in [line.strip() for line in f.readlines()]:
        dt = dateutil.parser.parse(line)

        if last_dt is not None:
            delta = dt - last_dt
            if delta.total_seconds() > max_gap:
                print delta.total_seconds(), last_dt, dt

        last_dt = dt
