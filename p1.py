import os
import re
import csv

# iteration
for combination in range(1,531442):
    # Every point is connected to three other points
    graph = {
        1: [2, 7, 12],
        2: [1, 3, 10],
        3: [2, 4, 10],
        4: [3, 5, 9],
        5: [4, 6, 9],
        6: [5, 7, 8],
        7: [1, 6, 8],
        8: [6, 7, 12],
        9: [4, 5, 11],
        10: [2, 3, 11],
        11: [9, 10, 12],
        12: [1, 8, 11],
    }

    # read from csv (created by iter.py)
    with open('cases.csv') as f:
        reader = csv.reader(f)
        rows = list(reader)
    n = combination
    input = rows[n]

    def run_glpsol():
        os.system("glpsol --lp lp\\"+str(n)+".lp -o output\output"+str(n)+".txt")
        outputfile = open("output"+str(n)+".txt", "r")
        opt_value = None
        for line in outputfile.readlines():
            if "Objective" in line:
                opt_value = float((re.findall("[0-9]+[,.]*[0-9]*", line))[0])
            if "PRIMAL SOLUTION IS INFEASIBLE" in line:
                opt_value = None
        outputfile.close()
        if opt_value == None:
            raise Exception("LP is unsolvable.")
        return opt_value

    # quarry limitations,
    # q is the quarry vertex number
    def quarry(q):
        count = 1
        for vertex in graph[q]:
            if (count < 3):
                s = "g_" + str(q) + "_" + str(vertex) + " - " + \
                    "g_" + str(vertex) + "_" + str(q) + " + "
                f.write(s)
                count = count + 1
            elif (count == 3):
                s = "g_" + str(q) + "_" + str(vertex) + " - " + \
                    "g_" + str(vertex) + "_" + str(q)
                f.write(s)
        s = " - 200 f" + str(q) + " = 0\n"
        f.write(s)

        count = 1
        for vertex in graph[q]:
            if (count < 3):
                s = "d_" + str(q) + "_" + str(vertex) + " - " + \
                    "d_" + str(vertex) + "_" + str(q) + " + "
                f.write(s)
                count = count + 1
            elif (count == 3):
                s = "d_" + str(q) + "_" + str(vertex) + " - " + \
                    "d_" + str(vertex) + "_" + str(q)
                f.write(s)
        s = " - 75 f" + str(q) + " = 0\n"
        f.write(s)

        count = 1
        for vertex in graph[q]:
            if (count < 3):
                s = "j_" + str(q) + "_" + str(vertex) + " - " + \
                    "j_" + str(vertex) + "_" + str(q) + " + "
                f.write(s)
                count = count + 1
            elif (count == 3):
                s = "j_" + str(q) + "_" + str(vertex) + " - " + \
                    "j_" + str(vertex) + "_" + str(q)
                f.write(s)
        s = " = 0\n"
        f.write(s)


    # factory limitations,
    # fa is the factory vertex number
    def factory(fa):
        count = 1
        for vertex in graph[fa]:
            if (count < 3):
                s = "g_" + str(fa) + "_" + str(vertex) + " - " + \
                    "g_" + str(vertex) + "_" + str(fa) + " + "
                f.write(s)
                count = count + 1
            elif (count == 3):
                s = "g_" + str(fa) + "_" + str(vertex) + " - " + \
                    "g_" + str(vertex) + "_" + str(fa)
                f.write(s)
        s = " + 70 f" + str(fa) + " = 0\n"
        f.write(s)

        count = 1
        for vertex in graph[fa]:
            if (count < 3):
                s = "d_" + str(fa) + "_" + str(vertex) + " - " + \
                    "d_" + str(vertex) + "_" + str(fa) + " + "
                f.write(s)
                count = count + 1
            elif (count == 3):
                s = "d_" + str(fa) + "_" + str(vertex) + " - " + \
                    "d_" + str(vertex) + "_" + str(fa)
                f.write(s)
        s = " + 20 f" + str(fa) + " = 0\n"
        f.write(s)

        count = 1
        for vertex in graph[fa]:
            if (count < 3):
                s = "j_" + str(fa) + "_" + str(vertex) + " - " + \
                    "j_" + str(vertex) + "_" + str(fa) + " + "
                f.write(s)
                count = count + 1
            elif (count == 3):
                s = "j_" + str(fa) + "_" + str(vertex) + " - " + \
                    "j_" + str(vertex) + "_" + str(fa)
                f.write(s)
        s = " - 60 f" + str(fa) + " = 0\n"
        f.write(s)


    # market limitations,
    # lists contains all quarry, factory and market vertex numbers
    def market(qList,fList,mList):
        count = 1
        g = ""
        d = ""
        j = ""
        for market in mList:
            for vertex in graph[market]:
                if (count < 3*len(mList)):
                    g += "g_" + str(vertex) + "_" + str(market) + " + "
                    d += "d_" + str(vertex) + "_" + str(market) + " + "
                    j += "j_" + str(vertex) + "_" + str(market) + " + "
                    count = count + 1
                elif (count == 3*len(mList)):
                    g += "g_" + str(vertex) + "_" + str(market)
                    d += "d_" + str(vertex) + "_" + str(market)
                    j += "j_" + str(vertex) + "_" + str(market)

        cQ = 1
        for quarry in qList:
            if (cQ < len(qList)):
                g += " - 200 f" + str(quarry)
                d += " - 75 f" + str(quarry)
                cQ = cQ + 1
            elif (cQ == len(qList)):
                g += " - 200 f" + str(quarry) + " <= 0\n"
                d += " - 75 f" + str(quarry) + " <= 0\n"
        f.write(g)
        f.write(d)

        cF = 1
        for factory in fList:
            if (cF < len(fList)):
                j += " - 60 f" + str(factory)
                cF = cF + 1
            elif (cF == len(fList)):
                j += " - 60 f" + str(factory) + " <= 0\n"
        f.write(j)

    # use the market vertex list to generate an objective function
    def maxi(mList):
        s = ""
        for market in mList:
            for edge in graph[market]:
                if edge in mList:
                    s += ""
                else:
                    s += "150 g_" + str(edge) + "_" + str(market) + " - " + \
                        "150 g_" + str(market) + "_" + str(edge) + " + " + \
                        "200 d_" + str(edge) + "_" + str(market) + " - " + \
                        "200 d_" + str(market) + "_" + str(edge) + " + " + \
                        "1000 j_" + str(edge) + "_" + str(market) + " + "
        plus = s.rfind(" + ")
        s = s[:plus] + "\n"
        f.write(s)

    f = open("lp\\"+str(n)+".lp", "w")
    f.write("Maximize\n")
    ma = 0
    mList = []
    for buildings in input:
        ma = ma + 1
        if (buildings == "market"):
            mList.append(ma)
    maxi(mList)
    f.write("Subject To\n")

    # transportation limitaions
    for vertex in graph:
        for edges in graph[vertex]:
            lp = "g_" + str(vertex) + "_" + str(edges) + " + " + \
                 "g_" + str(edges) + "_" + str(vertex) + " + " + \
                 "d_" + str(vertex) + "_" + str(edges) + " + " + \
                 "d_" + str(edges) + "_" + str(vertex) + " + " + \
                 "j_" + str(vertex) + "_" + str(edges) + " + " + \
                 "j_" + str(edges) + "_" + str(vertex) + \
                 " <= 165\n"
            f.write(lp)

    # energy limitations
    s = ""
    count = 0
    for buildings in input:
        count = count + 1
        if (count < 12):
            if buildings == "quarry":
                s = "100 f" + str(count) + " + "
            elif buildings == "factory":
                s = "300 f" + str(count) + " + "
            elif buildings == "market":
                s = "0 f" + str(count) + " + "
        elif (count == 12):
            if buildings == "quarry":
                s = "100 f" + str(count)
            elif buildings == "factory":
                s = "300 f" + str(count)
            elif buildings == "market":
                s = "0 f" + str(count)
        f.write(s)
    s = " <= 850\n"
    f.write(s)

    # call related functions to write file
    locator = 0
    qList = []
    fList = []
    for buildings in input:
        locator = locator + 1
        if (buildings == "quarry"):
            quarry(locator)
            qList.append(locator)
        elif (buildings == "factory"):
            factory(locator)
            fList.append(locator)

    market(qList,fList,mList)

    # general limitaions: they should be greater than 0
    s = ""
    for vertex in graph:
        for edges in graph[vertex]:
             s = "g_" + str(vertex) + "_" + str(edges) + " >= 0\n" + \
                 "d_" + str(vertex) + "_" + str(edges) + " >= 0\n" + \
                 "j_" + str(vertex) + "_" + str(edges) + " >= 0\n"
             f.write(s)
        s = "f" + str(vertex) + " >= 0\n"
        f.write(s)
        s = "f" + str(vertex) + " <= 1\n"
        f.write(s)

    f.write("End\n")
    f.close()

    try:
        run_glpsol()
        os.system("type output.txt | findstr x_")
    except Exception:
        print("Infeasible Supply-Demand vector")
