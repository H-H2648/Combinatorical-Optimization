from MST import MST

if __name__ == "__main__":
    temp = MST(5, [
        ((0, 1), 1),
        ((0, 2), 2),
        ((0, 4), 6),
        ((1, 2), 3),
        ((1, 3), 7),
        ((2, 3), 5),
        ((2, 4), 6),
        ((3, 4), 4)
        ])
    print(temp.naive_kruskal())